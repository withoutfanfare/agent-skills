# Horizon configuration, worked through

Horizon requires the `redis` queue connection; it is not compatible with
Redis Cluster. Install with `composer require laravel/horizon`, then
`php artisan horizon:install` to publish `config/horizon.php`.

## Supervisors and balancing

Each environment in `config/horizon.php` holds one or more supervisors,
each supervising a group of workers:

```php
'environments' => [
    'production' => [
        'supervisor-default' => [
            'connection' => 'redis',
            'queue' => ['default'],
            'balance' => 'auto',
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
        'supervisor-images' => [
            'connection' => 'redis',
            'queue' => ['images'],
            'balance' => 'auto',
            'minProcesses' => 1,
            'maxProcesses' => 1,
        ],
    ],
],
```

`balance` picks the strategy:

- `auto` (the default) scales worker processes to whichever queue has the
  most work, using `minProcesses` and `maxProcesses` as the floor and
  ceiling. It does not enforce priority between queues in one supervisor;
  a queue listed first is not favoured. `autoScalingStrategy` chooses
  whether that scaling looks at `time` (estimated time to clear the
  queue) or `size` (job count).
- `simple` splits a fixed `processes` count evenly across the listed
  queues, with no autoscaling.
- `false` processes queues strictly in the order listed, like Laravel's
  default worker, while still autoscaling the total process count between
  `minProcesses` and `maxProcesses`.

To give one queue real priority over another, use separate supervisors
with their own `maxProcesses` (as above), rather than relying on queue
order within a single `auto` or `simple` supervisor.

## Tries, timeout and backoff at the supervisor level

```php
'supervisor-default' => [
    // ...
    'tries' => 10,
    'timeout' => 60,
    'backoff' => [1, 5, 10],
],
```

These apply when the job class itself does not define `$tries`, which
takes precedence. Set `tries` explicitly whenever a job uses
`WithoutOverlapping` or `RateLimited` middleware, since both consume
attempts; otherwise Horizon's single-attempt default exhausts a job on
its first release. As with a plain worker, the supervisor's `timeout`
must stay a few seconds shorter than the connection's `retry_after` in
`config/queue.php`, or a job may be processed twice.

## Metrics

Horizon's metrics dashboard needs a periodic snapshot to populate. Add to
`routes/console.php`:

```php
Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

## Deploying

```bash
php artisan horizon:terminate
```

This lets any job currently running finish, then exits; the process
supervisor (Supervisor, systemd) that runs `php artisan horizon` restarts
it, picking up the newly deployed code. Run it as a step in the deploy,
after code is in place, not before.

## Useful commands

```bash
php artisan horizon:status              # running or paused
php artisan horizon:supervisor-status supervisor-default
php artisan horizon:pause               # stop picking up new jobs
php artisan horizon:continue
php artisan horizon:forget <id>         # delete one failed job
php artisan horizon:clear --queue=images
```
