---
name: road-test
description: >-
  Runs browser-driven acceptance testing of a feature, journey or whole site
  until every scenario has a verdict, recording evidence and reporting each
  failure with severity, cause and a fix. Never changes code. Use when the
  user asks for UAT, acceptance testing, to test something end to end, or to
  walk through the site and find what is broken. Not for proving one change
  works; use `prove-it`.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Road test

Pick one target and keep going until each scenario on the list is
decided (passed, failed, blocked or needs a decision) and every
failure is written up with evidence. Failed logins, missing features and
broken pages do not end the run; they become findings. The run ends when
the list is complete, or when something needs a person, with the
reason stated.

This skill finds and diagnoses. It writes no application code during the
run; fixing mid-run spoils the coverage. To prove one change works with
the lightest evidence that will do, use `prove-it` (if installed).

## 1. Agree the contract

Before opening a browser:

1. **The target:** one journey, one page, one feature or the whole site.
   Break a vague request into candidate journeys and confirm them.
2. **The environment:** what the user named; otherwise a test config file
   if the project has one (for example `docs/uat/config.md`); otherwise
   local, from the app's configured URL or dev server. Local is the
   default; use staging only when asked.
3. **Production guard:** if the target looks like production (the live
   domain, a production environment flag, live payment keys), stop and get
   written confirmation before a single click.
4. **Accounts:** which roles are needed. Let the user sign in and hand over
   the tab where that is easier; never ask for passwords in chat.
5. **The report:** start `docs/uat/<date>-<target>.md` from
   [assets/report-template.md](assets/report-template.md) with the goal,
   environment, URL and commit.

Done when: target, environment and accounts are agreed and the report file
exists.

## 2. Learn what should happen

Read the routes, screens, components and tests for the target, and recent
commits (recent changes are where bugs are). Note anything already known
to be broken; it is not a new finding.

Done when: each journey has an expected outcome grounded in the code.

## 3. Build the scenario list

If a test plan exists (from `test-plan`, if installed), build the scenario
list from it.

Numbered scenarios in the report, each with steps, expected result and
priority, in this order:

1. Journeys that must work.
2. Error and edge paths: bad input, empty states, expired or missing
   records, back and refresh mid-flow, permission boundaries.
3. Sweeps: console errors, failed network requests, broken images, a
   phone-width viewport, dead links, page titles.

[references/scenarios.md](references/scenarios.md) lists standard journeys
by application type. Show the list to the user to trim before running.

Done when: the user has approved the list.

## 4. Preflight

Most local "bugs" are the environment. Check: the site responds; the
environment is the one expected; queue workers and the scheduler are
running if the flow needs them; front-end assets are current; outside
services are in test mode. On a remote, also check it is not production
and that search engines are blocked if pre-launch. Record the result.

Done when: preflight passes, or the failure is fixed (locally) or reported
(remotely) before any scenario runs.

## 5. Run each scenario

Use whichever browser automation tools this environment provides. For each
scenario: perform the steps as a user would; look at what rendered (page
text or a screenshot); check console errors and failed requests; on a
failure, save a screenshot and repeat once to confirm.

**Write the verdict into the report before starting the next scenario.**
The file on disk is the state, so an interrupted run loses nothing.

Rules that keep verdicts honest:

- A pass requires seeing it. A redirect to the right address is not proof
  the action worked; check the page content.
- Blocked is a valid verdict: record what is needed and carry on.
- When the intended behaviour is missing or contradictory, record "needs a
  decision" with the question, not a failure.
- Use identifiable test data (`uat+<date>@example.com`), and stop to ask
  before anything irreversible or outward-facing: real payments, emails to
  real people, deletions.
- Avoid actions that open native browser dialogs; they can freeze
  automation.
- On a remote, change nothing outside the app's own interface; see
  [references/remote-safety.md](references/remote-safety.md).

Done when: every scenario has a verdict in the report.

## 6. Triage the failures

For each failure: severity, cause class and the smallest proposed fix,
traced to a file and line in the local code where possible. Rubric and
evidence rules: [references/triage.md](references/triage.md). Blocker,
major and minor mean what they mean in every other skill; polish is a
fourth, lowest level used only here.

Done when: every failure has all the evidence the triage guide requires.

## 7. Report and hand over

In the conversation: blockers first, counts of passed, failed, blocked and
needs-decision, and the report path. Also list every record created on a
remote so it can be cleaned up, and offer (without doing it unasked) to
raise the confirmed bugs in the tracker and to plan the fixes.

Done when: the user has the blockers, the counts, the report path and the
list of remote records to clean up.

## It's working if

- Every scenario has a verdict, and every failure has evidence that exists
  on disk.
- No verdict of "passed" was inferred rather than seen.
- The environment under test is exactly as it was, apart from ordinary
  test records that are listed for clean-up.
