---
name: tour
description: >-
  Writes a guided walkthrough of this codebase, a feature or a single request,
  following the path data actually takes and explaining what each stop does,
  why it is built that way and what trips people up. Use when the user asks
  for a tour or walkthrough of the code, how a feature works end to end, or
  help getting up to speed on a project. Not for explaining a general
  concept or technology outside this codebase; use `unpack`.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Tour

The fastest way into an unfamiliar codebase is a colleague saying "start
here, then look at this, and watch out for that". This skill writes that
walk-through: a readable path through the code, in the order things
happen, with the reasons and the traps along the way. It explains what
exists; judging it is a job for other skills. To explain a concept rather
than this codebase, use `unpack` (if installed).

## 1. Choose the kind of tour

| Tour | Covers | Order |
|---|---|---|
| Whole codebase | the big picture for a newcomer | outside in: what it is, how requests arrive, where logic lives, how data is stored, what it talks to, how it is tested and deployed |
| Feature | one capability end to end | follow a user action from click to database and back |
| Layer | one layer in depth (the API, the queue workers) | the layer's entry points, then its shared pieces |
| Request | one request or command, call by call | the exact call chain, branches included |

If the user did not say, ask; if they cannot say, start with the whole
codebase.

Done when: the kind of tour and its starting point are named.

## 2. Map before writing

Read enough to draw the map: top-level folders and what lives in each;
entry points (routes, commands, scheduled tasks, listeners, webhooks); the
core abstractions everything leans on; the data model; outside services and
how their failures are handled.

Done when: you could sketch the system on one page.

## 3. Walk the path

Write one stop per meaningful point on the path:

```markdown
### Stop 3: Checkout controller, where an order is born
`src/Http/CheckoutController.php`

What it does, in two to four sentences, and why it is shaped this way.
- The method or property that matters, and what it does
- The convention it follows (or breaks)

Next: the pricing service it hands over to.
```

Keep each stop short. The reader can open the file; the tour tells them
which file, what to notice and where to go next.

Done when: the path is complete from its start to its end, with no jump
the reader cannot follow.

## 4. The house rules

After the stops, list the conventions a newcomer needs to fit in: naming,
where each kind of code goes, how errors are handled, how tests are
organised, where configuration lives.

Done when: someone could add a small feature "the way this codebase does
it" from this section alone.

## 5. Watch out for

List the surprises: side effects hidden in listeners or observers, names
that mislead, historical decisions that explain odd structures, fragile or
performance-sensitive areas, and anything mid-migration.

Done when: every surprise names the file where it lives.

## 6. Save it

Save the tour where the project keeps docs (ask, or use `docs/tours/`),
with the date and the commit it describes, because code moves on.

Done when: the tour is saved with its date and commit, and you have given
the path.

## It's working if

- A newcomer can follow the stops in order without getting lost.
- Every stop names a real file, and the files exist.
- The "watch out for" section saves someone a bad afternoon.
