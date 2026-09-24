---
name: which-skill
description: Maps your situation to the right skill in this library, and to what usually comes next.
license: MIT
disable-model-invocation: true
argument-hint: "what you are trying to do"
allowed-tools: Read Glob
---

# Which skill

Nobody remembers every skill. Describe the situation and this map
recommends a route: the skill to start with, and the ones that usually
follow. Skills marked *(typed)* only run when you ask for them by name
(`/name` in Claude Code, `$name` in Codex), so name them in the
recommendation; the rest can also start on their own when a request
matches.

## How to answer

1. Restate the situation in one line.
2. Find it in the routes below. If two fit, say which you would pick and
   why.
3. Recommend: the first skill, then the next one or two, and anything to
   avoid. Check the skills are linked in this project (`agent-skills
   status`); if not, give the `agent-skills add` command.

Done when: the user has one starting skill and knows what comes after it.

## Existing work: the front door

`work` takes an issue, pull request or release, works out where it really
stands, what gate comes next, and the one safe next step. Start here when
there is already a ticket.

## From idea to shipped

1. **Shape it.** `spike` to test feasibility; `sketch` when a question needs
   something to click; `t-shirt` for a rough size; `pitch` to argue a
   direction in writing; `adversary` to threat-model before building;
   `relocate` when production data has to move; `user-flow` for journeys and
   acceptance criteria.
2. **Check the plan.** `preflight` tests a plan's claims before anyone
   builds; `handover` packages a task for someone else.
3. **Build.** `scaffold` for a new feature slice, `schema` for tables,
   `api-design` for endpoints, plus the stack skills below. `cover` writes
   the tests.
4. **Prove it.** `prove-it` runs the change for real; `road-test` drives a
   browser through whole journeys; `test-plan` writes scripts for human
   testers.
5. **Review.** `review` answers "is this the right change?" and "is it
   built well?".
6. **Ship.** `raise` opens the pull request, `shepherd` sees it merged,
   `changelog` and `doc-sync` keep the record straight, `launchpad` sets up
   the pipeline.

## Something is wrong

`triage` first (how serious, where, what next) → `sleuth` to find and fix
the cause → `hindsight` for the post-mortem → `runbook` so the next person
knows what to do → `watchtower` so it is caught sooner.

Slowness: `hotspot`. Red test suite: `realign`. Herd sites on a Mac that
will not load: `herd-doctor`.

## Keeping the codebase healthy

`reshape` for one area, `sweep` for the same change across many files,
`deepen` *(typed)* to find shallow modules, `debt-log` to rank technical
debt, `upkeep` for dependencies, `harden` for a security audit,
`access-audit` for accessibility, `findable` for search visibility,
`upgrade` for framework versions, `tour` to understand what is there.

## Before a launch

`wargame` *(typed)* runs parallel audits into a plain-English risk brief;
follow with `harden`, `road-test` and `watchtower` on whatever it flags.

## Words for people

`plainify` rewrites for a chosen reader; `unpack` explains a concept in
layers; `bulletin` *(typed)* writes an update for leaders, the team or
clients; `weekly` *(typed)* writes the week's engineering report;
`copydesk` for marketing copy; `microcopy` for interface text;
`wait-what` when a reply did not land.

## Memory and continuity

`ledger` records decisions and revisits them; `takeaways` captures lessons
at the end of a session; `catch-up` briefs you after time away;
`handover` briefs someone taking over.

## Laravel and PHP

`sleuth`, `scaffold`, `schema`, `seed`, `upgrade`, `tenancy`, `flags`,
`scheduler`, `notify`, `mailroom`, `localise`, `livewire`, `filament`,
`alpine`, `api-design`, `prove-it`, `herd-doctor`.

## Front end and desktop

`vue`, `nuxt`, `tailwind`, `house-style` (write down the design system you
already have), `design-pack` *(typed)* (package it for a design tool),
`user-flow`, `access-audit`, `tauri`, `tidy-build`.

## Guard rails for risky sessions

`careful` *(typed)* refuses destructive commands; `freeze` *(typed)* limits
edits to agreed paths.

## Git and delivery chores

`untangle` for rebases, conflicts, cherry-picks and releases; `share-safe`
before sending anything outside; `wizard` for a script that walks a person
through steps only they can do.

## Looking after the library

`pick` *(typed)* links the right skills for the task in hand;
`project-setup` *(typed)* records a project's facts for every session;
`usage-audit` *(typed)* reviews which skills earn their place; `doc-tidy`
*(typed)* organises a docs folder; `which-skill` *(typed)* is this map.

## It's working if

- Every recommendation names a first skill and what follows it.
- Typed skills are named so the user knows to ask for them.
- The route fits the situation, not just a keyword in it.
