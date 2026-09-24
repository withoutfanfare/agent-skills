---
name: localise
description: >-
  Adds or extends multi-language support in a Laravel app: translation
  files, locale switching, localised dates and currency, and RTL layout.
  Use when adding translations, wiring up a language switcher, or the user
  mentions i18n, l10n, locale, multi-language support, or right-to-left
  layout.
license: MIT
allowed-tools: Read Write Edit Grep Glob Bash
---

# Localise

Localisation usually starts well (a handful of strings moved into a
translation file) and quietly falls apart later: a new locale gets added
to the switcher before half the strings exist for it, a date renders in
the server's locale instead of the visitor's, or a right-to-left layout
breaks because a padding rule was written as `left` instead of `start`.
This skill builds the pieces in an order where each one is checked before
the next depends on it.

## 1. Choose the translation file format and stick to it

Nested PHP arrays (`lang/{locale}/messages.php`) suit small, structured
sets of strings and support pluralisation. Flat JSON (`lang/{locale}.json`,
keyed by the actual source-language sentence) suits large or growing
projects, because a translator can work from the key itself without
cross-referencing a separate source string.

Pick one as the project's default and do not mix both for the same kind of
content; a string findable in only one of the two formats becomes a string
someone forgets to translate.

Done when: there is one file format in use per kind of content
(interface strings, validation messages), and it is written down
somewhere a new contributor would find it.

## 2. Wire the app to resolve locale correctly

Decide the resolution order once, and implement it as a single piece of
middleware so every request goes through the same logic:

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

Store a logged-in user's preference on the user record, not only in the
session, so it survives across devices; store a guest's choice in the
session so it survives across pages within one visit. Reading the
browser's `Accept-Language` header only as a fallback, after both of those,
respects a deliberate choice the user already made over guessing from
their browser.

Done when: switching locale as a logged-in user on one device shows the
same locale on a second device, without re-selecting it.

## 3. Translate the content, not just the labels

Call `__()` (or `trans()`) for any UI string, `trans_choice()` for anything
with a count-dependent plural form, and route translated strings into
Blade and any component-based view layer through the same helpers rather
than duplicating strings inline. Validation messages need their own
locale-specific file (`lang/{locale}/validation.php`) including custom
per-field names, or a translated form still shows English error text.

Done when: a grep for hardcoded English sentences in Blade files or
components (outside comments) returns nothing for the screens in scope.

## 4. Localise dates, numbers and currency, not just strings

A date or price is part of the content too, and a locale that translates
the labels around it but leaves the date in the server's format looks
half-finished. Use Carbon's locale-aware formatting and the framework's
number formatter, driven by the active locale rather than a fixed one:

```php
Carbon::now()->locale(app()->getLocale())->translatedFormat('l jS F Y');
Number::currency($order->total, in: $order->currency, locale: app()->getLocale());
```

Done when: switching locale changes the date and currency formatting on
the same page, not only the surrounding text.

## 5. Support right-to-left layout without hardcoding direction

Mark which configured locales are RTL, set the page's `dir` attribute from
that list, and write layout CSS with logical properties
(`margin-inline-start`, `padding-inline-end`) or a utility framework's
`rtl:`/`ltr:` variants, rather than literal `left`/`right`. A layout
written with logical properties needs no separate RTL stylesheet; one
written with literal direction does, and that second stylesheet drifts out
of sync with every future change to the first.

Skip this step entirely if no RTL locale is in scope; do not add
unused RTL scaffolding speculatively.

Done when: switching to an RTL-marked locale mirrors the layout correctly
without a second, separately maintained stylesheet.

## 6. Find what's still missing

Missing keys fail silently by default: the key itself is shown instead of
translated text, and nobody notices until a user in that locale reports it.
Register a handler that surfaces this in development instead of hiding it:

```php
if (app()->isLocal()) {
    Lang::handleMissingKeysUsing(function (string $key, array $replace, ?string $locale) {
        Log::warning("Missing translation key [{$key}] for locale [{$locale}]");
        return $key;
    });
}
```

Done when: a deliberately untranslated key produces a visible log entry in
development, not just the raw key on the page.

## 7. Prove every locale actually has every key

A regression test that compares each configured locale's key set against
the base locale's catches a string added in English and never carried
over, at merge time rather than in production:

```php
it('has every base locale key for each configured locale', function () {
    $base = array_keys(trans('messages', locale: 'en'));

    foreach (config('app.available_locales') as $locale) {
        $keys = array_keys(trans('messages', locale: $locale));
        expect($keys)->toEqual($base);
    }
});
```

Done when: this test is in the suite and fails when a key is removed from
one locale's file but not another's.

Worked examples of each translation file format, the middleware, the
switcher route and view, and the parity test: see
[references/examples.md](references/examples.md).

## It's working if

- A logged-in user's locale preference follows them to a new device.
- Dates, numbers and currency change format along with the surrounding
  text when the locale changes.
- The key-parity test fails the moment a translation is added in one
  locale and forgotten in another.
