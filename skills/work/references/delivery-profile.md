# Delivery profile

The skill knows nothing about a particular project until the project tells
it: which states its board has and what earns entry to each, which branch
pull requests go to, where specs and test plans are kept, which commands
make up the regression check, how releases go out, and who signs off. The
delivery profile is where the project writes that down once, so every
person and every AI tool gets the same safe defaults. The project owns the
content; the skill only fixes the shape. Start from
[the template](../assets/delivery-profile.md).

## Finding it

Take the first of these that exists:

1. `docs/delivery-profile.md` in the root of the item's repository.
2. A heading called "Delivery profile" in the nearest `CLAUDE.md` or
   `AGENTS.md`.
3. If the item's branch was created before the profile landed, fetch it
   from the base branch and say you did:
   `git show origin/<base>:docs/delivery-profile.md`. Take `<base>` from
   the worktree's recorded base if the worktree tool stores one, or else the
   repository default, and never from the environment's main-branch hint.

If none exists, write "No delivery profile: no stage anchors" in the
receipt and act cautiously. The map shows `Evidence says: Unknown: no
delivery profile defines stage anchors` with drift `unknown`. The default
stage names may suggest a mode and a next action but never a stage. Ask
which branch pull requests should target. Reply inline instead of saving
files. Leave the tracker untouched. Assume no environment is reachable
until shown otherwise. Offer to draft a profile afterwards; never create
one unasked.

## Sections

| Section | What the skill takes from it |
|---|---|
| Lifecycle | the map's rows (each state in board order with applies-when, evidence anchor, gate, arrival note and mode), the single tracker route, the Definition of Ready, the kinds of tracker write an assistant is allowed, and WIP or staleness limits worth reporting |
| Branches and pull requests | the base branch for every pull request, protected branches, branch and worktree naming, how a worktree gets made (the tool, what it copies in, steps afterwards, whether it pushes the new branch straight away), description rules |
| Commits and quality gates | the commit style, and the exact commands required before a commit, a push and a pull request |
| Artefact locations | folders and filename patterns for briefs, decision records, UAT plans, reports, evidence and docs |
| Environments | each environment's address, what may be done there, and who deploys to it |
| Release | the release branch and who merges into it, schedule and cut-off, what makes an item eligible, the urgent route, how deploys start, smoke checks, rollback, how the issue is closed |
| People and authority | who signs off product decisions, who reviews, who may authorise a release, who can accept risk |
| Documentation | which readers each kind of change needs docs for, which `plainify` purpose suits each, and where those docs go |
| Project traps | links to the project's own guardrails |

## A lifecycle row

```text
State | Applies when | Evidence anchor | Gate to enter | Note on entry | Mode
```

- **Applies when** holds `always` or a condition, for example "only when
  the change touches `services/billing-sync/`". Conditional does not mean
  optional to skip: the state remains on the route until current evidence
  proves the condition false, and it shows as `Not applicable` only with
  that proof beside it.
- **Evidence anchor** is the single observable fact that shows the item has
  got to this state, phrased so it can be checked against the exact
  candidate (pull request number, head or merge commit, deployment,
  environment, acceptance scope).
- **Gate to enter** is the readiness list. It never proves arrival: a
  complete gate does not put an item in the state, and an anchor that is
  reached while its gate has gaps is an entry breach for the map to
  report, not grounds for placing the item one state earlier.

Starting points for anchors, to be restated in the project's own terms.
Every state needs one that someone can check:

| State | Anchor |
|---|---|
| Todo | the item exists, and checking the configured sources turns up no later anchor |
| In Progress | commits or changes belonging to the item sit on its branch or worktree (or the project logs a start event and it is there) |
| Integration Testing | the exact head is running in the integration environment |
| In Review | a pull request, still open, whose head is the exact commit and whose target is the review base the profile names |
| Merged | the pull request's merge time has been inspected and its exact merge commit is in the base (closed status, passing checks or a comment saying "merged" do not count) |
| Staging Review | staging runs the exact merge commit, or a build explicitly traced to it (a branch name is never proof) |
| Approved | the profile's place for sign-offs holds the named acceptance owner's decision, made about the exact deployed candidate against today's acceptance criteria |
| Live | production runs the exact approved candidate and the profile's production checks have run |

A profile with no lifecycle section has no anchors either: the evidence
state is `Unknown` with the same message as a missing profile, and the
default stage names choose only a mode.

An **old-style profile** lists states and gates but has no applies-when or
evidence anchor column. For these the skill reports `Evidence says:
Unknown: delivery profile needs evidence anchors` with drift `unknown`,
proposes a draft of the six-column table as the next action, and never
treats a gate as an anchor.

## Where each part is used

- Before any mode runs, the profile is read and then cited in the receipt.
- The lifecycle table supplies the map's rows, anchors and gates.
- The tracker route, permitted writes and arrival notes come from the
  lifecycle notes ([tracker](tracker.md)).
- Spec checks issues against the Definition of Ready.
- Build makes the worktree exactly as the worktree line describes, falling
  back to a hand-made one plus whatever the profile says it needs copied in.
- Lasting artefacts are saved only to the listed locations, otherwise the
  draft goes inline.
- Ship takes the base branch, push target and pre-push commands from here,
  never from a guess or the environment's hint.
- Document takes its readers, their `plainify` purposes and the save
  locations from here.
- Release takes eligibility, the merger, the deploy trigger, smoke checks,
  rollback and the final close from here, and invents none of them.
- An edited profile (new base branch, new board state) may invalidate the
  map, the handover and release preparation. Say so when it happens.

## Writing a profile for a project

1. **Look for what is already written.** Search for an engineering
   handbook, delivery policy, contributing guide or instruction-file
   sections that already set these rules, for example
   `git grep -il "base branch\|pull request\|lifecycle"` across the docs.
   Link to them and summarise; do not copy them out.
2. **Date them.** Note when each linked source last really changed and
   which one wins if they disagree (normally the nearest instruction file),
   so an outdated handbook gets noticed instead of followed.
3. **Mirror the board as it is.** List the tracker's actual states in its
   order, reuse the entry rules the handbook already has, and add one
   checkable anchor per state. If the board and the handbook disagree,
   note it for the owner instead of choosing.
4. **Say what an assistant should do.** "Default branch" might mean the
   repository default or the pull request base; write the working rule
   ("every pull request targets `staging`") and mention the other only as
   background.
5. **Keep fallbacks conditional.** Phrase them as "only if ..., then ...",
   never as a loose "or".
6. Propose it on its own branch and pull request, so the project's
   reviewers can check the facts.

## Guardrails

- The profile never gives permission. It sets where writes go and which
  kinds are acceptable; the user still decides when.
- If what you observe contradicts the profile (a base branch that is
  missing, a listed command that errors, a board state with no profile
  row), halt and describe the mismatch rather than choosing the reading that lets
  you proceed.
- The first time you use an environment address in a session, check it (a
  `HEAD` request will do). If it is dead, look at the repository's deploy
  workflows and smoke scripts, which tend to be right when the profile has
  drifted, and correct the profile in the same run. Never just work round
  a dead address.
- Keep secrets, credentials and private addresses out of the profile.
