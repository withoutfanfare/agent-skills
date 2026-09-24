# Laravel specifics

## Metadata: a value object plus one Blade partial

Keep the metadata-building logic in one small class rather than scattered
across views, and render it from a single Blade partial so every page's
head looks the same shape.

```php
<?php

declare(strict_types=1);

namespace App\Support;

final class SeoMeta
{
    public function __construct(
        public readonly string $title,
        public readonly string $description,
        public readonly ?string $canonical = null,
        public readonly ?string $image = null,
        public readonly string $type = 'website',
        public readonly bool $noindex = false,
    ) {}

    public static function forPage(string $title, string $description): self
    {
        return new self(
            title: $title,
            description: Str::limit($description, 160),
            canonical: url()->current(),
            image: asset('images/default-share.jpg'),
        );
    }
}
```

```blade
{{-- resources/views/partials/seo-head.blade.php --}}
<title>{{ $seo->title }} | {{ config('app.name') }}</title>
<meta name="description" content="{{ $seo->description }}">
<link rel="canonical" href="{{ $seo->canonical ?? url()->current() }}">

<meta property="og:type" content="{{ $seo->type }}">
<meta property="og:title" content="{{ $seo->title }}">
<meta property="og:description" content="{{ $seo->description }}">
<meta property="og:image" content="{{ $seo->image }}">

<meta name="robots" content="{{ $seo->noindex ? 'noindex, nofollow' : 'index, follow' }}">

@stack('seo')
```

```php
// In a controller
public function show(Product $product): View
{
    $seo = new SeoMeta(
        title: $product->name,
        description: $product->summary,
        canonical: route('products.show', $product),
        image: $product->image_url,
        type: 'product',
    );

    return view('products.show', compact('product', 'seo'));
}
```

For an Inertia or Livewire-driven page, pass the same `SeoMeta` object as a
prop and set the document head from the front-end component instead of a
Blade partial; keep the object itself framework-agnostic so both routes can
build it the same way.

## Structured data with `@push`

Push JSON-LD onto a stack from the view that has the data, and render the
stack once in the shared layout, so a page can add zero, one or several
schema blocks without the layout needing to know about them in advance.

```blade
@push('seo')
<script type="application/ld+json">
{!! json_encode([
    '@context' => 'https://schema.org',
    '@type' => 'Product',
    'name' => $product->name,
    'sku' => $product->sku,
    'offers' => [
        '@type' => 'Offer',
        'priceCurrency' => 'GBP',
        'price' => (string) $product->price,
        'availability' => $product->in_stock
            ? 'https://schema.org/InStock'
            : 'https://schema.org/OutOfStock',
    ],
], JSON_UNESCAPED_SLASHES) !!}
</script>
@endpush
```

Use `json_encode`, not manual string concatenation. A product name with a
quote or ampersand in it breaks hand-built JSON silently.

## Sitemap generation

`spatie/laravel-sitemap` is the common choice. Build a scheduled Artisan
command rather than generating the sitemap on every request:

```bash
composer require spatie/laravel-sitemap
```

```php
// app/Console/Commands/GenerateSitemap.php
final class GenerateSitemap extends Command
{
    protected $signature = 'sitemap:generate';

    public function handle(): int
    {
        $sitemap = Sitemap::create()
            ->add(Url::create(route('home'))->setPriority(1.0));

        Product::query()->published()->each(
            fn (Product $product) => $sitemap->add(
                Url::create(route('products.show', $product))
                    ->setLastModificationDate($product->updated_at)
                    ->setChangeFrequency(Url::CHANGE_FREQUENCY_WEEKLY)
                    ->setPriority(0.8)
            )
        );

        $sitemap->writeToFile(public_path('sitemap.xml'));

        return self::SUCCESS;
    }
}
```

Schedule it in `routes/console.php` (Laravel 11+) or the console kernel:

```php
Schedule::command('sitemap:generate')->daily();
```

For a large catalogue, chunk the query (`chunkById`) rather than `each` on
an unconstrained query, so generation doesn't hold the whole table in
memory.

## robots.txt

Serve it as a static file in `public/robots.txt` for a fixed set of rules.
If the disallowed paths depend on environment (block everything on a
staging deploy, for example), generate it from a route instead:

```php
Route::get('/robots.txt', function () {
    $content = app()->environment('production')
        ? "User-agent: *\nAllow: /\n\nSitemap: " . url('/sitemap.xml')
        : "User-agent: *\nDisallow: /\n";

    return response($content)->header('Content-Type', 'text/plain');
});
```

This is the single most common way a staging site accidentally gets
indexed: the static file gets deployed as-is to every environment, so
staging inherits production's `Allow: /`.

## Core Web Vitals in a Blade stack

- Use `<img loading="lazy" width="" height="">` consistently; a package
  like `spatie/image` or an Eloquent cast can store width and height
  alongside an uploaded image so the template never has to guess them.
- Defer non-critical asset bundles with Vite's `defer` option or a plain
  `defer` attribute on the compiled script tag.
- Watch for a queued job's result being polled on the page (Livewire
  polling, an Echo listener) firing too eagerly; excessive polling competes
  with user interaction for the main thread and hurts INP.
