---
name: log-triage
description: >-
  Turns a pile of application logs (a production log file, a log export, or
  logs pasted in) into a ranked triage list: fingerprints entries by
  exception, message shape and stack frame, counts and dates each one,
  separates new problems from known ones, and gives the top few a likely
  cause with confidence. Use when the user asks to go through the logs,
  triage a log file, or find the most common errors in a log export.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Log triage

A week of production logs holds thousands of lines but usually only a
handful of actual problems, each repeated under different ids and
timestamps. Reading it top to bottom finds whatever happened most
recently, not what happens most often or hurts most. This skill groups the
noise into a short, ranked list, so the same handful of causes only get
counted, not read, twice.

Not for one reported bug someone is asking about, use `triage` (if
installed). Not for chasing down a single reproducible failure, use
`debug` (if installed). Not for writing up an incident that already
happened, use `post-mortem` (if installed): this skill runs before any of
those three, to find what is worth a look in the first place.

## 1. Collect a bounded time window

Get the logs: a file path, a log service's export, an SSH session the
user has given access to, or logs pasted directly into the chat. Fix the
window before going further, a day, a week, since the last deploy, so
"most common" means something and the run finishes. Reading logs over SSH
is fine when the user has provided access; never go looking for
credentials to get it yourself.

Done when: the source and the time window are both stated.

## 2. Normalise and group into fingerprints

Run the bundled script (in Claude Code the folder is `${CLAUDE_SKILL_DIR}`;
otherwise use the path this skill was linked from, `.agents/skills/log-triage`
or `~/.agents/skills/log-triage`) against the log file or
a pasted copy saved to a temporary file:

```bash
python3 "${CLAUDE_SKILL_DIR:-.agents/skills/log-triage}/scripts/fingerprint_log.py" storage/logs/laravel.log --since 2026-09-20
```

It groups entries by exception class, a normalised message (ids, numbers,
emails and UUIDs stripped) and the top in-app stack frame, and prints a
markdown table ranked by count with first seen, last seen and a rough
count of distinct users or tenants affected, without printing the raw
values. Read [references/fingerprinting.md](references/fingerprinting.md)
for what the script does and does not recognise, and how to handle a log
shape it cannot parse.

Done when: the fingerprint table exists and its row count is far smaller
than the number of log lines.

## 3. Rank by what matters, not just count

Frequency alone misleads: three occurrences of a checkout failure outrank
three hundred occurrences of a harmless deprecation warning. Re-order the
table by combining count with severity (blocker, major, minor, by the same
factors as `triage`: data risk, how many are affected, whether it is
getting worse) and note anything low-count but severe separately so it
does not fall off the bottom of a frequency-only list.

Done when: the working list is ordered by real priority, with anything
promoted or demoted from pure frequency order explained in one line.

## 4. Separate new from already known

Keep a small ledger in the project, `docs/log-triage/ledger.md` unless the
user names another path, one row per fingerprint: first seen, last
checked, status (new, tracked, resolved, accepted) and a link if an issue
exists. Compare today's fingerprints against it, and against open issues
if a tracker is connected, before calling anything new.

Done when: every fingerprint in the ranked list is marked new or already
known, with a link for the ones that are known.

## 5. Give the top few a likely cause

For the top handful of new or worsening fingerprints, read the code at the
top in-app stack frame the script reported and give a likely cause with a
confidence word (certain, likely, possible) and the evidence for it, the
same way `debug` isolates a cause but without building a full reproduction
here; that is the next step, not this one.

Done when: each of the top few has a cause, a confidence and the file and
line it points to.

## 6. Offer to draft issues, never create them unasked

For fingerprints worth tracking, draft an issue: the fingerprint's
message shape, count and date range, the likely cause and confidence, and
the file and line, with any id, email or other personal data redacted
first. Show the drafts and ask before creating anything in an issue
tracker; never create issues without that go-ahead.

Done when: a draft exists for each fingerprint worth tracking, redacted,
and the user has said yes or no to creating each one.

## 7. Update the ledger and report

Add or update a row for every fingerprint looked at today, then report:
the window covered, the ranked list with counts and dates, what is new
against what was already known, the causes found, and which issues were
drafted or created.

Done when: the ledger reflects today's run and the report covers every
section above.

## It's working if

- The report is short enough to read in one sitting, however large the
  source log was.
- A fingerprint seen last week is marked known, not reported again as new.
- Nothing in a drafted issue is a real id, email address or other personal
  data lifted straight from the log.
