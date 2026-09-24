---
name: doc-tidy
description: >-
  Tidies a project's documentation folder: finds stale, duplicate, orphaned
  or broken-link docs and organises what is left into a sensible structure.
license: MIT
disable-model-invocation: true
allowed-tools: Read Grep Glob Bash Edit Write
---

# Doc tidy

Docs rot quietly. A page that was right on the day it was written keeps
looking authoritative long after the code it describes has changed, so
readers and agents alike trust it and get misled. Two pages that started
as one copy drift apart until they disagree. A broken link just looks like
carelessness, but it is usually a sign the target moved or was deleted
and nobody updated the pointer. This skill finds all three problems and
puts the surviving docs into a structure that makes sense, without
deleting anything the user has not agreed to lose.

This is not `doc-sync` (if installed): that skill updates docs to match a
code change. This one cleans up what has already accumulated.

## 1. Map the folder

List every documentation folder in scope (usually `docs/`, but check for
more than one, plus READMEs scattered through the codebase). For each,
note its file count, rough age (last commit date per file, via
`git log -1 --format=%ad -- <file>`), and whether an index or table of
contents already exists.

Done when: you have a file list for every docs folder in scope, each with
a last-changed date.

## 2. Scan for broken links

Run the link mapper bundled with this skill against each docs folder (in
Claude Code the skill's folder is `${CLAUDE_SKILL_DIR}`; otherwise use the
path this skill was linked from):

```bash
python3 "${CLAUDE_SKILL_DIR:-.}/scripts/doc_map.py" docs/
```

It reports broken internal links, broken heading anchors, and files with
no incoming internal link (orphans). It only checks links between the
files it scans; it does not follow links out to the rest of the
repository or to the internet. If code comments or a README elsewhere
link into the docs folder, grep for those separately
(`grep -rn "docs/" --include=*.md --include=*.php --include=*.ts .` or
similar for the project's languages) so a rename does not silently break
them too.

Done when: you have the full list of broken links, broken anchors and
orphaned files for every folder in scope.

## 3. Judge staleness, not just age

An old file is not automatically a stale one. Read each candidate and
check it against the thing it describes: does the described command,
file path, API shape or screenshot still match the code? A setup guide
for a stable process can be a year old and still correct; a page about a
feature that shipped last month can already be wrong if the feature
changed twice since. Treat these as strong stale signals:

- it names files, functions or routes that no longer exist in the repo
- it contradicts a newer doc on the same topic
- it is marked draft, TODO or "WIP" and nobody has touched it in months
- its only inbound links are themselves broken or from other stale docs

Done when: every candidate doc is marked current, stale, or unclear
(needs the user's judgement), with the evidence for each call.

## 4. Find duplicates

Two docs can duplicate each other under different names: same setup
guide written twice, a topic covered in both a top-level README and a
docs page, an old draft left beside its finished replacement. Compare
titles, headings and opening paragraphs rather than relying on exact
filename matches. When you find a pair, work out which is more complete
and more recently accurate; that is the one to keep.

Never delete a doc outright. Propose which copy to keep and what to do
with the other (merge its unique content into the keeper, then remove
it, or redirect readers to the keeper with a short note) and get the
user's go-ahead before removing anything.

Done when: every duplicate pair has a proposed resolution and nothing has
been deleted without agreement.

## 5. Organise what stays

Group surviving docs by audience or topic, matching whatever structure
the project already leans towards rather than inventing a new one from
scratch. Give every folder with more than a couple of files an index
(`README.md` or `index.md`) that links to everything in it, so nothing
becomes an orphan again. Prefer moving and relinking over renaming when a
file's content did not change: a rename breaks every inbound link, so do
it only when the current name is genuinely misleading, and update every
reference (docs and code comments) in the same change.

Use relative links between docs (`../guide.md`, not an absolute path from
the repository root) so the folder still works if it is moved or read
outside its usual home. Anchors only break when the heading text
changes, so check anchors again after any heading edit.

Done when: every folder in scope has an index, and every doc that stays
is reachable from it.

## 6. Fix links and re-scan

Apply the fixes: correct relative paths, remove links to files that no
longer exist (or point them at the replacement), and update anchors that
moved. Re-run the scanner from step 2 to confirm the count has dropped to
zero, or list what is deliberately left (for example, a link into a
folder outside the scan that you have verified by hand).

Done when: `doc_map.py` reports zero broken links and zero broken anchors
for every folder in scope, or the remainder is explained.

## 7. Report

```markdown
## Doc tidy: <folder(s)>
**Scanned:** <n files across n folders>

### Fixed
- <broken link/anchor fixed, file:line>

### Removed or merged (with agreement)
- <file>: <what happened, and why>

### Left for a decision
- <file>: <stale/duplicate/unclear, and what you'd need to resolve it>

### Structure changes
- <folder>: <index added, files moved, etc.>
```

## It's working if

- The link scanner reports zero broken links and anchors on the folders
  you touched.
- Nothing was deleted or merged without the user agreeing to it first.
- A reader can start at any folder's index and reach every current doc
  in it without hitting a dead link.
