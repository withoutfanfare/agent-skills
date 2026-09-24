# Laravel migration notes

## A table, built to the conventions in SKILL.md

```php
Schema::create('subscriptions', function (Blueprint $table) {
    $table->id();
    $table->foreignId('customer_id')->constrained()->cascadeOnDelete();
    $table->string('plan', 40);
    $table->string('status', 20)->default('trialing');
    $table->unsignedInteger('price_pence');
    $table->timestamp('trial_ends_at')->nullable();
    $table->timestamp('cancelled_at')->nullable();
    $table->timestamps();

    $table->index(['customer_id', 'status']);
});
```

`foreignId('customer_id')->constrained()` assumes the column points at
`customers.id`; pass a table name when it does not
(`->constrained('accounts')`). Pair it with one of `cascadeOnDelete()`,
`nullOnDelete()` or `restrictOnDelete()`, chosen the way step 3 of
SKILL.md describes, never left as the default (which is to block the
delete with a database error).

## Many-to-many join table

```php
Schema::create('product_tag', function (Blueprint $table) {
    $table->foreignId('product_id')->constrained()->cascadeOnDelete();
    $table->foreignId('tag_id')->constrained()->cascadeOnDelete();

    $table->primary(['product_id', 'tag_id']);
});
```

Use a composite primary key instead of a surrogate `id` when the join
table carries no data of its own. The moment it needs extra columns
(quantity, position, a timestamp of when the tag was applied), give it a
normal `id` and a unique index on the pair instead, because a composite
primary key cannot be a foreign key target for anything else.

## Polymorphic relationships

```php
Schema::create('comments', function (Blueprint $table) {
    $table->id();
    $table->morphs('commentable'); // adds commentable_type, commentable_id, and their index
    $table->text('body');
    $table->timestamps();
});
```

`morphs()` adds the index for you; do not add a second one.

## Safe changes: add and default, don't lock

```php
// Nullable, no read of existing rows required
$table->string('middle_name')->nullable();

// Non-nullable, but a default means existing rows don't need a value supplied
$table->boolean('marketing_opt_in')->default(false);
```

A non-nullable column with no default fails immediately against a table
that already has rows, because Laravel has nothing to put in the existing
ones.

## Expand-contract for a column rename

```php
// Migration 1: add the new column alongside the old one
Schema::table('customers', function (Blueprint $table) {
    $table->string('full_name')->nullable();
});

// Application code: write to both columns while both exist

// Migration 2, once the backfill has run and both columns agree:
Schema::table('customers', function (Blueprint $table) {
    $table->dropColumn('name');
});
```

Backfill with `chunkById` rather than a single `UPDATE` on a large table,
so the write does not hold a lock across the whole table at once:

```php
DB::table('customers')->whereNull('full_name')->orderBy('id')
    ->chunkById(1000, function ($rows) {
        foreach ($rows as $row) {
            DB::table('customers')->where('id', $row->id)
                ->update(['full_name' => $row->name]);
        }
    });
```

## A unique index that must survive soft deletes

`SoftDeletes` leaves the row in the table with `deleted_at` set, so a
plain unique index on `email` blocks a new customer from reusing an
address a deleted account once held. Scope the index to live rows with a
raw statement, since Laravel's schema builder has no `->unique()` option
for a partial index:

```php
DB::statement(
    'CREATE UNIQUE INDEX customers_email_unique ON customers (email) WHERE deleted_at IS NULL'
);
```

## Commands worth knowing while designing

```bash
php artisan make:migration create_subscriptions_table
php artisan migrate --pretend      # print the SQL a migration would run, without running it
php artisan migrate:rollback       # undo the last batch, to check the down() method actually works
php artisan schema:dump            # snapshot the schema once old migrations are pruned
```

Always write and test the `down()` method for a migration that changes or
drops something; a migration that only knows how to move forward is a
one-way door.
