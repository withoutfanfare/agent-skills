# Laravel scaffolding notes

## Generating the pieces

```bash
php artisan make:model Listing -mfrc --policy
```

produces a model, migration, factory and resource controller together; the
`--policy` flag adds the authorisation class alongside them. The `-r` flag
means a resource controller, not an API resource: run
`php artisan make:resource ListingResource` separately if you need one.
Open each generated file and check it against your actual columns before
building on it: the generator has no idea what fields you need.

## Model

```php
declare(strict_types=1);

protected $fillable = ['heading', 'reference', 'seller_id'];
protected $casts = [
    'goes_live_at' => 'datetime',
    'is_featured' => 'boolean',
];

public function seller(): BelongsTo
{
    return $this->belongsTo(User::class);
}
```

Any column not named in `$fillable` is silently dropped whenever you call
`create()` or `update()` with it, no exception, no warning: the record
looks saved and one field is simply missing. Setting `$guarded = []`
swings to the other extreme and lets mass assignment touch every column on
the table, including something like an `is_admin` flag if one exists.

## Migration

Add an index to every foreign key and to any column a large table's
queries filter by. `foreignId('seller_id')->constrained()` assumes the
related table is called `sellers` purely from the column's name; if the
real table is `users`, the migration will fail at run time unless you pass
`constrained('users')` yourself.

Before Laravel 11, the SQLite database most test suites run against could
not drop a foreign key or alter a column in place, so a migration built
around `->change()` or `dropForeign()` worked on MySQL but failed under the
tests. Laravel 11 and later (with SQLite 3.26 or newer) handle both, so on a
current app that guard is usually unnecessary.

The trap that remains is `->change()` itself: since Laravel 11 it replaces
the whole column definition, so any modifier you leave off (`nullable`,
`default`, `unsigned`, `comment`) is dropped. Restate every modifier you
want to keep:

```php
$table->string('heading', 200)->nullable()->default('')->change();
```

## Validation

```php
public function rules(): array
{
    return [
        'heading' => 'required|string|max:255',
        'reference' => ['required', Rule::unique('listings')->ignore($this->route('listing'))],
    ];
}
```

A bare `unique:listings` rule fails an update every time, because the
record collides with its own current row. Scope the rule with
`Rule::unique(...)->ignore(...)` wherever the request could be an edit.

## Authorisation

```php
// Policy
public function update(User $user, Listing $listing): bool
{
    return $user->id === $listing->seller_id;
}

// Controller
Gate::authorize('update', $listing);
```

Laravel 11 and later ship a bare base controller without the
`AuthorizesRequests` trait, so `$this->authorize()` and
`authorizeResource()` do not exist unless you add that trait yourself. Use
the `Gate` facade (`use Illuminate\Support\Facades\Gate;`) instead.

Running `make:policy` and letting Laravel auto-discover it registers the
class, but the class does nothing on its own: a controller still has to
call `Gate::authorize()`, or the route still needs the `can:` middleware
(or `->can('update', 'listing')`). Skip that wiring and every route stays open regardless
of what the policy says.

## API resources

Reading a relationship inside a Resource without eager loading it fires
one query per record: harmless for a single record, an N+1 problem the
moment it runs inside a paginated list. Pair `whenLoaded('seller')` in the
resource with `->with('seller')` in the controller so the two always agree.

## Verifying the scaffold

```bash
php artisan migrate
php artisan migrate:rollback
php artisan migrate
php artisan tinker --execute="dd(Listing::factory()->create()->fresh()->toArray());"
php artisan test --filter=ListingTest
```

Wrap writes that touch more than one table in `DB::transaction()`, so a
failure partway through never leaves an orphaned related record behind.
