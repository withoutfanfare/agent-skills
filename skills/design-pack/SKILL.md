---
name: design-pack
description: >-
  Packages a codebase's design system (colours, type, spacing, components
  and screenshots of representative pages) into an upload pack for a design
  tool. Use when asked to build a design reference pack, export the design
  system, or prepare a style upload for a Figma-style ingestion tool.
license: MIT
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Grep Glob
---

# Design pack

Design tools that learn a house style from uploaded material are only as
good as what gets uploaded. A folder of random screenshots and a copied
colour list teaches them the wrong lesson: which page happened to be open,
not what the system actually is. This skill turns a codebase into a
focused pack: real tokens, a written account of the rules, and screenshots
chosen to show every layout the product has.

The output is a folder plus two short pieces of paste-ready text for the
tool's own setup form (a blurb and a notes field), if the target tool asks
for them.

## 1. Check whether a built-in importer already covers this

Many design tools can import a component library directly (a built
Storybook site, or a compiled JS/TS package with an entry point) without
any manual packing. Check the target tool's own docs or CLI for a sync or
import command first, and check what project shapes it recognises.

If the project matches one of those shapes and the tool has a native
importer, prefer it and stop here. If the project is anything else (a
server-rendered app, a CMS theme, a static site, a component library the
importer cannot compile), this skill is the route. Building a throwaway
React mirror of the components just to satisfy an importer is usually a
mistake: it drifts from the real thing the moment either one changes.
Mention it, do not recommend it.

Done when: you know whether a native importer applies, and have picked a
route.

## 2. Survey the design sources

Find what exists before packing anything:

- **Tokens**: a Tailwind theme block, `:root` custom properties, a config
  file, a tokens JSON, SCSS variables.
- **Components**: the component directory and roughly how many there are.
- **Written rules**: any existing design or brand document, style guide,
  or retrospective that records decisions.
- **Fonts**: self-hosted files or a font service link.
- **Imagery**: the public image folders, grouped by kind (photography,
  illustration, icons, logos).
- **A running instance**: a local dev server or a live URL to screenshot.

When neither a token file nor any written design documentation exists,
flag that up front before continuing. The pack ends up resting almost
entirely on the screenshots in that case, and the person who requested it
deserves to know that in advance.

Done when: you can list what each category holds, or that it is absent.

## 3. Capture representative screenshots

Use [scripts/capture-pages.mjs](scripts/capture-pages.mjs) (or the
project's own browser automation tool, such as Playwright, if it already
has one wired up) rather than a plain `--screenshot` flag: most headless
browsers only capture the current viewport, not the full page.

```bash
node scripts/capture-pages.mjs \
  --base https://example.test \
  --out design-pack/screenshots \
  --routes / /catalogue /product/example /account /contact
```

Pick 8 to 12 routes between desktop and mobile so that, taken together,
they hit every distinct layout the product uses: a landing or promo page,
a browse or index page, a single-item page, a form, and a signed-in view
if you can reach one without borrowing real credentials. Two screenshots
of the same layout add nothing the tool didn't already learn from the
first.
Run it again with a narrow viewport for two or three mobile captures.

Never capture a page holding real customer data, order details or anything
personally identifiable. Use a seeded demo account or a page with sample
content instead, and check each screenshot before it goes in the pack.

Look at a handful of the results before moving on. A capture that stitches
several scrollable slices together can come back looking plausible and
still be wrong: a repeated band at a seam, a section that never finished
animating in, a page that stops short of its own footer. Check the bottom
of a tall page, not just the top.

Done when: the screenshots folder holds a curated, checked set covering
every distinct layout, with no real user data in shot.

## 4. Extract tokens verbatim

Copy the token source into `tokens.css` (or `.json`) by reading the actual
file, not by retyping values from memory. Note at the top of the file
where it came from. Keep any comments that explain a choice ("the accent
sits slightly off pure red because the brand mark uses the same swatch"):
that kind of note is exactly the context a generic extractor cannot infer
from the numbers alone.

Done when: the token file matches the source exactly and states its
origin.

## 5. Write the design system document

Read [references/design-system-template.md](references/design-system-template.md)
for the shape and the reasoning behind each part, then write
`design-system.md`.

Two rules matter more than covering every section:

- **Every value traces back to code or a rendered page.** Resolve a
  `clamp()` to a real pixel figure at a stated viewport. Check a claim
  before writing it down, such as confirming a button label in the source
  before calling it the standard one. A guessed rationale is worse than
  leaving the line out, because whatever you write here gets followed.
- **Record what has been tried and reverted.** A rule paired with the
  real decision that produced it ("cards used to carry a repeated status
  label; removing it did more to calm a busy grid than any restyling")
  is far more useful than a list of dos, and it is the one part a plain
  CSS scan can never produce on its own.

Done when: `design-system.md` exists, every factual claim has a source you
checked, and it says plainly where the codebase gave you nothing to go on.

## 6. Assemble the pack

```text
design-pack/
├── README.md          a short note explaining the folder's purpose, the
│                        upload step and how to regenerate it later
├── design-system.md   the written account from step 5
├── tokens.css          extracted verbatim, with its source noted
├── screenshots/        desktop-*.jpg and mobile-*.jpg
├── components/         a handful of component templates plus 2-3 full pages
├── fonts/               self-hosted font files, if any
└── imagery/             grouped by family: photography, illustration, icons, logos
```

Curate `imagery/`: keep it to a small, well-chosen set per family so the
pattern is obvious at a glance; a folder stuffed with every content
thumbnail on the site just buries the signal. Convert any unusual formats
(avif, tiff) to jpg or png so the pack opens everywhere.

Put the folder somewhere easy to find and drag from, and warn whoever asked
for it about the folder size if the screenshots are heavy, so they can
gitignore it if it lives inside the repo.

Done when: every folder above exists with real content or is left out
because the project genuinely has none.

## 7. Draft the upload form text, if the tool needs it

Some tools ask for a short blurb and a free-form notes field alongside the
upload.

- **Blurb** (two or three sentences): who the product is for and what it
  does, then one line on what the pack covers.
- **Notes** (roughly 150 to 250 words): the rules a generic extractor would
  miss, in priority order: point to the authoritative files first, then
  anything absolute (one typeface only, dark mode only, no serif anywhere),
  then the signature visual effect, then the clearest anti-pattern.

Say plainly what should not go in alongside the pack: the whole repository
(vendor code and content images swamp the signal), and an older version of
the same product if the design has since moved on.

Done when: both pieces of text exist, or you have noted the target tool
does not ask for them.

## 8. Verify before handing over

State what you actually checked: screenshot dimensions read back and a few
opened and looked at, the token file's structure (balanced braces, the
blocks you expected), and the file count in each pack folder. Against each
claim in `design-system.md`, note how you confirmed it.

Nobody on this side of the process can confirm how the destination tool
will actually read the pack once it is uploaded. Say that outright instead
of leaving the impression the job is fully closed out, and recommend a
test upload on a disposable project before anyone points it at something
that matters.

Done when: the verification list above is written down, with a clear line
between what you checked and what only the upload itself will confirm.

## It's working if

- Every screenshot shows a distinct layout, none carry real user data, and
  the tall ones were checked at the bottom, not just the top.
- Every value in `design-system.md` and `tokens.css` traces to a file or a
  rendered page you actually looked at, not a guess.
- The person uploading the pack knows exactly what to drag in, what to
  leave out, and what still needs checking after upload.
