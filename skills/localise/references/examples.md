# Worked examples

## Nested PHP array format

```php
// lang/en/messages.php
return [
    'welcome' => 'Welcome back, :name!',
    'items_in_basket' => '{0} Your basket is empty|{1} One item in your basket|[2,*] :count items in your basket',
];
```

```php
__('messages.welcome', ['name' => $user->first_name]);
trans_choice('messages.items_in_basket', $basket->count());
```

## Flat JSON format

```json
// lang/fr.json
{
    "Welcome back, :name!": "Content de vous revoir, :name !",
    "Your order has been confirmed.": "Votre commande a été confirmée."
}
```

```php
__('Welcome back, :name!', ['name' => $user->first_name]);
```

The JSON format's keys are the literal source-language sentence, so a
translator working from the English original never has to look up a
separate key name.

## Locale-switching middleware and route

```php
class SetLocale
{
    public function handle(Request $request, Closure $next)
    {
        $locale = $request->user()?->locale
            ?? $request->session()->get('locale')
            ?? $request->getPreferredLanguage(config('app.available_locales'))
            ?? config('app.locale');

        App::setLocale($locale);

        return $next($request);
    }
}
```

Register it in the `web` group (in `bootstrap/app.php` on Laravel 11 and
later) so every page request runs it after the session has started.

```php
Route::post('/locale', function (Request $request) {
    $request->validate(['locale' => 'required|in:' . implode(',', config('app.available_locales'))]);

    $request->session()->put('locale', $request->locale);
    $request->user()?->update(['locale' => $request->locale]);

    return back();
})->name('locale.switch');
```

```blade
<form method="POST" action="{{ route('locale.switch') }}">
    @csrf
    <select name="locale" onchange="this.form.submit()">
        @foreach (config('app.available_locales') as $locale)
            <option value="{{ $locale }}" @selected(app()->getLocale() === $locale)>
                {{ strtoupper($locale) }}
            </option>
        @endforeach
    </select>
    <noscript><button type="submit">Change language</button></noscript>
</form>
```

## RTL layout without a second stylesheet

```blade
<html dir="{{ in_array(app()->getLocale(), config('app.rtl_locales')) ? 'rtl' : 'ltr' }}">
```

```css
.card {
    padding-inline-start: 1rem;   /* becomes right padding automatically under dir="rtl" */
    margin-inline-end: 0.5rem;
}
```

With a utility framework's logical variants:

```html
<div class="ps-4 me-2 rtl:text-right">
```

## Validation messages per locale

```php
// lang/fr/validation.php
return [
    'required' => 'Le champ :attribute est obligatoire.',
    'attributes' => [
        'email' => 'adresse e-mail',
    ],
    'custom' => [
        'email' => [
            'required' => 'Merci de renseigner votre adresse e-mail.',
        ],
    ],
];
```

## Logging missing keys in development

```php
// AppServiceProvider::boot()
if (app()->isLocal()) {
    Lang::handleMissingKeysUsing(function (string $key, array $replace, ?string $locale) {
        Log::warning("Missing translation key [{$key}] for locale [{$locale}]");
        return $key;
    });
}
```

## Scanning for missing keys ahead of a release

A small artisan command comparing a locale against the base locale's file
tree catches gaps before the missing-key handler in production would:

```php
class CheckTranslations extends Command
{
    protected $signature = 'translations:check {locale}';

    public function handle(): int
    {
        $base = collect(File::allFiles(lang_path('en')))->map->getFilename();
        $target = collect(File::allFiles(lang_path($this->argument('locale'))))->map->getFilename();

        $missing = $base->diff($target);

        if ($missing->isNotEmpty()) {
            $this->error('Missing files: ' . $missing->implode(', '));
            return self::FAILURE;
        }

        return self::SUCCESS;
    }
}
```
