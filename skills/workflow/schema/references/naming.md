# Naming conventions

One convention, held across the whole schema:

- Table names: plural nouns (`orders`, `order_items`), because a table is
  a set of rows.
- Primary keys: a single `id` column per table, even when a natural key
  exists (an email address changes; a surrogate key does not).
- Foreign keys: `<singular of the referenced table>_id` (`user_id` on a
  table that belongs to `users`). When a table has two foreign keys to the
  same target, qualify both (`billed_to_id` and `shipped_to_id`, both
  referencing `addresses`).
- Booleans: a verb prefix (`is_active`, `has_paid`), never a bare noun,
  so a reader never has to guess which direction true points.
- State: one `status` column with a small, named set of values, not a
  scatter of booleans that can drift out of sync (`is_shipped`,
  `is_delivered`, `is_cancelled` can all end up true at once).
- Money: store the smallest unit as an integer (pence, cents), never a
  float, and name it accordingly (`total_pence`).
- Timestamps: `created_at` and `updated_at` on every table that changes
  after creation; a separate nullable timestamp for each meaningful state
  change (`paid_at`, `cancelled_at`) rather than reusing `updated_at` to
  mean "and this is when it was paid".
