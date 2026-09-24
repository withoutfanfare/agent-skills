---
name: tailwind
description: >-
  Builds and extends a Tailwind CSS design system so a codebase stays
  visually consistent: reads or sets up the token config (colour, spacing,
  type scale), writes new UI against those tokens rather than one-off
  values, and checks contrast, dark mode and touch targets before calling a
  component done. Use when building a UI kit, adding a new component,
  setting up Tailwind for a project, or the user mentions design tokens,
  theme colours, or things looking inconsistent across pages.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Tailwind

A Tailwind project without a token system grows one button style per
developer and one shade of blue per page. This skill treats the Tailwind
config as the single source of truth for colour, spacing and type, and
every new piece of UI as something built from those tokens, not invented
next to them.

## 1. Find the existing tokens

Before adding anything, read what is already there:

```bash
find . -iname "tailwind.config.*" -not -path "*/node_modules/*"
grep -n "theme" -A 30 tailwind.config.*
```

Note the colour palette, spacing scale, font sizes and any custom plugins
already in use. If a component library or CSS file defines classes outside
Tailwind (a `.btn` in plain CSS, inline styles), record that too: it is a
second source of truth fighting the first, and a candidate to migrate.

Done when: you can list the project's colour names, spacing unit and type
scale from the config itself, not from guessing.

## 2. Decide: extend or set up

If a config exists with a reasonable `theme.extend`, work within it. If
there is no config, or `theme` replaces Tailwind's defaults wholesale
without a stated reason, propose a minimal one. A fresh stub with a
worked colour scale and an 8-point spacing comment is at
[assets/tailwind.config.stub.ts](assets/tailwind.config.stub.ts); adapt the
brand colours, do not paste it unchanged.

Keep the token names generic (`primary`, `surface`, `danger`), not tied to
a specific shade of a specific brand, so the same component code survives
a rebrand.

Done when: there is one config file that owns colour, spacing and type,
and you know whether you edited it or are building on it as found.

## 3. Check the token set is complete enough to build with

A workable set has, at minimum:

- a **primary** colour with a light-to-dark scale (roughly 5 to 10 steps),
  plus **neutral** and at least one **semantic** colour (success, warning,
  danger);
- a spacing scale on a consistent unit, usually 4px or 8px steps, so
  `gap-4` and `p-6` always mean the same physical space;
- two or three named font sizes with their line heights, not a free choice
  of any Tailwind size on every element.

Where a token is missing and the task needs it, add it to the config
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
  both. `darkMode: 'class'` needs a `dark:` variant on every colour that
  does not already come from a token that flips automatically.
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
pattern and replace it with a lookup table of complete class names, or add
the pattern to `safelist` in the config with a stated reason.

```bash
grep -rn '\$\{.*\}-[0-9]\{2,3\}' --include="*.{tsx,jsx,vue,blade.php}" .
```

Done when: no new class name is assembled from a runtime variable, or each
one that must be has a matching safelist entry.

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
