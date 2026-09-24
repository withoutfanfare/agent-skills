# Hand-offs and environment

This skill orchestrates; other skills do specialised jobs better. If one is
installed, call it, then fold what it produced back into the map before
continuing, because a result that stays inside another skill's report
leaves the map out of date. If none is installed, the mode reference covers
the job.

| Job | Skill, when installed | Fallback |
|---|---|---|
| Opening a pull request | `raise` | the ship part of [review](modes/review.md) |
| Getting a pull request through CI and review threads | `shepherd` | the respond part of [review](modes/review.md) |
| Independent code review | `review` | the independent review part of [review](modes/review.md) |
| Browser acceptance runs to a verdict | `road-test` | [verify](modes/verify.md) |
| A manual QA plan drawn from code and docs | `test-plan` | the planning part of [verify](modes/verify.md) |
| Documentation in plain English | `plainify` | [document](modes/document.md) |
| Tests for the acceptance criteria | `cover` | the project's own testing habits |
| Lasting decision records | `ledger` | [decision record template](../assets/decision-record.md) |
| Writing the code | the project's own engineering skills | the project's instruction files |

Convert what comes back into this skill's terms: review findings arrive on
the same blocker/major/minor scale, their confidence words certain, likely
and possible map to High, Medium and Low, and they begin as
`disposition: Open`; browser
results become `PASS`, `FAIL` or `NEEDS DECISION` against a named release
candidate, and anything not run gets no verdict.

## Everyday wording

People rarely type a mode name. Treat these as equivalent:

| They say | Mode |
|---|---|
| "open the PR", "push it", "ship it" | `ship` |
| "fix it", "implement this", "build it" | `build` |
| "document this", "write the docs" | `document` |
| "review this", "is this ready?" | `review` |
| "reply to the review", "address the review comments" | `review` (respond) |
| test this end to end | `verify` |
| go back to the spec, pin down the requirements | `spec` |
| update the board, move it to <state>, post the comment | a tracker write ([tracker](tracker.md)) |

## Completion ledgers

Some setups include a completion-ledger skill: a file with one checkbox
per criterion, each tied to a shell check and an expected output, plus a
checker that will not accept "done" while a box is open. Those checkboxes
are unrelated to this skill's stage gates. When you use one, the expected
output must be something the check prints literally, such as a token
(`... && echo GONE`) or a fixed summary line, because the checker compares
text and cannot read intent. A criterion that waits on a person is marked
as waiting and raised under Needs you.

## Working away from the session's folder

If the session started in a different repository, or the folder belongs to
another session, mention it once and do not let it steer anything:

- do the work in the item's own worktree, made the way the profile's
  worktree line prescribes (which tool, which files it copies in such as
  environment files and built assets, which steps follow);
- run any checker yourself inside that worktree, since a hook watching
  only the session's folder will happily pass a build it never looked at;
- do not touch a folder that another session holds. Taking it over is for
  the person to decide.
