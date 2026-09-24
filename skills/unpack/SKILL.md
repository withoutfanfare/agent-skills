---
name: unpack
description: >-
  Explains a technical concept, system or technology in layers, from a
  one-sentence summary to a deep dive, researched from reliable sources and
  pitched at the reader's level, with analogies and examples. Use when the
  user asks to explain how something works, what something is, the
  difference between two technologies, or asks for an explanation "like I'm
  new to this".
license: MIT
allowed-tools: Read Grep Glob WebSearch WebFetch
---

# Unpack

A good explanation lets the reader stop as soon as they have enough. It
starts with one sentence that is true, adds a layer at a time, and uses
familiar things to carry unfamiliar ones. This skill researches first, so
the simple version is simple because it is well understood, not because
detail was skipped.

To rewrite an existing document for a different reader, use `plainify` (if
installed).

## 1. Know the reader

Work out, from the conversation or one question: what they already know,
why they are asking (a decision, a task, curiosity), and how deep they
want to go. A developer choosing a queue needs different layers from a
client wondering why the site was down.

Done when: the reader's level and purpose are known.

## 2. Research

Understand the subject properly before simplifying it: official
documentation first, then well-regarded technical writing. Look for why
it exists and what problem it solves, not only what it is, and for the
common misunderstandings. For anything recent or fast-moving, check
current sources rather than memory. If the question is about this
codebase, read the code.

Done when: you can state the core idea in one sentence and name one common
misunderstanding.

## 3. Build the layers

1. **One sentence:** what it is, in ten to twenty plain words.
2. **The picture:** two or three short paragraphs on what it does, why it
   exists and when you would use it.
3. **The key ideas:** three to five building blocks, each with a concrete
   analogy or example.
4. **How it works:** a step-by-step walk-through with a real example.
5. **In practice:** when to use it, when not to, and what people get
   wrong.
6. **Deep dive** (only if wanted): internals, edge cases, trade-offs,
   sources.

Stop at the layer the reader needs, and offer the next.

Done when: each layer stands on its own and uses no term the previous
layers did not explain.

## 4. Write clearly

- Explain every technical term the first time, in a few words.
- One idea per paragraph; short sentences.
- Analogies should match the real mechanism closely enough not to mislead;
  say where an analogy breaks down.
- Prefer a small concrete example to an abstract description.
- For comparisons, a table of what each is best at beats paragraphs.

Analogy ideas and layer templates are in
[references/analogies.md](references/analogies.md).

## 5. Check understanding

End with an offer to go deeper on a specific layer, or a short question
that checks the key idea landed.

## It's working if

- The one-sentence summary is accurate, not just short.
- A reader can stop after any layer and still have something true and
  useful.
- Sources back the facts that matter.
