---
name: migrate-data
description: >-
  Plans a safe migration of production data: choosing between a maintenance
  window, expand-and-contract, dual writes or a shadow table, then writing
  the step-by-step plan with validation, batching, monitoring and a tested
  way back. Use when the user needs to move, reshape, split, merge or
  backfill existing data, or asks for a data migration or rollback plan.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Relocate

Adding a column is mechanical. Changing the shape of millions of existing
rows while the application keeps running is where data gets lost. This
skill plans that work so every step can be checked, paused and reversed,
and so the plan is rehearsed on realistic data before it touches the real
thing.

For designing a new schema, use `schema` (if installed) instead.

## 1. Understand the move

- **What moves or changes:** tables, columns, entities, and the
  transformation (copy, reshape, compute, split, merge).
- **How much:** row counts. What is instant at ten thousand rows takes hours
  at ten million.
- **Source of truth** during the move, and after it.
- **Downtime allowed:** none, or a window of how long.
- **Who reads and writes this data:** queries, reports, APIs, jobs,
  scheduled tasks, other services.

Done when: all five are answered with numbers and names, not guesses.

## 2. Find everything that touches it

Search the code for every model, query, job, endpoint, export and report
that reads or writes the affected data, and check test factories and seed
data. Each one must keep working at every step of the plan.

Done when: there is a list of readers and writers, each marked with the
step at which it switches over.

## 3. Pick a strategy

| Strategy | How it works | Choose when |
|---|---|---|
| Maintenance window | stop writes, migrate, switch, restart | small data, downtime acceptable |
| Expand and contract | add the new shape; write to both; backfill; switch reads; remove the old | the safe default for live systems |
| Dual writes | the application writes old and new while a backfill catches up | expand and contract is impractical; needs strong consistency checks |
| Shadow table | build a full new table beside the old, then swap | large reshapes; easy way back while the old table exists |

Recommend one and say why the others lose.

Done when: the strategy is chosen with a one-paragraph reason.

## 4. Write the plan

```markdown
# Data migration: <what>
Strategy · Rows · Expected duration · Downtime · Way back: easy|hard

## Before
- Row counts and checksums of the affected data, saved
- Checks for surprises: nulls where none are expected, duplicates, orphans, odd encodings
- Backup or snapshot taken and restore tested
- Rehearsal on a copy of production-sized data, timed

## Steps
### 1. <step>: what runs · reversible? · how to verify · how to undo
### 2. ...

## Backfill
Batch size, pause between batches, restart point if interrupted,
progress reporting, load limits on the live database

## Checks after each step
Counts, checksums, spot comparisons of sample rows, error rates

## Way back
Per step: the exact undo, and the last point at which undo is still possible

## Watch
Metrics and logs to watch during and after, and who is on hand
```

Every step must be safe to run twice and safe to stop halfway.

Done when: each step has a verification and an undo, and the plan names
the point of no return.

## 5. Rehearse

Run the plan on a copy with realistic volume. Record timings and anything
that surprised you, and update the plan before the real run.

Done when: the plan has been run end to end on realistic data, with
timings recorded.

## It's working if

- Nothing in the plan is irreversible until a clearly marked, agreed point.
- Counts and checksums prove no rows were lost or duplicated.
- The real run matches the rehearsal's timings and results.
