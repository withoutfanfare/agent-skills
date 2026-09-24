---
name: microcopy
description: >-
  Writes interface text in the product's locale, British English by default:
  buttons, labels, hints, error, success, empty and loading states,
  confirmations and notifications, clear, short and accessible. Use when the user asks for UI copy or microcopy,
  button text, error or success messages, empty states, or wants interface
  wording reviewed.
license: MIT
allowed-tools: Read Grep Glob Edit Write
---

# Microcopy

Interface text is read in a hurry, mid-task, often under stress. It works
when people do not notice it: the button says what will happen, the error
says how to fix it, the empty screen says what to do first. This skill
writes and reviews that text.

## 1. Read the screen in context

Open the view or component and understand the task: what the person is
trying to do, what just happened, and what they should do next. Read the
product's existing interface text for its conventions (sentence case,
tone, how it addresses the user).

Done when: you can describe the moment each piece of text appears in.

## 2. Write to the pattern

| Element | Pattern | Good | Weak |
|---|---|---|---|
| Button | verb + object | Save changes · Send invitation | Submit · OK |
| Error | what happened + how to fix it | Your password needs at least 12 characters. | Invalid input. |
| Success | what was done (+ detail) | Invitation sent to sam@example.com | Success! |
| Empty state | what is here + why + first action | No invoices yet. Your first one will appear after your first order. | No data. |
| Loading | the action in progress | Uploading 3 files… | Loading… |
| Destructive confirm | the consequence + a specific button | Delete this project and its 42 files? This cannot be undone. [Delete project] | Are you sure? [Yes] |
| Field hint | what to enter and why | We use this to send your receipts. | Enter email. |

Rules throughout: sentence case; the second person ("your"); no filler
("please", "simply", "just"); no blame ("you entered it wrong"); the
product's locale, British English unless the codebase or user says
otherwise; dates as 4 November 2026.

Done when: every string follows its element's pattern.

## 3. Keep it short

Buttons: up to about 25 characters. Errors: one or two short sentences.
Success: under about 100 characters. If it does not fit, the design may
need changing, not the words cramming.

## 4. Make it accessible

- Icon-only buttons get an accessible name (`aria-label`) and the icon is
  hidden from screen readers.
- Error text is linked to its field (`aria-describedby`), and the field is
  marked invalid (`aria-invalid="true"`).
- Messages that appear without a page load are announced (`role="status"`
  or `role="alert"` for urgent errors).
- Links describe their destination: "Read the setup guide", never "click
  here".
- Colour is never the only signal of an error or success.

Done when: every interactive element has a meaningful accessible name.

## 5. Put it where it belongs

If the project keeps strings in translation files, add them there with
sensible keys rather than hard-coding them in views.

## It's working if

- A person can predict what a button does before pressing it.
- Every error message includes how to fix the problem.
- A screen reader user hears the same information a sighted user sees.
