---
name: catch-up
description: >-
  Summarises what changed in a project while the user was away: commits by everyone, branches, pull requests, issues, handover notes,
  reverted work and anything left uncommitted, on one screen, ordered by
  what needs them first. Use when the user says "catch me up", asks what has
  happened here or where they left off, or is returning after time away.
license: MIT
argument-hint: "optional: how far back, for example '2 weeks'"
allowed-tools: Read Glob Grep Bash
---

# Catch-up

Arriving cold at a project (Monday morning, back from leave, switching
between clients), the question is "where was I, and what needs me first?".
This skill answers it on one screen so the user can start working instead
of reading history.

## 1. Set the window

Use the window the user gave. Otherwise, anchor on their own last commit
in this repository:

```bash
git log -1 --author="$(git config user.email)" --format='%cr (%h)'
```

Fall back to the last two weeks if they have never committed here.

Done when: the window's start date is known.

## 2. Gather

Collect these, running independent commands together:

- **Handover notes first:** any handover or brief files the project uses
  (for example `HANDOFF.md`, `docs/handover/`, `docs/briefs/`). If one exists, it leads
  the briefing, and the rest shows what changed after it was written.
- **Git:** commits since the window by everyone (teammates' work matters
  too), the current branch, unmerged local branches, stashes, and
  uncommitted changes.
- **Pull requests and issues:** open, recently merged and recently closed,
  through `gh` or the project's tracker, if available. Skip quietly if not.
- **Plans and to-do files** changed inside the window.
- **What did not hold:** reverts (`git log --grep='^Revert'`), pull
  requests closed without merging, reopened issues. The next attempt
  should start where the last one failed.

Done when: each source has been checked or noted as unavailable.

## 3. Check claims against live state

A branch, pull request or ticket mentioned in a note is a claim, not a
fact. Confirm each one with `git` or `gh` before it goes in the briefing.

Done when: every item in the briefing was confirmed against live state.

## 4. Brief

One screen, plain words, ordered by what needs the user first. Explain what
a change means, not just its commit message. Group by theme, not by
commit.

```text
# <project>: since <date>

## Your first job
- <the most urgent thing: an unfinished branch, failing checks, a review waiting>

## Since you left
- <one line per thread, yours and others'>

## Tried and did not hold
- <reverted fixes, abandoned approaches; five at most>

## Loose ends
- <uncommitted changes, stashes, unmerged branches, old handover notes>

## Suggested first move
<one concrete next action>
```

Leave out empty sections. If nothing needs the user, say so in two lines;
a short briefing is a good result.

Done when: the brief fits one screen, names a first job or says nothing
needs the user, and ends with one concrete next action.

## It's working if

- The user can start real work straight after reading.
- Everything listed is true right now, not just when a note was written.
- Other people's work is included, not only the user's.
