# Laravel debugging notes

## Where to look first

- `storage/logs/laravel.log` for the stack trace and context.
- `php artisan optimize:clear` before anything else. A stale config, route
  or view cache makes old behaviour look like the current bug.
- `git log --oneline -- <path>` on the affected files, to see what changed
  recently.

## N+1 queries

```php
DB::enableQueryLog();
// run the code path
dd(DB::getQueryLog());
```

A repeated query with only the bound ID changing is the signature. Fix with
eager loading (`with()`), not by silencing the symptom.

## Queue jobs that silently fail or never run

- Check the `failed_jobs` table before assuming the job never dispatched.
- If `QUEUE_CONNECTION` is a real driver (not `sync`) and no worker is
  running locally, jobs queue up and nothing happens. Run
  `php artisan queue:work --once` to process one and watch it fail loudly.
- Jobs must be idempotent: a job retried after a timeout can run twice.

## Livewire components

- A public property can hold an Eloquent model, but only its class and key
  travel to the browser; the next request re-fetches it fresh, dropping any
  query constraints (`select()`, filters) used to load it. When a value
  "loses" a column or a constraint between requests, look there, and prefer
  a `#[Computed]` property for data the component only reads.
- An untyped public property hydrates as a string. `$this->count === 1`
  fails when the browser sent `"1"`.
- Check the `hydrate()`/`dehydrate()` hooks and `wire:model` binding when a
  value "isn't updating" between requests.

## A save that reports success but the database disagrees

Work through these in order:

1. **Wrong record.** Log `$model->id` right before `save()`. A lookup like
   `firstOrCreate` keyed on something other than the primary key can
   resolve to a different row than the one in view.
2. **Wrong connection.** In a multi-connection or multi-tenant app, log
   `$model->getConnectionName()` and confirm it is the one you expect.
3. **A wrapping transaction rolled back later.** Log
   `DB::connection($conn)->transactionLevel()` before the save.
4. **Nothing was dirty.** `$model->getDirty()` empty means no `UPDATE` runs
   at all; `save()` still returns `true`.
5. **Verify with a raw read**, bypassing Eloquent entirely:
   ```php
   DB::connection($model->getConnectionName())
       ->table($model->getTable())
       ->where('id', $model->id)
       ->first();
   ```

## Cross-layer bugs (frontend claims backend "isn't working")

Check each boundary in order rather than guessing which layer is at fault:

1. Browser network tab: what payload went out, what came back.
2. `prepareForValidation()` / `failedValidation()` on the Form Request: did
   validation see and accept what you expect?
3. The controller: log the validated data at the top of the method.
4. The model or trait: log the lookup result and the connection before
   `save()`.
5. The database: re-read the row after the write (see above).

A common false lead: a frontend framework holding stale reactive state
sends an old value that looks, from the backend, exactly like a backend
bug.

## Regression test shape

```php
it('reproduces the bug', function () {
    // Arrange: the exact condition from the report
    // Act: trigger it
    // Assert: the reported wrong behaviour (before the fix)
});
```

Run one test by name while iterating: `php artisan test --filter="reproduces the bug"`.
