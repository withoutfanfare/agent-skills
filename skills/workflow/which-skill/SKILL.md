---
name: which-skill
description: Maps the user's situation to the right skill in this library, and to what usually comes next.
license: MIT
disable-model-invocation: true
argument-hint: "what you are trying to do"
allowed-tools: Read Glob Bash
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
   avoid. Check the skills are linked, in this project (`agent-skills
   status`) or for every project (`agent-skills home status`); if not,
   give the `agent-skills add` command.

Done when: the user has one starting skill and knows what comes after it.

## Existing work: the front door

`work` takes an issue, pull request or release, works out where it
stands, what gate comes next, and the one safe next step. Start here when
there is already a ticket.

## From idea to shipped

1. **Shape it.** `spike` to test feasibility; `prototype` when a question needs
   something to click; `estimate` for a rough size; `proposal` to argue a
   direction in writing; `threat-model` to threat-model before building;
   `migrate-data` when production data has to move; `user-flow` for journeys and
   acceptance criteria.
2. **Check the plan.** `plan-review` tests a plan's claims before anyone
   builds.
3. **Build.** `scaffold` for a new feature slice, `schema` for tables,
   `api-design` for endpoints, plus the stack skills below. `write-tests` writes
   the tests.
4. **Prove it.** `prove-it` runs the change for real; `acceptance-test` drives a
   browser through whole journeys; `test-plan` writes scripts for human
   testers.
5. **Review.** `review` answers "is this the right change?" and "is it
   built well?".
6. **Ship.** `open-pr` opens the pull request, `land-pr` sees it merged,
   `changelog` and `doc-sync` keep the record straight, `pipeline` sets up
   the pipeline.

## Something is wrong

`triage` first (how serious, where, what next) → `debug` to find and fix
the cause → `post-mortem` for the post-mortem → `runbook` so the next person
knows what to do → `monitoring` so it is caught sooner.

Slowness: `speed-up`. Red test suite: `fix-tests`. Herd sites on a Mac that
will not load: `herd-doctor`.

## Keeping the codebase healthy

`refactor` for one area, `bulk-edit` for the same change across many files,
`deep-modules` *(typed)* to find shallow modules, `debt-log` to rank technical
debt, `dep-audit` for dependencies, `security-audit` for a security audit,
`access-audit` for accessibility, `seo` for search visibility,
`upgrade` for framework versions, `walkthrough` to understand what is there.

## Before a launch

`launch-risk` *(typed)* runs parallel audits into a plain-English risk brief;
follow with `security-audit`, `acceptance-test` and `monitoring` on whatever it flags.

## Words for people

`plainify` rewrites for a chosen reader; `explain` explains a concept in
layers; `status-update` *(typed)* writes an update for leaders, the team or
clients; `weekly-report` *(typed)* writes the week's engineering report;
`copywriter` for marketing copy; `microcopy` for interface text;
`re-explain` when a reply did not land.

## Memory and continuity

`decision-log` records decisions and revisits them; `takeaways` captures lessons
at the end of a session; `catch-up` briefs you after time away;
`continuity` pauses your own work in a dated snapshot and resumes it later,
in any tool; `handover` briefs someone else taking over.

## Laravel and PHP

`debug`, `scaffold`, `schema`, `seed`, `upgrade`, `tenancy`, `feature-flags`,
`scheduler`, `notify`, `mailable`, `localise`, `livewire`, `filament`,
`alpine`, `api-design`, `prove-it`, `herd-doctor`.

## Front end and desktop

`vue`, `nuxt`, `tailwind`, `style-guide` (write down the design system you
already have), `design-pack` *(typed)* (package it for a design tool),
`user-flow`, `access-audit`, `tauri`, `tidy-build`.

## Guard rails for risky sessions

`careful` *(typed)* refuses destructive commands; `freeze` *(typed)* limits
edits to agreed paths.

## Git and delivery chores

`git-guide` for rebases, conflicts, cherry-picks and releases; `secret-scan`
before sending anything outside; `wizard` for a script that walks a person
through steps only they can do.

## Looking after the library

`pick-skills` *(typed)* links the right skills for the task in hand;
`project-setup` *(typed)* records a project's facts for every session;
`usage-audit` *(typed)* reviews which skills earn their place;
`improve-skill` *(typed)* tests a skill with pass or fail checks and keeps
only the changes that raise its score; `instruction-audit` *(typed)* trims
an AGENTS.md or CLAUDE.md file to what the agent needs; `doc-tidy`
*(typed)* organises a docs folder; `which-skill` *(typed)* is this map.

## It's working if

- Every recommendation names a first skill and what follows it.
- Typed skills are named so the user knows to ask for them.
- The route fits the situation, not just a keyword in it.
