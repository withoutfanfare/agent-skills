---
name: test-plan
description: >-
  Writes a manual QA test plan for a feature from its code and docs: user
  stories with exact steps and checkable expected results, edge cases, a
  regression checklist, accessibility and browser checks, and a sign-off
  section. Use when the user asks for a QA or test plan, test scripts for
  testers, or test documentation for a feature.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Test plan

A tester with a vague plan tests the happy path and signs it off. A tester
with a good plan knows the exact steps, the exact values to type and what
they should see, and has a list of the awkward cases to try. This skill
writes that plan from the code itself, so it matches what was
built.

For automated tests, use `write-tests`; to run a plan in a browser, `acceptance-test`
(if installed).

## 1. Learn the feature

Read the feature's docs, then its code: the screens and routes people
use, the data it reads and writes, the rules it enforces, the outside
services it calls, and the settings that change its behaviour. Check
existing tests for what is already covered.

Done when: you can list every role that uses the feature and every action
each role can take.

## 2. Write user stories with test steps

One story per meaningful action:

```markdown
### US-<FEATURE>-01: <title>
**As a** <role> **I want to** <action> **so that** <benefit>

**Before you start**
- <data or account needed, in a named state>

**Steps**
1. Go to **Settings › Team**.
2. Select **Invite person**.
3. Enter `sam@example.com` in **Email**, choose **Editor**.
4. Select **Send invitation**.

**Expected**
- A message reads "Invitation sent to sam@example.com".
- Sam appears in the list with status **Invited**.
- An email arrives at sam@example.com within a minute.

**Evidence:** screenshot of the list; the email.
**Reset:** remove Sam from **Team**.
```

Rules: one action per step; exact values to type; interface names in bold,
exactly as they appear; expected results that can be checked (a message, a
value, a redirect, an email), never "it works".

Done when: every role's actions from step 1 have a story.

## 3. Add edge cases

A table per story or area: empty and maximum inputs, invalid formats,
duplicates, permissions (signed out, wrong role, someone else's record),
back button and refresh mid-flow, slow or failed outside services, and
concurrent edits.

Done when: every rule found in the code has at least one case that tries to
break it.

## 4. Add the cross-cutting checks

- **Regression:** the existing features this one touches, as a checklist.
- **Accessibility:** keyboard-only use, screen reader labels, focus order,
  contrast, error announcements.
- **Browsers and devices:** the ones the project supports, including a
  phone-sized screen.
- **Performance and security** notes where relevant: expected response
  times, permission checks to confirm.
- **Bug report template** and a **sign-off** section with names and dates.

Done when: each section is filled or marked "not applicable" with a reason.

## 5. Save

Save it where the project keeps QA documents (ask, or use
`docs/<feature>/test-plan.md`), and report the path and a one-line summary
of what it covers.

Done when: the plan is saved and the user has its path and summary.

## It's working if

- A tester who has never seen the feature can run every story without
  asking a question.
- Every expected result is something you can see or check.
- The edge cases come from the code's actual rules, not a generic list.
