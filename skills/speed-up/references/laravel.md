# Laravel performance notes

## Measuring

```php
DB::enableQueryLog();
// ... run the slow code ...
$queries = DB::getQueryLog();
logger()->info('queries', ['count' => count($queries), 'ms' => collect($queries)->sum('time')]);
```

Laravel Telescope (Requests and Queries tabs) and Laravel Debugbar show
the same per request. Sort queries by count to spot repeats.

## Repeated queries

- Load relationships up front: `Post::with('author', 'tags')->get()`, and
  nested: `with('items.product')`.
- Counts without loading rows: `withCount('comments')`; sums and averages:
  `withSum()`, `withAvg()`.
- Relationships used in Blade loops count too; load them in the controller.
- Stop regressions outside production, in `AppServiceProvider::boot()`:

```php
Model::preventLazyLoading(! app()->isProduction());
```

## Queries and indexes

- Check the plan: `DB::select('EXPLAIN ' . $query->toSql(), $query->getBindings())`.
- Index the columns you filter and sort on, in that order, in a migration:
  `$table->index(['account_id', 'created_at']);`
- `select()` only the columns needed; `pluck()` for one column;
  `exists()` rather than `count() > 0`.
- Large sets: `chunkById()` or `lazyById()` rather than `get()` or `all()`.

## Caching

- `Cache::remember($key, $ttl, fn () => ...)` for expensive lookups.
- Clear on change with model events or observers (`saved`, `deleted`), or
  use cache tags where the store supports them.
- Framework caches in production: `php artisan optimize` (config, routes,
  events, views), and OPcache on.

## Background work

Queue slow side effects (`dispatch()`, `ShouldQueue` on mailables,
notifications and listeners) and set sensible `timeout` and `tries` on each
job.
