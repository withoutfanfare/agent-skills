---
name: continuity
description: >-
  Writes a short, dated snapshot so you can pause your own work and pick it
  back up later, in this session, a new one, or a different tool: the goal,
  what is actually verified and when it was last checked, decisions kept
  separate from options still open, loose threads with an owner and a
  trigger, and the limits a snapshot must never widen. On resume it rechecks
  anything that may have changed before acting on old claims, and it can
  also run a narrow memory review that proposes edits rather than making
  them. Use when someone wants a continuation prompt, a handoff prompt for
  their own next session, to pick up from an existing brief, says they need
  to stop here for now, or asks to resume earlier work. To brief a different
  person or agent who is taking the task over, use `handover` instead.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Continuity

Work that spans sessions loses its thread twice: once when the person
stops and the details are still fresh enough to skip writing them down,
and again on return, when a stale note gets trusted as if it were still
true. This skill covers both ends: capturing a snapshot precise enough to
restart from, and, on the way back in, treating that snapshot as a claim
to check rather than a fact to act on.

Three modes. Pick the one asked for; do not run the others unprompted.

## Pause: write the snapshot

### 1. Fix the moment

Note the date and, if relevant, the branch, worktree or environment this
snapshot describes. Without a timestamp it cannot be trusted later against
anything that has since moved on.

Done when: the snapshot's opening line states the date.

### 2. Separate what is true from what is proposed

Walk back through the session and sort what happened into: things you
checked yourself (a command run, a file read, a test passed, each with
roughly when), choices that were actually made and why, and ideas that
were floated but not agreed. Only the first two count as state; the third
stays labelled as a proposal.

Done when: nothing in the snapshot reads as settled unless it was.

### 3. List what is still open

For each loose thread: what it is, who owns it (you, someone else, or
nobody yet), what would trigger picking it up again (a reply, a date, a
result landing), and how you would know it is finished. Leave a value
unknown rather than filling it with a guess.

Done when: every open thread has an owner and a trigger, or both are
marked unknown.

### 4. State the limits that still apply

Write down what you were and were not authorised to do, and which
decisions still need a person. A snapshot describes the boundary; it must
never quietly widen it for whoever reads it next.

Done when: a reader could not use the snapshot to justify doing more than
you could have done yourself.

### 5. Give the next session a running start

Name the first concrete action, then write a paragraph the next session
can paste in as-is: what this is, where the snapshot sits, what to do
first.

```markdown
## Snapshot: <task>, <date>

**Goal:** <what finishing looks like>

**Verified state:** <what you checked, and when; flag anything unverified>

**Decisions:** <choice, reason>; separately, **Proposed, not decided:** <idea>

**Open threads:** <what, owner, trigger, done condition> (one per line)

**Limits:** <what is authorised, what still needs a decision>

**First action:** <the single next step>

**Resume prompt:**
> <a paste-ready instruction naming this snapshot, the sources to reread,
> and the first action>
```

Save it where the project already keeps this kind of note, or return it
inline if there is no such place; do not invent a new location for one
snapshot. If the project's issue tracker already tracks a thread, link to
the ticket instead of restating it here, and keep this snapshot as the
one place that ties the threads together, not a second backlog.

Done when: the snapshot is saved or returned, and the resume prompt alone
would let a fresh session start correctly.

## Resume: pick the work back up

### 1. Read before acting

Load the snapshot and anything it points to. Note its date and how long
ago that was; the gap tells you how much to distrust.

Done when: the snapshot's age is known.

### 2. Recheck what might have moved

For each item marked as verified state, decide whether it is the kind of
fact that could have changed since (a file's contents, an issue's status,
whether a branch merged) and check the ones that could have. Treat a
snapshot claim as unconfirmed until you have looked, not as ground truth.

Done when: every changeable fact needed for the first action has been
checked against the real thing, not just read from the snapshot.

### 3. Reconcile and continue

Where reality now differs from the snapshot, say so in one line, then
carry on with the work using the current picture. Only stop and ask if the
difference changes what is authorised, or if information needed to
proceed is genuinely missing.

Done when: the session is acting on checked, current state, and any
difference from the snapshot has been noted.

## Memory review: propose, do not sweep

Only when asked. If the project has a memory tool, scope the review to the
project or topic named, not the whole store.

### 1. Find candidates

Look for entries that are stale (superseded by later work), duplicated,
contradictory, or filed under the wrong project.

Done when: each candidate has its location, the evidence, and a suggested
action (archive, merge, correct, move).

### 2. Leave the decision with the user

List the candidates; do not archive, edit or delete anything yourself
unless the user approves each one, or the tool is explicitly opened for
edits. A decision that was later reversed is not the same as a wrong
entry; keep both events on record rather than erasing the first.

Done when: nothing has changed in memory beyond the edits the user agreed.

## It's working if

- A snapshot read cold, with no memory of the session, is enough to start
  the next action correctly.
- Resuming never carries forward a fact that had quietly gone stale.
- Threads live in one place each: the tracker for tracked commitments, the
  snapshot only for what ties them together.
