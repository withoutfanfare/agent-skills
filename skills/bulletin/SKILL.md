---
name: bulletin
description: Writes a progress update pitched to its audience: leadership, the team, or clients and partners.
license: MIT
disable-model-invocation: true
argument-hint: "leadership | team | partners, optional period"
allowed-tools: Read Grep Glob Bash
---

# Bulletin

The same week of work reads differently to a director, a developer and a
client. Leaders want what needs a decision; the team wants what is blocked
and who is on it; clients want what is getting better and when. This
skill gathers the facts once and writes the version the reader needs.

For the fixed weekly engineering report built from git and the tracker,
use `weekly` (if installed). To rewrite one existing document for a reader,
use `plainify` (if installed); its executive reader is the leadership
audience here.

## 1. Pick the audience

| Audience | Tone | Detail | Leads with |
|---|---|---|---|
| Leadership | concise, decision-focused | high level | risks and decisions needed |
| Team | direct, technical where useful | granular | shipped, blocked, next, owners |
| Clients and partners | positive, plain | features, no internal debt | what is better and what is coming |

Use the audience the user named. If none, ask once; if still unclear, write
for leadership.

Done when: the audience is set.

## 2. Gather the facts

Use whichever of these the project has, for the period (default: the last
two weeks):

- the roadmap or plan documents, and any decision records;
- merged pull requests and notable commits;
- completed, in-progress and blocked items in the issue tracker, if
  connected;
- releases and their notes.

Note what could not be reached rather than filling gaps with guesses.

Done when: you have shipped, in-progress and blocked items, each traceable
to a source.

## 3. Write it

**Leadership** (one page at most):

```markdown
# Update: <period>
## Headline
<two sentences: overall state and the one thing that needs attention>
## Decisions needed
- <decision, options, recommendation, by when>
## Risks
- <risk, impact, what is being done>
## Progress
- <area>: <state in one line>
```

**Team:**

```markdown
# Team update: <period>
## Shipped
## In progress (owner, expected)
## Blocked (what on, who can unblock)
## Next up
```

**Clients and partners:**

```markdown
# What's new: <period>
## Improvements you can use now
## Coming soon (with honest timing)
## Thank you / how to give feedback
```

For clients: describe benefits, not implementation; leave out internal
debt, team issues and uncommitted dates.

Done when: the update fits its audience's template and every claim traces
to a source from step 2.

## 4. Check the tone

Read it as the recipient. Remove jargon for non-technical readers, and
make sure bad news is stated plainly, with what is being done about it.

## It's working if

- A leader finds the decisions they need to make in the first screen.
- The team can see exactly what is blocked and who can unblock it.
- A client reads only things they can use or look forward to.
