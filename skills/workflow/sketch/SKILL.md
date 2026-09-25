---
name: sketch
description: >-
  Builds a quick, throwaway prototype that answers one design question
  before real building starts: a single self-contained HTML file to try a
  state model or flow, or several radically different variations to compare
  a look. Use when the user asks to prototype or mock something up, wants to
  try a few versions, or a design question cannot be settled by talking.
license: MIT
allowed-tools: Read Write Edit Bash Glob Grep
---

# Sketch

Some questions are faster to answer by touching something than by
discussing it: will these states cover every case, which arrangement is easiest to scan,
is this interaction pleasant to use? A sketch is the smallest program
that lets someone answer one such question. It is throwaway in how it is
built (no tests, no error handling, hard-coded data, speed over craft),
and its answer is what goes into the real build.

## 1. Write the question down

State the one question the sketch will answer, in a sentence, and confirm
it with the user. "Which of three ways of showing a subscription's billing
history reads best on a phone?" is a question. "Mock up billing" is not.

Done when: the user has agreed the question.

## 2. Pick the shape

| Question is about | Build |
|---|---|
| State, logic or a flow | One self-contained HTML file: inline CSS and JavaScript, no build step, opens with a double-click. Buttons drive the states and the current state is always visible. |
| Look and feel | Three different variations, switchable from one place: a variant picker in one HTML file, or one temporary route in the app. Three different directions beat six tweaks of one. |

Done when: the shape is chosen and the user knows what they will get.

## 3. Build fast

Minutes to a first version, not hours. Use realistic data (real-looking
names, long names, empty states) because fake data hides layout problems.
Skip everything that does not help answer the question.

Done when: the user can open it and try it.

## 4. Let the user drive

Hand it over, ask the question again, and watch for the answer. If the
question sharpened rather than resolved, change the sketch and go again.

Done when: the user has given a verdict on the question.

## 5. Record the answer

Write the answer in a short paragraph where the real work will see it: the
spec, the issue, or the pull request description. Keep the sketch for
reference in a scratch folder or a `sketch/<name>` branch, linked from that
paragraph. It is never merged into the product.

Done when: the answer is written where the build will use it, with a link
to the sketch.

## It's working if

- Each sketch answered exactly one named question.
- It was quicker than debating the question in a meeting.
- No sketch code ended up in the product.
