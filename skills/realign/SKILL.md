---
name: realign
description: >-
  Gets a failing test suite green honestly: each failing test is either
  brought back in line with the code's current behaviour, keeping what it
  was meant to prove, or flagged as a likely real bug. Never weakens an
  assertion or edits production code to fake a pass. Use when the user asks
  to fix the tests, repair the test suite, or says the tests are red.
license: MIT
allowed-tools: Bash Read Edit Grep Glob
---

# Realign

There are two ways to turn a red suite green. One updates tests that
drifted from the code; the other deletes assertions until nothing
complains. Only the first is worth anything. This skill treats the
production code as the truth, updates how each test checks, never what it
checks, and hands anything that looks like a real bug to a human.

To write new tests, use `cover` (if installed).

## 1. Understand how the suite runs

Find the project's test command (package scripts, Makefile, contributor
docs), the base test classes and when each applies, and how test data and
databases are set up. Confirm the tests use a throwaway database before
running anything.

Done when: you can run the suite with the project's own command, and you
know what it connects to.

## 2. Run it and sort the failures

Run the whole suite once, as its own command, and list every failing test.
Group failures that share a cause (one renamed method can break forty
tests).

Done when: every failing test is listed, grouped by suspected cause.

## 3. Ask one question per failure

**Does the feature this test covers actually work?** Check by reading the
code, and by trying the behaviour if you can.

- **Yes, it works:** the test drifted. Align it (step 4).
- **No, it is broken:** this may be a real bug. Flag it (step 5) and move
  on. Do not edit production code.
- **Cannot tell:** flag it with what you found.

Done when: every failure has one of the three answers.

## 4. Align, keeping the intent

Change how the test verifies, never what it verifies. Common fixes:

| Symptom | Honest fix |
|---|---|
| Expected value changed on purpose | Update the expectation to the new correct value, and say why |
| Mock no longer matches the interface | Update the mock to the current interface |
| Missing setup after a schema or model change | Add the data the test needs |
| Hard-coded IDs or dates | Use generated references or a fixed clock |
| Wrong base class or database helper | Use the one the project uses for this kind of test |
| Deprecated test syntax | Move to the current syntax |

A test that passes alone but fails in the full suite points to shared state
or test order, not the assertion. Look there first.

Run each fixed test on its own, then its neighbours.

Done when: the aligned test passes and still fails if the behaviour it
covers is broken.

## 5. Flag, with evidence

For each suspected real bug, write: the test name, the failure output, what
the code does, what the test expects, and why you think the code is wrong.
Leave the test failing.

Done when: every flagged test has a write-up a developer can act on without
rerunning anything.

## 6. Finish with a full run

Run the whole suite as its own command (not piped through anything that
hides the exit code) and report:

```text
Passing: <n>   Aligned this session: <n>   Flagged: <n>
```

Every number must trace to named tests.

Done when: the summary line comes from a full run whose exit code you saw,
and each count names its tests.

## It's working if

- Every failure that started the session is either aligned or flagged.
- No assertion was deleted or loosened just to pass.
- Production code is untouched.
