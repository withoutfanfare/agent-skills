---
name: weekly-report
description: Writes the week's engineering progress report from git history, merged pull requests and the issue tracker.
license: MIT
disable-model-invocation: true
argument-hint: "optional: week number or date range"
allowed-tools: Read Grep Glob Bash Write
---

# Weekly

A weekly report should take minutes to produce and seconds to skim. Most
of it is already in git and the issue tracker; the work is gathering it,
grouping it by what it means, and saying the important thing first.

For an ad hoc update pitched to a particular audience, use `status-update` (if
installed).

## 1. Set the period

Default to the last full working week, Monday to Friday. Work out the ISO
week number for the title. Use the period the user gave, if any.

Done when: start date, end date and week number are known.

## 2. Gather

Run the gathering commands together. Give git the times as well as the
dates: a bare date means the current time of day on that date, which drops
part of the first and last day.

```bash
git log --since="<start> 00:00" --until="<end> 23:59:59" --no-merges --pretty=format:'%h|%an|%s'
git shortlog -sn --since="<start> 00:00" --until="<end> 23:59:59" --no-merges
git log --since="<start> 00:00" --until="<end> 23:59:59" --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20
gh pr list --state merged --search "merged:<start>..<end>" --limit 100 --json number,title,author,labels,mergedAt
```

Add the issue tracker if it is connected: items completed, items still in
progress, blocked items, and the current cycle's progress. Skip quietly if
not available.

Done when: you have the merged pull requests, commit counts, contributors
and tracker items for the period.

## 3. Group by meaning

Sort the work into: features, fixes, improvements, quality (tests,
tooling, docs), infrastructure, and technical debt. Merge related pull
requests into one line with their numbers. Leave out noise (formatting,
dependency bumps) unless it matters.

Done when: every merged pull request sits in exactly one group.

## 4. Write the report

```markdown
# Week <nn>: <Mon dd> to <Fri dd Month yyyy>

## Summary
- <two to four bullets: what shipped that matters, and the top risk>

## Numbers
Pull requests merged · commits · contributors

## Shipped
### <feature>
What it does for users, in one or two sentences. (#123, #127)

## Fixes and improvements
- <area>: <what changed> (#130)

## Quality
- <tests, tooling, docs>

## In progress and blocked
| Item | State | Owner | Blocker |

## Next week
- <the few things planned>
```

Past tense, plain words, specific numbers. Describe what changed for users
before how it was built.

Done when: every section is filled or removed, and each claim links a pull
request or tracker item.

## 5. Save

Save it where the project keeps reports (ask, or use
`docs/reports/week-<nn>.md`).

Done when: the report is saved and the user has its path.

## It's working if

- The summary alone tells a reader how the week went.
- Every item links to its pull request or tracker entry.
- It took minutes, because the data came from the tools, not from memory.
