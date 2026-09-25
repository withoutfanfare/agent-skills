---
name: improve-skill
description: >-
  Tests an existing skill against realistic prompts and a set of pass or
  fail checks, then edits it one change at a time, keeping only the edits
  that raise the score.
license: MIT
disable-model-invocation: true
argument-hint: "the skill folder to improve"
allowed-tools: Read Grep Glob Bash Write Edit
---

# Improve skill

A skill's wording is a guess until someone runs it. Reading it and deciding
it "sounds clearer now" tells you nothing about whether it still triggers
on the right requests or still produces the same result, because a small
wording change can quietly break what used to work. This turns that guess
into a score, and refuses to keep an edit unless the score goes up.

## 1. Fix the target and what "better" means

Name the skill folder and read its `SKILL.md` in full, plus anything under
`references/`. Decide, before writing anything else, which of these the
skill needs to improve on: firing reliably on the requests it should
answer, staying quiet on requests that belong elsewhere, the quality or
completeness of what it produces, or more than one of those. Everything
below is scoped to that goal, so a wording-only skill does not need output
checks and a background job with no description text does not need
trigger checks.

Done when: the skill folder is confirmed to exist and the goal is written
as one sentence.

## 2. Collect matched requests and near misses

Write four to six requests a real person would type that this skill should
handle, in different phrasing, covering its different branches (not five
copies of the same sentence). If triggering matters, add two or three
near-miss requests, close enough in topic that a lazy description would
wrongly catch them, that this skill must NOT start for. Label each line
`fire` or `quiet`.

Done when: every request is labelled, and at least one `fire` request
exercises each major step of the skill.

## 3. Write the pass or fail checks

For each request, write three to six checks that only need a plain reading
of the result to answer yes or no, no judgement about tone or taste.
[references/check-patterns.md](references/check-patterns.md) has the
categories and worked examples: trigger checks, structure, length,
required content, banned content and step order. Spread the checks across
categories rather than writing five variations on one rule, and word each
one so a person with no other context could mark it without guessing what
you meant.

Done when: every check reads as a plain yes/no question, and none of them
use words like "good", "clear" or "compelling".

## 4. Save the request and check set to a file

Put the requests and checks in one JSON file next to the skill, following
the layout in
[references/run-file-format.md](references/run-file-format.md). Keeping it
as a file, rather than only in conversation, means the same set can be run
again after every edit.

Done when: the file exists and parses as JSON.

## 5. Record the baseline, skill removed

Run every request once with the skill unavailable, so you know what the
underlying model already does unaided. In Claude Code, this means a
headless run (`claude -p "<request>"`) from a copy of the project with the
skill's folder taken out of the skills path; in Codex, `codex exec
"<request>"` with the folder removed from `.agents/skills`. For each
`quiet` request, "did not act like the skill" is itself a pass. Mark every
check against this unaided output.

Done when: a baseline score (checks passed out of checks run) is recorded
and kept for comparison.

## 6. Run with the skill in place and score it

Put the skill back and repeat the same requests through the same headless
commands. For a `fire` request, check whether the skill started at all
before marking the output checks: in Claude Code, add `--output-format
stream-json --verbose` and look for a `Skill` tool call naming it; in
Codex, `codex exec --json` prints the run's events, so look for its
`SKILL.md` being read; for a `quiet` request on a
typed-only skill (`disable-model-invocation: true` in Claude Code,
`allow_implicit_invocation: false` in `agents/openai.yaml` for Codex),
confirm it really did stay out unless asked for by name in both harnesses,
since the two settings are read independently and one can be set without
the other. Score triggering and output separately, so a skill that fires
correctly but writes a weak report is not confused with one that never
starts.

Done when: two scores exist, current and baseline, split by trigger and
output where both apply.

## 7. Change one thing, then compare

From the checks that still fail, pick the one that would lift the score
most if fixed, and make a single, minimal edit to `SKILL.md` that targets
only that check, leaving everything else untouched. Re-run steps 5 to 6.
If the score rose, keep the edit and move to the next failing check. If it
stayed the same or fell, undo the edit (`git checkout` on the file, or
restore the text you changed) and note that check as attempted, so it is
not picked again. Stop when the score meets your target, when every
failing check has been attempted once, or after eight attempts, whichever
comes first.

Done when: every kept edit corresponds to a score increase you can point
to, and the stopping reason is one of the three above.

## 8. Report the run

```markdown
## Skill improvement: <name>

**Goal:** <trigger reliability / output quality / both>
**Baseline:** <score>, **Final:** <score>

### Changes kept
| Check targeted | Edit | Score before | Score after |

### Still failing
| Check | Why it resists a small edit |
```

Done when: the report names every kept edit and every check still failing,
with no unexplained score movement.

## It's working if

- The score after your edits is higher than the score before, not just
  "reads better" to you.
- A typed-only skill's near-miss requests were checked in both harnesses,
  not assumed from one setting.
- Nobody has to re-read the whole skill to see what changed and why; the
  report names the exact check each edit was for.
