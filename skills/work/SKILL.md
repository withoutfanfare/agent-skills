---
name: work
description: >-
  Picks up an existing issue, pull request or release, decides from fresh
  evidence which lifecycle stage it has truly reached, checks that against
  the tracker board, names the gate before the next state and takes one safe
  step. Use when asked to pick up a ticket, where a PR stands, what blocks a
  release, or for spec, build, review, ship, UAT or sign-off work.
license: MIT
---

# Work

A tracker card records what someone last remembered to update. Code gets
merged under cards that still read In Progress, cards reach Approved with no
sign-off on record, and passing CI gets mistaken for a finished feature.
This skill meets an item wherever it genuinely is, shows which gate stands
between it and the next state, and moves it one safe step. Intent,
trade-offs, risk and product calls stay with people; bookkeeping, evidence
and checking are the skill's job. Nothing is posted, pushed or moved unless
the user asks.

## How it is called

`/work` in Claude Code, `$work` in Codex. A recognised first word selects a
mode, and plain language wins over word order ("take ABC-123 back to spec"
selects `spec`).

`work <item>` gives the map, the gate and one next safe action; add
`carry on` to continue until a person is needed; `work status <item>` gives
the map alone; `work <mode> <item>` (`spec`, `build`, `recover`, `review`,
`ship`, `document`, `verify`, `accept`, `release`) runs that mode, then maps.

