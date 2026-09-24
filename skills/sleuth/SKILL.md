---
name: sleuth
description: >-
  Tracks down a bug methodically: builds a minimal, repeatable reproduction
  first, isolates the real cause by narrowing rather than guessing, applies
  the smallest fix, and locks it in with a regression test. Use when the
  user reports an error, exception, crash, stack trace, or says something
  "used to work" and now doesn't. Not for judging how serious or urgent a
  report is; use `triage`.
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Sleuth

Bugs get fixed twice as slowly when the first attempt is a guess dressed up
as a fix. This skill forces the reproduction to exist before any theory
does, then narrows it down systematically instead of reading code and
hoping. A fix that was never seen failing, and never seen passing, is not
verified: it is a hope with extra steps.

To judge how urgent a report is before investigating, use `triage` (if
installed).

## 1. Collect what is known

Gather the error message in full, the exact steps or input that trigger it,
when it started (a commit, a deploy, a data change), and how many people or
cases are affected. Check the obvious sources first: application logs,
recent commits touching the area, and configuration that differs between
where it works and where it doesn't.

Done when: you can state the bug in one sentence a stranger would
understand.

## 2. Build a loop that goes red for the right reason

Before forming any theory about the cause, get one command, script, or
request that you have actually run and that reliably reproduces the
symptom: not "throws an error" but the user's exact wrong output or
behaviour. Quote its failing output.

Check the loop against each of these before trusting it:

- **It exercises the real path.** The same code, config and data shape the
  user hit, not a simplified stand-in that happens to also fail.
- **It fails for the right reason.** An exception in setup and an empty
  result both look red; only a result that matches the reported symptom
  proves the loop measures this bug, not something adjacent.
- **It is fast and deterministic.** Seconds, not minutes, and the same
  verdict every run. For a bug that only reproduces sometimes, run it
  enough times to know the rate before trusting a single green result.

If you cannot build this loop (needs access you don't have, needs a
production artefact, needs the user to attach something), say so and ask,
rather than moving on to theorising anyway.

Done when: you have run the loop at least once and pasted its failing
output, and the output matches the reported symptom.

## 3. Cut the reproduction down to the minimum

Starting from whatever first reproduced the bug, remove one input, one
config value, one step at a time, re-running the loop after each cut. Keep
a cut only if the bug still reproduces without it. Stop when every
remaining piece is load-bearing: removing any one of them makes the bug
disappear.

A minimal reproduction usually reveals the cause on its own, because
everything irrelevant has been stripped away.

Done when: no further piece can be removed without losing the failure.

## 4. Isolate the cause, don't assume the layer

When a bug could originate in more than one layer (the interface, the
request handling, the business logic, the data store), check each boundary
in turn rather than committing to a guess. Log or inspect what crosses each
boundary: what was sent, what was received, what was read back after a
write. A report that sounds like "the save isn't working" is just as often
stale input reaching the save as a broken save itself.

Rank the plausible causes by the evidence gathered so far, most likely
first, and say what would confirm or rule out each one before spending time
on it. Layer-by-layer checks for queues, Livewire and saves that do not
stick: [references/laravel.md](references/laravel.md).

Done when: one cause is confirmed by direct evidence, not inferred from
its plausibility alone.

## 5. Apply the smallest fix and write a regression test

Fix the cause you confirmed, not everything that looked untidy nearby. Then
write a test that fails against the old code and passes against the fix; if
you still have the pre-fix code available, show it failing first so the
test is proven to measure the right thing.

Done when: the regression test fails on the old behaviour and passes on
the fix, and you have shown both.

## 6. Confirm nothing else broke

Run the loop from step 2 again (it should now pass) and run the wider test
suite for the affected area as its own command, not piped through anything
that could hide a non-zero exit code.

Done when: the original loop is green, the new regression test is green,
and the surrounding suite is unchanged or green.

## 7. Report

State the confirmed cause, the fix, the regression test added, and the
commands run with their results. If a cause was suspected but never
confirmed, say so rather than folding it into the fix silently.

## It's working if

- The reproduction existed, and was seen failing, before any fix was
  written.
- The regression test's failure message describes the reported bug, not a
  generic assertion.
- The final report names one confirmed cause, not a list of things that
  might have been it.
