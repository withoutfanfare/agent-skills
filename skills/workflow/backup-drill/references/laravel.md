# Laravel

## spatie/laravel-backup

The common package for this in a Laravel project: `php artisan backup:run`
dumps the configured databases and zips configured file directories to one
or more configured disks (which can include an S3-compatible one). Before
trusting it:

- Read `config/backup.php` for which databases and directories are
  actually included; a project can install the package and still leave a
  second database or an upload directory out of the config.
- `php artisan backup:list` shows what backups exist on each configured
  destination and their size, which is a fast first check for "is anything
  actually landing here" before attempting a restore.
- The package zips a database dump using the same underlying tool as
  [references/mysql-postgres.md](references/mysql-postgres.md) or
  [references/sqlite.md](references/sqlite.md), so restoring means
  unzipping the archive and running the same restore command by hand; the
  package itself does not restore.
- `php artisan backup:monitor` and its health checks belong with alert
  design, covered by `monitoring` (if installed), not with this drill.

## Restoring into a local or throwaway environment

Point `.env` for the throwaway target at its own isolated database and
disk before running any `artisan` command, and confirm with
`php artisan tinker` or `php artisan config:show database` that the
connection really is the throwaway one, not production, before running a
restore command against it.

## Queues and caches

If the queue driver is Redis or a database table, a queued job in flight
is state that a database dump alone may not capture consistently if the
queue and the main database are dumped at different moments. Note this as
a gap in step 2 rather than assuming the queue is covered by the database
backup.
