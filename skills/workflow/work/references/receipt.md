# Receipt

What the skill hands back at the end of every run, and the checks it
passes first.

## Re-read before writing

Tracker and repository facts change while you work: someone drags the card,
reassigns it, changes the cycle, the host links a pull request, CI finishes.
Just before the receipt, read again:

- repository: dirty files, branch heads, check results;
- tracker: state, assignee, cycle, linked pull requests, new comments.

If a re-read fails, show the value from the last good read with its time,
say it may have moved since and why the read failed, and propose nothing
that depends on it. If no read of it has succeeded at any point in this run,
say exactly that; never invent a time. Never restate an early snapshot as if
it were current. Each operation stands alone: one failed call does not cast
doubt on another that just succeeded.

## Needs you

Whenever the run needs something from the user (a decision, a permission,
access), that comes first, in every mode including status, as a short
numbered block. Each entry gives:

1. the question in one line;
2. the recommended answer;
3. one line on what it costs or changes;
4. the exact words that unblock it: the item key plus a letter for a
   one-off choice (`ABC-123 b`), or for a lasting decision that belongs in a
   brief or decision record, its `DEC-<n>` id (`DEC-2 a`). A `D-<n>` is an
   open question in a brief's decision table; a `DEC-<n>` is the decision
   record drafted when that choice will outlive the item.

Readers skip decisions buried in tables, paragraphs or the Next list, so it always has its own entry here as well. Leave the
heading out only when nothing is needed.

## Host-prescribed headings

Some environments fix the shape of a handover (a Stop hook, or the user's
own instructions naming headings such as You asked / Done / Verified / Also
/ Next). Check for this before writing. If one applies, write the receipt
once, in that shape: the map and outputs under the "done" heading, commands
and their output lines under the "verified" heading, files and stale
evidence under the "also" heading, and the needs-you block plus the next
action at the top of the "next" heading. Writing both shapes leaves the
reader unsure which one counts.

## Closing lines

- **Try next time**: a single sentence giving the quickest invocation for
  getting here, skipped if the user has already used it this session.
- If the session is running two streams at once (for example an issue and
  a change to the team's process), tag each section with the stream it
  belongs to.

## Checklist

The receipt is ready when all of these hold:

- the current state, drift and next gate rest on inspected evidence;
- actions described as done produced real outputs, and nothing planned is
  described as executed;
- every number was measured again during this run or is tagged
  `Unverified`, and volatile facts come from the re-read above;
- mode-specific result words keep the meaning their mode defines;
- no human approval was assumed because of AI output, a silence or the
  passing of time;
- each tracker write appears with the state it replaced and the state it
  set;
- the proposed next action is the one the present map points to.
