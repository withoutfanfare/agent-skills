---
name: raise
description: >-
  Opens one clear, reviewable pull request from the current branch, with a
  description that starts with the problem in plain words and ends with
  proof it works. Use when the user asks to open, raise, create or file a
  pull request, or to "put this up for review".
license: MIT
allowed-tools: Bash Read Grep Glob
---

# Raise

A pull request is a request for someone's attention. This skill makes that
attention cheap to give: the right base, nothing unrelated in the diff, and
a description that says why before it says what. It opens the pull request
and stops. Seeing it through checks and review is a separate job (see
`shepherd`, if installed).

## 1. Check nothing is already open

```bash
gh pr view --json url,state 2>/dev/null
```

If this branch already has an open pull request, update that one instead of
opening a second.

Done when: you know whether you are creating or updating.

## 2. Choose the base

Use, in order: a base the project documents (contributing guide, agent
instructions file, delivery notes); the integration branch if the project
has one (often `develop`); otherwise the repository default. When unsure,
see where recent pull requests went:

```bash
gh pr list --state merged --limit 5 --json baseRefName,title
```

Done when: the base is named and you can say where that choice came from.

## 3. Read the whole diff

Fetch first, so the comparison is with the base as it is on the remote,
not a stale local copy:

```bash
git fetch origin <base>
git diff origin/<base>...HEAD --stat
git diff origin/<base>...HEAD
```

The diff should do what the user set out to do and nothing else. If it
mixes unrelated work, say so and ask before going further. If it is too big
for anyone to review well, suggest splitting it rather than writing a
heroic description.

Done when: you have read every changed file, and the diff matches the goal.

## 4. Write the title

Follow the repository's commit style (check recent merged titles), because
a squash merge turns the title into the permanent commit message. Say what
changed for the user, not which files moved:

- Weak: `fix(checkout): refactor tax calculation in CheckoutService`
- Strong: `fix(checkout): stop tax being charged twice on repeat orders`

Done when: the title matches the house style and names the outcome.

## 5. Write the description

Four parts, in this order, so a reviewer gets the why before the how:

1. **Problem:** what was wrong or missing, in a sentence or two anyone on
   the team could follow.
2. **Fix:** what changes, and why this approach over the obvious
   alternative.
3. **Proof:** what you ran and what it showed. Paste the command and the
   output line that matters; add screenshots for anything visual.
4. **Where to look:** only for larger diffs. Point to the few files where
   the substance is, list generated or mechanical files
   separately, and call out any migration or behaviour change.

If the repository has a pull request template, fill its headings with this
content rather than replacing it. Describe the change itself; leave out how
it was produced.

Done when: someone who has not seen the branch could review it from the
description alone.

## 6. Open it

Push the branch if it is not on the remote yet, then open a ready pull
request (not a draft, so automated reviews run) unless the repository's own
flow uses drafts.

```bash
gh pr create --base <base> --title "<title>" --body-file - <<'EOF'
<description from step 5>
EOF
gh pr view --json url,title,baseRefName,headRefOid
```

Done when: the second command shows the pull request with the right base
and head commit, and you have given the user the link.

## Tidying commits (only when asked)

On a branch nobody else has pulled, commits can be regrouped so each reads
on its own: data first, then logic, then wiring, then interface, then
tests. The code must end up identical, so fingerprint it first:

```bash
before=$(git rev-parse 'HEAD^{tree}')
# ... regroup the commits ...
[ "$(git rev-parse 'HEAD^{tree}')" = "$before" ] && echo "code unchanged"
```

Push only after it prints `code unchanged`. If the branch was already on
the remote, the regrouped history needs `git push --force-with-lease`,
which refuses if anyone else pushed in the meantime.

Done when: the tree check prints `code unchanged` before anything is pushed.

## It's working if

- The reviewer's first question is about the approach, not "what is this
  for?"
- Every pull request has a proof section with a real command and result.
- There is never more than one open pull request for a branch.
