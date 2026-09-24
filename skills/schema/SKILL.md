---
name: schema
description: >-
  Designs relational database schemas: tables, keys, relationships,
  indexes and constraints, and writes the migration that creates or
  changes them safely. Use for 'design a schema', 'add a table', 'what
  columns should this have', 'add an index', 'add a foreign key', or
  'is this migration safe to run on a live database'.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Schema

A schema written without a plan tends to grow one table at a time, each
shaped by whatever screen needed it that week. The result is columns that
mean two different things in two tables, foreign keys that were never
added because nobody got round to it, and a migration that locks a live
table because nobody asked what it would cost. This skill designs the
shape first, then writes the migration to match it.

## 1. Work out what you are actually storing

List the entities the feature needs and, for each one, how it is
identified, which other entities it belongs to or owns, and roughly how
many rows it will hold. A "subscription" that belongs to one customer and
has many "invoices" is a different shape from a "subscription" that many
customers share.

Also note how the data will be read: the questions the application will
ask most often ("all orders for this customer", "invoices overdue by more
than 30 days"). Index decisions in step 4 come straight from this list, so
skipping it here means guessing later.

Done when: you can name every table, what it belongs to, and the two or
three questions it will be asked most often.

## 2. Name things so the schema reads itself

Consistency here saves every future query from a lookup. Pick one
convention and hold it across the whole schema: plural table names, a
single `id` primary key, `<singular>_id` foreign keys, verb-prefixed
booleans, one `status` column instead of a scatter of flags, money as
integer minor units, and a timestamp per meaningful state change. The full
list with reasons is in [references/naming.md](references/naming.md).

Done when: every table and column name follows the same convention, and a
reader could guess an unseen column's purpose from its name alone.

## 3. Choose keys, relationships and cascade behaviour

For each relationship between two entities, decide which of the four
shapes it is, because the shape decides where the foreign key lives:

| Relationship | Where the foreign key goes |
|---|---|
| One record belongs to one other (one-to-one) | On the dependent table |
| Many records belong to one (one-to-many) | On the "many" side |
| Many-to-many | On a join table, one foreign key to each side |
| One record can belong to several different kinds of thing (polymorphic) | A type column plus an id column on the dependent table |

For a many-to-many join table, name it after both sides
(`order_product`, not `order_items` if `order_items` actually carries its
own data like quantity and price, which makes it a real table, not a pure
join). Add a unique constraint on the pair of foreign keys so the same
pairing cannot be inserted twice, unless the join genuinely allows
repeats.

Then decide, for every foreign key, what happens when the row it points
to is deleted. This is the decision most schemas skip, and it is the one
that causes either orphaned rows or unexpected mass deletion later:

- **Cascade the delete** only when the child record has no meaning
  without the parent (delete an order, its line items go with it).
- **Set the foreign key to null** when the child should survive
  (delete a staff account, the posts they wrote should stay, author
  unset), which requires the column to be nullable.
- **Block the delete** when losing the parent while children exist is
  probably a mistake (a product category with products still in it).

Done when: every foreign key has a stated delete behaviour and a reason,
not just whatever the framework defaults to.

## 4. Add the indexes the query list from step 1 needs

An index speeds up exactly the queries that use it and slows down every
write to that table, so add indexes to match real access, not every
column that might one day appear in a `WHERE` clause.

- A column tested for equality on its own (`WHERE customer_id = ?`) needs
  a single-column index.
- Two or more columns always tested together
  (`WHERE customer_id = ? AND status = ?`) need one composite index
  covering both, with the columns tested for equality first and any range
  or sort column last, not two separate single-column indexes.
- A column used to sort a filtered list (`WHERE status = ? ORDER BY
  created_at`) wants the sort column added to that same composite index,
  so the database can skip a separate sort step.
- Every foreign key needs an index unless the database creates one
  automatically, because a delete or update on the parent has to search
  the child table for matching rows.
- A uniqueness rule (one active subscription per customer, one slug per
  article) is a unique index, not application-level checking alone,
  because only the database can stop two concurrent writes both passing
  the same check.

Skip an index on a column with only a handful of distinct values (a
boolean, a three-state status) unless it is always paired with something
more selective; on its own it rarely narrows the search enough to earn
its upkeep cost.

Done when: every query from step 1 has an index that covers it, and no
index exists that nothing in step 1 needs.

## 5. Write the migration and check it is safe to run

Before writing it, classify the change:

- **Safe on a live table**: adding a nullable column, adding a column
  with a default, adding a new table.
- **Needs a plan**: renaming or removing a column or table, changing a
  column's type, adding a required column to a table that already holds
  rows, adding a unique constraint that existing data might violate,
  adding an index to a large table (a plain `CREATE INDEX` on PostgreSQL
  blocks writes until it finishes; use `CREATE INDEX CONCURRENTLY`), and
  adding a foreign key to a large table (the database checks every
  existing row while holding a lock).

For anything in the second group, expand before you contract (add the new
shape, backfill, switch reads, then remove the old); `relocate` (if
installed) plans and rehearses that sequence step by step.

Make the migration safe to retry, and run it against a copy of the schema
(or in dry-run form) before it touches real rows.

For Laravel migration syntax, `Schema::create`, `Blueprint` methods and
`artisan` commands, see [references/laravel.md](references/laravel.md).

Done when: the migration has run cleanly against a real or copied
database, and any change in the "needs a plan" group has a stated
backfill and cutover order rather than a single all-at-once step.

## 6. Report the shape

State the tables and their columns, the relationships with their delete
behaviour, the indexes and which query each one serves, and, for any
breaking change, the deploy order. This is what the next person reviews,
so it needs to stand alone from the migration file.

## It's working if

- Someone unfamiliar with the feature can read the table and column names
  and describe what the data means, without opening the code.
- Every query the feature needs is covered by an index, and no index
  exists that nothing needs.
- A rename, type change or new required column ships as a sequence of
  safe steps, never as one migration that fails or locks on existing
  data.
