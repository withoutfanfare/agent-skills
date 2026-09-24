---
name: scheduler
description: >-
  Sets up Laravel's task scheduler safely: choosing between a scheduled
  command, job or closure, guarding against overlapping and multi-server
  runs, and wiring up chains, batches and retry handling for jobs that
  depend on each other. Use when scheduling an artisan command, adding a
  cron entry, chaining or batching jobs, or making a scheduled job retry
  properly on failure.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Scheduler

A scheduled task that looks fine in testing can quietly duplicate itself in
production: two servers running the same job, or a slow run overlapping the
next one. The failure only shows up as an odd number in a report or a
double-charged row weeks later. This skill builds the schedule with the
guards in place from the start, then checks that a dependent chain of jobs
recovers when one link fails.

## 1. Choose the right kind of task

A one-line closure is fine for something trivial and stateless, such as
clearing a cache. Anything with real logic, its own dependencies, or that
needs to run on the queue belongs in a job or an artisan command, not a
closure buried in the schedule definition. Prefer a command when a human
might also want to run it by hand; prefer a job when the work only ever
runs in the background.

Done when: you can say why this task is a command, a job or a closure, not
just that it works.

## 2. Define the schedule with the overlap guards on

Every recurring task needs to answer two questions before it ships: what
happens if the previous run is still going, and what happens if this runs
on more than one server. Skipping either one is how duplicate processing
gets into production.

```php
// routes/console.php (Laravel 11 and later)
use Illuminate\Support\Facades\Schedule;

Schedule::command('reports:nightly-digest')
    ->dailyAt('02:00')
    ->withoutOverlapping()   // a slow run does not collide with the next
    ->onOneServer()          // only one server runs this, even if several run the scheduler
    ->runInBackground();
```

On Laravel 10 and older the same chain hangs off `$schedule->command(...)`
inside `schedule()` in `app/Console/Kernel.php`; follow whichever style the
project already uses.

`withoutOverlapping()` needs a working cache lock, so confirm the cache
driver is not `array` or `null` in the environment the schedule runs in.
`onOneServer()` is stricter: the default cache must be `database`, `redis`,
`memcached` or `dynamodb`, and every server must share that same cache, or
each server takes its own lock and the task runs everywhere. Set an explicit
expiry (`withoutOverlapping(120)`, in minutes) for any task that could
itself hang, so a crashed run does not lock the task out forever.

Done when: every new schedule entry has an explicit overlap and
single-server decision, not the framework's defaults by omission.

## 3. Pick chain or batch for related jobs

A chain runs jobs strictly in order and stops the chain at the first
failure; use it when step two is meaningless without step one having
succeeded (generate a file, then email it). A batch runs jobs in parallel
and tracks their combined progress; use it when the jobs are independent
and you need to know when they have all finished, or how many failed.

```php
Bus::chain([
    new BuildMonthlyExport($account),
    new EmailExportReady($account),
])->catch(function (Throwable $e) use ($account) {
    Log::error("Export chain failed for account {$account->id}", ['error' => $e]);
})->dispatch();
```

Pass data forward through a model reference the later job re-fetches (an ID,
not the whole object), not through job constructor state that could go
stale between steps. A batch that grows without limit is a memory and
database problem waiting to happen: cap how many jobs one batch can hold,
or split the work into several batches.

Done when: the choice between chain and batch is written down, and the
failure path (`catch()`, or `allowFailures()` plus checking
`$batch->failedJobCount`) is implemented, not just the happy path.

## 4. Make failure handling recover

Set `$tries`, `$backoff` and `$timeout` on the job class itself, not just at
dispatch time, so they survive a retry from the failed-jobs table. Backoff
should grow between attempts (`[10, 60, 300]`), not retry instantly into the
same failure. Implement `failed()` for the terminal case: the job has
exhausted its retries and someone or something needs to know.

```php
class SyncSupplierCatalogue implements ShouldQueue
{
    public int $tries = 5;
    public array $backoff = [10, 60, 300, 900];
    public int $timeout = 120;

    public function failed(Throwable $exception): void
    {
        Notification::route('mail', config('mail.ops_address'))
            ->notify(new ScheduledJobFailed($this, $exception));
    }
}
```

Distinguish failures worth retrying (a timeout calling another service)
from ones that never will succeed on retry (invalid data); call `fail()`
immediately for the second kind instead of burning through `$tries`.

Done when: a job that cannot possibly succeed on retry fails fast, and one
that legitimately might recover backs off between attempts.

## 5. Verify the schedule runs

Reading the code proves nothing about production. Confirm the pieces that
make a schedule real:

```bash
php artisan schedule:list          # shows every registered entry and its next run
php artisan schedule:run           # runs anything due right now, for a manual check
crontab -l                          # confirms the single cron line calling schedule:run exists
```

For a queued job, also confirm a queue worker is running
(`php artisan queue:work` under a process supervisor, not a bare terminal),
since a perfectly scheduled job that never gets picked up looks identical
to one that silently failed.

Done when: `schedule:list` shows the new entry with the expected timing, and
you have confirmed something is running `schedule:run` and, if relevant,
`queue:work`.

## 6. Report

State what was scheduled and its frequency, the overlap and server guard
decisions, the chain or batch structure if any, the retry and backoff
configuration, and the command output from step 5 that proves it is live.

Done when: the report quotes the step 5 output showing the task is live.

## It's working if

- Every schedule entry has a deliberate answer for overlap and
  multi-server, not the framework default by accident.
- A failing link in a chain stops the chain and is reported, instead of the
  next step running on missing data.
- `schedule:list` and a check of the queue worker were run, not
  assumed.
