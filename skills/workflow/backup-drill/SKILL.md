---
name: backup-drill
description: >-
  Proves a project's backups can actually be restored, not just that they
  run: finds where state lives (databases, uploaded files, object storage,
  secrets and config), checks how each is backed up, sets recovery targets
  in plain words, then restores for real into a throwaway target and times
  it. Use when the user asks to test a backup, run a restore drill or
  disaster recovery test, or check whether a database dump actually
  restores.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Backup drill

A backup nobody has restored is a hope, not a backup: the dump job can run
green for a year while the file it produces is empty, corrupt, or missing
half the tables. This skill is the fire drill: find what would be lost,
restore it for real into a disposable copy, and prove the result is usable
before an actual emergency is the first time anyone tries.

Not for moving or reshaping live data while the application keeps running,
use `migrate-data` (if installed). Not for deciding what should alert when
backups fail, use `monitoring` (if installed). Once this drill has working
restore steps, hand them to `runbook` (if installed) so on-call can follow
them without you.

## 1. Find what holds state

List every place the project would lose something if it vanished: the
primary database, uploaded files or object storage, secrets and env
config, and any queue or cache whose contents matter if lost (a job queue
mid-flight, a cache that is really the only copy of something). Read the
deployment config and `.env.example` rather than guessing; a service
nobody mentions is the one that turns out to hold state.

Done when: every place holding state is named, with what would be lost if
each one disappeared right now.

## 2. Find how each is backed up

For each item in step 1, find the actual backup mechanism: the cron
schedule or scheduled task, the tool (a database dump, a snapshot, a
sync job), where the output lands, and how long it is kept. Read the
config, not the README's claim about it; a backup job can be defined and
disabled, or defined and silently failing. Stack notes:
[references/mysql-postgres.md](references/mysql-postgres.md),
[references/sqlite.md](references/sqlite.md),
[references/object-storage.md](references/object-storage.md),
[references/laravel.md](references/laravel.md).

Done when: every item has a named mechanism, schedule and destination, or
is flagged as having none.

## 3. Set recovery targets in plain words

For the project as a whole, or per item if they differ:

- **Recovery point objective (RPO):** how much recent data can be lost,
  stated as time ("up to one hour of writes"). This is set by the backup
  frequency, not wished for afterwards.
- **Recovery time objective (RTO):** how long restoring is allowed to
  take, stated as time ("back up within thirty minutes").

Compare both against what step 2 actually delivers; a nightly dump cannot
give a one-hour RPO, whatever the target says.

Done when: RPO and RTO are each one plain sentence, and any gap against
the real backup frequency is stated, not smoothed over.

## 4. Choose a throwaway, isolated target

Pick or create a target that is not production and cannot become it by
accident: a fresh local database or a disposable container. A cloud
target is fine only if it is covered by the same data-protection terms as
production, since the backup holds real personal data. Confirm its connection details point
away from production before running anything, by reading the config back,
not by assuming the environment variable is what you last set it to.

**Never restore over, or write to, production.** If no safe target can be
made, say so and stop rather than testing against the real thing.

Done when: the target is confirmed isolated, and its connection string or
path has been read back and checked.

## 5. Run the real restore

Fetch the most recent real backup (or the most recent one you are allowed
to use) and restore it into the target with the project's actual restore
command, not a simplified stand-in. Note the exact commands and their
output as you go; this is the material step 7 turns into a written
procedure.

Done when: the restore command has run to completion against the
throwaway target, with its output captured.

## 6. Check the result, not just the exit code

A restore command can exit zero having restored nothing useful. Check:

- **Row counts** on the main tables, compared with a count taken from the
  source at backup time if you have one.
- **Checksums or spot comparisons** of a sample of rows against a value
  recorded before the backup was taken, where practical.
- **A smoke query**: something that only returns a sensible answer if the
  data is really there (the newest few records, a count grouped by a
  status column).
- **The application booting against the restored copy** and rendering a
  page or two that reads from the database, not just connecting to it.

Done when: counts, a smoke query and the app booting have all been run
against the restored target, with results shown, not assumed.

## 7. Time it and write down what worked

Record how long the fetch and the restore actually took, against the RTO
from step 3. Then write the restore steps that worked, as commands with
their real output, ready to become a runbook: hand them to `runbook` (if
installed) rather than leaving them only in this session's transcript.

Done when: the timing is recorded against the RTO, and the working restore
steps are written down somewhere durable.

## Guardrails

Backup dumps and restored copies contain real personal data. Keep dumps and
restored databases out of git, delete the throwaway copy and any local
dump file once the drill is done, and never point a restore at production,
even to "just check" something quickly.

Done when: the throwaway target and any local dump files have been deleted
and you have said so.

## It's working if

- The restore ran against a real, recent backup into a target that was
  never production, and could not have become it by accident.
- The check in step 6 used real numbers (counts, a checksum, a query
  result), not "the command didn't error".
- Someone else could follow the written restore steps without you present.
