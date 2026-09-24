# Laravel Pennant notes

Pennant is Laravel's first-party feature flag package. Install it, then
apply the general method in the main skill using these specifics.

```bash
composer require laravel/pennant
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
php artisan migrate
```

## Defining a flag

Define flags in a service provider's `boot()` method with `Feature::define()`.
The callback receives the scope (usually the authenticated user, or `null`
for a guest):

```php
use Laravel\Pennant\Feature;
use App\Models\User;

Feature::define('new-checkout-flow', function (User|null $user) {
    if ($user === null) {
        return false; // guests: no anonymous checkout preview
    }

    return $user->is_beta_tester;
});
```

Type-hinting the parameter as plain `User $user` is the common way this
goes wrong, and it goes wrong quietly: when the scope is `null` (a guest, a
queued job, an artisan command) Pennant never calls the definition and
returns `false`. That can hide a missing guest decision, and it is
surprising when you wanted guests to see the feature. Use `User|null` and
handle `null` on purpose.

## Percentage rollouts with Lottery

`Illuminate\Support\Lottery` gives a weighted random choice, useful for
the percentage stage of a rollout:

```php
use Illuminate\Support\Lottery;

Feature::define('new-checkout-flow', fn (User|null $user) => match (true) {
    $user === null => false,
    $user->is_beta_tester => true,
    default => Lottery::odds(1, 4)->choose(), // roughly 25%
});
```

`Lottery::odds()` is re-rolled on every evaluation unless the result is
stored, which Pennant does automatically for a given scope once resolved,
so the same user keeps the same result on later requests.

## Checking a flag

```php
// PHP
Feature::active('new-checkout-flow');
Feature::for($user)->active('new-checkout-flow');
Feature::for(null)->active('new-checkout-flow'); // explicit guest check
```

```blade
{{-- Blade --}}
@feature('new-checkout-flow')
    <x-new-checkout />
@else
    <x-classic-checkout />
@endfeature
```

```php
// routes/web.php, gating a route
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/checkout/preview', PreviewController::class)
    ->middleware(EnsureFeaturesAreActive::using('new-checkout-flow'));
```

Use the same string literal (or a constant referencing it) in the
definition, every PHP check, every `@feature` directive and every route
middleware entry, so a rename or typo cannot leave one call site behind.

## Managing stored values

```bash
php artisan pennant:purge new-checkout-flow   # clear stored values for one flag
php artisan pennant:purge              # clear all stored values
```

`Feature::for($user)->forget('new-checkout-flow')` clears one scope's
stored value so it is re-evaluated on the next check, useful after
changing a definition while testing.

## Testing both states

```php
use Laravel\Pennant\Feature;

it('shows the new checkout to a beta tester', function () {
    $user = User::factory()->create(['is_beta_tester' => true]);

    Feature::for($user)->activate('new-checkout-flow');

    $this->actingAs($user)
        ->get('/checkout')
        ->assertSee('New checkout');
});

it('shows the classic checkout to a guest', function () {
    $this->get('/checkout')
        ->assertSee('Classic checkout');
});
```

`Feature::activateForEveryone('new-checkout-flow')` in a `beforeEach()`
is useful for tests that need the feature on throughout, without
activating it per user.

## Removing a flag after full rollout

1. Delete the `Feature::define()` call from the service provider.
2. Delete every `Feature::active()` / `Feature::for()->active()` check,
   every `@feature` directive, and every `EnsureFeaturesAreActive`
   middleware entry,
   keeping only the branch that is now always true.
3. Run `php artisan pennant:purge new-checkout-flow` to clear the stored
   per-scope values from the `features` table (or the configured store).
