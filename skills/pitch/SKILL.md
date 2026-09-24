---
name: pitch
description: >-
  Writes a technical proposal (an RFC or design document) that argues for a
  change: the problem, the proposed approach grounded in the real codebase,
  honest alternatives including doing nothing, trade-offs, risks and open
  questions, ready for others to review in their own time. Use when the user
  wants to write an RFC, a design doc or a technical proposal, or needs team
  buy-in for an approach.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Pitch

Some decisions are too big for a chat thread and too technical for a
meeting. A written proposal lets people think before they react, and
leaves a record of why the choice was made. It is an argument, not a plan:
it makes the case for a direction the team has not yet agreed, and it
invites disagreement by being honest about the weaknesses.

Once a direction is agreed, turning it into work is a different job;
check the resulting plan with `preflight` (if installed). If it is not yet
known whether the approach can work at all, run a `spike` (if installed)
first, and size the work with `t-shirt` (if installed).

## 1. Pin down the proposal

Get these from the conversation, asking only for what is missing:

- **The change:** an approach, an architecture decision, a new tool, a
  process.
- **Why now:** what prompted it, and what happens if nothing changes.
- **Who must agree:** the people and teams affected.
- **Reversibility:** a cheap, reversible change deserves a short pitch; a
  permanent one deserves a thorough one.
- **Alternatives already considered**, even informally.

Done when: all five are known, or marked unknown with a reason.

## 2. Ground it in the code

Read the affected area: how it works today, the patterns it follows,
where the change would connect, the tests around it, any known problems
(`TODO`, `FIXME`, open issues). A proposal written from memory of the code
reads well and fails in review.

Done when: every claim the proposal makes about the current system can
point to a file.

## 3. Write it

```markdown
# Proposal: <title>
Author · Date · Status: draft · Reviewers · Decide by: <date>

## Summary
<two or three sentences; a busy reader should get the whole idea here>

## Problem
<what is wrong today, with evidence: incidents, numbers, code paths,
recurring pain. Make it convincing even to someone who will dislike the
solution.>

## Proposal
<the approach in enough detail to judge: what changes, key design points,
how it fits existing systems, how we get there from here>

## Alternatives
### <Alternative A>: what it is, what it does better, why not
### <Alternative B>: ...
### Do nothing: what happens, honestly. Sometimes this wins.

## Trade-offs
<what this proposal gives up>

## Risks and unknowns

## Open questions
<what reviewers should weigh in on>

## Rollout
<phases, how we know it worked, how we back out>
```

Treat alternatives fairly: name their real advantages. A proposal that
wins against straw men is not trusted.

Done when: every section is filled or deliberately marked "not
applicable" with a reason.

## 4. Pressure-test before sharing

Read it as its sharpest critic would. For each likely objection, check the
proposal answers it or lists it as an open question. Cut anything that
argues from preference rather than evidence.

Done when: the three strongest objections are addressed in the text.

## 5. Save and share

Save it where the team keeps proposals (ask, or use `docs/proposals/`), and
suggest who should review it and by when.

Done when: the proposal is saved, the path is given, and the reviewers and
a review date are named.

## It's working if

- A reviewer can disagree precisely, pointing at a named trade-off.
- "Do nothing" is a real option in the alternatives, not a formality.
- Statements about the current system are backed by the code.
