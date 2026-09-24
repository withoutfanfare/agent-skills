---
name: doc-sync
description: >-
  Brings the documentation inside a repository back in line with the code:
  updates developer and user docs in place, writes API reference and
  migration guides for breaking changes, and creates a README where none
  exists. Use when the user asks to update, sync or write the docs, document
  a feature or API, or write a migration guide. Not for tidying a docs
  folder of stale or duplicate pages; use `doc-tidy`.
license: MIT
allowed-tools: Bash Read Edit Write Grep Glob
---

# Doc sync

Documentation drifts one merged change at a time until nobody trusts it.
This skill closes the gap for a set of changes: it finds what the code now
does, finds where the docs describe it, and edits them in place. When the
docs and the code disagree, the code is right.

For a changelog entry, use `changelog` (if installed) instead. To tidy a
docs folder of stale, duplicate or broken-link pages, use `doc-tidy` (if
installed).

## 1. Find what changed

Start from git even when the user has described the change:

```bash
git log --oneline -15
git diff <base>...HEAD --stat
```

Use the branch's base, or the last release tag. Sort each change into what
it means for the docs:

| Change | Developer docs | User docs |
|---|---|---|
| New feature | how it is built, configured and called | how to use it |
| Behaviour change | updated explanation | updated steps |
| API change | request, response, errors, auth | affected tasks |
| Configuration | variables and defaults | settings guidance |
| Breaking change | migration guide | what users must do |
| Internal refactor | architecture notes, if structure changed | usually nothing |

Done when: every change is placed in the table, or marked "no docs impact".

## 2. Find where the docs live

Look for the existing structure (`docs/`, `documentation/`, a wiki folder,
README sections) and read the index or table of contents. Work within that
structure. Do not reorganise it unless asked. If there are no docs at all,
propose a small structure (a README plus `docs/` if needed) and confirm
before creating it.

Done when: for every change, you know which existing page covers it, or
that a new page is needed.

## 3. Edit in place

- Update the page that already covers the topic; do not start a parallel
  page.
- Match the page's voice, headings and formatting.
- Show, do not describe: the exact command, request or code a reader would
  type, rather than "an option exists for this".
- Remove anything the change made false: old options, removed endpoints,
  outdated screenshots.
- Developer docs explain how things work and how to change them. User docs
  explain how to get a task done. Keep each in its lane.

Done when: every page on the list reflects the new behaviour.

## 4. Breaking changes and APIs

Each breaking change comes with a migration guide: the reason for the
change, code as it was and as it must be now, and the steps to move
across, numbered.

Every new or changed endpoint gets: method and path, parameters with types,
an example response, authentication, error responses, and any rate limits.
Flag anything deprecated, with a link to what replaces it.

Done when: each breaking change has a guide and each endpoint change has a
reference entry.

## 5. Check your own work

- Every code example uses names that exist in the current code (search for
  them).
- New pages are linked from the index or contents.
- Links resolve.
- Nothing describes planned behaviour as if it exists.

Done when: all four checks pass.

## 6. Report

List pages updated and created, and one line per change saying what the
docs now say.

Done when: the report lists every page updated or created, each with one
line on what it now says.

## It's working if

- A reader following the docs gets the behaviour the code actually has.
- No topic is described in two places.
- Breaking changes come with a way through them.
