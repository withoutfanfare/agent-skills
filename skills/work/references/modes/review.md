# Review mode

Reviewers have limited attention, and it belongs on whether the change is
correct, well built and safe. It should not go on working out what the
change was for. This mode covers both ends of that: the author explains,
someone independent inspects, the author answers, and finally the work goes
up as a pull request.

## Pick the operation

Name the operation first.

| Operation | Output |
| :-- | :-- |
| `Author handover` | Written from the author's side: what the change sets out to do, its boundaries, the choices made, the risks, and which checks have run. |
| `Independent technical review` | Findings someone can act on, drawn from the code as it stands now and the evidence behind it. |
| Both | Two documents kept apart. The review never cites the handover as evidence: nobody can independently verify their own work. |
| `Respond to review` | Once comments arrive, the author sorts every thread against today's code, makes the agreed fixes, answers, and asks for another look. |
| `Ship` | Commits, pushes and raises the pull request. |

For a lasting artefact, fill in the [handover template](../../assets/pr-handover.md)
or the [review report](../../assets/review-report.md).

**Hand-offs.** If they are installed, three skills can do parts of this:
`review` performs the independent review, `raise` creates the pull request,
and `shepherd` carries it through CI and comment threads until it merges.
Whatever they hand back is restated in this mode's terms (severity,
disposition, the stage map). A `review` finding arrives on the same
blocker/major/minor scale as below, though a "nice to have" minor can drop
to Polish; its confidence words certain, likely and possible map to High,
Medium and Low. Anything brought back begins life as `disposition: Open`. When none
of them is installed, this file is the process.

## Inputs

Collect before starting:

- the pull request link (or the repository) with its base, its head and the
  complete head SHA;
- intent as it stands today: acceptance criteria and any decision records;
- whatever the author knows, and what they have already verified;
- the diff itself, plus callers that did not change but matter, the tests,
  migrations and runtime configuration;
- CI outcomes, and a safe way to reproduce anything suspicious;
- when the draft is old: who owns it, how long since anything happened, how
  far the base has moved.

Put gaps in context at the top, ahead of any detailed finding. A head that
keeps moving, or intent that contradicts itself in a material way, can make
the honest answer `Not reviewable yet`.

## Independent technical review

These steps build on each other (risk cannot be ranked before the files are
mapped; duplicates cannot be merged before findings exist), so take them in
sequence.

1. Fix the base, the head and the complete SHA. Any check you quote must
   have run against that exact head.
2. Read the issue, the specification, the decisions and the handover
   together. Call out where they disagree.
3. Group the changed files, and any untouched ones that matter, by what
   they do and which risk area they sit in.
4. Decide whether this is a single unit a reviewer can understand and
   verify without the rest.
5. Start with the dangerous ground: anything touching money, data that
   could be lost, migrations, who may do what, the walls between tenants,
   effects outside the system, and causes shared by several symptoms.
6. Follow each important path from the input through validation, storage
   and side effects to the response and what happens on failure.
7. Treat every test as a claim, and check it really would go red if the
   defect it guards against came back.
8. When it is safe and practical, reproduce a suspected defect.
9. Collapse findings that come from one root cause, then order them by how
   bad and how likely they are.
10. Product behaviour nobody has defined goes under `Awaiting a decision`.
    It is not a code defect.
11. Finish with the disposition and the next action.

Done when: nothing is left implicit. The operation, the exact head, the map
of changes, the reviewability call, the findings, the evidence still
missing and the recommended disposition are all written down. Then go back
to the [stage map](../stage-map.md).

### Size, shape and stale drafts

None of these rejects a change by itself, but each one is a warning:

- one pull request carrying several unrelated behaviours or risk areas;
- no single purpose you can state for the diff;
- machine-generated files interleaved with hand-written logic that matters;
- UI, payments, permissions and migrations bundled when they need not be;
- nowhere to verify or roll back one part on its own;
- a handover written for some other head.

Slices that each keep the product working are better. When splitting is
unsafe, the author owes a reason and a suggested order for reading it.

Base drift is measured by a dry-run merge, never by how many commits behind
the branch is. git 2.38 and newer: `git merge-tree --write-tree <base> <head>`
lists conflicts directly. Older git: run
`git merge-tree $(git merge-base <base> <head>) <base> <head>`; it prints
the full merged tree, so search the output for `<<<<<<<`. Report which
files conflict and which files both sides edited, with each side's commits.
Always aim it at the item's checkout using `git -C <path>`.

