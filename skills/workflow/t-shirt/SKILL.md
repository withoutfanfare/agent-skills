---
name: t-shirt
description: >-
  Sizes a feature request as S, M, L or XL by reading the code it would
  touch: modules affected, system boundaries crossed, test coverage and
  known risks, with a confidence rating. Use when the user asks how big a
  feature is, wants an estimate or sizing, or asks whether something is a
  quick job.
license: MIT
allowed-tools: Read Grep Glob Bash
---

# T-shirt

An estimate made from a feature's description is a guess; one made from
the code it will touch is a forecast. This skill reads the affected code
before naming a size, and says how sure it is, because a confident "M" and
a hopeful "M" should not look the same.

## 1. Restate the request

Write what is being asked for in one or two sentences, including what is
out of scope. If the request is ambiguous enough to change the size, list
the questions and size the most likely reading.

Done when: the scope is written down and any size-changing ambiguity is
listed.

## 2. Find the code it touches

From the entry points (routes, commands, screens, jobs), follow the calls
and list the files and modules that would change. Read them; do not size
from file names. Look for an existing feature built the same way: a
well-worn pattern is the best predictor of effort.

Done when: there is a list of affected modules, each with what would change.

## 3. Count the boundaries

List every boundary the change crosses: front end and back end, service
and database, this system and an outside API, one team's code and
another's. Each boundary costs more than its line count suggests, because
both sides must change together.

Done when: boundaries are listed, or "none: contained in one module".

## 4. Check the safety net

For each affected module, look at its tests: thorough, happy path only, or
none. Low coverage does not make work harder, but it makes it riskier,
because breakage goes unnoticed.

Done when: each module has a coverage rating.

## 5. Size it

| Size | Typical shape |
|---|---|
| S | a few files in one module, an existing pattern, no new boundary |
| M | several files across two or three modules, perhaps one boundary, mostly familiar patterns |
| L | many modules, more than one boundary, something new to design |
| XL | deep changes across the system, several boundaries, real unknowns; consider splitting or a `spike` (if installed) first |

These are guides. Two files across a critical boundary can be an L; fifteen
files following a template can be an M.

Rate confidence: **certain** (read everything; should land within a third
either way), **likely** (some areas unclear; could be off by double), or
**possible** (key parts unseen or requirements vague; suggest a `spike`).

Done when: there is one size and one confidence, each with a reason.

## 6. Report

```markdown
## Sizing: <feature>
**Size:** <S|M|L|XL> · **Confidence:** <certain|likely|possible>
<one or two sentences on why>

**Touches:** <module: what changes>
**Boundaries:** <list or none>
**Tests in affected areas:** | Area | Coverage |
**Risks that could grow it:** <specific, from the code>
**Unknowns:** <what could not be assessed, and why>
```

Done when: every field in the template is filled, with "none" or a reason
where there is nothing to say.

## It's working if

- Every size is backed by named modules and boundaries, not adjectives.
- Confidence is honest: a possible rating comes with what would raise it.
- Risks point at real code, not general worries.
