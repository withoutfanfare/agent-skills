---
name: snippet-keeper
description: >-
  Creates, replaces and deletes snippets in the user's SnippetsLab library, filing
  each one in the right folder with the right tags and moving superseded or
  unwanted snippets to the SnippetsLab Bin. Use when the user asks to "add a
  snippet", "save this to SnippetsLab", "write a cheatsheet", "update that
  snippet", "delete these snippets", "clean up old snippets", or when a CLI
  cheatsheet needs a new version. For searching and reading snippets only, the
  snippetslab skill is enough.
license: MIT
---

# Snippet keeper

SnippetsLab's own tools (the `lab` CLI and the snippetslab MCP server) can
search, read and create snippets, but cannot edit or delete them, and the app
has no AppleScript commands. Without this skill, every update leaves a stale
copy behind and the user has to delete old UUIDs by hand. Here, a replaced or
unwanted snippet is moved to the Bin by a guarded script, so the library
stays clean and nothing is lost until the user empties the Bin.

## 1. Look before you write

Search titles and content for the subject (`search_snippets`, brief results)
before creating anything. If a snippet already covers it, the job is a
replacement (step 3), not a second copy.

Call `list_filters` and pick the folder by UUID and existing tags by name.
Reuse tags (`cheatsheet`, `reference`, `laravel`, `markdown` …) rather than
inventing near-duplicates.

Done when: you know whether this is a new snippet or a replacement, and which
folder UUID and tags it gets.

## 2. Create the snippet

Use the MCP `create_snippet` (or `lab create`). Defaults:

- **Language** `MarkdownLexer` for how-tos and cheatsheets; the code's own
  language for a pure code snippet.
- **Title** says what it does, e.g. `Laravel: add Google reCAPTCHA v3 to
  forms (how-to)`, `grove: create a worktree`, `<Tool> CLI Cheatsheet`.
- **Note** gives the source and date, e.g. the repo and commit it came from.
- If the library has a template snippet for this kind of snippet (search
  for "template"), read it first and follow it.
- British English. No secrets, keys, passwords or customer data: use
  placeholders like `RECAPTCHA_SECRET_KEY=...`.

Done when: the create call returned a UUID, and `get_snippet` on it shows the
content you meant.

## 3. Replace an existing snippet

Snippets cannot be edited. Create the new version first (step 2), confirm it
with `get_snippet`, then move the old one to the Bin (step 4). Never bin the
old one before the new one exists.

Done when: the new UUID exists and the old UUID is binned.

## 4. Move snippets to the Bin

Deleting is the user's call. Before binning anything they did not name themselves,
list each snippet's title and UUID and get a yes. Replacing your own just-made
version (step 3) counts as asked when they asked for the update.

Then run, from this skill's folder:

```bash
scripts/trash-snippet.sh <uuid> [<uuid> ...]
```

For each UUID it fetches the title, opens the snippet in SnippetsLab by its
link, checks that SnippetsLab is the front app and that exactly one row is
selected with that exact title, uses Edit › Delete, and then confirms with
`lab fetch` that the snippet has gone. It prints `BINNED`, `SKIP` or `FAIL`
per UUID and exits non-zero if any failed. It refuses rather than guessing,
so a `FAIL … ABORT:` line means nothing was deleted.

- It brings SnippetsLab to the front for a second per snippet. Tell the user
  before a batch so they aren't typing elsewhere at that moment.
- It needs Accessibility permission for the app running it (System Settings
  › Privacy & Security › Accessibility). If System Events is refused, ask
  the user to grant it; do not try another route.
- Never empty the Bin (Library › Empty Bin…). That is the user's.

Done when: every UUID printed `BINNED`, and `info` shows the trashed count up
by that many.

## 5. Report

List every snippet created (title and UUID) and every one binned (title and
UUID) in the end-of-turn summary. A binned snippet can be restored from the
Bin in SnippetsLab until the Bin is emptied.

Done when: the summary names each snippet touched.

## It's working if

- A replacement leaves exactly one live copy of the snippet in the library.
- `scripts/trash-snippet.sh` prints `BINNED` for each UUID and SnippetsLab's
  trashed count rises by the same number.
- The user no longer gets "delete these old UUIDs" to-dos after a cheatsheet
  update.
