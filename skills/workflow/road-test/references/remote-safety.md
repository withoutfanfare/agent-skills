# Testing on a remote environment

On a local target, normal development freedom applies. On a remote
(staging, a review app, anything that is not your machine) you may look at
anything and change nothing. State changes happen only through the app's
own interface, as an ordinary user would make them.

## Allowed, to explain something already seen in the browser

- Reading logs: `tail`, `grep`, `less` on log files.
- Inspection commands that report without changing anything, such as a
  framework's "about", route list or configuration display.
- Queue and worker status commands.
- Read-only git commands, to confirm which commit is deployed.
- Listing and reading configuration and log files, and checking disc
  space.
- Read-only database queries (`SELECT`) with a `LIMIT`.

## Never

- Interactive consoles or REPLs on the server (they can do anything).
- Migrations or any database command other than a read-only query.
- Cache clearing, optimisation or rebuild commands.
- Queue retries, flushes or restarts.
- Deploys, builds, package installs.
- Any file write, delete, permission or ownership change.

If a diagnosis needs something on the "never" list, stop and ask the user,
explaining what you would run and why.
