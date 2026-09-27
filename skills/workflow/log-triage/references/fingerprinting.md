# How the fingerprint script groups entries

`scripts/fingerprint_log.py` reads plain text, standard library only, and
recognises two shapes of log entry, one per line at the start of an entry
with any following lines (a stack trace, extra context) folded into the
same entry:

- **Laravel/Monolog style**: `[2026-09-27 10:15:32] production.ERROR:
  message text {"context":"json"}` followed by an optional `[stacktrace]`
  block.
- **Generic style**: `2026-09-27 10:15:32 ERROR message text`, with or
  without a leading bracket around the timestamp.

Lines that do not start a new entry (no recognised timestamp and level) are
treated as a continuation of the previous entry, which is how a stack
trace spread over several lines stays attached to the error it belongs to.

## What a fingerprint is built from

For each entry, the script extracts three things and groups on all three
together:

1. **Exception class**, if the text names one: a namespaced class ending
   in `Exception` or `Error` (`Illuminate\Database\QueryException`,
   `TypeError`). Left blank when no such name appears.
2. **Top in-app stack frame**: the first frame in the stack trace whose
   path is not inside `vendor/`, `node_modules/` or similar, trimmed to
   start from `app/` or `src/` if the path contains one. This is usually
   the most useful single line to go and read.
3. **Normalised message**: the entry's first line with UUIDs, email
   addresses, long hexadecimal strings and any other run of digits
   replaced with a placeholder, so `"Undefined array key \"postcode\""`
   with a different user id each time collapses to one fingerprint instead
   of one per occurrence.

## Distinct users or tenants affected

If an entry's context looks like a trailing JSON object (Monolog commonly
appends one), the script looks for keys that plausibly identify who was
affected (anything containing `_id`, or named `user`, `tenant`, `account`,
`customer` or `email`) and counts how many distinct values appear across a
fingerprint's occurrences. It never prints the values themselves, only the
count, so the table itself is safe to paste into a chat or a draft issue
without a separate redaction pass. Treat the count as a rough signal, not
an exact tally: a value repeated under two different key names is counted
twice.

## What it does not handle

- **JSON-lines logs** (one JSON object per line, common in some log
  services): the script will not recognise these as entries at all. Export
  or reformat to a plain `timestamp level message` line first, or extract
  the fields you need with a short one-off script instead of trying to
  force this one to parse a shape it was not built for.
- **Multi-process interleaved logs**, where two requests' lines are
  written out of order: the script has no way to tell they are unrelated,
  and a stack trace can attach to the wrong entry. A time window narrow
  enough that this is rare is more useful here than a smarter parser.
- **Non-PHP stack traces** in a different frame format (Python
  tracebacks, Node stack traces): the frame pattern looks for a
  `path.ext(line)` or `path.ext:line` shape, which covers PHP, Python, JS,
  TS, Ruby and Go paths reasonably well, but a framework with an unusual
  trace format may report no frame at all. The fingerprint still works
  from the exception class and message alone in that case.

## When the script cannot parse the source at all

Fall back to `grep` for the error text, level or exception name directly,
and count and date matches by hand; say plainly that the fingerprinting
step was skipped and why, rather than presenting a hand count as if it
came from the script.
