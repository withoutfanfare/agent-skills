---
name: changelog
description: >-
  Adds entries to the project's CHANGELOG from the changes about to be
  committed or released, following the file's own format. Use when the user
  asks to update the changelog, add a changelog entry, or record what
  changed before a commit or release.
license: MIT
allowed-tools: Bash Read Edit Grep Glob
---

# Changelog

A changelog is for people deciding whether to upgrade, not for a list of
touched files. Good entries say what changed for the reader, in one line
each, grouped the way the file already groups them.

## 1. Find the changes

```bash
git diff --staged -M --stat
git diff --staged -M
```

`-M` shows a moved file as a rename instead of a delete plus an add. If
nothing is staged, check `git status`: the work is often unstaged. Ask
whether to describe the unstaged changes, or a range of commits (for a
release, everything since the last tag), rather than reporting "nothing to
log".

Done when: you know exactly which changes the entries will describe.

## 2. Learn the file's conventions

Read the existing CHANGELOG before writing a word. Note:

- how sections are headed (`## [Unreleased]`, version numbers, or dates);
- which categories it uses (Added, Changed, Fixed, Removed, Security,
  Deprecated, or its own);
- how an entry looks (bold component name? issue numbers? full sentences?);
- any link definitions at the bottom that new headings need.

If there is no changelog yet, create one in the
[Keep a Changelog](https://keepachangelog.com) style with an
`## [Unreleased]` section.

Done when: you could describe the file's format to someone else.

## 3. Write the entries

- Group related file changes into one entry. A feature touching twelve files
  is one line.
- Say what changed and why it matters to a reader, in plain words.
- One line per entry, in the file's style.
- Leave out test-only changes, small refactors and internal renames unless
  they change behaviour someone depends on.
- Always include breaking changes, new dependencies and security fixes.

Done when: every entry reads sensibly to someone who has not seen the diff.

## 4. Put them in the right place

Add entries to the unreleased section (`## [Unreleased]`, or the file's
own name for it), at the top of their category, and create that section
above the newest release if it is missing. Never add to a released
section: its version is already out. Search for the section first; a
second heading for the same release splits the entries and breaks
anything that parses the file. If headings carry link
references, add or update those too.

Done when: the file has one unreleased section, with the new entries
at the top of their categories.

## 5. Show the result

Show the user the new entries as a diff, so they can adjust wording before
committing.

Done when: the user has seen the diff of the new entries and approved or
adjusted the wording.

## It's working if

- A reader can tell what changed for them from the headings and first
  words of each entry.
- The file still looks like one consistent document.
- Nothing staged is left undescribed, and nothing unrelated is described.
