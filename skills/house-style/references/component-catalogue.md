# Component catalogue

A checklist of component types and the states worth checking for each.
Not every project has every component; skip what genuinely isn't there
rather than inventing it, but check before assuming it's missing.

## Buttons

- Variants: primary, secondary, tertiary/ghost, destructive, icon-only.
- States: default, hover, active/pressed, focus (keyboard, not just
  mouse), disabled, loading.
- Sizing: at least two sizes usually exist even if nobody named them;
  compare a nav button against a form submit button.

## Form fields

- Text input, textarea, select, checkbox, radio, toggle.
- States: empty, filled, focus, disabled, valid, invalid (with the
  actual error message styling, not just the border colour).
- Label placement (above, inline, floating) and required-field marking.

## Cards and list items

- Border, shadow and radius together (they usually move as a set).
- Padding rhythm between the card edge, its heading and its body.
- Hover treatment, if the card is clickable; if it isn't, note that too.

## Navigation

- Primary nav (header/sidebar): resting, hover, active/current-page.
- Mobile variant, if the layout collapses at a breakpoint.
- Breadcrumbs, tabs, pagination: usually share a "current item" treatment
  worth cross-checking against the primary nav's active state.

## Overlays

- Modal/dialogue box: backdrop treatment, entry/exit animation if any,
  close affordance, max width.
- Toast/notification: placement, auto-dismiss timing, and how success
  differs from error.
- Tooltip/popover: trigger (hover vs click), positioning, delay.

## Data display

- Tables: header styling, row hover, zebra striping or dividers, empty
  state, loading state.
- Badges/pills/tags: how many semantic colours they come in and whether
  that set matches the semantic colours used elsewhere.
- Empty states: illustration or icon conventions, message tone.

## Motion

- Note the transition duration and easing used for hovers versus the one
  used for overlays entering and leaving; they are often different, and
  that difference is itself a pattern worth recording.
- Don't document every `transition: all 0.2s` individually; group by
  where the timing is used (micro-interaction vs page-level).
