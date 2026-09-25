---
name: plainify
description: >-
  Rewrites technical material into clear plain English for a chosen reader
  and format (an executive briefing, a client email, a user guide, release
  notes), leading with the point. Use when the user asks to put something in
  plain English, simplify it for non-technical people, rewrite it for a
  client or boss, or write a guide someone non-technical must follow.
license: MIT
allowed-tools: Read Grep Glob Bash WebFetch Write
---

# Plainify

Technical writing usually starts with how and ends with so what. Readers
need it the other way round. This skill takes technical material (a pull
request, an incident, a spec, a diff, a wall of text) and rewrites it for
one specific reader in one specific shape, so the point comes first and
every paragraph earns its place.

To explain a concept from scratch, use `explain` (if installed); to
re-explain a reply that did not land, `wait-what` (if installed).

## 1. Get the source

Accept whatever the user gives: pasted text, a file, a link (fetch it), an
issue or pull request (fetch it with the tools available), or git history
("plainify the last five commits"; read the log and diff). Work from the
real content; never from a guess about it.

Done when: you have read the whole source.

## 2. Set the two dials

**Reader** and **shape**. If the user named a purpose ("a UAT script", "an
onboarding guide"), it sets both; see the purpose table in
[references/presets.md](references/presets.md). If they gave only a reader,
choose the shape and say which. If neither can be worked out, ask one short
question with the likely options.

More than one reader means more than one version: a single compromise
serves nobody. An explicit length from the user overrides the preset
depth.

The presets only rewrite existing material. To write a full test plan,
runbook, marketing copy or progress update, `test-plan`, `runbook`,
`copywriter` or `bulletin` (if installed) does the whole job.

Done when: reader and shape are set, and said out loud if you chose them.

## 3. Apply the presets

Read the entries for the chosen reader and shape in
[references/presets.md](references/presets.md). They set what the reader
already knows, what they care about, how much jargon is allowed, the tone,
and the depth.

Done when: you can name the reader's assumed knowledge, jargon level, tone
and depth from the presets.

## 4. Rewrite

- **Point first.** The answer, the decision or the "so what" opens the
  piece.
- **Layers.** A headline, then three to five key points, then optional
  detail. Stopping early still leaves the reader with the gist.
- **Jargon to match the reader.** For non-technical readers, remove it, or
  explain a term in a few words the first time it appears. For developers
  and operators, keep every precise term, name and path; plain English for
  them means well organised, not simplified.
- **Concrete.** An example or a short analogy for anything hard.
- **Scannable.** One idea per paragraph, short sentences, helpful headings.
- **Framed around the reader.** "What this means for you", "what to do
  next".
- **Honest.** Never invent a fact to make the story smoother. Flag gaps in
  the source instead.

Rewrite; do not just trim. Reorder so the point leads.

Done when: the first two lines alone tell the reader what they most need
to know.

## 5. House style

Markdown always (even for chat messages and emails, so it renders where it
is pasted). The product's locale, British English unless the codebase or
user says otherwise. A warm, human voice at the right formality.
Commas, colons and full stops rather than long dashes.

Done when: the draft is Markdown, in the right locale, and has no long
dashes.

## 6. Deliver

In the conversation by default. Save a file only if asked: next to the
source file, or wherever the user says, named from the source and the dials
(for example `payment-outage--client--email.md`). Confirm the path.

Done when: the rewrite is in the conversation, or saved at a path you have
confirmed to the user.

## It's working if

- The intended reader could act on it after reading only the top.
- Technical readers lost no precision; non-technical readers met no
  unexplained jargon.
- Nothing in it is less true than the source.
