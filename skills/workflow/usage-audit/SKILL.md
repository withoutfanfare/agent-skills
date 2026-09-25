---
name: usage-audit
description: Reviews which library skills are actually used and recommends what to keep, reword, make typed-only, merge or retire.
license: MIT
disable-model-invocation: true
argument-hint: "optional: window in days (default 90)"
effort: low
allowed-tools: Read Grep Glob Bash
---

# Usage audit

Every skill the agent can start by itself costs a little attention in every
session, and a large library gets harder to choose from. Usage data turns
"I think nobody uses that" into evidence. This skill reads the local usage
log, lines it up against the library, and proposes changes. It changes
nothing itself; the owner decides.

## 1. Get the data

```bash
agent-skills usage 90 --json
```

The window defaults to 90 days; use the one the user gave. If the log is
empty, tracking may be off: point to `agent-skills track` and stop. Note
that the log covers one person on one machine; say so when drawing
conclusions for a team.

The log records that a skill started, not how. It cannot tell a start the
user asked for by name from one the agent chose, and a skill typed as a
slash command may not reach the log at all, so treat a typed-only skill's
count as a floor. Say this beside any recommendation that leans on it.

Done when: you have uses, projects and last-used dates per skill, and the
list of unused library skills.

## 2. Allow for age

A skill added last week with no uses tells you nothing. For each unused or
rarely used skill, find when it was added:

```bash
git log --diff-filter=A --format=%as -- 'skills/*/<name>/SKILL.md' | tail -1
```

Leave out anything younger than half the window.

Done when: every candidate has an age, and young skills are set aside.

## 3. Sort into recommendations

Each recommendation carries its numbers (uses, projects, last used, age):

- **Keep:** used regularly, across projects. Note any that have not been
  improved in a long time despite heavy use.
- **Reword the description:** a skill the agent may start itself, used
  rarely or never, although its job clearly comes up. Suggest the phrases
  people use.
- **Make typed-only:** a skill the agent may start itself that is rarely used.
  Typed-only skills cost nothing until called.
- **Let the agent start it:** a typed-only skill used so often that typing it
  is friction.
- **Merge:** two skills that do the same job and often start in the same
  session. The report has no session data: read the raw log (its path is
  the `log` field in the JSON; one line per start, with a `session` field)
  and group the lines by session.
- **Retire:** unused across the whole window, old enough to judge, and not
  a deliberate rare ritual (a yearly task that shows zero uses is fine, and
  should be said to be fine).

Done when: every library skill is in exactly one group, or explicitly
"no change".

## 4. Report, then stop

```markdown
# Usage audit: last <n> days
Data: <uses in total>, <n> skills used, <n> unused (<n> too new to judge)

## Recommendations
| Skill | Action | Evidence | Reason |

## No change
<skills and why>
```

Changing a description, flipping to typed-only (add
`disable-model-invocation: true` and the matching `agents/openai.yaml`),
merging or retiring a skill is for the owner to approve, then do as normal
changes with the linter and catalogue run afterwards.

Done when: every recommendation has evidence, and nothing was changed
without the owner's approval.

## It's working if

- Every recommendation has numbers beside it.
- New and deliberately rare skills are excused, not swept into "retire".
- The report ends with decisions for a person, not with changes made.
