---
name: deepen
description: Finds shallow modules in a codebase and designs deeper interfaces for the one you pick.
license: MIT
disable-model-invocation: true
---

# Deepen

A deep module does a lot behind a small interface: callers use it without
knowing how it works. A shallow one makes callers understand nearly as much
as it does, so one idea ends up scattered over many thin files. Shallow
code slows people down, and it slows agents down more, because every change
means reading five files to understand one concept.

This skill finds the shallow places, lets you choose one, and designs
several genuinely different deeper interfaces for it. It does not refactor;
it ends with a proposal ready to implement.

*The deep-module idea comes from John Ousterhout's "A Philosophy of
Software Design". The shape of this skill was inspired by Matt Pocock's
architecture-improvement skill.*

## 1. Explore like a newcomer

Pick a real task someone might do in this codebase and follow it: read the
entry point, follow imports and calls, read the tests. Note where
understanding stalls. Signs of shallowness:

- **Scattered concept:** one idea (an order's status, a user's plan) spread
  over many small files with no single home.
- **Pass-through layers:** functions that only forward their arguments.
- **Leaky interface:** callers must know internal details, or call things
  in a particular order, to use a module correctly.
- **Split for testing only:** logic pulled into tiny pure functions for
  easy unit tests, while the real bugs live in how they are wired together.
- **Coupled neighbours:** modules that look separate but always change
  together.

Done when: you have at least three candidate areas, each with a file-level
example of the problem.

## 2. Present candidates, then wait

For each candidate, give: the modules involved, where the pain shows (a
concrete example), a one-line sketch of what "deeper" would look like, and
a risk and impact rating (low, medium, high). Recommend the best
impact-to-risk ratio.

Then stop and let the user choose. Which module to deepen is a matter of
taste and priorities, not something to decide alone.

Done when: the user has picked one candidate.

## 3. Design three different interfaces

Produce three designs that differ in kind, not in detail: for example, one
built around a single entry-point object, one around plain functions and
data, one around events or a pipeline. If you can run parallel helpers, give
each the brief in [references/design-brief.md](references/design-brief.md)
and one of the three directions; otherwise write them one after another
from the same brief.

Each design shows: the public interface (signatures only), what it hides,
how two or three real call sites would read, and what it makes harder.

Done when: three designs exist and each has at least one clear weakness
named.

## 4. Compare and recommend

Put the three side by side: size of interface, what callers must know, ease
of testing, migration effort, and what each gives up. Recommend one, or a
hybrid if parts combine well, and say why. Wait for the user to approve a
direction.

Done when: the user has approved a design.

## 5. Write the proposal

Save a refactoring proposal (or open an issue, if the user prefers) with:
current state and why it hurts; the approved interface; a migration path in
small steps that keeps everything working between them; files affected;
and how the tests will prove behaviour is unchanged.

Done when: the proposal is saved and linked for the user.

## It's working if

- The user chose the target; the skill never picked it alone.
- The three designs are different enough that choosing between them is a
  real decision.
- The proposal can be implemented step by step without a big-bang rewrite.
