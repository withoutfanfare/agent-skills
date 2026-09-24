---
name: watchtower
description: >-
  Designs monitoring before a feature or service ships: the few measures
  that reflect what users experience, targets for them, alerts that fire on
  real problems and reach the right person, and dashboards that answer "is
  it working?". Use when the user asks what to monitor, wants to set up
  monitoring or alerting, define SLOs, or cut down noisy alerts.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Watchtower

Teams usually discover their monitoring gaps during an incident: "we had
no alert for that". This skill designs monitoring up front by asking two
questions of every feature: how will we know it is working, and how will
we know when it breaks? The answer is a small set of measures users would
recognise, targets for each, and alerts nobody learns to ignore.

## 1. Understand what is being watched

Establish: the feature or service; the user journeys through it; what
matters most (being up, speed, correctness, freshness, cost); who will
look at the results; and what monitoring tools already exist. Read the
code for the journeys' entry points, outside calls and background jobs.

Done when: the key user journeys are listed, each with its entry point.

## 2. Choose the measures: service level indicators (SLIs)

For each journey, pick the few measures that match what a user feels:

| Question | Typical measure |
|---|---|
| Is it up? | share of requests that succeed |
| Is it fast enough? | response time at the 95th percentile |
| Is it right? | error rate by type; failed business checks |
| Is it keeping up? | queue depth, jobs per minute, time waiting |
| Is the data fresh? | age of the newest record, sync lag |

Skip measures nobody would act on.

Done when: each journey has two to four measures, and each can be computed
from data you have or can add.

## 3. Set targets: service level objectives (SLOs)

For each measure, a target and a window: "99.9% of checkout requests
succeed over 30 days"; "95% of searches return within 400 ms over 7 days".
Base targets on current performance where you have it, not on hope.

Done when: every measure has a target, a window and the data source.

## 4. Design alerts

Every alert answers "what is broken, and who acts?":

- **Alert on symptoms users feel**, not on causes: error rate over 1%,
  not CPU over 80%. Causes belong on dashboards.
- **Page a person only for urgent, actionable problems.** Everything else
  is a ticket or a daily summary.
- **Require duration**, so a single blip does not wake anyone: "for 5
  minutes".
- **Name the runbook** in every alert.
- **Check for silence**, not just noise: an alert when a job has not run,
  or a metric stops reporting.

Done when: each alert has a condition, a duration, a severity, a
destination and a runbook link or a note that one is needed.

## 5. Plan dashboards

One overview per service answering "is it working?" at a glance (the SLIs
against targets), and one diagnostic view per journey with the causes
(dependencies, resources, queue depths, recent deploys marked).

Done when: each dashboard has a named audience and question.

## 6. Write it up

```markdown
# Monitoring: <feature or service>
## Journeys
## Measures and targets
| Journey | Measure | Target | Window | Source |
## Alerts
| Alert | Condition | For | Severity | Goes to | Runbook |
## Dashboards
## What must be built
<instrumentation to add in the code, with where>
```

Done when: every journey has a measure, a target and an alert with a
runbook, and what must be built says where.

## It's working if

- Every alert, when it fires, has a clear action and owner.
- Users are not the first to notice a problem.
- Silent failures (a job that stopped) raise an alert, not just loud ones.
