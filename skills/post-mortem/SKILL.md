---
name: post-mortem
description: >-
  Runs a blameless post-mortem after a production incident: builds the
  timeline, traces the trigger back to root and contributing causes, and
  turns them into owned, checkable actions. Use when the user asks for a
  post-mortem, incident review or retrospective on an outage, or asks why an
  incident happened and how to stop it happening again.
license: MIT
effort: high
allowed-tools: Read Grep Glob Bash Write
---

# Hindsight

An incident is expensive tuition; a post-mortem is how you collect the
lesson. The aim is to change the system so the same failure cannot happen
the same way again. That only works if people speak freely, which is why
every finding is about systems, processes and tools, never about a person.

For lessons from an ordinary work session rather than an incident, use
`takeaways` (if installed).

## Blameless wording

| Instead of | Write |
|---|---|
| "The developer forgot validation" | "The endpoint had no input validation, and review did not catch it" |
| "On-call was slow" | "The alert threshold delayed detection by forty minutes" |
| "Nobody noticed the config change" | "The configuration change bypassed review" |

A person making a mistake is a symptom; the system letting it through is
the cause.

## 1. Gather the facts

Collect before concluding: alerts and their times, logs, deploys and
configuration changes in the window, messages from the incident channel,
support tickets, and what responders tried. Ask the people involved for
what they saw and did, including the dead ends.

Done when: you have timestamped evidence from detection to resolution.

## 2. Build the timeline

One table, in one time zone (say which), from the first relevant change to
confirmed recovery. Include dead ends: they show where tools and docs
failed the responders.

```markdown
| Time (UTC) | What happened |
|---|---|
| 14:02 | Release 2.3.1 deployed |
| 14:15 | First errors on the payment endpoint |
| 14:43 | Alert fires (threshold set to 5% for 20 minutes) |
```

Done when: the timeline explains every gap longer than a few minutes.

## 3. Find the causes

Separate three things:

- **Trigger:** what set it off (a deploy, a traffic spike, a provider
  change).
- **Root cause:** why the trigger could cause harm. Ask "why?" until the
  answer is a system property you can change, backing each answer with
  evidence rather than speculation.
- **Contributing factors:** what made it worse or slower to fix: slow
  detection, missing runbooks, confusing dashboards, risky deploy timing.

Also note what went well; it is worth keeping.

Done when: each cause is a factual statement with evidence, not a guess.

## 4. Decide the actions

Each action is specific, owned and checkable:

| Weak | Strong |
|---|---|
| Be more careful with deploys | Add a smoke test that calls the payment endpoint after each deploy, owner Sam, by 30 May |
| Improve monitoring | Alert when payment errors pass 1% for 5 minutes, routed to on-call |

Sort into: **prevent** (stop the root cause), **detect** (notice sooner),
**respond** (fix faster). One or two strong actions beat a long list
nobody finishes.

Done when: every root and contributing cause has at least one action with
an owner and a date, or an explicit decision to accept it.

## 5. Write it up

```markdown
# Post-mortem: <what happened>
Date · Severity: blocker|major|minor · Duration · Status: draft|final

## Summary
<four to six lines: user impact, how long, how many affected, how detected>

## Timeline
## Causes
Trigger · Root cause · Contributing factors
## What went well
## Actions
| Action | Type | Owner | Due | Tracking link |
## Lessons
```

Save it where the team keeps incident records (ask, or use
`docs/incidents/`), and link the actions to the issue tracker.

Done when: the post-mortem is saved and every action has an owner, a due
date and a tracking link.

## It's working if

- No sentence in the document blames a person.
- Every action has an owner, a date and a way to see it is done.
- The next similar incident is caught sooner or does not happen.
