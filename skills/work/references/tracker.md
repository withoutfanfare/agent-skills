# Tracker

The contract for reading and writing the project's issue tracker, whichever
product it is. Teams use the board to see where everything stands; this
skill's job is to keep it truthful by reading on every run, calling out
drift and preparing the updates the board wants, while leaving every
decision that belongs to a person with that person.

## One route

The lifecycle section of the profile names exactly one way to reach the
board. Common shapes:

- a command-line client, such as `gh issue view` and `gh project` for
  GitHub Issues and Projects, or a Jira or Linear CLI;
- the tracker's HTTP API, using a token the user has already set up;
- a tracker tool connected to the agent (an MCP server or an app
  connector).

Use that route only. On a machine with two routes, each may point at a
different workspace. If the named route is blocked or errors, record a read
gap in the receipt (`tracker not inspected: <reason>`); do not reach for
another route and do not guess the column. If the profile names no route,
ask the user to paste the issue and its recent comments, and note that the
tracker itself was not read.

Trackers name things differently. On GitHub the "state" may live in a
Projects status field or in labels; Jira has workflow statuses; Linear has
team workflow states. The profile spells each state the way the board
displays it. Client commands and tool names shift between versions, so
check them where you are and log a missing one as a read gap.

## Reads, every run

1. The issue itself: title, body, state, assignee, priority, cycle or
   sprint, labels, attachments, linked pull requests, and any branch name
   the tracker suggests.
2. Its comments, latest first: recent progress, blockers, and decisions
   someone recorded in the thread.
3. The board's states in order, set beside the profile's lifecycle table.
   A state that appears on one side only is a contradiction; report it and
   leave it for the owner.
4. The active cycle, if release eligibility hangs on it.
5. The column and its arrival note. If the profile sets work-in-progress
   (WIP) limits, count what sits in the current and the next state and
   report any breach along with who should hear about it. Check whether the note the profile wants
   on arrival in the current state is there; if it is missing, say so and
   draft it.

List these reads under Evidence in the receipt. When acceptance criteria
decide a gate, quote them word for word; testers check against the exact
wording, which a paraphrase loses.

All of this can change before the run ends, so read it again before the
receipt ([receipt](receipt.md)). If the route returns the issue and its
comments from separate calls, repeat both.

## Definition of Ready

Early in an item's life, compare the issue with the Definition of Ready
(or issue template) the profile points to (usually: the problem, its impact, what is
in and out of scope, testable acceptance criteria, test notes, dependencies
and references) before any other work. Each absent field makes the item
`Not ready`. Name those fields exactly, draft whatever the available
evidence supports, and where only a product rule could fill a gap, label
it `Decision required` rather than inventing one. Offer to put the draft into
the issue body, and only do so when the user agrees, merging it in so the
reporter's own words stay.

A field that a paste or export simply omits is `Unverified`, not absent.

## Drift

Of all the states, the evidence state is the highest one with its anchor
proven against the exact candidate ([stage map](stage-map.md)). Gates show readiness
and never set the evidence state or the drift.

| Word | What it means | What to do |
|---|---|---|
| `matches` | the board and the evidence agree | nothing |
| `lags` | the work has got further than the board shows, e.g. a pull request is open while the card still reads In Progress | draft the progress note and propose the move |
| `ahead` | the board shows more than the evidence supports, e.g. In Review with no pull request, or Approved with no sign-off on record | state it plainly and name the missing proof; never manufacture evidence to match the board |
| `unknown` | anchors are missing (no profile, or an old one), the tracker or the repository evidence is unavailable, two candidates compete, the board uses a state the profile lacks, or sources clash | say which side is missing or which sources clash |

`ahead` is the risky direction, because it is how untested work slips
into a release. Stale-item thresholds and WIP limits are reported as facts
to their owner; the skill does not enforce them.

## Notes the board wants

The lifecycle table says what note each state wants on arrival: a progress
update, a blocker note with an owner and expected date, testing notes with
a link to the pull request. Draft it as soon as the evidence reaches the
state or the item gets stuck. Keep it to five lines or fewer of facts plus
the next action, with links to the pull request, brief or evidence, written
as the team would write it and with no mention of the tool that drafted it.
The user posts it, or tells you to.

## Writes

Each kind of write needs the user's instruction and the profile's
permission:

| Write | Goes ahead when | Never |
|---|---|---|
| Comment | the user asks for it and the profile permits comments | record a decision or sign-off nobody made; write as if you were a named person |
| Description change | the user asks; the existing text and layout are kept | replace what the reporter wrote |
| Link a pull request or branch | the user asks, or it is part of a ship the user authorised | |
| State move | the user asks **and** the target state's gate is fully ticked by `Inspected` or `Run` evidence, unless the user knowingly accepts a gap already shown on the map | jump over states or move backwards without saying so; put the item into the approval state (the acceptance owner's recorded sign-off is required) or the live state (production verification is required) on the skill's own judgement |
| Cycle, priority, assignee, labels | the user asks | re-triage an issue as a by-product of other work |

An instruction covers one item and one write. "Move ABC-123 to In Review"
says nothing about the next issue, or about a later move of ABC-123.

List every write in the receipt with its state before and after. Take the
"before" from a read made right before the write, not from the start of the
session; otherwise you may overwrite a colleague's change and report a
before state that was never true. If that read fails, skip the write and
report it as not attempted, with the reason.

A read just before writing shrinks the race but does not remove it. Where
the tracker supports conditional or versioned updates, use them, so a
change made in the meantime makes your write fail instead of silently
overriding it. Where it does not, say in the receipt what the before state
was, when you read it, and that anything changed after that read would
have been lost without trace.

## Traps

- A fully ticked gate says the item is ready; only the anchor says it has
  arrived.
- Closed is not merged. `Merged` needs the merge time and the merge commit,
  both inspected, and that commit present in the base.
- A branch name the tracker suggests is naming advice, not proof that such
  a branch exists or holds the work.
- `Merged` tells you nothing about staging. The deployment is what counts.
- A comment that says "done" is a claim to check against the pull request,
  the deploy and the run.
