# Sitemaps and robots.txt

## Sitemap

Generate the sitemap from the same data the site itself uses to render
pages (routes, published content, categories), not a separate list someone
has to remember to update. Regenerate it on a schedule (daily is usually
enough) or trigger it on publish/unpublish for content-heavy sites.

A minimal sitemap entry:

```xml
<url>
  <loc>https://example.com/shop/wireless-keyboard</loc>
  <lastmod>2026-03-10</lastmod>
</url>
```

`changefreq` and `priority` are optional and Google ignores both. An
accurate `lastmod`, changed only when the content really changes, is the
one worth keeping.

Keep out of the sitemap:

- pages that redirect,
- pages that 404,
- pages marked `noindex`,
- draft or unpublished content,
- any URL with tracking or session parameters.

A site with more than roughly 50,000 URLs, or a sitemap file over 50MB,
needs a sitemap index file that lists several smaller sitemaps rather than
one giant file; most sitemap-generating libraries handle this
automatically once the count crosses the limit.

## robots.txt

Keep it short and specific. A common shape:

```text
User-agent: *
Allow: /

Disallow: /admin/
Disallow: /account/
Disallow: /search?

Sitemap: https://example.com/sitemap.xml
```

Gotchas:

- **`Disallow` doesn't stop indexing on its own**, it stops crawling. A
  disallowed page that's linked from elsewhere can still appear in results
  with no description, because the crawler can see the link but not the
  page. Use a `noindex` meta tag (which requires the page to be crawlable)
  for pages that must never appear in results at all.
- **Check the file is actually served at the root**, `/robots.txt`, not
  under a subpath, and that it isn't behind the same authentication as the
  rest of a staging environment (a very common way a whole site quietly
  vanishes from search results after a migration).
- **One directive per line, and paths are case-sensitive** on most servers,
  so `/Admin/` and `/admin/` are different rules.

## Verifying both together

After generating or changing either file, fetch both live and check they
agree: every sitemap URL should be allowed by robots.txt, and the sitemap
URL named in robots.txt should be the one that's actually being generated.
