# Worked example: a status badge

A small component is the easiest place to see the whole method: tokens in,
every state covered, contrast checked. This one is a badge that shows an
order's status in an online shop.

## Tokens used

The `success`, `warning` and `danger` scales from
[theme.css](theme.css), and the `sm` font size token.

## Markup (framework-neutral)

```html
<span class="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5
             text-sm font-medium
             bg-success-50 text-success-700
             dark:bg-success-900 dark:text-success-200">
  Delivered
</span>
```

Swap `success` for `warning` ("Processing") or `danger` ("Cancelled") by
changing the token name only; the structural classes stay identical, which
is what keeps every badge in the product looking like the same component
rather than three near-misses.

## States this component needs

A badge is not interactive, so it skips hover, focus and active. It still
needs:

- a distinct pairing per status, checked for 4.5:1 text contrast against
  its own background tint, not against the page background;
- a dark mode pairing, since a pale tint that reads clearly on white turns
  glaring on a dark surface, hence the separate `dark:` shades above (with
  the theme's colours, every pair here clears 4.5:1 in both modes);
- a plain-language label alongside the colour, so the status is not
  conveyed by colour alone.

## Turning this into a reusable component

Once two or three call sites repeat this pattern, extract a `Badge`
component that takes a `status` prop and maps it to the token pairing
internally, rather than leaving each call site to remember the class
names. That mapping is the part worth testing: it is easy to typo a token
name and get a badge with no matching dark mode class.
