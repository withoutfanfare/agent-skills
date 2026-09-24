---
name: triage
description: >-
  Turns a raw bug report (a complaint, a stack trace, a support ticket, a
  screenshot description) into a triage assessment: a one-line summary,
  the affected area in the code, severity and priority with reasons, ranked
  likely causes and the next step. Use when the user asks to triage a bug,
  asks how serious an issue is, or pastes a bug report or error to assess.
  Not for tracking down and fixing the cause; use `sleuth`.
license: MIT
allowed-tools: Read Grep Glob Bash
---

# Triage

A bug report arrives, and someone must decide: drop everything, schedule
it, or add it to the backlog. That decision needs judgement about impact
and a quick look at the code, not a full investigation. This skill is the
intake step: minutes, not hours, and it ends with a clear call and a next
step. To reproduce and fix the bug afterwards, use `sleuth` (if installed).

## 1. Restate the report

Pull out the facts from whatever arrived: what the person was trying to
do, what went wrong (with the exact error), when it started, who and how
many are affected, and whether there is a workaround. Note what is missing
rather than refusing to go on; real reports are rarely complete.

Write the bug as one clear sentence.

Done when: the one-sentence summary exists and missing facts are listed.

## 2. Find where it lives

Search the code for the error text, route, screen or feature names in the
report. Name the area as the business sees it and as the code has it:
"Billing › invoice PDF export, `src/Invoices/PdfExporter.php`". The area
decides who picks it up.

Done when: the likely area and files are named.

## 3. Judge severity by impact

| Severity | Means |
|---|---|
| blocker | must be fixed before anything else: data loss or exposure, money affected, or a core feature down for everyone |
| major | should be fixed; a real problem: an important feature broken without a workaround, or many users affected |
| minor | worth fixing, low risk: degraded but usable, a workaround exists, few users affected, or a rare edge case |

Weigh how many are affected (one user, one account, everyone), whether
data is at risk or only its display, whether there is a workaround, and
whether it is getting worse.

Done when: severity is set with a one-line reason tied to these factors.

## 4. Set priority

Priority is when to act, which is severity adjusted for context:

| Priority | Act |
|---|---|
| Now | stop other work |
| Next | in the next cycle |
| Later | backlog |

A minor bug hitting the biggest customer before a renewal may be "now";
a major bug in a feature nobody uses may be "next".

Done when: priority is set, with the context that moved it, if any.

## 5. Rank likely causes

From the code you looked at and the report's clues, list two or three
likely causes, most likely first, each with the evidence for it and what
would confirm or rule it out. Say plainly that these are hypotheses.

Done when: each cause has evidence and a confirming check.

## 6. Report

```markdown
## Triage: <one-line summary>
**Severity:** <blocker|major|minor>, <reason> · **Priority:** <now|next|later>, <reason>
**Area:** <business area>, <files>
**Affected:** <who, how many> · **Workaround:** <yes: how | no>

### Likely causes
1. <cause>: evidence · check to confirm
2. ...

### Missing information
### Next step
<one action: investigate X, ask the reporter for Y, hotfix Z>
```

Done when: every heading in the template is filled, and the next step is a
single action.

## It's working if

- The severity call can be defended from impact, not from how loud the
  report was.
- The next step is one concrete action.
- It took minutes; the deep investigation is left for later (`sleuth`).
