---
name: ledger
description: >-
  Keeps a living record of technical and product decisions: logs each one
  with its context, options and reasoning, sets a trigger to revisit it, and
  later records whether it held up. Use when the user says to log or record a
  decision, asks what was decided about something and why, or wants to
  review past decisions.
license: MIT
allowed-tools: Read Grep Glob Write Edit Bash
---

# Ledger

Six months on, nobody remembers why the team chose one database over
another, or why notifications poll instead of listening. The code shows
what was decided; only a record shows why, what else was on the table, and
what we expected to happen. This skill keeps that record, and comes back
to check whether each decision held up.

## Where the ledger lives

One file per decision in `docs/decisions/` in the repository, named
`YYYY-MM-DD-short-title.md`, unless the project already keeps decisions
somewhere else (an ADR folder, a wiki, a notes vault). Follow the existing
place and format when there is one.

## 1. Log a decision

Capture it while the reasoning is fresh. Take what the conversation already
holds; ask only for gaps, one question at a time.

```markdown
# <Searchable title, for example "Use Redis for session storage">
Date · Status: active · Confidence: high|medium|low · Scope: <areas>
Revisit: <a date, or a condition such as "if sign-ups pass 10,000 a day">

## Context
<what prompted the decision; the problem and constraints>

## Options
### <Option A>: pros · cons
### <Option B>: pros · cons

## Decision
<what was chosen and the main reason>

## We expect
<what we should see if this was right, in observable terms>

## Outcome log
```

A decision with only one option recorded is a record of a preference; ask
what else was considered.

Done when: the file exists with at least two options, an expected outcome
and a revisit trigger.

## 2. Look up a decision

Search the ledger by title, tags and text. Answer with the decision, its
date, the reasoning, and its current status, and link the file. If nothing
is recorded, say so rather than reconstructing a reason from the code.

Done when: the user has the decision and its source, or a clear "not
recorded".

## 3. Revisit decisions

List decisions whose revisit date has passed or whose condition may now be
true. For each one the user chooses, ask:

1. Are the original constraints still true?
2. Did the expected outcome happen?
3. Knowing what we know now, would we choose the same?

Record the answer in the outcome log with the date, and update the status:
**held up**, **partly held up** (with the caveat), **reversed** (with
what replaces it), or **superseded** (linking the newer decision). Set the
next revisit, or close it.

Done when: every reviewed decision has a dated outcome entry and a new
status.

## 4. Spot patterns

When there are enough entries, look across them: decisions made at low
confidence that later reversed, areas that keep being re-decided,
expectations that are consistently too optimistic. Report patterns with
the decisions behind them.

Done when: each pattern named lists the decisions behind it, or you have
said there are too few entries yet.

## It's working if

- Every entry says why, not only what.
- Revisits happen, and the outcome log shows real results.
- "Why did we do this?" gets answered from the ledger, not from memory.
