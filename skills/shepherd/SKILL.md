---
name: shepherd
description: >-
  Stays with one open pull request until it is merged or precisely blocked:
  reads failing checks, fixes real failures, answers review comments,
  resolves conflicts and arms auto-merge where allowed. Use when the user
  asks to babysit or watch a pull request, get it merged, or says CI keeps
  failing on it.
license: MIT
allowed-tools: Bash Read Grep Glob Edit Write
---

# Shepherd

Opening a pull request is quick; getting it merged is where the time goes.
Checks fail for real and for flaky reasons, reviewers ask questions,
the base branch moves on. This skill takes one open pull request and works
it until it lands, or until it can say exactly what is in the way.

## The finish line

The session ends in one of two states, never a vague third:

1. **Merged**, or armed to merge itself the moment checks pass.
2. **Blocked, with a diagnosis:** the named check, the log line that shows
   the failure, and the smallest action that would unblock it. "CI is red"
   is not a diagnosis; "the type check fails at `src/Orders.php:42` on a
   type introduced in this pull request" is.

Pull requests into a protected branch (commonly `main`) are merged by a
human unless the user says otherwise. For those, the finish line is "green,
conflict-free, approved and ready", reported, with no merge armed.

## 1. Get the situation report

```bash
gh pr view <n> --json state,mergeable,mergeStateStatus,reviewDecision,baseRefName,statusCheckRollup
gh pr checks <n>
```

`mergeable` only covers text conflicts. `mergeStateStatus` (`BLOCKED`,
`BEHIND`, `UNSTABLE`, `CLEAN`) is what says whether the merge can happen.

Done when: you can list every failing or pending check, every unanswered
review comment, and whether the branch is behind its base.

## 2. Diagnose failures before retrying

Read the failure before touching anything:

```bash
gh run view <run-id> --log-failed
```

Retry only what looks environmental: timeouts, a lost runner, network
errors, a different error each time. Retry just the failed jobs with
`gh run rerun <run-id> --failed`. When the same error appears on two runs,
it is not flaky: fix the code.

Change what a test expects only when the behaviour was meant to change.
Loosening an expectation to go green is overriding the check by another
route.

Done when: every failing check is labelled "flaky, retried" or "real, fixed
in <commit>", with the log line that justified the label.

## 3. Answer reviews

Only act on comments newer than the latest push; older ones are usually
dealt with. Sort each remaining comment:

- **One obvious answer** (a rename, a missing guard, a typo): make the
  change and quote the comment in the commit message.
- **A judgement call, or unclear:** reply with what you would do and why,
  and put the question to the user rather than guessing.

Automated review findings are checked against the code before acting; many
are wrong. Fix the real ones. Dismiss false positives with a one-line
reason. Anything about security or data loss goes to the user.

Keep the pull request to its original goal. Decline requests that would
grow it, politely, in a reply.

Done when: every newer comment has a change, a reply, or a question to the
user.

## 4. Keep it mergeable

If the branch is behind, update it (`gh pr update-branch <n>`, or merge the
base in). Resolve conflicts so both sides' behaviour survives, and leave a
short comment saying what conflicted and how it was settled. Regenerate
lockfiles rather than editing them. Never force-push a branch someone else
owns.

Done when: `mergeStateStatus` is no longer `BEHIND` or `DIRTY`.

## 5. Loop, with a limit

One round is: fix, push, wait, recheck. Wait sensibly between checks (a
minute or more; longer for slow pipelines) and tell the user what you are
waiting for. After three rounds that still end red, stop and report state 2.
A fourth attempt at the same failure means the diagnosis is wrong.

When everything is green and approved, arm auto-merge if the repository
allows it and the base is not protected:

```bash
gh repo view --json autoMergeAllowed
gh pr merge <n> --auto --squash   # or the repository's usual method
```

Done when: the pull request is merged or armed, or the three-round limit
was reached and reported.

## 6. Report

Final state; what was retried and why; each fix with its commit; comments
answered, deferred (with reasons) or escalated; conflicts resolved; and, if
blocked, the exact blocker and the smallest next step.

## Gotchas

- A pending check also makes `gh pr checks` return a failing exit code,
  so judge by what it prints.
- `gh run rerun` without `--failed` reruns the whole workflow.
- `gh pr merge --auto` does nothing if auto-merge is switched off for the
  repository; check first.
- Never use an admin override to merge past a required check.
- If the pull request becomes obsolete (the base already contains the
  change), stop and ask before closing anything.

## It's working if

- Every session ends merged, armed, or with a blocker precise enough to act
  on.
- No check was retried more than once without reading its log.
- Reviewers get replies, not silence while CI is polled.
