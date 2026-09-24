# Stage map rules

How step 2 of the skill decides where an item stands. Apply the steps in
this order on every run. The map uses the project's own vocabulary because
its rows are the profile's lifecycle rows, and every row brings four
pieces:

- **Applies when**: `always`, or a condition deciding whether this item
  passes through the state at all.
- **Evidence anchor**: one fact you can go and look at which shows the item
  got there.
- **Gate to enter**: what ought to be true before anyone moves the card
  into the state.
- **Note on entry**: the update the board expects on arrival.

A project with no anchors (no profile, a profile without a lifecycle
section, or an old-style one) still gets the
generic names Intent, Build, Review, Document, Verify, Accept and Release,
but only as labels for modes. None of them can be reported as the evidence
state.

## Choosing the evidence state

### 1. Settle on a single candidate

Narrow the item down to the dimensions its lifecycle cares about: which
branch or pull request, which exact head or merge commit, which build or
deployment, which environment. Acceptance scope is deliberately not one of
them; it only decides whether acceptance evidence (UAT, verification,
sign-off) is current for the candidate. So editing a criterion leaves the
head, merge and deployment anchors standing.

When two branches, pull requests, builds or deployments are equally
plausible and nothing says which is live, the state is `Unknown`. Resist
picking the one that is newer, greener or easier.

### 2. Admit only eligible evidence

Only `Inspected` or `Run` evidence proves an anchor, and only when it is
current for this candidate, environment and scope and no other
authoritative source disputes it. `Inferred` and `Unverified` facts are
pointers towards the next thing to look at; they satisfy nothing. "PR is
up, checks green" in a comment is a lead, not a pull request.

Facts about an earlier head, a replaced build, another environment or an
older scope remain in the receipt as history and are ignored when
choosing.

### 3. Decide which conditional states apply

Test each conditional state's condition against what was actually
inspected: the changed paths, the contracts the change touches. It becomes
`Not applicable` only when `Inspected` or `Run` evidence shows the
condition false, and the map cites that evidence.

Every weaker situation keeps the state on the route, gate and all:

- nothing inspected speaks to the condition (no changed-path list in the
  evidence at all);
- someone tried to inspect and the attempt failed;
- a comment or claim says the state is not needed, which is only
  `Inferred` or `Unverified`.

Until the condition is settled, the check that settles it (the changed
paths) is the first action for that gate,
ahead of drafting anything for it, since the answer may delete the gate.

### 4. Report the highest proven anchor

Go through the applicable states from first to last and keep the latest
one whose anchor the candidate has proven. That becomes **Evidence says**,
together with the anchor and whatever identifies the candidate precisely
enough to audit: pull request number, exact commit, environment, decision
record.

Gates never pull the state backwards. With its `Merged` anchor proven, an
item is `Merged` even if some earlier gate was skipped.

### 5. Fall back to Unknown

Report `Unknown`, and why, in any of these cases:

- no profile, or a profile with no lifecycle section: "Unknown: no
  delivery profile defines stage anchors";
- an old-style profile with no evidence anchor column, whose gates cannot
  stand in for anchors: "Unknown: delivery profile needs evidence
  anchors", and offer to draft the missing columns;
- more than one plausible candidate;
- two authoritative sources in conflict, for instance a health endpoint
  showing a commit whose deploy job is recorded as failed (neither side
  wins until someone looks again);
- a later anchor that cannot be linked to this candidate.

A convenient guess is never the fallback.

### 6. Work out drift

Set the evidence state beside the board's:

| Word | Used when |
|---|---|
| `matches` | they name the same state |
| `lags` (work is ahead of the board) | the board is on an earlier state |
| `ahead` (the board claims more than the evidence shows) | the board is on a later state, which is the risky case |
| `unknown` | either side is unresolved, or the board shows a state that has no profile row |

Give one of the four words plus the reason. If the board sits in a state
the profile has no row for (say `QA`), do not fold it into a neighbouring
state: drift is `unknown` and the mismatch is named.

### 7. Mark every gate

Mark the gates of every applicable state from the first up to and
including the evidence state, and then the gate of the next applicable
state, using eligible evidence only:

- ☑: `Inspected` or `Run` evidence shows the criterion satisfied.
- ☐: such evidence shows it unsatisfied; somebody looked where it would be
  and found nothing, or a run failed.
- `Unverified`: no eligible evidence covers it either way. That is a
  lookup, not a failure. On the gate line it becomes something for Next to
  go and check, and it bars any tracker write. On an earlier state's line
  it is noted there, and it does not reopen that gate: an earlier gate
  reopens only on a ☐.
- A paste or export that leaves a field out has not shown the field to be
  empty. An issue export with no "impact" line leaves the Definition of
  Ready criterion about impact `Unverified`, not ☐.
- Judge each criterion by the profile's own wording and no stricter.
  "UAT plan exists" is met by a plan you inspected, however old; whether it
  covers the current scope is a question for the later gate that mentions
  scope or sign-off.
- Once an item has moved past a criterion, the record of how things were
  meets it. A pull request that targeted `staging` and has since merged
  still satisfies "PR open against `staging`". Only criteria that were
  never met get ☐.
- Copy criteria exactly as the profile lists them, without splitting,
  combining or rephrasing, so a given gate looks identical on every run.

### 8. Pick the gate line

- Look at every gate from the first state through the evidence state. If
  any has a ☐, the line is **Unmet entry gate to <the earliest such
  state>**, listing all its open criteria, and fixing the first safe gap is
  the default next action. Open criteria on later gates go on those states'
  own lines.
- If none has a ☐, the line is **Gate to <next applicable state>**, with ☐
  on anything not yet proven, including criteria that are only `Inferred`
  or `Unverified`, each labelled.
- Beyond the final state, the line shows the profile's closing verification
  or upkeep condition, and nothing extra is made up.
- An `Unknown` evidence state supports no gate at all. The line says
  **Gate:** none until <what would settle the state>, and settling it is the
  next safe action.

### 9. Choose again after a change

A new head, merge commit, deployment or acceptance criterion voids the
evidence that belonged to the old one. Pick the state again from the
anchors still standing, instead of nudging the map backwards by feel. A
criterion that is new or edited voids UAT, verification and sign-off and
nothing else: the deployed candidate's anchors hold, so the state stays
where they put it (for example `Staging Review` when a criterion arrives
after approval), and the gate lists the acceptance work the new scope
still needs. The previous UAT and sign-off remain in the receipt as history
for the scope they did cover.

## Writing the map

The map is five short lines (**Board says**, **Evidence says**, **Drift**,
the gate line, **Next safe action**) and never a table, since tables wrap
badly in a terminal.

- **Board says** uses the board's own name for the state, since when, and
  whatever else on the card matters: assignee, cycle, linked pull request,
  whether the arrival note is there.
- **Evidence says** commits to one state or to `Unknown`.
- **Drift** always carries its bracketed gloss; the reader has not seen the
  definitions.
- The gate line shows each of the profile's criteria in the profile's
  order with one mark and one evidence label (`Inspected`, `Run`,
  `Inferred`, `Unverified`). Beyond three criteria, give each its own
  bullet.
- **Next safe action** is a single verb and object that this run is
  allowed to do (inspect, draft, ask). If the step after it depends on
  somebody's word, name that step and whose word. Posting, moving, pushing,
  merging, deploying or signing off never appears here as the action; they
  wait under Needs you.

Underneath the map, give passed states a line each and later states a
one-line summary of their gate. Every state carries one status from
`Complete`, `In progress`, `Actionable now`, `Blocked`,
`Awaiting a decision` and `Not applicable` (the last with its reason).
