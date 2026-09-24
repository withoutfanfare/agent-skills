---
name: tailwind
description: >-
  In a project that uses Tailwind CSS, builds and extends the design system
  so the codebase stays consistent: theme tokens for colour, spacing and
  type, new UI built from them, and checks on contrast, dark mode and touch
  targets. Use when building a UI kit or new component, setting up Tailwind,
  or the user mentions design tokens, theme colours, or pages looking
  inconsistent.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Tailwind

A Tailwind project without a token system grows one button style per
developer and one shade of blue per page. This skill treats the theme
tokens as the single source of truth for colour, spacing and type, and
every new piece of UI as something built from those tokens, not invented
next to them. It targets Tailwind CSS v4, where tokens live in CSS inside
an `@theme` block.

Projects still on v3 keep their tokens in `tailwind.config.js` under
`theme.extend`, use `darkMode: 'class'` and a `safelist` array. The method
below is the same; the v3 stub is at
[assets/tailwind.config.stub.ts](assets/tailwind.config.stub.ts).

## 1. Find the existing tokens

Before adding anything, read what is already there. If a `STYLEGUIDE.md`
exists (from `house-style`, if installed), read it first: it says which
values are deliberate.

```bash
grep -rlE --include='*.css' --exclude-dir=node_modules \
  '@import "tailwindcss"|@theme|@tailwind' .
find . -iname "tailwind.config.*" -not -path "*/node_modules/*"
```

The stylesheet with `@import "tailwindcss"` is the v4 entry point; its
`@theme` block holds the tokens. An `@tailwind base` line means v3; in
v4 a `tailwind.config.*` is read only if an `@config` line loads it. Note the
colour palette, spacing scale, font sizes and any custom plugins
already in use. If a component library or CSS file defines classes outside
Tailwind (a `.btn` in plain CSS, inline styles), record that too: it is a
second source of truth fighting the first, and a candidate to migrate.

Done when: you can list the project's colour names, spacing unit and type
scale from the `@theme` block (or v3 config) itself, not from guessing.

## 2. Decide: extend or set up

If an `@theme` block already defines the project's tokens, work within
it. If there is none, or it clears Tailwind's defaults wholesale
(`--color-*: initial`) without a stated reason, propose a minimal one. A
starting theme with worked colour scales and a 4px spacing unit is at
[assets/theme.css](assets/theme.css); adapt the brand colours, do not paste
it unchanged. Keep a legacy JS config only if the project already relies
on it, loaded with `@config "../tailwind.config.js";`, and add new tokens
in CSS.

Keep the token names generic (`primary`, `surface`, `danger`), not tied to
a specific shade of a specific brand, so the same component code survives
a rebrand.

Done when: there is one place that owns colour, spacing and type, and you
know whether you edited it or are building on it as found.

## 3. Check the token set is complete enough to build with

A workable set has, at minimum:

- a **primary** colour with a light-to-dark scale (roughly 5 to 10 steps),
  plus **neutral** and at least one **semantic** colour (success, warning,
  danger);
- a spacing scale on one base unit (`--spacing: 0.25rem`, so 4px), so
  `gap-4` and `p-6` always mean the same physical space;
- two or three named font sizes with their line heights, not a free choice
  of any Tailwind size on every element.

Where a token is missing and the task needs it, add it to `@theme`
rather than reaching for an arbitrary value (`bg-[#2f6feb]`). An arbitrary
value is a token that only exists once and will drift the next time
someone needs that colour.

Done when: every colour, spacing and size the new work needs has a token
name, not a one-off value.

## 4. Build the component against the tokens

Write the component's classes using token-backed utilities (`bg-primary-600`,
`p-4`, `text-base`) and cover its states in one pass, not as an afterthought:
default, hover, focus, active, disabled, and loading if it does async work.
A form control also needs error and success states. Every focusable
element needs a visible focus style; relying on the browser default is not
enough once custom colours are in play.

[references/states-and-a11y.md](references/states-and-a11y.md) has the full
state and accessibility checklist. [assets/component-example.md](assets/component-example.md)
shows one worked example (a status badge) built this way, to copy the
pattern from, not the exact classes.

Done when: the component's markup covers every state it can be in, each
using token classes.

## 5. Check contrast, dark mode and touch size

Run these checks against the finished component, not the design intent:

- Text on its background meets 4.5:1 contrast (3:1 for large text and UI
  outlines). Check the actual rendered colour pair, since a token that
  passes on white can fail on a tinted card background.
- If the project supports dark mode, the component has been viewed in
  both. v4 follows the system setting by default; a class toggle needs
  `@custom-variant dark (&:where(.dark, .dark *));` in the CSS. Every
  colour needs a `dark:` variant unless its token is redefined for dark
  mode, as the checklist explains.
- Any tappable element is at least 44 by 44 px, even if its visible
  content is smaller (pad a small icon button rather than shrinking its
  hit area).
- Motion respects `prefers-reduced-motion`; a transition that matters for
  understanding (a loading spinner) still needs a non-motion fallback.

Done when: contrast, dark mode and touch size have each been checked
against the rendered component, not assumed from the design.

## 6. Guard against class purging

A class built from a variable at runtime (`` `text-${color}-500` ``) will
not appear in the compiled CSS, because Tailwind scans source text for
whole class names, not evaluated strings. Search the new code for this
pattern and replace it with a lookup table of complete class names, or
list the classes with `@source inline("...")` in the CSS, with a comment
saying why (v3 uses `safelist` in the config instead).

```bash
grep -rnE '\$\{[^}]*\}-[0-9]{2,3}|\{\{[^}]*\}\}-[0-9]{2,3}' \
  --include='*.js' --include='*.jsx' --include='*.ts' --include='*.tsx' \
  --include='*.vue' --include='*.php' --exclude-dir=node_modules .
```

Done when: no new class name is assembled from a runtime variable, or each
one that must be is listed in an `@source inline()` entry.

## 7. Report

State which tokens you added or reused, which component(s) you built or
changed, the states covered, and the result of the contrast and dark mode
check. Flag any arbitrary value left in place and why (a genuine one-off,
or a token still owed).

## It's working if

- A new component's colours, spacing and type all trace back to a named
  token, with no arbitrary values left unexplained.
- Every interactive element has a visible focus state and passes contrast
  in both light and dark mode where dark mode is supported.
- The same component built by someone else from the same tokens would look
  the same.
