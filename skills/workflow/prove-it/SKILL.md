---
name: prove-it
description: >-
  Proves a change actually works by running it and capturing real evidence:
  test output, HTTP status codes, database state, or screenshots, never "the
  code looks correct". Climbs a ladder from a targeted test up to a
  browser-driven flow, only as high as the change demands. Use when asked to
  verify a change, prove it works, smoke test a flow, or confirm nothing
  broke.
license: MIT
allowed-tools: Read Grep Glob Bash
---

# Prove it

"Should work" is a guess, not evidence. This skill treats verification
as evidence collection, not code review: every claim it makes is backed by
something that ran, with output pasted, not summarised from
memory of what the code appears to do.

For acceptance testing a whole journey or site until every scenario has a
verdict, use `acceptance-test` (if installed).

## 1. Work out what the change touches

Read the diff or the description of the change and list what kind of
surface it affects: internal logic only, a request or route, data written
to storage, or a user-facing flow. This decides how high up the ladder in
step 3 you need to go; do not run every rung out of habit.

Done when: you can name which surfaces changed, and which did not.

## 2. Make sure nothing stale gets in the way

Before running anything, clear whatever could make old behaviour look like
the current code: build caches, compiled config, a stale served asset
bundle. Confirm any background workers this change depends on (a queue
processor, a scheduled job) are running if the verification needs
them, rather than assuming they are.

Done when: you know the run will exercise the current code, not a cached
version of it.

## 3. Climb the ladder, only as far as needed

Run rungs in order, stopping once the change is covered. Skip a rung
outright if nothing it would check has changed.

1. **Targeted test run.** The fastest and most specific: run only the
   tests for the changed area, by name or path.
2. **Static analysis and style.** A type checker or linter over the
   touched files, run to report only, not to auto-fix mid-verification.
3. **HTTP smoke pass.** For anything routing- or request-shaped: hit the
   real endpoints against a running instance and check the status codes
   and shape of the response, not just that the server started.
4. **Data state assertions.** For anything that writes: trigger the action,
   then independently read back the data it should have produced, rather
   than trusting the code's own return value.
5. **Browser-driven flow.** For anything user-facing and important
   (signup, checkout, an admin action): drive the actual flow with the
   browser automation tools available, asserting state at each step and
   saving one screenshot per step to a run folder.

A migration plus a background job might need rungs 1 and 4 and skip 3
entirely; a new public form might need 1, 3 and 5.

Done when: each rung run has pasted output, not a description of what it
would probably show.

## 4. Treat a missing result as a result

If a rung cannot be run (no access to a required environment, no way to
trigger the real channel), say exactly that and why, rather than skipping
silently or substituting a weaker claim. "Could not verify the SMS send
because no test credentials are configured" is a valid, useful outcome.

Done when: every rung that did not run has a stated reason, not a silent
gap.

## 5. Report

```markdown
## Verification: <what was verified>
**Result:** <passed / failed / blocked (could not run)>

### Rungs run
| Rung | Command | Result |
|---|---|---|
| Targeted tests | `...` | 12 passed |

### Evidence
<pasted output, status table, row counts, or screenshot paths>

### Not verified
<what could not be checked and why>
```

Lead with anything that failed or could not be checked; do not bury it
under the rungs that passed.

If this is a Laravel project, the commands and pitfalls are in
[references/laravel.md](references/laravel.md).
A worked smoke-check script: [scripts/http-smoke.sh](scripts/http-smoke.sh).

Done when: the report shows the result, each rung with its command, the
evidence, and what was not verified.

## It's working if

- Every claim in the report traces to pasted output from something that
  ran.
- The rungs chosen match what the change touches, not a fixed checklist
  run every time.
- Anything that could not be verified is named, not silently dropped.
