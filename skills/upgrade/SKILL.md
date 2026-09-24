---
name: upgrade
description: >-
  Plans and carries out a framework or language version upgrade (Laravel,
  Rails, Django, Node, PHP, and similar), from reading the official upgrade
  guide through fixing breaking changes to a tested rollback plan. Use when
  the user wants to upgrade a framework or runtime version, move to a new
  major release, or fix deprecation warnings left by a version bump. Not for
  routine dependency bumps or data migrations.
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Upgrade

A framework or language upgrade looks like a version number change and
behaves like a hidden rewrite: renamed methods, changed defaults, a
dependency that has not caught up. Done casually, it either stalls
half-finished or ships a build that passes locally and breaks in
production. This skill treats it as a project with a known shape: know the
starting point, know what changes, prove nothing broke, keep a way back.

## 1. Record the starting point

Before changing anything, run the full test suite and note whether it is
green. Write down the current framework and language versions, and how they
are pinned (a lockfile, a version manager file, a container base image).

If the suite is not green today, stop and say so: an upgrade cannot be
verified against a baseline that is already broken.

Done when: you can state the current versions and the suite's current
result in one line each.

## 2. Read the upgrade guide and list what applies

Find the target framework or language's own upgrade or migration guide for
this exact version jump (not a general changelog) and read it in full.
Pull out only the changes that touch this codebase: renamed or removed
APIs, changed defaults, new minimum versions of anything else, and any step
the guide says must happen in a particular order.

Write these as a short numbered list. A guide with forty entries usually
touches five things in a given project; the other thirty-five are noise to
filter out, not copy in.

Done when: you have a list of changes that actually apply here, each with
where it applies in the code.

## 3. Protect a way back

Create a branch for the upgrade and make sure the current state is
committed or tagged, so returning to it is a single command. If the
upgrade includes a data migration, plan and test its down direction (or a
backup and restore) before running the up direction anywhere real. Do this
work in a branch or staging environment, never directly on a production
target.

Done when: you can name the exact command that would undo everything done
so far.

## 4. Check what depends on the thing you are upgrading

List the project's direct dependencies that declare a compatibility range
against the framework or language version, and check each one's own
release notes for the target version. A library still pinned to the old
major version blocks the upgrade until it is updated or replaced, and
finding that on step 6 costs far more than finding it now.

Done when: every dependency with a version constraint on the thing being
upgraded is confirmed compatible, updated, or flagged as a blocker.

## 5. Make the change, then fix what it breaks

Bump the version declaration, then work through the list from step 2 one
item at a time: fix the breaking change, run the affected part of the
suite, move on. Prefer the framework's own automated upgrade tooling where
one exists (a codemod, a linter with an autofix mode) over hand-editing
every call site, then read its diff rather than trusting it blind.

Treat deprecation warnings as work, not noise: a warning today is a removed
feature next major version, and fixing it now costs one line instead of a
future emergency.

Done when: the change list from step 2 is empty and the codebase builds
without new warnings from the upgraded framework or language.

## 6. Prove it with the full suite, twice

Run the complete test suite, not just the areas touched. Then exercise the
paths a suite typically under-covers by hand: background jobs, scheduled
tasks, anything that only runs under a specific configuration. Compare this
result against the baseline from step 1: a suite that was already green and
stays green is evidence; a suite that was never run before the upgrade
proves nothing.

Done when: the full suite passes and you can say specifically what changed
in its result compared with the baseline.

## 7. Report

State the version moved from and to, the list of breaking changes fixed
with where, the dependencies that had to move too, the test result before
and after, and the rollback command from step 3. If anything from step 2
could not be resolved, say so plainly rather than shipping a partial
upgrade silently.

Framework-specific detail for PHP and Laravel upgrades, including
`composer.json` changes and known breaking changes by version, is in
[references/laravel.md](references/laravel.md).

## It's working if

- Every breaking change on the list from step 2 has a matching fix, or is
  named as unresolved in the report.
- The full suite ran green both before and after, not just after.
- Someone reading the report knows the exact command to undo the upgrade
  without asking.
