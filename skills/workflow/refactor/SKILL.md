---
name: refactor
description: >-
  Restructures code without changing what it does: spots the smell, picks the
  refactoring that fits (extract, move, rename, replace conditional, value
  object), and moves in small, tested steps. Also cleans up tell-tale signs
  of generated code before a commit. Use when the user asks to refactor,
  clean up, extract, simplify or restructure a piece of code.
license: MIT
allowed-tools: Bash Read Edit Write Grep Glob
---

# Reshape

Refactoring means changing structure while behaviour stays exactly the
same. The discipline is in that promise: tests before the first edit, one
change at a time, a green run after each. Mix in a feature or a bug fix and
nobody can tell which change broke what.

For the same mechanical change across many files, use `codemod` (if
installed). To redesign a module's interface rather than tidy its code,
use `deep-modules` (if installed).

## 1. Pin the behaviour down

Find the tests that cover the code. Run them and confirm they pass. If
coverage is thin, write characterisation tests first: tests that record
what the code does today, right or wrong, so any change in behaviour shows
up.

Done when: a passing test run covers every path you are about to touch.

## 2. Name the smell

Say what is wrong before choosing a fix:

| Smell | Usual refactoring |
|---|---|
| A long function doing several jobs | Extract function |
| A long parameter list, or values that always travel together | Introduce a parameter object or value object |
| A method that mostly uses another class's data | Move it to that class |
| The same condition on a type repeated in several places | Replace conditional with polymorphism |
| Plain strings or numbers standing in for a concept (money, email, status) | Value object |
| One class that knows everything | Extract class, by responsibility |
| Copy-pasted logic | Extract the shared part, once |
| Business rules in a request handler or view | Extract a service or action |

Pick one smell per pass. Framework-specific patterns are in
[references/laravel.md](references/laravel.md) for Laravel projects.

Done when: you can say, in one sentence, what smell you are removing and
which refactoring removes it.

## 3. Move in small steps

Make the smallest change that moves towards the target, run the tests, and
commit or checkpoint. Repeat. If a step turns tests red, undo that step
rather than patching forward.

If the tidy-up reveals a real bug, note it and report it separately; do not
fix it inside the refactor.

Done when: the target structure is reached with the tests green after every
step.

## 4. Remove the tells of generated code

Before committing, read the branch's own diff and compare it with the files
around it. Fix anything a person on this project would not have written:

| Tell | Fix |
|---|---|
| Comments that narrate what the next line does | Delete; keep only what the code cannot say |
| Defensive checks on trusted internal paths that neighbouring code does not have | Remove, and let errors surface where the project handles them |
| Casts or ignore comments added only to silence a type checker | Fix the type |
| Deep nesting where an early return reads better | Guard clauses |
| Options, helpers or layers nothing uses | Delete them |

The surrounding code is the standard, not a rule list.

Done when: the diff reads like the rest of the codebase.

## 5. Report

The smell, the refactoring, the steps taken, the test runs (command and
result), and any bugs found but not fixed.

Done when: the report names the smell, the refactoring, each test command
with its result, and any bugs left unfixed.

## It's working if

- The tests passed before, during and after, with no expectations changed.
- Each commit makes one structural change.
- A reviewer cannot find a behaviour change in the diff.
