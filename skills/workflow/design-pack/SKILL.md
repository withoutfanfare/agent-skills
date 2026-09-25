---
name: design-pack
description: Packages a codebase's design system and page screenshots into an upload pack for a design tool.
license: MIT
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Grep Glob
---

# Design pack

Design tools that learn a house style from uploaded material are only as
good as what gets uploaded. A folder of random screenshots and a copied
colour list teaches them the wrong lesson: which page happened to be open,
not what the system is. This skill turns a codebase into a
focused pack: real tokens, a written account of the rules, screenshots
chosen to show every layout, and any text the tool's setup form asks for.

## 1. Check whether a built-in importer already covers this

Many design tools can import a component library directly (a built
Storybook site, or a compiled JS/TS package). Check the target tool's docs
or CLI for an import command and the project shapes it accepts. If one
fits, use it and stop. Otherwise (a server-rendered app, a CMS theme, a
static site) this skill is the route. Do not build a throwaway React copy
of the components to satisfy an importer: it drifts from the real thing.

Done when: you know whether a native importer applies, and have picked a
route.

## 2. Survey the design sources

Find what exists before packing anything:

- **Tokens**: a Tailwind theme block, `:root` custom properties, a config
  file, a tokens JSON, SCSS variables.
- **Components**: the component directory and roughly how many there are.
- **Written rules**: any existing design or brand document, style guide,
  or retrospective that records decisions. A `STYLEGUIDE.md` from
  `house-style` (if installed) already holds the extracted system: reuse
  it rather than extracting again.
- **Fonts**: self-hosted files or a font service link.
- **Imagery**: the public image folders, grouped by kind (photography,
  illustration, icons, logos).
- **A running instance**: a local dev server or a live URL to screenshot.

If there is neither a token file nor written design documentation, say so
before going on: the pack will rest almost entirely on the screenshots.

Done when: you can list what each category holds, or that it is absent.

## 3. Capture representative screenshots

Run the script bundled with this skill (in Claude Code the folder is
`${CLAUDE_SKILL_DIR}`; otherwise use the path this skill was linked from)
from the project root; a plain `--screenshot` flag captures only the
viewport. It uses the project's Playwright, or the copy `npx -p playwright`
supplies (the first run may need `npx playwright install chromium`):

```bash
npx -p playwright node "${CLAUDE_SKILL_DIR:-.}/scripts/capture-pages.mjs" \
  --base https://example.test --out design-pack/screenshots --prefix desktop- \
  --routes / /catalogue /product/example /account /contact
```

Read [references/screenshots.md](references/screenshots.md) for choosing
routes, the mobile run and checking the results. Never capture real
customer data; use a seeded demo account or sample content.

Done when: the screenshots folder holds a curated, checked set covering
every distinct layout, with no real user data in shot.

## 4. Extract tokens verbatim

Copy the token source into `tokens.css` (or `.json`) from the actual file,
never from memory, and note at the top where it came from. Keep comments
that explain a choice ("the accent matches the brand mark's swatch"): that
is context a generic extractor cannot infer from the numbers.

Done when: the token file matches the source exactly and states its
origin.

## 5. Write the design system document

Read [references/design-system-template.md](references/design-system-template.md)
for the shape and the reasoning behind each part, then write
`design-system.md`. Two rules from it matter more than covering every
section: every value traces back to code or a rendered page, and what has
been tried and reverted is written down.

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

Keep `imagery/` to a small set per family so the pattern is obvious;
every thumbnail on the site buries the signal. Convert avif or tiff to jpg
or png. If the folder is heavy and inside the repository, say so, so it
can be gitignored.

Done when: every folder above exists with real content or is left out
because the project has none.

## 7. Draft the upload form text, if the tool needs it

Some tools ask for a short blurb and a notes field alongside the upload.
Write both as [references/upload-text.md](references/upload-text.md)
describes, and say what should stay out of the upload.

Done when: both pieces of text exist, or you have noted the target tool
does not ask for them.

## 8. Verify before handing over

State what you checked: screenshot dimensions read back and a few
opened and looked at, the token file's structure (balanced braces, the
blocks you expected), and the file count in each pack folder. Against each
claim in `design-system.md`, note how you confirmed it.

How the destination tool reads the pack cannot be checked from here. Say
so plainly, and recommend a test upload on a disposable project first.

Done when: the verification list above is written down, with a clear line
between what you checked and what only the upload itself will confirm.

## It's working if

- Every screenshot shows a distinct layout, none carry real user data, and
  the tall ones were checked at the bottom, not just the top.
- Every value in `design-system.md` and `tokens.css` traces to a file or a
  rendered page you looked at, not a guess.
- The person uploading the pack knows exactly what to drag in, what to
  leave out, and what still needs checking after upload.
