---
name: wargame
description: Runs parallel read-only audits of a project and turns them into a plain-English launch-risk brief.
license: MIT
disable-model-invocation: true
allowed-tools: Read Grep Glob Write
---

# Wargame

Reviews catch faults in code; a wargame looks for faults in the business,
which tend to hide where systems meet: where the payment provider meets fulfilment, where
the scheduler meets alerting, where the website meets search engines.
Several focused audits, run side by side and then checked against each
other, surface the risks a project half-knows about but has never written
down, ranked by how badly each would hurt, in words an owner can act on.

This is an assessment. No application code changes during a wargame.
For a security audit of the code itself, use `harden` (if installed).

## 1. Orient

Before any audits start, establish:

- **Stack and moving parts:** framework, queues, scheduler, outside
  services, where it runs.
- **What failure costs:** a shop loses orders and trust; a subscription
  product loses customers; an internal tool loses people's time.
- **Which areas to audit:** two to four. Technical and operations always;
  the money path if anything is bought, billed or invoiced; discoverability
  if a public site must be found. Swap in others when the project needs
  them (data integrity for a pipeline, tenant isolation for a shared
  platform). More than four dilutes each audit.
- **What is already known:** existing audits, open issues, project notes.
  Known problems go in the brief; do not spend audit time rediscovering
  them.

Done when: the areas are chosen and each has a one-line reason.

## 2. Fan out

Run one read-only audit per area at the same time, using the briefs in
[references/audit-briefs.md](references/audit-briefs.md), adapted to this
stack. If parallel helpers are not available, run the audits one after
another from the same briefs. Every audit must return, per item: what
exists (with file and line), what is missing, a severity (blocker: must
be fixed before launch; major: should be fixed, a real problem; minor:
worth fixing, low risk) and a timing (before launch, soon after, later).
Audits read code; they do not run the application.

Done when: every area has a structured report.

## 3. Cross-check before believing

Expect roughly one wrong claim per report. Compare the reports with each
other and with what you know. When one audit says a safeguard is missing
and another found it scheduled, read the code yourself and record the
verdict. Corrections go in the "in good shape" section so the next
wargame does not reopen them.

Done when: every conflict between reports has a verdict from the code.

## 4. Write the brief

Plain English throughout; explain any technical term the first time it
appears. Lead with the worst.

1. **The scenarios that would hurt:** three to six, each told as a short
   story with a name ("The order that vanished", "The quiet weekend"): what
   happens, who notices or does not, what it costs. A story gets acted on
   where a list of missing webhooks does not.
2. **Safety nets that are not connected:** things built but never wired in:
   services never called, emails nothing sends, alerts that go nowhere.
   Often the cheapest fixes.
3. **Known problems still waiting:** previously found issues that will bite
   on launch or deploy day.
4. **In good shape:** say it plainly. It earns trust for the bad news and
   records the cross-check corrections.
5. **Order of work:** this week, before launch, first fortnight after.
6. **What this cannot see:** findings come from reading code, not the live
   system. Name the ones that need checking against live configuration.

Deliver it in the conversation, and save it where the project keeps notes
if it has a place.

Done when: the brief follows this order and every scenario traces to
evidence.

## 5. Plan, on request

When the user asks for a plan from the brief: phase 0 protects what cannot
be recovered and starts by checking the audit against the live system;
then launch blockers, first weeks, soon, and "only if the business asks".
Each task has what, why it hurts, rough effort, and a "done when" that can
be observed (an alert fires, a restore succeeds), never "code written".

Done when: phase 0 comes first and every task has an observable done when.

## It's working if

- Severity is measured in business damage: an unrecoverable loss outranks
  any missing nicety, and a silent failure outranks a loud one.
- Every scenario is backed by file and line evidence.
- A non-technical owner can read the first page and know what to do this
  week.
