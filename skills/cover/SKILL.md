---
name: cover
description: >-
  Writes tests for a feature, existing code or a bug, in the project's own
  test framework and style, and proves each one fails for the right reason
  before it passes. Use when the user asks to write or add tests, improve
  test coverage, or add a regression test for a bug.
license: MIT
allowed-tools: Bash Read Edit Write Grep Glob
---

# Cover

A test earns its place by failing when the behaviour breaks. Plenty of
tests pass forever because they check nothing, or check the wrong thing.
This skill writes tests that match the project's conventions, cover the
cases that matter, and are shown to fail for the right reason at least
once.

To repair tests that are already failing, use `realign` (if installed).

## 1. Make sure tests cannot touch real data

Find out what the test run connects to before running anything: test
environment files, the test runner's configuration, any database or
service URLs it sets. The test run must use a throwaway database (in-memory
or a dedicated test file or schema) and fake outside services.

If the configuration points at a shared, development or production
database, stop and ask. Never run tests to find out.

Done when: you can name the database and services the tests will use, and
they are safe to wipe.

## 2. Learn the house style

Read two or three existing tests near the code you are covering. Note the
framework, file locations and naming, how test data is built (factories,
fixtures, builders), how outside services are faked, and the command the
project uses to run tests (package scripts, a Makefile, contributor docs).

Done when: your new test would look at home next to its neighbours.

## 3. Decide what to cover

For a feature or unit of code, work through:

| Case | Question it answers |
|---|---|
| Happy path | Does the expected use work? |
| Invalid input | Is bad input refused with a clear error? |
| Permissions | Can only the right people do it? |
| Edges | Empty, zero, one, many, maximum, non-ASCII text |
| Failure | What happens when a dependency fails? |

Test behaviour through the public surface (the endpoint, the command, the
public method), not private details, so the tests survive refactoring.

Done when: there is a short list of named cases, each tied to one of the
questions.

## 4. For a bug: fail first, for the right reason

Write the test before touching the code, run it, and read the failure. An
exception, an empty result and the predicted wrong value all show red; only
the predicted wrong value proves the test measures the bug. Quote that
failure message.

If the test passes, or fails for some other reason, fix the test before
fixing the code.

Done when: the quoted failure matches the bug the user described.

## 5. Write and run

Write the tests, then run them with the project's command. For tests of new
behaviour, check each one can fail: break the behaviour briefly (or invert
an expectation), confirm the test goes red, then restore.

Run the wider suite for the area as its own command (never piped through
another command that hides the exit code).

Done when: the new tests pass, each has been seen failing, and the
surrounding suite still passes.

## 6. Report

The cases covered, the command run and its result, and anything left
untested with the reason.

Laravel and Pest specifics: [references/laravel.md](references/laravel.md).

Done when: the report names the cases covered, the command run and its
result, and anything left untested with the reason.

## It's working if

- Every new test has been seen to fail at least once.
- A regression test's failure message describes the user's bug.
- The tests never touched a database or service that matters.