Everyday wording maps onto modes ("open the PR" is `ship`, "fix it" is
`build`, "deal with the review comments" is `review` responding; the full
list is in [hand-offs](references/hand-offs.md#everyday-wording)). Several
modes in one request run in delivery order (spec, build, review, document,
verify, accept, release) unless the user limits the scope to fewer.

## 1. Resolve the item

1. Pin down what is in scope: an issue, branch, pull request, release
   candidate or pasted material (a title alone proves nothing). Find the
   repository via the issue's branch, its linked pull request or the
   profile, and run git there with `git -C <path>`. A session opened in
   another repository, or a folder another session owns, is mentioned once
   and otherwise ignored ([hand-offs](references/hand-offs.md)).
2. Load the project's **delivery profile** (the file
   `docs/delivery-profile.md`, else a "Delivery profile" heading in the closest `AGENTS.md` or `CLAUDE.md`;
   see [how profiles work](references/delivery-profile.md)): states with
   evidence anchors and gates, base branch, quality commands, artefact
   locations, environments, release route, owners. Missing profile, or an
   old one lacking the evidence anchor column: the evidence state is
   `Unknown`; ask before picking a base branch, creating files or touching
   the tracker, and offer the profile draft (or the anchors) as next action. Read the
   nearest project instructions too.
3. Read the board through the profile's route: the issue, comments newest
   first, state, cycle, linked pull request ([tracker](references/tracker.md)).
   No route, or a failing one: continue from the repository or pasted facts
   and list what went unread.
4. Note the precise repository, branch, commit, pull request head, build and
   environment behind every claim that depends on them.
5. When two sources disagree, show the disagreement. Do not quietly side
   with whichever helps.

Done when: the scope is named, each source read is listed, and each source
that could not be reached is listed too.

## 2. Build the stage map

Open [the stage map rules](references/stage-map.md) before drawing a map.
The full procedure and the awkward cases live there. The essentials:

- An **evidence anchor** proves arrival in a state; a **gate** only proves
  readiness to enter it. The state comes from anchors, never from gates.
- Work from **one candidate** (branch or pull request, exact commit, build,
  environment); two plausible ones with nothing to choose between make the
  state `Unknown`. Only current `Inspected` or `Run` facts about it prove an
  anchor; `Inferred` and `Unverified` facts say what to inspect next.
- A conditional state stays on the route until `Inspected` or `Run`
  evidence shows its condition false; settling that comes first.
- **Evidence says** the highest applicable state with a proven anchor, or
  `Unknown` when there are no anchors, the candidate is ambiguous,
  authoritative sources clash, or a later anchor cannot be tied to the
  candidate.
- **Drift** is one word: `matches`, `lags` (work is ahead of the board),
  `ahead` (the board claims more than the evidence shows) or `unknown` (a
  side is unresolved, or the board uses a state the profile lacks).
- **The gate line** names the earliest gate holding a ☐, from the first
  state through the evidence state, as **Unmet entry gate to <state>**.
  With no such gap it is **Gate to <next applicable state>**. While the
  state is `Unknown` it reads **Gate:** none until <what would settle it>.

The map is five lines of prose, never a table:

```markdown
**Board says:** In Progress since 3 March · S. Patel assigned · no pull request linked · no entry note yet
**Evidence says:** In Review, via PR #88 into `develop` at exact head 3f9c2a1 with 3/3 checks passing (Inspected); entry gate not yet met
**Drift:** lags (work is ahead of the board)
**Unmet entry gate to In Review:** ☑ pull request raised into `develop` (Inspected) · ☑ CI passing on that head (Inspected) · ☐ test notes written (Inspected: none found)
**Next safe action:** write draft test notes based on the acceptance criteria
```

Put the drift word's meaning in brackets every time. List the profile's
own criteria in its own order, each with a tick and an evidence label;
switch to bullets past three. The next safe action is one verb with one
object that this run can do now (inspect, draft, ask); when the following
step needs someone's permission, add that step and whose permission. For
money, tenancy, permissions, migrations or personal data, keep every
control the [operating model](references/operating-model.md) lists, even
when it slows things down.

Done when: the evidence state cites its anchor and candidate (or says
`Unknown` and why), drift is derived from it, the gate line faces the right
way, and a single next action follows from that gate.

## 3. Run

- **Default**: after the map, do **one** safe action that needs no fresh
  permission and no human judgement (check the issue against the Definition
  of Ready, draft missing testing notes, pin the pull request head and list
  findings, draft the note the board wants), then hand back.
- **Carry on** (or "as far as you can"): keep doing safe, useful actions,
  confirming passed stages quickly instead of rebuilding their artefacts,
  and redraw the map after each real result, until the next step needs
  permission, access or judgement. A sound spec is a checkpoint passed, not
  a place to stop; no test environment is no reason to skip planning UAT.
- **Status**: the evidence list and the map, nothing drafted. "What stage
  is this at and what can you finish now?" is a default run.
- **Focused mode**: read that mode's reference alone, do it, redraw the
  map; "only" means stop after it. A mode finishes when its completion
  check passes or its exact blocker is written down.
  [spec](references/modes/spec.md) · [build](references/modes/build.md) ·
  [recover](references/modes/recover.md) ·
  [review, respond, ship](references/modes/review.md) ·
  [document](references/modes/document.md) ·
  [verify](references/modes/verify.md) · [accept](references/modes/accept.md) ·
  [release](references/modes/release.md). `review` stays ambiguous
  until it is known to mean handover, independent review, respond or ship,
  and `verify` until it is known to mean plan, execute or report; the mode
  reference says to state the operation before starting.

Specialist skills take their own steps when installed
([hand-offs](references/hand-offs.md)); fold what they return into the map.

Done when: each action taken produced a real output, and each focused mode
passed its completion check or recorded its exact blocker.

## 4. Tracker writes

Reads cost nothing; writes need a yes. Each run reads the board, states the
drift and drafts whatever note the profile expects, and stops there. A
comment, a link or a state change happens only when the user asks in this
session and the profile permits that kind of write. A state change also
needs the destination gate fully ticked from `Inspected` or `Run` evidence,
unless the user has knowingly accepted a gap the map already showed.
Approved-type and live-type states are never set on the skill's own
judgement: one records a named person's sign-off, the other a production
check. If any in-scope UAT scenario has not run, do not offer sign-off:
run it, or take the gap to the acceptance owner as a decision. The full
rules, including the fresh read before a write, are in
[tracker](references/tracker.md).

Done when: each write traces to an instruction and shows its state before
and after.

## 5. Freshness, authority and artefacts

If an earlier stage changes, leave later artefacts in place and flag only
the claims it affects, with what to recheck
([which change stales what](references/operating-model.md#freshness)). Then
choose the evidence state again from the anchors that still hold.

Reading, analysis and drafting need no permission. Ask first before any of
these: editing code without a build or fix request; pushing, opening a pull
request or replying to review threads (the base branch is always the
profile's); writing to the tracker; changing shared test data with no
agreed reset; merging to a release branch, deploying, or running a
production smoke check; accepting technical or product risk; moving a
decision out of `Proposed` into `Accepted`, `Superseded` or `Reversed`. A
worktree tool that pushes a new branch identical to its base is only
setting up, and needs no permission. Permission covers the item and action
it named. Halt immediately on a credible credential leak, cross-tenant
access, a live payment, unexpected personal data, or damage to production.
Reserve `NEEDS DECISION` for intended behaviour that is missing or
contradictory, and look up plain facts yourself.

The files in [assets/](assets/) say what an artefact must contain; they
are not forms. Refresh what exists (usually the issue), save new files only
where the profile or user says, otherwise reply inline, and never inside
the skill's folder.

Done when: each later artefact either rests on a current source or shows
what needs rechecking, and no action went past its permission.

## 6. Return the receipt

Re-read the moving parts (repository and tracker) just before writing, as
[receipt](references/receipt.md) describes, then use this shape:

```markdown
## Needs you
1. The board shows In Review but no PR exists: (a) open one now, (b) put the card back to In Progress. I recommend (b); review has not begun. Reply `ABC-123 b`.

## Where we are
<the five-line map>

## Done this run
<actual outputs, each claim tagged Inspected, Run, Inferred or Unverified>

## Next
<the single next safe action, and what would clear the gate>

## Evidence
<what was read; downstream artefacts now stale>
```

**Needs you** leads every receipt, status runs included, whenever a
decision, permission or access is required; leave it out only when nothing
is. The same reference covers host-prescribed headings, **Try next time**
and two streams in one session.

Done when: every item on the receipt checklist in that reference holds.

## Gotchas

- Boards trail branches, pull requests and deploys, so check both sides.
- Passing CI says nothing about a browser journey or a product outcome.
- Report work-in-progress (WIP) limits and staleness to an owner; never enforce them.
- A criterion changed after review can stale more than the brief: do the
  freshness pass.

## It's working if

- A developer reads their item in the board's language (state, drift, the
  next gate as ticks) plus one next step, without opening this file.
- A clear issue flows on to the next useful stage rather than being bounced
  as already specified, and nothing reaches the tracker or the remote
  without the user saying so.
- Runs halt only at a named boundary of access, permission, safety or
  judgement, and say exactly what would lift it.
