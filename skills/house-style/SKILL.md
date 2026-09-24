---
name: house-style
description: >-
  Reads an existing codebase's colours, type, spacing and components and
  writes them up as a style guide document, so new screens match what is
  already there instead of drifting. Use for "what's our design system",
  "write a style guide from this codebase", "document our UI patterns", or
  before building new UI in a project you did not design. Not for building
  components or packing screenshots for a design tool; use `tailwind` or
  `design-pack`.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# House style

Left to guess, an agent building a new screen reaches for a plausible
blue and a round number for spacing, both close enough to pass a glance
and both wrong. Multiply that across a few features and the app looks
stitched together from two different products. This skill reads what is
actually there, separates the deliberate system from one-off accidents,
and writes it down once so every later change can match it on sight
instead of by guesswork.

To build new Tailwind UI against the guide, use `tailwind` (if installed);
to pack it with screenshots for a design tool, `design-pack` (if installed).
Both read the `STYLEGUIDE.md` this skill writes.

## 1. Sample the surfaces, don't read everything

Pick six to ten screens or components that between them cover the app:
a listing or landing page, a form, a modal or drawer, a data table, a
card or list item, and the shared layout or navigation. List them by
name before opening a single file. Reading every template in a large
codebase burns the budget you need for judgement later, and a good
sample shows every pattern a full read would.

Done when: the sample is named and covers layout, a form and at least
one overlay (modal, drawer or dropdown).

## 2. Tell the system apart from the accidents

Look for where design values are declared on purpose, roughly in this
order of reliability: CSS custom properties under `:root` or a theme
selector, a Tailwind or similar config's theme section, Sass/Less
variables, a JS/TS theme object. Then look at how the sampled files
actually use colour, size and spacing values, not just where they are
declared.

A value used the same way in three or more unrelated places is part of
the system. A value that shows up once, in a colour nobody else uses or
a padding that matches nothing else, is drift: someone typed a number
that looked right on the day. Keep a short "drift" list alongside the
system rather than folding stray values in as if they were intentional;
[scripts/value_census.py](scripts/value_census.py) greps a directory for
hex/rgb/hsl colours and length values and counts how often each one
repeats, which is a fast way to tell a token from a one-off before you
start reading component code closely. It counts literal values only, so
Tailwind classes (`bg-blue-600`, `p-4`) are missed: in a Tailwind project,
read the theme config and grep the class names instead. It skips
`node_modules`, `vendor`, `dist` and `public/build`.

Done when: every value you plan to document is backed by a source file
and a usage count, and the drift list is separate from it.

## 3. Extract colour and type as a scale, not a list of swatches

For colour, record the brand palette, the semantic set (success, error,
warning, info), the neutral/grey ramp, and how each shifts for hover,
active, disabled and focus, not just its resting state. For type,
record the font stack with fallbacks, the full size scale with what each
step is actually used for (not just "h1, h2, h3"), the weights in use,
and line-height paired with each size. A scale that skips a step ("we
have 14px and 24px but nothing between") is worth noting as-is; don't
invent the missing step.

Done when: colour and type are recorded as scales with usage context,
including interactive states, not as isolated values.

## 4. Extract spacing, layout and component patterns

Record the spacing scale (the arithmetic between steps matters more than
the exact numbers), container widths, breakpoints, radius and shadow
values, in the order they actually recur. Then catalogue the components
your sample touched: for each, its variants, its states (default, hover,
active, disabled, loading, error) and one real code excerpt, copied from
the codebase, not paraphrased. [references/component-catalogue.md](references/component-catalogue.md)
lists the component types and states worth checking so none are missed.

Done when: every documented component has at least one real excerpt and
its state variations are named, even where a state is missing ("no
loading state exists yet").

## 5. Check the sample against two more surfaces

Open two screens or components you did not read in step 1. If they use
only values already documented, the sample generalises. If they
introduce a new colour, spacing step or component variant, either add it
to the system (if it recurs) or add it to the drift list (if it looks
like a one-off). Skipping this check is how a style guide quietly
describes half the app.

Done when: two unsampled surfaces have been checked and any new pattern
is filed as system or drift.

## 6. Write the style guide

```markdown
# <Project> style guide

## Colour
### Brand / primary
### Semantic (success, error, warning, info)
### Neutrals
### Interactive states (hover, active, disabled, focus)

## Typography
### Font stack
### Scale (size, weight, line-height, used for)

## Spacing & layout
### Spacing scale
### Breakpoints & containers
### Radius & shadow

## Components
### <Component>: variants, states, example

## Known drift
Values that appear once or twice and don't fit the system above, kept
separate so nobody mistakes an accident for a rule.
```

Save it as `STYLEGUIDE.md` in the project root unless the person asked
for another path. Every value in it should trace back to a real file; if
you can't point to where it comes from, leave it out rather than guess.

Done when: the document exists at the agreed path and every section
under Colour, Typography and Components cites real code.

## 7. Prove it is usable, not just accurate

Pick one component type you did not document in detail (say, a tag or a
tooltip) and write a five-line spec for it using only the guide. If you keep
needing to peek at the original files to fill gaps, the guide is too
thin in that area; go back and add the missing states or values.

Done when: a five-line spec of the new component exists that cites only
guide sections.

## It's working if

- Someone who never opened the codebase could build a new form or card
  that looks native, using only the style guide.
- The "known drift" section exists and is short: it names the accidents
  instead of hiding them inside the system.
- Every colour, spacing value and component state in the guide has a
  real file it came from.