Stale work gets the same treatment every time. Check someone still needs it
and still owns it. Measure drift and dependencies. Rewrite the handover,
rerun the checks that matter, and recommend one of refresh, split, a
deliberate pause, or closing it. An age limit is a nudge for the owner to
decide, never a target to hit.

### Finding contract

UAT uses the same four severity words as review, so readers carry one scale
from code review to test report.

- **Blocker**: severe harm to money, security, privacy or service is
  credible and could happen now.
- **Major**: probably a serious defect. Examples: one tenant reaching
  another's data, losing data, getting money wrong, a core journey that
  cannot be completed.
- **Minor**: a genuine problem with correctness, reliability,
  accessibility or maintainability, but its reach is limited.
- **Polish**: worth doing, though it hurts little today.

Each finding records where it is, what you saw, what sets it off, what it
costs in practice, the rule it breaks, the least change that fixes it, how
to prove the fix, and how sure you are.

```yaml
id: "RF-001"
title: "<lead with the impact>"
severity: "Blocker | Major | Minor | Polish"
location: "<file:line>"
trigger: "<the input, state or sequence that causes it>"
observed_evidence: "<what the code or behaviour shows today>"
impact: "<what goes wrong in practice>"
relevant_rule: "<spec, invariant or standard broken>"
recommended_change: "<least change that fixes it>"
verification: "<test or repro that proves the fix>"
confidence: "High | Medium | Low"
disposition: "Open | Fixed | Accepted risk | Not applicable | Already addressed | Deferred with owner | Rejected with evidence"
```

If there is nothing to act on, say that in so many words. Still state what
you looked at and where doubt remains.

### Disposition

The recommendation is exactly one of `Approve`, `Comment`,
`Request changes` or `Not reviewable yet`. An AI's analysis never counts as
technical sign-off, and this mode does not approve itself. The disposition
that counts is recorded by a qualified human or by a review policy that has
the authority.

### Guardrails

- Independent review changes nothing. Code gets written only if someone
  asks, and only once the findings are understood.
- Look at the live head and its callers. A diff you remember, or somebody's
  summary, will miss anything pushed since.
- Code an AI wrote meets the same bar as code a person wrote.
- Style taste is not a finding; evidenced defects are.
- Leave disagreements in plain view, and say whose authority is missing.
- A finding meant to help must not leak: keep secrets and unneeded personal
  data out.
- Passing CI says nothing about product correctness or browser acceptance,
  because CI never uses the product as a person would.

### Freshness

When the head moves, only the parts it touches go stale. For each finding,
note whether you rechecked it on the new commit or it is still open.
Unclear product intent surfaced by review goes back to [spec](spec.md);
missing tests or evidence go to [verify](verify.md).

### Report

One line naming the operation and how it went, then the findings (or the
handover) in the contract above. The diff does not need retelling. A line
or two covers the recommended disposition and what is missing; the findings
carry the detail.

## Respond to review

This runs when someone says "respond to the review" or "deal with the
comments", or when a review run meets a pull request with threads still
unresolved.

Sequence matters: sort a thread before touching the code, and have the fix
on the head before replying about it.

1. Gather every unresolved thread on today's head. Write each reviewer's
   point as a single line.
2. Check each against the code now, not what you remember, and give it one
   triage word:
   - **agree**: make the change;
   - **agree, different fix**: fix it another way and explain why;
   - **disagree**: answer with evidence, calmly;
   - **awaiting a decision**: it is really a product question, so it goes
     to whoever owns that decision, not to the reviewer.

   Every thread gets a word.
3. Make agreed fixes as small, focused commits following the profile's
   convention. Then run the profile's gates twice over: on the files you
   touched, and on the exact head.
4. Answer each thread, naming the commit and what it changed. Replies and
   pushed commits land outside the repository, so they need the user's go
   ahead; "address the comments and push" is enough. Ask for re-review only
   where the project does that explicitly.
5. List any thread still open with its reason. Undefined product behaviour
   goes to [spec](spec.md), missing evidence to [verify](verify.md).

Done when: each thread carries a triage word, the agreed fixes sit on a
pushed head with the gate results shown, and every reply is posted or
drafted.

The report is a table, one row per thread: the point raised, its triage,
and the change made. Add the gate results for the touched files. Short is
fine.

