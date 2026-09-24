# Component states and accessibility checklist

## States to cover on every interactive component

| State | What to check |
|---|---|
| Default | Matches the token palette, not a colour picked by eye |
| Hover | A visible but subtle shift (usually one step darker or lighter on the scale) |
| Focus | A visible outline or ring on keyboard focus, not only on click |
| Active | A shift distinct from hover, so a press is felt |
| Disabled | Reduced opacity and `cursor-not-allowed`; no hover or focus change |
| Loading | A spinner or skeleton, and the control is disabled while it runs |
| Error (inputs) | A distinct border and text colour, plus the message itself, not colour alone |
| Success (inputs) | A distinct but calmer signal than error, so the two are never confused |

Order states in the class list consistently (base, then hover, then focus,
then disabled) so a diff on one component reads the same way on the next.

## Focus rings

Use `focus-visible` rather than `focus`, so a mouse click does not leave a
ring behind but keyboard navigation always shows one:

```text
focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2
```

An outline in the same hue as the component's primary colour keeps it from
looking like an error state.

## Contrast targets (WCAG AA)

- Normal text against its background: 4.5:1.
- Large text (roughly 24px and above, or bold 19px and above): 3:1.
- Meaningful UI outlines (an input border, a focus ring, an icon that
  carries information alone): 3:1.

Check the pair that will render, including any background tint a
card or panel adds, not the token's contrast against plain white.

## Dark mode

A token flips on its own only when it is a CSS variable redefined under
the dark selector. In v4 every `@theme` token is already a CSS variable,
so setting `--color-surface` again inside `.dark` (see
[../assets/theme.css](../assets/theme.css)) makes every `bg-surface`
follow. In v3 the config token has to point at a CSS variable
(`surface: 'var(--surface)'`) for the same effect. Any other colour,
including Tailwind's built-in palette (`bg-slate-100`), needs an explicit
`dark:` class alongside it.

Avoid a flash of the wrong theme on load by setting the `dark` class on the
root element before the page paints, from a stored preference, rather than
after React or another framework hydrates.

## Touch targets

A tappable element needs at least 44 by 44 px of hit area on mobile, even
when its visible content is smaller. Pad the element rather than shrinking
its icon, and check spacing between adjacent tappable elements so a miss
does not land on the wrong one.

## Reduced motion

Wrap any transition that is purely decorative in a media query, and give a
transition that carries meaning (a save confirmation, a loading state) a
non-animated equivalent:

```css
@media (prefers-reduced-motion: reduce) {
  .transition-decorative { transition: none; }
}
```
