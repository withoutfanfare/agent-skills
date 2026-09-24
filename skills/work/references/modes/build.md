# Build mode

This is where code changes. The aim is a diff someone can review, with every
acceptance criterion proven by its own check, ready to hand to `ship`. Work
takes a ready issue or an accepted brief and goes through its criteria one
by one. The trigger is explicit: `work build <item>`, or the user saying
"build it", "implement this" or "fix it" mid-run. That grants authority to
edit code within the item's scope and no further. A bare `work` grants none.

Build mode organises the work rather than doing it all itself. The
project's `CLAUDE.md` or `AGENTS.md`, its framework skills and `cover` (when
installed, for tests) do the actual writing.

## Four preconditions

1. [Spec](spec.md) has returned `Ready` or `Ready with assumptions`. If it
   says `Not ready`, send the item back there; guessing at a missing decision
   now means rework when the real answer lands.
2. There is a branch or worktree that follows the profile's naming. Either
   reuse the one the item already has, or make one exactly as the profile's
   *Worktree setup* line describes: which tool, what it copies across (say,
   env files or built assets) and any steps after creation. Branch from the
   profile's pull request base. Ignore the environment's hint about the
   default branch; it may name the wrong one for this project. Some worktree
   tools push the fresh branch while it still matches its base. That counts
   as provisioning, not publishing, so it needs nobody's say-so. Pushing
   actual commits is left to `ship`.
3. On the tracker, the item sits in the profile's in-progress state, unless
   the user has told you to carry on regardless. If a work-in-progress limit
   is exceeded, mention it; it does not stop you.
4. Either the worktree has no uncommitted changes, or you list the ones it
   has and do not touch them.

## Steps

Steps 1, 2, 5 and 6 follow one another. Steps 3 and 4 hold at every moment.

1. Take one criterion at a time, in the listed order unless the user sets
   another. Where the project works test-first, begin with a check that
   fails. Then make the least change that turns it green, and lint and
   analyse just the files you changed, using the profile's tools.
2. Once a slice hangs together, commit it: stage only its paths and follow
   the profile's commit style. Note each commit hash you create. That way,
   if the head moves unexpectedly (a hook that auto-commits, a parallel
   session), `ship` can spot it.
3. **Decisions found on the way.** If the brief is silent on how something
   should behave, number the question with the next free `D-` id, go with
   the safe default, state which one, and add it to Needs you. Only pause
   the build when that default might be risky or hard to reverse. If the user
   settles it in chat, record it in the brief's decision table and its
   readiness line before the turn ends.
4. The diff holds this item and nothing else. Anything you had to change
   beyond its scope is listed with the reason.
5. Some changes only prove themselves once deployed: queues, migrations,
   integrations, flows that cross services. If the profile has an
   **integration testing** state and this is such a change, wait for the
   user's go-ahead, then deploy or merge to the integration branch named in
   the profile. Exercise the named paths, keep the evidence, and advise
   where the item goes next: on to review, or back with a list of
   follow-ups.
6. Before `ship` takes over, run the profile's pre-push gates against the
   exact head commit.

## Optional completion ledger

This applies if a completion-ledger skill is installed (one checkbox per
criterion, each with a shell check whose expected output is a literal token
or summary line, never prose), and either the item has at least three
acceptance criteria or the build will plainly run beyond thirty minutes.

Set the ledger up before writing code. Give each criterion its own line,
attach a shell check whenever a command can settle it, and write down the
exact text that check will print. Because the checker compares strings, not
meaning, an expectation phrased in prose can never pass. The checker then
decides when the work is complete, and the receipt quotes its N of N. When a
criterion hangs on someone's answer, give it a `WAITING:` line and list it
under Needs you.

Parallel subagents are only worth it when the plan hands each of them its
own set of files. That is unusual within one issue, so default to working
alone.

## Guardrails

- This mode never opens a pull request and never pushes to the review or
  release branch; those belong to `ship`, which checks its own authority.
  Two pushes are allowed here and only two: the worktree tool pushing an
  untouched new branch (precondition 2), and the integration-testing merge
  the user approved in step 5.
- Stay inside the item's code and its own worktree: nothing destructive,
  no writes to shared data, no production access.
- Passing tests show the tests pass. Whether the journey works is for UAT,
  a later gate.
- Whatever was already in the worktree before this run, uncommitted files
  and history alike, stays exactly as it was.

## Completion check

Done when all of these hold:

- each acceptance criterion either has a green check or a stated reason it
  has none (with a completion ledger: the checker exits 0, or every line
  still open has a `WAITING:` or `ABANDON:` line that the receipt shows);
- the profile's quality gates are green on the files you changed and on the
  exact head;
- every decision found on the way appears in both the brief and the receipt;
- no push went further than an approved integration-testing merge;
- the [stage map](../stage-map.md) shows the gate to the next state, open
  boxes included.

Keep the receipt brief; do not retell the steps. Cover how each criterion
was proven (or the ledger's N of N), what the gates reported for the changed
files, any decisions found on the way with their `D-` ids, and whatever you
left outside scope, with the reason. End on the single stage-gate line from
the map. A compact list or two or three short paragraphs normally does it.
