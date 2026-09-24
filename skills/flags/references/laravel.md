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

Feature::define('new-checkout-flow', function (mixed $scope) {
    if (is_null($scope)) {
        return false; // guests: no anonymous checkout preview
    }

    return $scope instanceof User && $scope->is_beta_tester;
});
```

Type-hinting the callback parameter as `User $user` instead of `mixed
$scope` is the most common way this goes wrong: Pennant passes `null` for
every unauthenticated request, and a typed parameter throws a
`TypeError` for all of them rather than quietly returning false.

## Percentage rollouts with Lottery

`Illuminate\Support\Lottery` gives a weighted random choice, useful for
the percentage stage of a rollout:

```php
use Illuminate\Support\Lottery;

Feature::define('new-checkout-flow', fn (mixed $scope) => match (true) {
    is_null($scope) => false,
    $scope->is_beta_tester => true,
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
Route::get('/checkout/preview', PreviewController::class)
    ->middleware('feature:new-checkout-flow');
```

Use the same string literal (or a constant referencing it) in the
definition, every PHP check, every `@feature` directive and every route
middleware entry, so a rename or typo cannot leave one call site behind.

## Managing stored values

```bash
php artisan pennant:feature            # list flags and their states
php artisan pennant:purge new-checkout-flow   # clear stored values for one flag
php artisan pennant:purge              # clear all stored values
```

`Feature::for($user)->forget('new-checkout-flow')` clears one scope's
stored value so it is re-evaluated on the next check, useful after
changing a definition while testing.

## Testing both states

```php
use Laravel\Pennant\Feature;

public function test_beta_tester_sees_new_checkout(): void
{
    $user = User::factory()->create(['is_beta_tester' => true]);

    Feature::for($user)->activate('new-checkout-flow');

    $this->actingAs($user)
        ->get('/checkout')
        ->assertSee('New checkout');
}

public function test_guest_sees_classic_checkout(): void
{
    $this->get('/checkout')
        ->assertSee('Classic checkout');
}
```

`Feature::activateForEveryone('new-checkout-flow')` in a test's `setUp()`
is useful for tests that need the feature on throughout, without
activating it per user.

## Removing a flag after full rollout

1. Delete the `Feature::define()` call from the service provider.
2. Delete every `Feature::active()` / `Feature::for()->active()` check,
   every `@feature` directive, and every `feature:` middleware entry,
   keeping only the branch that is now always true.
3. Run `php artisan pennant:purge new-checkout-flow` to clear the stored
   per-scope values from the `features` table (or the configured store).
