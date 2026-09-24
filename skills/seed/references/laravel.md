# Laravel notes

## Factories

Put one generator call per attribute in `definition()`, chosen for what the
field means (see the main skill's field table), and prefer the model's own
casts and fillable list over guessing at columns:

```php
public function definition(): array
{
    return [
        'name' => fake()->name(),
        'email' => fake()->unique()->safeEmail(),
        'phone' => fake()->phoneNumber(),
        'bio' => fake()->paragraphs(2, true),
        'status' => fake()->randomElement(['active', 'invited', 'suspended']),
        'signed_up_at' => fake()->dateTimeBetween('-2 years', 'now'),
    ];
}
```

For a `belongsTo` relationship, reference or create the parent inline
rather than leaving the foreign key to chance:

```php
'shop_id' => Shop::factory(),
```

For a `hasMany` relationship, attach children after the parent exists, in
`configure()`:

```php
public function configure(): static
{
    return $this->afterCreating(function (Order $order) {
        OrderLine::factory()
            ->count(fake()->numberBetween(1, 5))
            ->for($order)
            ->create();
    });
}
```

## States for named scenarios

A state is a named variation on the base definition, applied with
`->state()` or a dedicated method. This is where the boundary and edge
cases from the main skill's step 4 live:

```php
public function withOrders(int $count = 3): static
{
    return $this->has(Order::factory()->count($count));
}

public function suspended(): static
{
    return $this->state(fn (array $attributes) => [
        'status' => 'suspended',
        'suspended_at' => now(),
    ]);
}
```

Usage: `Customer::factory()->suspended()->count(3)->create();`

## Seeders

Match the seeder's shape to what it is for:

- **Idempotent seeder**, safe to run against a database that already has
  data (roles, plans, settings that must exist exactly once):

  ```php
  Role::firstOrCreate(['slug' => 'admin'], ['name' => 'Administrator']);
  ```

- **Development seeder**, bulk data plus explicit named scenarios, run
  against a database that is expected to be wiped and rebuilt:

  ```php
  Customer::factory()->count(200)->create();
  Customer::factory()->create(['name' => 'New signup, no orders']);
  Customer::factory()->withOrders(5)->create(['name' => 'Repeat buyer']);
  Customer::factory()->suspended()->create(['name' => 'Suspended test account']);
  ```

- **Test seeder**, deterministic data for a repeatable assertion. Seed the
  faker instance so the same run always produces the same values:

  ```php
  fake()->seed(1234);
  ```

Run a specific seeder with `php artisan db:seed --class=CustomerSeeder`, and
wrap multi-step seeders in a database transaction so a failure partway
through does not leave half-written data.

## Keeping generated data apart from real data

Use `fake()->unique()->safeEmail()` (Faker's `safeEmail()` draws from
reserved example domains) rather than a real provider, and check any script
that could run against a non-local database before running it:

```bash
php artisan tinker --execute="echo config('database.default');"
```

If that prints a production connection name, stop.

## Locale

Set the app's Faker locale when the project's users are concentrated in
one country, so names, phone numbers and addresses look native rather than
the US-English default. It is the `faker_locale` option in
`config/app.php`, which recent skeletons read from the environment:

```bash
# .env
APP_FAKER_LOCALE=en_GB
```
