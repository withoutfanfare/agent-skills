---
name: takeaways
description: >-
  Captures what was learned in a work session before it is forgotten:
  surprises, misleading signals, what was harder than expected and why,
  decisions and their reasons, and gotchas, drawn out through a short
  conversation and saved where the team will find it. Use when the user
  asks to capture what was learned, save insights, write up lessons, or wrap
  up a session.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Takeaways

During real work you build a detailed picture of how the system
behaves: which documentation was wrong, which signal sent you the wrong
way, which approach failed and why. It evaporates when the session ends.
The most valuable parts are the ones nobody would think to write down
unprompted, so this skill asks.

For a production incident, run a blameless post-mortem with `post-mortem`
(if installed) instead.

## 1. Rebuild the session yourself first

Before asking anything, look at what happened: the commits and changed
files, errors hit and how they were resolved, and points where the approach
changed direction. Your questions should come from this, not from a
template.

Done when: you can name the two or three moments in the session most
likely to hold a lesson.

## 2. Ask one good question at a time

Open with a question specific to what happened:

> "The fix turned out to be in the queue configuration, not the job. What
> made us look at the job first?"

Then follow the answer. Areas worth drawing out, as they come up
naturally:

- **Surprises:** what did not behave as expected, and why.
- **Harder than expected:** where the estimate broke, and the cause.
- **Patterns:** approaches that worked and will work again here.
- **Do differently:** what you would do differently from the start.
- **Decisions:** what was chosen, what was rejected, and why.
- **Useful finds:** documentation, code paths or tools worth finding
  again.

Stop when answers start repeating. Three sharp lessons beat ten vague ones.

Done when: each lesson is specific enough to act on. "Be careful with
imports" is not; "the importer silently skips rows with a trailing comma"
is.

## 3. Write it up

```markdown
# <Topic>: what we learned (<date>)
## Context
<the task and the state of things, briefly>
## Lessons
<each one with enough context to help someone who was not there>
## Gotchas
<concrete traps, each with where it lives>
## Decisions
<choice, reason, alternatives rejected>
## References
<links and file paths>
```

Done when: someone who was not in the session could use every item.

## 4. Save it where it will be found

Ask where, or follow the project's habit: a `docs/notes/` or `docs/lessons/`
folder, the project's agent instructions file for rules every future
session should follow, a notes vault, or a memory tool if one is connected.
A gotcha that should change how future work is done belongs in the
instructions file as a short rule, as well as in the write-up.

Done when: the write-up is saved and the user knows where.

## It's working if

- Every lesson is concrete and names where it applies.
- Rules that should change future behaviour reached the place future
  sessions read.
- The capture took minutes, not an hour.
