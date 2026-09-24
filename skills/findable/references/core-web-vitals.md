# Core Web Vitals: code patterns

Three metrics, three distinct causes, three distinct fixes. Don't apply all
three blindly; measure first and match the fix to the metric that's
failing.

## Largest Contentful Paint (LCP)

The browser should be told about the biggest above-fold element as early as
possible, and nothing else should compete with it for bandwidth.

```html
<!-- Tell the browser about the hero image before it would otherwise find it -->
<link rel="preload" as="image" href="/images/hero.jpg">

<!-- Anything below the fold can wait -->
<img src="/images/related-product.jpg" loading="lazy" alt="Related product">
```

Common causes worth checking before reaching for preload: a render-blocking
web font, an oversized unoptimised image, or a slow server response for the
initial HTML (which no amount of front-end tuning fixes).

## Cumulative Layout Shift (CLS)

Every element that loads after the initial paint needs its final size
known up front, so nothing else moves when it appears.

```html
<!-- Explicit dimensions reserve the space immediately -->
<img src="/images/product.jpg" width="800" height="600" alt="Product photo">

<!-- A ratio-based wrapper does the same for an embed of unknown size -->
<div style="aspect-ratio: 16 / 9;">
  <iframe src="https://player.example.com/video/123" title="Product demo"></iframe>
</div>
```

Late-injected content is the other common cause: a cookie banner, an
onload advert, or a webfont swap that changes text size. Reserve space for
each, or use `font-display: optional` where a slight flash of fallback text
is acceptable.

## Interaction to Next Paint (INP)

The page should keep responding to clicks and taps while other work is
happening.

```html
<!-- Non-critical scripts shouldn't block the main thread during load -->
<script src="/js/analytics.js" defer></script>
```

```javascript
// Break large synchronous work into chunks the browser can interrupt
function processInChunks(items, chunkSize = 50) {
  let i = 0;
  function next() {
    const end = Math.min(i + chunkSize, items.length);
    for (; i < end; i++) processItem(items[i]);
    if (i < items.length) requestIdleCallback(next);
  }
  next();
}
```

## Measuring

Don't trust a code change without a measurement. Use the browser's own
performance panel against a throttled connection, or a Lighthouse-style
report, before and after. Field data (what real visitors experienced) from
a search console or real-user-monitoring tool is more trustworthy than a
single local run, since a local machine and connection rarely matches a
real visitor's.
