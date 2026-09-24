---
name: filament
description: >-
  Builds Filament 4 admin panel resources: forms, tables, widgets, actions
  and relation managers, wired to the underlying policy so access is
  actually enforced, then proves it with a test. Use when creating an admin
  CRUD screen, a dashboard widget, or the user mentions Filament, an admin
  panel, or make:filament-resource.
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Filament

A Filament resource that renders is not the same as one an authorised user
can use and an unauthorised one is blocked from. This skill builds the
resource's form, table and actions, wires it to a policy that
runs, and proves both the access it grants and the access it denies.

It targets Filament 4, where forms are schemas (`Filament\Schemas\Schema`,
with `Section` under `Filament\Schemas\Components`), every action lives in
`Filament\Actions`, and tables take `->recordActions()` and
`->toolbarActions()`. On Filament 3, forms take `Form $form`, table
actions sit under `Filament\Tables\Actions`, and tables use `->actions()`
and `->bulkActions()`; check `composer.lock` before copying an example.

## 1. Generate and read the resource

```bash
php artisan make:filament-resource Post --generate --view
```

Read what it produced before extending it. It infers columns and fields
from the schema; it does not infer which of those belong on the form, on
the table, or on neither (an internal flag column rarely belongs on a
form).

Done when: you know which fields go on the form, which on the table, and
which are deliberately left off both.

## 2. Build the form around how it will be edited

Group related fields with `Section::make()`, and mark a field `->live()`
only where another field needs to react to it (a slug generated from a
title, for instance) since every `->live()` field adds a round trip on
change. Remember that `afterStateUpdated()` only fires on a field marked
live, and that `$get()`/`$set()` operate on the unsaved form state, not
the underlying model.

For a relationship field, use `->relationship('author', 'name')`, which
takes the relationship's method name, not the foreign key column.

Done when: every field that should react to another one is marked
`->live()`, and none that shouldn't are.

## 3. Build the table for how it will be scanned

Add `->searchable()` and `->sortable()` to the columns someone will
search or sort by, not every column reflexively. Use filters for
the dimensions users will narrow by (status, owner, date range).
Bulk actions can sit in a `BulkActionGroup::make([...])` dropdown or be
listed directly as buttons; both work, so follow what the panel already
does.

Done when: the columns, filters and actions match how the resource will
be used, not just what the generator produced.

## 4. Wire authorisation and prove it both ways

Filament reads the model's policy automatically. Create one if none exists:

```bash
php artisan make:policy PostPolicy --model=Post
```

A `viewAny()` that returns `false` for a given user removes the resource
from their navigation entirely and returns 403 Forbidden on its pages directly, which looks
like the resource vanished rather than like a permissions problem: check
the policy first if a resource "disappears".

Write two tests, not one: an authorised user reaching the index and create
pages successfully, and a second, unauthorised user refused on the same
routes. A resource proven only for the authorised case is half proven.

Done when: both tests exist, both have been run, and both pass.

## 5. Add widgets and custom actions only where they earn their place

A stats widget or a custom row action should answer a question someone
has ("how many are pending") or perform a real workflow step
("mark as shipped"), not decorate the panel. Confirm destructive custom
actions with `->requiresConfirmation()`.

Done when: each widget or custom action added maps to a stated need, not a
generic possibility.

## 6. Report

The resource built, the policy wired and its test evidence from step 4,
and any field, filter or widget deliberately left out.

For verification of the resource inside the full app (auth flow, real
data volume), hand off to `prove-it` (if installed).

Full field and widget reference, and further gotchas:
[references/patterns.md](references/patterns.md).

Done when: the report names the resource, the policy and its test result,
and anything deliberately left out.

## It's working if

- An unauthorised user's test against the same routes as the authorised
  one fails without the fix, and passes with it.
- Every `->live()` field has a reason another field needs to react to it.
- Selecting rows in the table shows the bulk actions the resource
  offers, and each one runs.
