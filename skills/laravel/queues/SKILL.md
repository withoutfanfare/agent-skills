---
name: queues
description: >-
  Builds Laravel queued jobs that survive real failures, not just the
  happy path: safe payloads, retries with backoff, timeouts that do not
  race the connection's retry window, uniqueness, batches and chains, and
  workers that actually run in production. Use when the user asks to
  queue a job, make a job retry safely, add batching or chaining, set up
  queue workers or Horizon, or asks why a job ran twice or failed
  silently. Not for scheduling when a job runs (use `scheduler`) or
  building notifications (use `notify`).
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Queues

A job that works every time in local development can still fail in
production in ways synchronous code never does: the worker restarts
mid-job, two workers pick up the same message, a slow external call gets
retried on top of itself. This skill builds the job so a retry is safe, a
failure is visible, and a worker is actually running to process it, not
just a class that compiles.

For deciding when a job runs, use `scheduler`. For choosing a delivery
channel and message content, use `notify`.

## 1. Decide whether this needs a queue

Queue anything that calls an external service, sends mail, or does
enough work that the request should not wait for it. Do not add a queue
speculatively to something fast and purely internal.

Done when: you can say what would go wrong if this ran synchronously.

## 2. Design the payload for a safe retry

Pass a model, not its whole relation tree; Laravel serialises it as a
class and ID and re-fetches fresh data when the job runs. Then make the
job idempotent: running it twice must produce the same end state as
running it once, so check the current state before acting rather than
assuming a job only ever runs once.

Done when: dispatching the same job twice does not double the effect.

## 3. Set tries, backoff, retryUntil, maxExceptions and the timeout

```php
class SyncSupplierCatalogue implements ShouldQueue
{
    public int $tries = 5;
    public array $backoff = [10, 60, 300, 900];
    public int $maxExceptions = 3;
    public int $timeout = 60;      // must be less than the connection's retry_after
    public bool $failOnTimeout = true;
}
```

`$tries` caps total attempts; a `retryUntil()` method caps by time
instead, and wins if both are set, so pick one. `$maxExceptions` lets a
job that releases itself back many times (polling with `release()`, say)
still fail once that many unhandled exceptions have piled up. Backoff should grow between attempts, not retry instantly into
the same failure, and anything that cannot possibly succeed on retry
should call `fail()` immediately instead of burning through `$tries`.

`$timeout` is how long a worker lets the job run before killing it;
`retry_after`, set per connection in `config/queue.php`, is how long the
queue waits before assuming a job died and releasing it for another
attempt. If `timeout` is not comfortably shorter than `retry_after`, a
slow-but-still-running job gets released and picked up a second time
while the first attempt is still executing, so it runs twice.

Done when: the retry numbers fit this job's failure mode, and `timeout`
is checked against the connection's `retry_after`, not copied from
another job.

## 4. Handle the terminal failure

Make sure the `failed_jobs` table exists so exhausted jobs land somewhere
visible: Laravel 11 and later ship it in the default jobs migration; older
apps add it with `php artisan make:queue-failed-table` then `migrate`. Implement `failed()` for what should happen once a job is truly
done retrying:

```php
public function failed(Throwable $exception): void
{
    Notification::route('mail', config('mail.ops_address'))
        ->notify(new JobFailed($this, $exception));
}
```

Done when: a job exhausting its retries produces something a person will
see, not just a silent row in `failed_jobs`.

## 5. Add uniqueness and concurrency middleware where two runs would collide

`ShouldBeUnique` (with `uniqueId()` and `$uniqueFor`) stops a second
identical job being pushed while one is already queued or running. The
`WithoutOverlapping` middleware instead stops two jobs with the same key
running at the same moment: the second is released back to wait, or
dropped with `dontRelease()`.
`RateLimited` or `RateLimitedWithRedis` caps how often a job runs against
a rate-limited external API.

Done when: any job whose concurrent runs would corrupt data or double a
side effect has one of these guards, not just a comment saying it should.

## 6. Choose chain or batch for related jobs

A chain runs jobs strictly in order and stops at the first failure; use
it when step two is meaningless without step one succeeding. A batch runs
jobs in parallel and tracks combined progress; use it when the jobs are
independent and you need to know when they have all finished.

```php
Bus::chain([
    new BuildExport($account),
    new EmailExportReady($account),
])->catch(fn (Throwable $e) => Log::error('Export chain failed', ['error' => $e]))
  ->dispatch();
```

For a batch, decide whether one failure should stop the rest
(`allowFailures()` if not) and check `$batch->failedJobCount` rather than
only the happy path in `then()`.

Done when: the choice is written down, and the failure path is
implemented, not just the happy path.

## 7. Dispatch after the transaction commits

If a job reads a row the current request just wrote inside a database
transaction, dispatching before that transaction commits risks the
worker running before the row exists. Set `after_commit` on the
connection in `config/queue.php`, or call it per dispatch:
`ProcessOrder::dispatch($order)->afterCommit()`.

Done when: a job depending on data written in the current request either
uses `afterCommit()` or the connection has `after_commit` set,
deliberately, not by accident.

## 8. Choose a driver and run real workers

The `database` driver needs nothing extra and suits moderate volume;
`redis` is faster and required for Horizon. Whichever driver, a queue
only processes when something is running `php artisan queue:work` under
a process supervisor, or Horizon, is actually running. Run
`php artisan queue:restart` (or `horizon:terminate` under Horizon) as
part of every deploy, so workers pick up the new code once the current
job finishes.

Horizon's supervisors, balancing strategies and per-queue priority are
worked through in [references/horizon.md](references/horizon.md).

Done when: you can name the driver, and confirm, not assume, that a
worker or supervisor is running.

## 9. Prove it with fakes, then one real run through a worker

```php
Queue::fake();
ProcessOrder::dispatch($order);
Queue::assertPushed(ProcessOrder::class);
```

A fake proves the dispatch happened with the right job and data; it
proves nothing about a worker actually completing it. Separately, run a
real worker at least once (`php artisan queue:work --once`, or
`--stop-when-empty` against a populated queue) and confirm the job's real
side effect happened, not just that the command exited without error.

Done when: a fake-backed test asserts the dispatch, and a real worker run
has produced the expected side effect at least once outside the test
suite.

## 10. Report

State what the job does, the retry and timeout configuration and why,
the uniqueness or overlap guard if needed, the chain or batch structure if
any, the driver, and the step 9 evidence that a real worker processed it.

Done when: the report quotes the step 9 output showing a real run, not
just the fake assertion.

## It's working if

- Every job's `timeout` is shorter than the connection's `retry_after`,
  checked, not assumed.
- A job that could run twice concurrently has a uniqueness or overlap
  guard, and one that cannot succeed on retry fails fast.
- A real queue worker has processed the job at least once, with the
  resulting data change checked, not only the fake assertion.
