---
name: seed
description: >-
  Generates realistic fake data for development, demos and tests: factories,
  seeders and one-off scripts whose values look plausible, respect the
  model's constraints and never collide with real records. Use when the
  user asks to seed a database, write a factory, generate sample or demo
  data, populate a test database, or fill an app with fake users, orders or
  content.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Seed

Fake data is easy to generate and easy to get wrong. Random strings in a
name field, emails that collide on a unique index, order totals that ignore
a foreign key, a seeder that doubles every row on a second run: all of it
passes a glance and fails the first real use. This skill builds seed data
that reads as real, respects the schema, and can be dropped into a
database as often as needed without harm.

## 1. Read the model before generating anything

Look at the table or model definition, not just its name: every column's
type, nullability and default; unique and foreign-key constraints;
validation rules if the project has them; and any relationships the record
must satisfy (a review needs an order, an order needs a customer). A
`status` column with a check constraint or an enum type tells you the exact
values allowed; guessing gets it wrong half the time.

Done when: you can list every field with the kind of value it needs and
which fields are constrained.

## 2. Match each field to a generator, not a random string

Pick a generator by what the field means, not its type. A `phone` column is
a string, but `random_string(11)` will not look like a phone number to
anyone testing the UI. Work field by field:

| Field means | Generate |
|---|---|
| Person's name | a name generator, first and last split if the schema splits them |
| Email | a fake address on a safe domain, unique per row |
| Free text (short) | a short sentence or phrase |
| Free text (long) | a few paragraphs |
| Date | a range that makes sense for the field (`created_at` in the past, `expires_at` in the future) |
| Money | a plausible amount for the domain (cents for a coffee, pounds for a laptop), not a huge random float |
| Status or category | one of the exact allowed values, weighted so the common ones are common |
| Identifier (SKU, reference) | the project's real format, for example `ABC-123`, not a raw UUID if humans read it |

Done when: every field in the definition maps to a named generator or a
fixed choice, and none of them is a bare random string standing in for
meaning.

## 3. Build relationships from the data, not around it

Create parent records first and reference them, rather than generating
disconnected rows and hoping foreign keys line up. For a one-to-many
relationship (a shop with many orders), create the parent, then generate
children that reference it explicitly. For a many-to-many relationship,
attach a realistic number of related records, not the same count for every
row: a subscriber has one plan, a customer has between one and five orders,
a product has zero to a dozen reviews.

Done when: every foreign key on a generated row points at a row that
exists, and the count on each side looks like real usage rather
than a fixed number repeated everywhere.

## 4. Cover named scenarios, not just bulk rows

Bulk data alone hides bugs that only show up at the edges. Alongside the
main volume, generate named cases that exercise the boundaries: an account
with no orders yet, one with far more than typical, a record with every
optional field left blank, a record with every optional field filled, a
value at the exact edge of a limit (a discount of exactly 100%, a title at
the maximum length). Give each scenario a recognisable value (a name, a
slug) so a developer can find it again without querying for it.

Done when: the boundary and empty-state cases relevant to this model are
present and named, not left to chance in the random bulk.

## 5. Make runs repeatable and safe to repeat

Decide, and say which, before writing the seeding logic:

- **Idempotent**: running it twice does not duplicate rows. Look up by a
  natural key (an email, a slug, a code) before creating, or check whether
  the target table is already populated before seeding it at all.
- **Deterministic**: a fixed random seed produces the same data every run,
  useful for a test fixture that must not shift under a developer's feet.
- **Fresh bulk data**: intentionally different data on every run, for a
  development database being refreshed.

State which of these applies in the seeder or script itself, in a comment
or its name, so the next person does not have to read the generator calls
to find out.

Done when: running the seeding twice does what you decided it should, and
that decision is visible in the code.

## 6. Keep fake data recognisably fake

Use a domain and value ranges that could never be mistaken for a real
customer or a real payment: `example.com` or `example.org` email addresses,
placeholder phone numbers reserved for fiction where the locale has them,
and no data lifted from a real account, real names or a real spreadsheet.
Never seed a fake row into a production database, and never let a seeding
script read from or write to live customer data as a shortcut for
"realistic" values.

Done when: nothing generated could pass for a real person's data if it
leaked, and no step reads from a live or production data source.

Framework-specific factory, seeder and generator notes:
[references/laravel.md](references/laravel.md).

## It's working if

- Every generated record satisfies the schema's constraints on the first
  insert, with no unique-key retries or foreign-key failures.
- A developer can point at a handful of seeded rows and describe what
  scenario each one is meant to show.
- Running the seed step twice leaves the database in the state you decided
  on, not a surprise.
