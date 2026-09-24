# Metadata: a per-page-type pattern

The shape that avoids duplicate tags is a small metadata object built once
per page, from that page's own data, then rendered into a single head
template. The exact mechanism varies by stack; the shape doesn't.

## The pattern

1. A page (a controller, a route handler, a page component) builds a plain
   data structure: title, description, canonical URL, image, type, and an
   optional `noindex` flag.
2. Missing fields fall back to site-wide defaults (the site name, a default
   share image) rather than being left blank.
3. One shared template renders that structure into the actual tags:
   `<title>`, `meta description`, `link rel="canonical"`, Open Graph and
   Twitter tags, and the robots meta tag.

```text
buildMeta(page):
  title       = page.title ?? siteName
  description = truncate(page.summary ?? defaultDescription, 160)
  canonical   = page.canonicalUrl ?? currentUrl (stripped of query params
                that don't change the content: sort, filter, tracking)
  image       = page.image ?? defaultShareImage
  noindex     = page.noindex ?? false
```

```html
<title>{{ title }}</title>
<meta name="description" content="{{ description }}">
<link rel="canonical" href="{{ canonical }}">

<meta property="og:type" content="{{ type }}">
<meta property="og:title" content="{{ title }}">
<meta property="og:description" content="{{ description }}">
<meta property="og:image" content="{{ image }}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ title }}">
<meta name="twitter:description" content="{{ description }}">

<meta name="robots" content="{{ noindex ? 'noindex, nofollow' : 'index, follow' }}">
```

## Gotchas

- **Query parameters split one page into many.** A product page reachable
  as `/shop/item?sort=price` and `/shop/item?ref=email` is one page to a
  human and two URLs to a crawler unless the canonical tag says otherwise.
  Strip parameters that don't change the content when building the
  canonical URL.
- **Truncate descriptions on word boundaries.** Cutting mid-word at exactly
  160 characters looks broken in search results; truncate a little short
  and add an ellipsis, or truncate at the nearest space.
- **A single-page app needs the tags in the initial HTML, not injected
  after load.** If the framework renders meta tags client-side only, check
  what a crawler actually receives (view source, or fetch the raw HTML)
  rather than what the browser shows after JavaScript runs.
- **Don't reuse the homepage's Open Graph image everywhere.** A page-specific
  image (the product photo, the article's header image) gets a noticeably
  better click-through rate when shared.

## Laravel

See [laravel.md](laravel.md) for a concrete `SeoMeta` value object, Blade
head partial and controller usage.
