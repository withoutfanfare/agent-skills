---
name: runbook
description: >-
  Writes an operational runbook for one failure scenario that works for a
  tired person at three in the morning: how to recognise it, a two-minute
  assessment, diagnosis as a decision tree, exact fix commands, how to
  confirm recovery and when to escalate. Use when the user asks to write a
  runbook or on-call guide, or to document what to do when a specific thing
  breaks.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Runbook

Docs explain how a system works. A post-mortem explains what went wrong.
A runbook says what to do right now, when the person who knows is on
holiday and whoever is on call is half awake. Its job is to replace
thinking under pressure with following steps, so every step is a command
or a check, not advice.

## 1. Pin down the scenario

One runbook, one scenario. Establish:

- **Trigger:** the exact alert name, error message, metric or report that
  means this runbook applies.
- **Reader:** on-call engineer, any developer, support?
- **Urgency:** minutes or hours.
- **Systems involved:** services, databases, queues, outside providers.
- **History:** past incidents and post-mortems for this scenario.

Done when: the trigger is specific enough that someone could tell whether
this runbook applies in under a minute.

## 2. Get the real commands

Find the actual configuration, log locations, dashboards, deploy and
rollback commands, queue and worker setup, and health checks. A runbook
with invented commands fails at exactly the wrong moment.

Done when: every command you will write has been checked to exist, and
read-only ones have been run where safe.

## 3. Write it

```markdown
# Runbook: <scenario>
Updated · Owner · Severity · Typical time to fix

## You are here because
<alert name, error text or symptom, exactly as it appears>

## First two minutes (read-only)
1. <check>: `<command or link>`: healthy looks like <x>
2. <how to size the impact: who and how many are affected>
**Escalate now if:** <conditions, then jump to Escalation>

## Diagnose
### Is it <cause A>?
Check: `<command>`. If <result>, go to Fix A. If not, continue.
### Is it <cause B>?
...

## Fix A: <cause>
1. `<command>` (safe to run twice: yes/no)
2. ...
**If this makes it worse:** <how to undo>

## Confirm recovery
<the exact checks that prove it is fixed, and for how long to watch>

## Escalation
<who, how to reach them, what to tell them, after how long>

## Afterwards
<log the incident, open a post-mortem if <condition>, update this runbook>
```

Rules for every step: exact commands, not prose; say what "good" output
looks like; mark anything destructive and say how to undo it; keep
read-only checks before any change.

Done when: every diagnosis branch ends in a fix or an escalation.

## 4. Test it

Walk through it against a staging system, or with the person who last
handled this scenario, and fix every step that needed interpreting.

Done when: someone other than the author has followed it without asking
a question.

## 5. Save it

Save it where on-call people look (ask, or use `docs/runbooks/`), and link
it from the alert that triggers it, if the alerting tool allows.

## It's working if

- The person on call reaches a fix or an escalation without improvising.
- Every command in it runs as written.
- The alert links straight to the runbook.
