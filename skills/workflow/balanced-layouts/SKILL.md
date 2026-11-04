---
name: balanced-layouts
description: >-
  Designs web page sections that are compact and balanced, one section type
  at a time: real-content wireframes in two or three variants, the user
  picks, only the chosen one is built and then rolled out, all checked
  against firm layout rules (no thin centred columns, no stranded headings,
  no empty halves, small uniform photos, no underlined links, one button
  style). Use when the user asks to design, lay out or redesign a page or
  section, wants wireframe options, or says a page looks unbalanced, empty,
  unfinished, too white or "like a template". Not for writing up an existing
  design system (`style-guide`) or a throwaway flow prototype (`prototype`).
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
---

# Balanced layouts

Pages built for the space rather than the content look unfinished: a big
heading alone down one side, a thin ribbon of text in the middle of a wide
screen, a large weak photograph beside two lines, half a section left
empty. Broad redesign sweeps make it worse, because the user cannot judge
twenty changes at once. This skill designs one section type at a time,
composed for the content it really has, and lets the user choose before
anything is built.

## 1. Read the context and the content

Read the project's design files first (`DESIGN.md`, `PRODUCT.md`, any
patterns or lessons notes) and follow them where they are more specific
than this skill. Then take stock of the real content for the section:
how many words, which pictures and how good they are (resolution, shape,
age), which numbers, quotes and dates exist.

Done when: you can say in two lines how much content the section holds and
whether its pictures are strong enough to be large.

## 2. Pick one section type

Choose a single kind of section (a long story, a timeline, a page opener,
a table, a gallery, a page ending) and one real page that shows its
hardest case. Do not touch other section types in this round.

Done when: the section type and the page to try it on are named.

## 3. Wireframe two or three variants

Build quick HTML wireframes with the project's real fonts, real pictures
and real copy, never lorem ipsum or grey boxes, and screenshot each at
desktop width (and phone width if layout differs). Make the variants
genuinely different structures, not colour swaps. Under each, write its
one weakness honestly, and recommend one with the reason.

Done when: the screenshots are shown to the user inline, each with its
weakness, and one is recommended.

## 4. Build only the chosen variant

Wait for the user's pick. Build that variant on the real page, as a
reusable component or layout, not a one-off. Keep every word, fact and
quote of the original content unless the user said otherwise.

Done when: the chosen variant renders on the real page and the old one is
gone from it.

## 5. Check it against the rules

Capture the page at 1440, 1024 and 390 pixels wide (scroll through first
if the site reveals content on scroll) and check every item in the rules
below. Fix what fails before showing it.

Done when: every rule passes at all three widths and nothing scrolls
sideways on the phone.

## 6. Roll out and record

Apply the approved pattern to every section of that type across the site.
Record the pattern (purpose, rules, where used) in the project's design
notes, and list each judgement call you made that the user did not ask
for: new headings, moved paragraphs, changed backgrounds, new short copy.

Done when: the notes are updated and the judgement calls are listed in
your report.

## The rules

Layout:
- Compact and balanced. Compose each section for the amount of content it
  has; no decorative empty space.
- Never a thin, narrow, centred column of text on a wide page. Prose shares
  the grid with something that belongs to it: pictures, facts, dates, a
  quote, a sticky page index.
- No stranded headings: a large heading never sits alone beside long text
  or over empty space. Headings sit with their text.
- No empty halves. Both sides of a split come out level; if they cannot,
  choose another structure.
- No eyebrows (small labels above headings). A small line goes beneath a
  title, if anywhere.
- Few dividing lines. Space and alternating background tones separate
  sections.

Pictures:
- Weak, old or oddly shaped photographs cannot carry a layout. Show them
  small, at one uniform crop (for example 4:3), beside the words they
  illustrate, with a focus point set so faces survive the crop.
- Only genuinely strong, high-resolution images run large.
- Drawings, book covers and objects are shown whole inside the same frame,
  never cropped.
- When a section needs visual weight and has no strong picture, use type,
  numbers or data (a timeline, a chart, big figures), not a bigger picture.
- No small text in an accent colour over photographs.

Links and controls:
- No underlined links anywhere. Links show themselves by colour, weight, an
  arrow or a background.
- Links on photographs or dark bands are solid light buttons, never thin
  text or outline buttons.
- One button shape across the site, gently rounded; filters, chips and
  pagers share it.

Tone:
- Headings about real people stay gracious, whatever the text says.
- Modern web pages, not a printed book or newspaper pastiche.
- Motion, if any, is calm and optional; content reads without it.

## It's working if

- The user picks from screenshots rather than describing changes in words.
- Reviews stop finding empty halves, thin columns or stranded headings.
- Each approved section type appears the same way everywhere it is used.
