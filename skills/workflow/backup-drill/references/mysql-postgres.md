# MySQL/MariaDB and PostgreSQL

## Logical dumps

A logical dump writes out the schema and data as statements or a portable
archive. It restores cleanly onto a different server version and is easy to
inspect, but a full restore of a large database can take hours because
every row is reinserted and every index rebuilt.

MySQL/MariaDB:

```bash
# Take (on a replica if one exists, to avoid load on the primary)
mysqldump --single-transaction --routines --triggers db_name > db_name.sql

# Restore into the throwaway target
mysql -h throwaway-host -u restore_user -p db_name < db_name.sql
```

`--single-transaction` gives a consistent snapshot without locking tables,
for InnoDB. Without it, a dump taken while writes are happening can mix
rows from different points in time.

PostgreSQL:

```bash
# Custom format: compressed, supports parallel restore
pg_dump -Fc db_name > db_name.dump

# Restore
pg_restore -d throwaway_db --clean --if-exists -j 4 db_name.dump
```

`-j 4` restores with four parallel workers; raise it on a bigger machine to
cut restore time, which is exactly what step 7 of the main skill wants
measured.

## Point-in-time recovery (PITR)

A logical dump only recovers to the moment it was taken. PITR replays a
base backup plus a log of every change since, to reach a specific second,
useful for "restore to just before the bad migration ran" rather than only
to last night.

- **MySQL/MariaDB**: binary logs (`log_bin`) recorded since a full backup,
  replayed with `mysqlbinlog --stop-datetime=... | mysql`.
- **PostgreSQL**: write-ahead log (WAL) archiving plus a base backup
  (`pg_basebackup`), replayed by setting `recovery_target_time` and letting
  PostgreSQL apply archived WAL up to that point.

Both need the base backup and every log segment since it kept together;
losing a segment in the middle breaks replay from that point on. If the
project does not already archive these logs, PITR is not available however
recent the last full backup is, and the drill's RPO should say so plainly
rather than assume it.

## What to check after restoring

Row counts on tables with foreign keys are the first thing a broken dump
gets wrong (constraint violations either abort the restore or, worse, get
skipped silently depending on flags). Compare `information_schema` or
`pg_catalog` table lists between source and restored target; a dump that
silently dropped a table restores without error and looks fine until
someone queries it.