## Ship

Triggered by `work ship <item>`, or by "push", "open the PR" or "ship it"
in a review run. Ship takes a finished change and makes it reviewable as a
pull request. Because it acts outside the repository, it needs explicit
authority before anything happens.

### Preconditions, strictly in this order

Each check assumes the earlier ones passed. Running gates on an unsettled
tree, or pushing before looking for an existing pull request, means acting
on facts that are already out of date. Clear all six before any commit or
push.

1. **Authority is explicit, and given in this session.** The user asked in
   so many words to commit, push or open the pull request, or typed
   `work ship`. A stage reading "Ready", green tests, or approval given for
   a different item do not count. Without authority, pushing crosses the
   line: stop and ask.
2. **The delivery profile has been read.** It supplies the base branch,
   the protected branches, pull request conventions and the gates (see
   [delivery profile](../delivery-profile.md)). No profile? Ask which
   branch is the base, before anything else. Do not trust the
   environment's default-branch hint or the repository's default branch:
   either may point somewhere this project does not use as its base.
3. **The working tree is clean, or everything in it is meant to be
   there.** Show `git status`. Stage the item's own files and nothing more,
   scoped the way the profile says, and list whatever you are leaving out
   on purpose. Formatters touch only files you changed. Run one across a
   whole folder and unrelated files end up in the commit; a pre-commit
   fixer will also reapply itself to anything staged. Check the branch's
   commits against the ones made in this run. If any came from elsewhere
   (an auto-commit hook, a different session), say so before pushing it.
4. **Gates ran on the exact head.** Run the pre-push commands the profile
   lists (lint, tests, static analysis) and paste real lines of their
   output into the receipt. Note which SHA they ran on. Just before
   pushing, check that SHA still equals `HEAD`; if an amend or a formatter
   hook moved it, run the gates again rather than assuming. A failure that
   was already there before your change is named, never hidden.
5. **Any existing pull request for the branch is still open.** If the
   branch already has one, look at its state first. For example, with the
   GitHub CLI: `gh pr list --head <branch> --state all`. A merged or closed
   pull request is never pushed to or edited, because that would quietly
   bring back history reviewers had already closed off. The new commits get
   a fresh pull request and their own description, and the receipt
   explains why two exist.
6. **The push goes to the item's own branch and nowhere else.** Protected
   branches are never pushed to; they refuse direct pushes by design. When
   the branch already exists on the remote, only a fast-forward is allowed,
   so no rewrite can wipe out commits another person may be building on.

### Raising the pull request

- Target the profile's base branch from the item's branch. The title obeys
  the profile's convention and includes the issue key, such as `ABC-123`.
- The description follows the profile. When it gives no rules, write, in
  this order: what was wrong, in everyday words; how it is fixed; any
  change in behaviour or risk the reviewer needs to know; how to check it
  (commands plus a manual route); links to the brief, the decisions and
  the UAT plan; and the project's template headings, marking any that do
  not apply "n/a" with the reason. Problem and fix come first. A list of
  touched files explains nothing.
- If the tracker can hold a link and the profile permits it, connect the
  pull request to the work item. The issue's state stays as it is: moving
  it is a separate write that comes later and needs the user's word. The
  profile may expect a note when an item enters review (the link, testing
  notes). Draft that note, and post it only when the user says so. See
  [tracker](../tracker.md).
- The receipt records the base, the head, the complete head SHA and the
  pull request's URL.
- Anything a later gate will ask for (a UAT plan for the staging-review
  gate, deployment notes, runbook edits) is written before shipping so it
  rides in the feature pull request. If something only gets written after
  the merge, it goes wherever the profile directs, or onto a new branch
  with a new pull request. It never goes onto the branch that already
  merged.

### Once it is up

- Usually the gate into the profile's review state is now met. The stage
  map records that, and flags drift if the board still shows the old
  column.
- A reviewer can now treat handover and review as `Actionable now`.
- A further commit on the branch makes the description's checking steps,
  and any review evidence, out of date. Say that and bring them up to date.

Done when: a pull request targets the profile's base branch with the
correct head SHA and the receipt carries the gate output, or the receipt
names the precise precondition that stopped it.

The report is a brief receipt: how the six preconditions came out (or which
one stopped it), the gate output for the exact head, and, once the pull
request exists, its base, head, head SHA and URL.
