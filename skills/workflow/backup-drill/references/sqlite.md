# SQLite

SQLite's database is a single file, which makes backup look deceptively
simple: copying the file is not safe while the application is writing to
it, because a plain file copy can land mid-write and capture a torn,
inconsistent page.

## Taking a consistent copy

```bash
# The backup command reads a consistent snapshot even during writes
sqlite3 app.db ".backup /path/to/app-backup.db"
```

This uses SQLite's own backup API rather than a filesystem copy, so it is
safe to run against a live database. `cp app.db app-backup.db` is not
equivalent and should be treated as a finding in step 2 if that is what the
project actually does.

If the database uses write-ahead logging (`PRAGMA journal_mode=WAL`), also
check for a `-wal` file alongside the main one; a filesystem-level copy
that misses it can restore to a state older than the last checkpoint.

## Restoring

Restoring is just putting the backed-up file where the application expects
its database, into the throwaway target's own path, never over the
project's real database file:

```bash
cp app-backup.db /path/to/throwaway/app.db
```

## What to check

Row counts and a smoke query, as in the main skill. Also open the file
with `sqlite3 app.db "PRAGMA integrity_check;"`, which walks every page and
catches corruption that a row count alone would miss.

## Point-in-time recovery

SQLite has no built-in equivalent to a database server's transaction log.
A project that needs finer recovery than "the last `.backup` snapshot"
either takes snapshots more often or replicates the file continuously with
a tool built for it; if the project has neither, say plainly in step 3
that only snapshot-granularity recovery exists.
