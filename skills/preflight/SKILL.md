---
name: preflight
description: >-
  Reviews a design spec or implementation plan before anyone builds from it:
  checks every factual claim against the real repository, tools and systems
  without changing anything, finds blockers, pushes back with cheaper
  alternatives, and writes clearly marked review notes into the document
  itself. Use when the user asks to review or sanity-check a plan or spec,
  asks whether a plan has blockers, or wants pushback on a design.
license: MIT
effort: high
allowed-tools: Read Grep Glob Bash Edit
---

# Preflight

A plan is a stack of claims: this file exists, that command takes this
option, the database has that table, the hook behaves like so. Plans fail
on the claims nobody checked. So a preflight reads the document once, then
spends most of its time in the repository, the shell and the systems the
plan depends on, and only then writes notes, next to the text they
challenge.

## 1. Collect the claims

Read every target document in full (the spec before the plan, because the
plan inherits its assumptions). Note its status: a draft is reviewed for
direction, an approved plan for whether it can actually be carried out.

List every checkable claim in a scratch file, with where it appears:
paths, functions, tables and packages; versions and branch state;
commands and their options; outside systems (hooks, configuration,
databases, other repositories); tools the plan tells its executor to use;
project rules it must follow; numbers that drive behaviour (limits,
intervals, sizes).

Done when: there is one line per claim.

## 2. Check each claim, changing nothing

Settle each claim with the cheapest command that proves it, and keep the
command and its output line together as evidence.

Only look. Never install, migrate, write to a database, start a
long-running process or make a network write. Open databases read-only.
Probe commands with `--help` and read-only subcommands. If a claim can only
be checked with a login, a device or a deployment, mark it **unverified**
and say what would settle it.

Look past the plan's own map: read the source of any hook, script or
service it relies on. The strongest findings usually come from behaviour
the plan never mentions.

Done when: every claim is verified, wrong, or unverified, each with
evidence or a reason.

## 3. Judge

Sort findings into four kinds, and keep them honest: a suggestion dressed
as a blocker wastes someone's decision.

- **Blocker:** the plan cannot be carried out as written, or doing so
  would break a stated constraint or lose data.
- **Push back:** you disagree with a decision. Always give the cheaper or
  safer alternative and its cost. Scope counts: name the slice that could
  ship alone.
- **Suggestion:** improves the plan; work can proceed without it.
- **Question:** needs an answer before a task can start; give both
  readings and which you would take.

Prefer the smallest change, built-in features over new machinery, and no
abstraction with a single user. Thorough authors tend to over-build; ask
whether the first release needs each piece.

Done when: every finding has a kind, a location, evidence and a proposed
change.

## 4. Write notes into the document

Add each note as a quote block directly under the text it concerns. Never
edit, delete or reflow the author's text, and never tick a checkbox: the
diff should contain only added lines, so the notes can be read and removed
independently.

```markdown
> **Review: Blocker.** The problem in one or two sentences.
> Evidence: `command` → `output line`
> Proposed: the change, in one sentence.
```

Add one summary after the document's title or status line:

```markdown
> **Review summary (<date>).** Checked against <branch and commit>, <other
> repositories and systems probed>. Blockers: n · Push back: n ·
> Suggestions: n · Questions: n. Held up as written: <claims>. Decisions
> needed: 1. … 2. …
```

Done when: `git diff --numstat <file>` shows no deleted lines, and the
number of notes matches what you intended.

## 5. Report

In the conversation: the counts, the blockers and questions in one line
each, and where the notes are.

## It's working if

- Every finding carries the command and output that prove it.
- The author's text is untouched; only notes were added.
- Nothing in any system changed during the review.
