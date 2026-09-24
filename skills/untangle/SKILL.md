---
name: untangle
description: >-
  Guides git decisions that are easy to get wrong: rebase or merge, resolving
  conflicts without losing either side, cherry-picks, and preparing releases
  and hotfixes. Use when the user hits a merge conflict, asks whether to
  rebase, wants to cherry-pick a fix, or needs to cut a release or hotfix
  branch.
license: MIT
allowed-tools: Bash Read Grep Glob
---

# Untangle

Git commands are easy to look up. What bites is choosing the wrong one: a
rebase on a branch someone else has pulled, a conflict resolved by quietly
dropping one side, a release "finished" by pushing straight to a protected
branch. This skill is about those choices.

## 1. Read the room first

Before changing history, find out where you are and who else is here:

```bash
git status
git branch -vv
git log --oneline --graph -15
```

Note which branches are protected in this repository (usually `main` or
`master`, sometimes `develop`), whether the current branch has been pushed,
and whether anyone else (another person, another worktree, another agent
session) may have it checked out.

Done when: you can say which branch you are on, whether it is shared, and
which branches only a human merges into.

## 2. Rebase or merge

| Situation | Choose |
|---|---|
| Your own branch, not yet pushed or shared | Rebase onto the base to stay current or tidy up before review |
| Your own branch, already pushed, nobody else on it | Rebase is possible, then `git push --force-with-lease`; merge is safer |
| Anyone else may have the branch | Merge. Never rewrite shared history |
| Bringing finished work into an integration branch | Merge with `--no-ff`, or the repository's pull request flow |

Never use plain `--force`. `--force-with-lease` refuses to overwrite pushes
you have not seen.

Done when: the choice matches the table, and history on shared branches is
untouched.

## 3. Resolve conflicts without losing anything

For each conflicted file, work out what each side was trying to do before
editing a line. The resolution keeps both behaviours. When the two sides
genuinely contradict each other, stop and ask rather than guess whose
intent wins.

Lockfiles (`package-lock.json`, `composer.lock`, `yarn.lock`, `Cargo.lock`)
are never merged by hand. Resolve the manifest, then regenerate the lockfile
with the package manager.

After resolving, run the tests that cover the conflicted files.

Done when: no conflict markers remain (`git diff --check`), the lockfile
was regenerated rather than edited, and the relevant tests pass.

## 4. Cherry-pick with care

A cherry-picked commit gets a new hash. If the source branch is merged
later, the same change arrives twice and can conflict with itself. Prefer
merging the source branch when that is an option. When cherry-picking is
right (a fix needed on a release branch now), use `git cherry-pick -x` so
the new commit records where it came from.

Done when: the picked commit carries its origin line, and you have noted
whether the source branch will be merged later.

## 5. Releases and hotfixes: stop at "ready"

1. Branch from the right base: releases from the integration branch,
   hotfixes from the production branch.
2. Make the release changes: version, changelog, fixes, green tests.
3. Push the branch and open a pull request.

Merging into a protected branch and pushing the release tag are for a
human, unless the user explicitly says otherwise for this repository. Report
exactly what remains: the merge, the tag, and `git push origin <tag>`.

Done when: the pull request exists and the remaining human steps are listed.

## Gotchas

- Adding a path to `.gitignore` does not untrack files already committed.
  Run `git rm --cached <path>` as well.
- `git push` does not push tags. Push them by name, or with `--tags`.
- `git reset --hard` discards uncommitted changes for good; committed work
  can be recovered from `git reflog`, uncommitted work cannot. Stash first.
- After a squash merge, `git branch -d` refuses to delete the feature
  branch because git cannot see the merge. Confirm the squash landed, then
  use `-D`.
- Renaming or deleting the source branch of an open pull request closes the
  pull request on most hosts, often for good.

## It's working if

- No shared branch ever had its history rewritten.
- Every resolved conflict can be explained as "kept A's behaviour and B's".
- Release work ends with a pull request and a clear list of human steps.
