---
name: spike
description: >-
  Investigates an open technical question within a fixed scope and returns a
  go, no-go or go-with-conditions recommendation backed by evidence from the
  codebase, documentation and a small experiment where needed. Use when the
  user asks whether something is feasible, wants to investigate or spike on
  an approach, compare options, or asks "can we use X for this?".
license: MIT
allowed-tools: Read Grep Glob Bash WebSearch WebFetch Write
---

# Spike

A spike buys certainty before a team commits. The output is a decision,
not a tour of the topic: go, no-go, or go with conditions, with the
evidence that led there. Research that changes no decision is not worth
doing, so the first step is making sure the question is real.

Once the answer is in, argue for the direction with `pitch` (if
installed) and size the work with `t-shirt` (if installed).

## 1. Frame the question

A spike question has three parts:

- **The question:** what we need to learn. "Can full-text search on the
  product catalogue run under 100 ms with our current database?" is a
  spike; "look into search" is a topic.
- **The constraints:** budget, deadline, team skills, current stack,
  performance or compliance targets.
- **The decision it feeds:** what we will do differently depending on the
  answer. If nothing would change, say so and stop.

Sharpen a vague request with the user before going further.

Done when: the three parts are written down and the user agrees with them.

## 2. Set the scope

| Scope | When |
|---|---|
| Narrow | One approach, tested against this codebase |
| Comparative | Two or three options side by side |
| Exploratory | New territory for the team; aims to map it, not master it |

State the scope and what "enough evidence" looks like, so the spike ends
when it has answered the question rather than when interest runs out.

Done when: scope and stopping point are stated.

## 3. Gather evidence, most reliable first

1. **This codebase:** how the area works today, the patterns in use, where
   new code would connect, anything that would conflict.
2. **Prior attempts:** abandoned branches, reverted commits, old issues on
   the same idea (`git log --all --grep`).
3. **Primary documentation:** official docs and changelogs for anything
   being evaluated. Check version compatibility, licence and how actively
   it is maintained.
4. **A small experiment**, when documentation cannot settle it: the
   smallest throwaway code that answers the riskiest assumption. Keep it
   out of the main branch and say it is throwaway.

Mark every claim with where it came from. Separate what you verified from
what you assumed.

Done when: each option has evidence for fit, effort and risk, with
sources.

## 4. Weigh each option

For each option, answer:

- **Fit:** how it connects to what exists; what it changes; what new moving
  parts it adds to run in production.
- **Effort:** a rough size (S, M, L, XL) and the parts most likely to run
  over.
- **Gain:** specific and measurable where possible ("search under 100 ms on
  500,000 products", not "faster search").
- **Cost:** new dependencies, complexity, learning, ongoing upkeep.
- **Cheaper path:** whether most of the gain is available for much less
  work.

Done when: every option has all five answered, or says why one cannot be.

## 5. Write the report

Save it where the project keeps such documents (ask, or use
`docs/spikes/`):

```markdown
# Spike: <title>
Date: <date> · Scope: <narrow|comparative|exploratory>
**Question:** <framed question>
**Verdict:** go | no-go | go with conditions: <conditions>

## Why
<three to five sentences a decision-maker can read alone>

## Options
| Option | Fit | Effort | Gain | Cost | Cheaper path |
|---|---|---|---|---|---|

## Evidence
<findings with sources; verified and assumed marked separately>

## Risks and open questions
## If we go: first steps
```

Done when: the report exists and its verdict follows from its evidence.

## It's working if

- The verdict is stated in the first lines, not left for the reader to
  infer.
- A reader can tell verified facts from assumptions.
- The spike stopped once the question was answered.
