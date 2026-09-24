---
name: access-audit
description: >-
  Audits a web page, component or design for accessibility against WCAG 2.2,
  covering keyboard operation, semantic structure, ARIA correctness, colour
  contrast and screen reader behaviour, and reports findings by severity with
  a concrete fix for each. Use for "check this page for accessibility
  issues", "is this accessible", "a11y review", "WCAG check", or before
  shipping a form or a custom widget such as a modal or dropdown.
license: MIT
allowed-tools: Read Grep Glob Bash
---

# Access audit

Accessibility bugs rarely show up in a normal click-through: the page looks
fine and works fine with a mouse. They show up when someone drives it with a
keyboard only, or with a screen reader reading the markup aloud, and by then
the cost of fixing them is much higher. This skill finds those bugs before
that happens, ties each one to the specific rule it breaks, and hands over a
fix rather than just a complaint.

## 1. Work out what you're looking at and what evidence you can get

An audit of a live page, a component's source, or a static design mock each
need a different starting point. A live page lets you check real behaviour:
tab order, focus, what gets announced. Source alone lets you read the
markup and infer behaviour without running it. A design file only shows
colour, spacing and text, so contrast and content checks carry the weight
and interaction checks get flagged as unknown until there's a build to test.

Where an automated scanner (such as axe) is available against a running
page, run it first. It catches missing labels and some contrast failures
quickly, but it typically finds a minority of real issues, so treat a clean
scan as a starting point, not a result.

Done when: you know which of live behaviour, source and visuals you can
check, and you have used whichever automated tooling is available.

## 2. Decide where to look first

Don't run a fixed checklist top to bottom. Let the interface tell you
where the risk is: a screen built around a form needs labels, validation
and error handling checked first; a content or marketing page needs
headings, landmarks and image text checked first; anything with custom
interactive behaviour (a modal, a tab set, a menu, an autocomplete) needs
its keyboard handling and ARIA state checked first, because that's where
custom widgets diverge from what assistive technology expects.

Done when: you can say which part of the interface carries the highest risk
and why, before reading the rest.

## 3. Check the four things that must always be covered

Whatever order you worked in, confirm all four before calling the audit
finished:

- **Reachable and operable by keyboard alone.** Every interactive element
  can be reached with Tab, activated the way its type expects (Enter or
  Space for a button, arrow keys inside a composite widget), and nothing
  traps focus so it can't move on. Focus order should follow the order a
  sighted user reads the page in, and the currently focused element should
  be visibly obvious.
- **Every control has a name a screen reader can announce**, and every
  piece of custom-built UI exposes the role, state and value a native
  equivalent would give it for free (a div styled as a checkbox still needs
  to say "checkbox, checked" or "unchecked").
- **Colour and content don't rely on colour alone.** Text against its
  background, and any control's border or icon against its surroundings,
  meets the minimum contrast ratios, and meaning (an error,
  a required field, a status) is also carried by text or an icon, not just
  a colour change.
- **Changes that happen without a page reload are announced.** A validation
  error, a save confirmation, a spinner starting or stopping: if it isn't
  wrapped in something a screen reader watches, a non-visual user never
  learns it happened.

The full pattern library, worked markup examples, the contrast table and
the three AA criteria WCAG 2.2 added (focus not hidden, target size,
accessible sign-in) are in [references/patterns.md](references/patterns.md);
use it for the detail once you know which areas need closer inspection.

Done when: each of the four areas has been actively checked, not assumed,
for the part of the interface under audit.

## 4. Flag what you can't verify instead of guessing

Some calls need information the available evidence doesn't give you:
whether an image is decorative or informative, whether a click handler on a
div is also wired to a key event, whether a gradient background pushes
contrast under the limit at some point but not others. Record these as
open questions with the specific thing that would resolve them, rather than
marking a pass or a fail you can't back up.

Done when: every uncertain finding names the exact check that would settle
it.

## 5. Rate and report

Grade each finding:

| Severity | Meaning |
|---|---|
| blocking | stops a keyboard or screen reader user completing the task |
| serious | usable with real difficulty, or wrong information is announced |
| moderate | an inconvenience or a smaller standard not met |
| cosmetic | technically non-compliant but no real effect on use |

```markdown
## Accessibility audit: <what was audited>

| # | Severity | Area | Location | Issue | WCAG | Fix |
|---|---|---|---|---|---|---|
| 1 | blocking | keyboard | header nav | menu only opens on hover | 2.1.1 | add click/Enter handler, keep focus inside while open |

### Needs manual verification
- <question that couldn't be settled from the available evidence>
```

Order the table by severity so the reader hits the blockers first, and give
the fix as an instruction, not just a description of the problem.

Done when: every finding in the table has a severity, a location and a fix,
and open questions are listed separately from confirmed findings.

## It's working if

- A blocking finding always names the specific interaction that fails and
  who it fails for.
- Every fix in the report is something a developer could act on without
  asking a follow-up question.
- Findings that couldn't be confirmed are visibly separate from the ones
  that were.
