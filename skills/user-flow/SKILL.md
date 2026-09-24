---
name: user-flow
description: >-
  Maps a user flow end to end, checks it against the surrounding information
  architecture, and turns it into testable acceptance criteria and a short
  usability plan. Use when shaping a new feature, asking "what should this
  screen do", mapping a journey, writing acceptance criteria for a journey
  or screen flow, or reviewing
  navigation and page structure for usability problems.
license: MIT
allowed-tools: Read Grep Glob Write Edit
---

# User flow

A feature request describes an outcome, not the screens that get someone
there. Without a mapped flow, edge cases get discovered in review, the
empty and error states are an afterthought, and acceptance criteria end up
too vague to test against. This skill turns a feature idea into a flow,
places it in the wider navigation, and writes down what "working" means in
a form a reviewer or a test can check.

## 1. Name the goal and the starting points

Write one sentence: who is doing this, and what are they trying to achieve.
Then list every place they might start from: a first visit, a link from an
email or search result, a return visit already signed in, a deep link into
the middle of the flow. A flow designed only for the tidiest starting point
breaks for everyone else.

Done when: the goal is one sentence, and every realistic entry point is
listed, not just the main one.

## 2. Map the steps

Walk the flow one screen or state at a time. For each step, capture what
the person sees, the action they take, and how the system responds. A
short table keeps this checkable:

```markdown
| Step | Screen | Action | System response |
|---|---|---|---|
| 1 | Product page | Selects size, taps "Add to basket" | Basket updates, confirmation shown |
| 2 | Basket | Taps "Checkout" | Guest/sign-in choice shown |
| 3 | Checkout | Fills address, submits | Order validated and placed |
```

Mark every branch point (a choice, a validation failure, a fork by user
type) rather than only the happy path. A flow with no branches has not
been looked at closely enough.

Done when: the table covers every step from the entry points in step 1 to
the goal, with branches marked.

## 3. Put the deciding information next to the decision

At each step, name the decision the person is making ("is this the right
item", "can I afford it", "am I about to pay the right amount") and check
that the information needed for it sits beside the control, not elsewhere
on the page or a scroll away. A price shown below the "buy" button, or a
total that only appears on the next screen, is a flow that looks complete
on paper and fails in use.

Done when: each decision point in the table has its supporting information
named and located.

## 4. Cover the states a happy-path flow skips

For each step, check what happens in these cases, and add any that apply
to the table:

- first-time use, with no existing data;
- an empty result (nothing found, nothing in the basket);
- a validation, permission or network error;
- a slow or loading state;
- the content at its most extreme: the longest title, the largest number,
  the fullest list, not just the sample data used to design it.

Skip a case only when it genuinely cannot happen, and say why, rather than
leaving it out silently.

Done when: every step has a stated first-time, empty, error and extreme
case, or a reason it does not apply.

## 5. Check the flow against the surrounding structure

List the pages or screens the flow touches, their parent in the
navigation, and their purpose, so the flow's place in the wider site or
app is visible:

```markdown
| Page | Parent | Purpose |
|---|---|---|
| Basket | Header nav | Review items before checkout |
| Checkout | Basket | Collect payment and delivery details |
```

Check that someone can reach the start of the flow from normal navigation
(not only from a link you happen to be testing), and that leaving the flow
partway through does not strand them somewhere with no way back.

Done when: every page in the flow has a named parent and a stated purpose.

## 6. Write acceptance criteria

Turn the mapped flow into criteria that state a trigger and an outcome, so
each one can be checked against a running feature rather than argued
about:

```gherkin
Scenario: Returning customer reorders a saved item
  Given a signed-in customer with a previous order
  When they choose "buy again" from order history
  Then the item is added to their basket at the current price
  And they see a confirmation naming the item
```

Write one scenario per branch identified in step 2, including at least one
failure or edge case, not only the happy path.

Done when: every branch and every case from step 4 has a matching scenario.

## 7. Set a usability check

Name two or three tasks a real person could attempt against the finished
flow ("find and reorder a past purchase", "recover from a declined card"),
and a plain pass mark for each (completed without help, completed but
confused, gave up). This is what turns the flow from a document into
something you can watch someone use.

Done when: each task has a pass mark, and neither requires explaining the
design to the person doing it.

## It's working if

- Someone unfamiliar with the feature can follow the table and reach the
  goal without asking what happens next.
- Every acceptance scenario traces to a step or branch in the mapped flow.
- The first usability session finds problems in an empty state or an
  error path, not just the happy path, because those were already written
  down to check.
