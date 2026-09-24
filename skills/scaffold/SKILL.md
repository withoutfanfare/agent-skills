---
name: scaffold
description: >-
  Generates a complete feature end to end: data model, storage layer,
  request handling, validation, authorisation and tests, wired together and
  proven to run, not just a pile of generated files. Use when creating a new
  model, resource, or CRUD feature from scratch, or when the user asks to
  scaffold or generate a feature.
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Scaffold

Generators are good at producing files and bad at producing a working
feature. Left alone they skip authorisation, leave validation as an
afterthought, and never prove the pieces fit together. This skill builds
the full vertical slice, in the project's own conventions, and shows it
running before calling it done.

## 1. Learn the project's shape

Find an existing feature that resembles the one being built (similar data,
similar CRUD shape) and read it end to end: where the data model lives,
how the storage layer is defined, how a request reaches the handler, where
validation and authorisation sit, and how the response is shaped. Match
that shape rather than introducing a new pattern.

If nothing comparable exists, use the project's own generator or scaffolding
command if it has one, then read what it produced before changing it.

Done when: you can name the files a comparable feature touches, in order.

## 2. Design the data first

Decide the fields, their types, and which are required, before writing any
handler. List:

- which fields can be set by a user, and which are computed or system-owned
  (an ID, a timestamp, an owner reference);
- indexes needed for lookups this feature will actually perform;
- relationships to existing data, and which side owns the foreign key.

Done when: the field list and relationships are written down before any
handler code exists.

## 3. Build the full slice

Write, in order: the data model and its migration or schema change, the
handler or controller, request validation, an authorisation check on every
write operation (create, update, delete), and the response shape (a
serialiser, resource, or view). Wrap multi-step writes in a transaction so a
partial failure cannot leave inconsistent data.

Authorisation is not optional on any write path. A feature with validation
but no ownership or permission check lets any authenticated caller act on
anyone's data.

Stack-specific detail and pitfalls: [references/laravel.md](references/laravel.md).

Done when: every write path has both a validation rule and an
authorisation check, and you can point to both for each one.

## 4. Cover it with tests

Write tests for: the happy path, rejected invalid input, a second user
being refused access to the first user's data, and the empty and edge-case
inputs (nothing, the maximum, an unusual character set). Build test data
through the project's own factories or fixtures, never by inserting rows by
hand.

Done when: an authorisation test exists and explicitly proves a second
user is refused, not just that the first user succeeds.

## 5. Prove it runs, not just that files exist

A scaffold is done when it demonstrably works. Reverse any schema change
and reapply it to confirm it is not one-directional. Create one record
through the real code path (not a hand-built row) and read it back. Run the
generated tests and show the output.

For full-flow verification against a running app, hand off to `prove-it` (if installed).

Done when: a record created through the real path round-trips correctly,
and the test run output is pasted, not summarised.

## 6. Report

The files created, the schema change (and that it reverses cleanly), the
tests run and their result, and anything intentionally left out (a feature
listed but not requested).

Done when: the report lists the files, the reversible schema change, the
test command with its result, and what was left out.

## It's working if

- Every write path found in step 3 has a matching authorisation test that
  fails for a second user.
- The schema change has been reversed and reapplied at least once.
- A record created through the generated code, not inserted by hand, comes
  back correctly on read.
