---
name: notify
description: >-
  Builds a notification that reaches a user through the right channel
  (email, SMS, chat, in-app, push), queued, with a sensible fallback and a
  test that proves it was actually sent rather than just constructed. Use
  when the user asks to notify or alert someone, send an email or text on
  an event, or add an in-app or push notification.
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Notify

A notification class that compiles is not a notification a user ever
receives. This skill builds the message for the channels it actually needs,
wires it to fire on the right event, and proves delivery with a fake rather
than a real email landing in someone's inbox during development.

## 1. Define the event and audience

State in one sentence what triggers the notification, who receives it, and
what they need to do or know as a result. If the trigger is unclear (an
event, a scheduled check, a manual action) or the audience is unclear (one
user, a group, an address with no account), settle that before writing any
code.

Done when: the trigger and recipient are both named, not implied.

## 2. Choose the channel, or channels

| Situation | Channel |
|---|---|
| Needs a permanent record, can wait | email |
| Time-sensitive, short | SMS or push |
| Team or internal, needs quick visibility | chat integration |
| Only matters while the user is in the app | in-app / database |

A notification can go to more than one channel at once, but each channel
adds a place it can fail silently, so only add the ones the requirement
actually needs. If the recipient can choose their channel, read that
preference rather than hard-coding one.

Done when: the channel list is justified by the requirement, not just
"send everything everywhere".

## 3. Write the message per channel

Each channel gets its own build method; do not reuse one body of text
across all of them; email tolerates length and formatting, SMS and push do
not. Keep the content short enough to act on at a glance, and include
whatever the recipient needs to act (a link, a reference number) without
requiring them to go find it.

Done when: each channel's message stands alone and makes sense without the
others.

## 4. Queue it, and handle failure per channel

Notifications that make an outside call (a mail server, an SMS gateway)
must not block the request that triggered them. Queue the notification and
make each channel idempotent: a retried send should not double-charge a
text message credit or double-send an email if it's safe to detect that.

Decide what happens when one channel fails but another succeeds: the user
still hears about it through the channel that worked, and the failure is
recorded somewhere a person will see it, not just logged and forgotten.

Done when: the notification is queued, and a single channel's failure is
handled without silently swallowing it.

## 5. Prove delivery with fakes, then check the real path once

In tests, fake the outbound channel and assert the notification was
queued or sent, with the right recipient and the right content, not just
that no exception was thrown. Separately, confirm at least once (locally
or in a staging environment) that the real channel actually delivers: a
faked assertion proves the code path, not the provider configuration.

Done when: a test asserts the notification was sent with specific content,
and the real channel has been exercised at least once outside the test
suite.

## 6. Report

The trigger, the channels used and why, the queueing and failure handling,
and the test evidence from step 5.

Stack-specific detail: [references/laravel.md](references/laravel.md).

## It's working if

- Every channel used has its own test asserting it fired with the right
  content, not a single generic assertion covering all of them.
- A failure on one channel does not silently prevent the others or vanish
  unseen.
- The real channel has been checked to actually deliver at least once, not
  only faked in tests.
