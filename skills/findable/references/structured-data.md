# Structured data: JSON-LD by page type

Structured data is a block of JSON describing the page's content in terms
a search engine already understands. It doesn't change what a user sees;
it changes what can appear in results (a star rating, a price, an event
date). Add one block per page, matched to what the page is.

## Product page

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Wireless keyboard",
  "description": "A compact wireless keyboard with a rechargeable battery.",
  "image": "https://example.com/images/wireless-keyboard.jpg",
  "sku": "WK-2201",
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/shop/wireless-keyboard",
    "priceCurrency": "GBP",
    "price": "34.99",
    "availability": "https://schema.org/InStock"
  }
}
```

Only add `aggregateRating` when there are real reviews behind it. An
invented or default rating is against most search engines' structured data
policies and can get the listing penalised.

## Article or blog post

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Five ways to speed up your checkout",
  "image": "https://example.com/images/checkout-speed.jpg",
  "datePublished": "2026-03-04T09:00:00+00:00",
  "dateModified": "2026-03-10T11:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Sam Carter"
  }
}
```

## Organisation (usually once, on the homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Co",
  "url": "https://example.com",
  "logo": "https://example.com/images/logo.png",
  "sameAs": [
    "https://www.linkedin.com/company/example-co",
    "https://twitter.com/examplecom"
  ]
}
```

## FAQ (only on a page with a genuine, visible Q&A list)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How long does delivery take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most orders arrive within three working days."
      }
    }
  ]
}
```

## Gotchas

- **Mirror what's on the page.** Structured data that claims a price,
  rating or availability the visible page doesn't show is treated as
  spam by some search engines, not just ignored.
- **Validate every time, not just the first time.** A refactor that
  renames a field breaks the JSON without touching the rendered
  page, so nobody notices until a search console report flags it weeks
  later. Run a schema validator after any change nearby.
- **One schema type per concept.** Don't wrap a Product schema and an
  Article schema around the same block trying to cover both; pick the type
  that matches what the page is.
