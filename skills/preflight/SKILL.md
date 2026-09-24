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

Every plan rests on assertions about the world: a file is where it says,
a command accepts a given option, a table has a given column, a hook does
what the plan expects. Plans go wrong where those assertions were never
tested. A preflight skims the document, then tests its assertions against
the real repository, shell and connected systems, and only after that
writes its notes, placed beside the lines they question.

## 1. Collect the claims

Read every target document in full (the spec before the plan, because the
plan inherits its assumptions). Note its status: a draft is reviewed for
direction, an approved plan for whether it can be carried out.

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

Observe only: no installs, no migrations, no database writes, no servers
left running, nothing sent over the network that changes anything. Open databases read-only.
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
- **Push back:** a decision you would make differently. Offer the
  alternative that is cheaper or less risky, and what it would cost. Scope
  counts: name the slice that could ship alone.
- **Suggestion:** improves the plan; work can proceed without it.
- **Question:** needs an answer before a task can start; give both
  readings and which you would take.

On the shared blocker/major/minor scale, a blocker is a blocker, push back
is major and a suggestion is minor; a question is not rated.

Prefer the smallest change, built-in features over new machinery, and no
abstraction with a single user. Thorough authors tend to over-build; ask
whether the first release needs each piece.

Done when: every finding has a kind, a location, evidence and a proposed
change.

## 4. Write notes into the document

Add each note as a quote block directly under the text it concerns. The
author's words stay exactly as written, checkboxes included: the
diff should contain only added lines, so the notes can be read and removed
independently.

```markdown
> **Review: Blocker.** The problem in one or two sentences.
> Proof: `the command you ran` gave `the line that matters`
> Suggest: what to change, briefly.
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

Done when: the summary gives the counts, one line per blocker and question,
and the path to the notes.

## It's working if

- Every finding carries the command and output that prove it.
- The author's text is untouched; only notes were added.
- Nothing in any system changed during the review.
