---
name: findable
description: >-
  Makes a web app's pages easier for search engines to find, understand and
  rank: page metadata, structured data, sitemaps, robots rules, internal
  links and Core Web Vitals. Use when adding SEO metadata, generating a
  sitemap, fixing robots.txt, improving internal linking, or when the user
  mentions SEO, meta tags, canonical URLs, schema markup or page speed.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Findable

A page a search engine cannot parse or reach might as well not exist. Most
SEO damage is quiet: a missing canonical tag, a sitemap nobody regenerates,
an image with no width and height shunting the layout as it loads. None of
it throws an error, so it survives in production until someone notices
traffic has stalled. This skill works through the concrete, checkable parts
of SEO, in the order that matters most: can the page be found, can it be
understood, does it load well.

## 1. Confirm the page is reachable and indexable

Before touching metadata, check nothing is silently blocking the page:

- Is it linked from somewhere a crawler will find (navigation, a sitemap,
  another page), or is it orphaned?
- Does `robots.txt` allow the path?
- Does the response include a `noindex` meta tag or `X-Robots-Tag` header
  that shouldn't be there (common on pages copied from a staging template)?
- Does the page return a real 200, not a soft 404 (a "not found" message
  served with a 200 status)?

Grep the codebase for `noindex`, `X-Robots-Tag` and the route in question
to rule out an accidental block before assuming the fix is metadata.

Done when: you can state plainly whether the page is crawlable and
indexable, with the evidence for it.

## 2. Set metadata per page, not per site

Every page needs its own title, description and canonical URL, built from
the page's own data (a product name, an article title), not a single
site-wide default copied everywhere. Duplicate titles across a category of
pages is one of the most common findings in an audit and one of the
easiest to fix once you see the pattern.

Cover, per page:

- **Title**: unique, states what the page is, roughly 50 to 60 characters
  before it truncates in results.
- **Description**: unique, roughly 150 to 160 characters, written as a
  reason to click, not a keyword list.
- **Canonical URL**: the one address this content should rank under, even
  when the same content is reachable through several URLs (filters, sort
  order, tracking parameters).
- **Open Graph and Twitter card tags**: title, description, image and type,
  so shared links render properly.
- **Robots directive**: explicit `index, follow` on public pages, and
  `noindex` only where genuinely intended (thank-you pages, internal
  search results, duplicate filtered views).

Build this from a single place per page type (a template, a component, a
helper function) rather than hand-writing tags in every view: that is what
lets duplicate titles happen in the first place. Stack-neutral pattern and
a Laravel-specific example are in
[references/metadata.md](references/metadata.md).

Done when: every page type produces a unique title, description and
canonical URL from its own data, and you have checked at least one real
example renders correctly.

## 3. Add structured data where it earns a richer result

Structured data (JSON-LD, usually) tells a search engine what the page
represents. It's only worth adding where it changes what appears in
results: products get price and availability, articles get author and
date, organisations get a knowledge panel, FAQs get an expandable list.
Adding it to a page type it doesn't fit is wasted work.

Validate whatever you add against a schema testing tool before calling it
done. Malformed JSON-LD is invisible in the rendered page, easy to ship
without noticing, and quietly ignored by search engines. Examples for the
common schema types are in
[references/structured-data.md](references/structured-data.md).

Done when: each schema block validates without errors and matches real
data on the page (no invented prices, ratings or dates).

## 4. Keep the sitemap and robots.txt honest

A sitemap that lists removed pages, or misses new ones, teaches a crawler
to distrust it. Generate it from the same source of truth as the site's
routes and content (not a hand-maintained list), and regenerate it on a
schedule or on publish, not once at launch. Confirm the sitemap is:

- reachable at the URL `robots.txt` points to,
- valid XML,
- free of URLs that 404, redirect, or carry a `noindex` tag.

Keep `robots.txt` minimal: allow what should be crawled, disallow admin and
internal paths, and always list the sitemap. Framework-specific generation
detail is in [references/sitemaps-and-robots.md](references/sitemaps-and-robots.md).

Done when: fetching the live sitemap URL returns valid XML with no dead
links, and `robots.txt` disallows only paths that genuinely shouldn't be
crawled.

## 5. Strengthen internal links

Search engines follow links to decide what a page is about and how
important it is. Pages with no incoming internal links rarely rank well,
however good their content. Look for:

- orphaned pages (no other page links to them),
- descriptive link text ("read our returns policy", not "click here"),
- a logical hierarchy so a crawler can reach any page in a few clicks from
  the homepage,
- breadcrumbs on deep pages, both for users and as a breadcrumb schema
  candidate.

Done when: every page that should rank has at least one descriptive
internal link pointing to it, traced from the homepage or a hub page.

## 6. Improve Core Web Vitals

Page experience affects ranking as well as conversion. Work the three
metrics that matter, each with a distinct fix:

- **Largest Contentful Paint (loading speed)**: the biggest above-fold
  element should load early. Preload it, don't lazy-load it, and lazy-load
  everything below the fold instead.
- **Cumulative Layout Shift (visual stability)**: every image and embed
  needs explicit dimensions or a reserved space, so content doesn't jump as
  it loads.
- **Interaction to Next Paint (responsiveness)**: defer non-critical
  scripts and break up long-running JavaScript so the page keeps responding
  to input.

Measure before and after with a real tool (browser devtools' performance
panel, or a Lighthouse-style report) rather than assuming a change helped.
Code patterns are in
[references/core-web-vitals.md](references/core-web-vitals.md).

Done when: you have a before-and-after measurement for each metric you
touched, not just the code change.

## 7. Report what changed

Summarise, per page or page type: what metadata is now set, what structured
data was added and whether it validated, whether the sitemap and robots.txt
were touched, and which Core Web Vitals fixes were applied. Note anything
you could not verify (for example, a production crawl or a real Lighthouse
run) so the user knows what still needs checking outside this session.

Done when: the report lists concrete changes per page type, not a generic
"SEO improved" claim.

## It's working if

- Every page type has a unique title and description built from its own
  data, not a copy-pasted default.
- The sitemap and robots.txt agree with each other and with what's actually
  live.
- Structured data validates and Core Web Vitals fixes carry a real
  measurement, not just the code.
