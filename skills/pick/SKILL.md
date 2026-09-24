---
name: pick
description: >-
  Links the skills a task actually needs into this project, and unlinks
  the rest.
license: MIT
disable-model-invocation: true
argument-hint: "<what you are about to do>"
allowed-tools: Bash Edit Glob Grep Read Write
---

# Pick

Every linked skill is loaded into every session in that project, whether or
not the current work touches it, and once the roster grows past a handful
it gets genuinely harder to pick the right one out of the list. This skill
narrows the linked set down to whatever the work in front of you actually
calls for, rather than leaving whatever was linked last time. Run it again
whenever the work changes shape: a design task and a review task pull in
almost entirely different skills, even inside the same repository.

## 1. Know the task

Read the task from the argument. If none was given, stop and ask a single
question: "What are you about to work on?" A task description is a
sentence or two ("clean up the checkout flow", "go through the open pull
request and address its comments", "wire up webhook handling"), never just
the project's name.

Done when: you can restate the task in a single sentence and name which
kind of work it falls under (design, build, review, ship, docs, or
debugging).

## 2. Read the catalogue

```bash
python3 .claude/skills/pick/scripts/catalogue.py
```

This prints the stack signals found in the project folder, the current
`.agent-skills` and `.agent-skills.local` manifests (or a note that neither
exists), what is linked here right now, and every library skill with its
description, marked where it is typed-only. Read all of it before choosing;
there is no scoring service behind this, the judgement is yours, from the
descriptions and the stack evidence in front of you.

Done when: the catalogue's output is in front of you, and you have made a
note of any `# keep:` comment line the manifest already carries.

## 3. Choose

Decide what the task needs from the whole library, not from what happens
to be linked already. Aim for a sensible range, enough to cover the task
without duplicating it; going much beyond that needs a reason in the
report.

1. **Keep list.** A `# keep: name name` comment line in `.agent-skills`
   names skills the project always wants. Carry those forward whatever the
   task, each also written as its own manifest line.
2. **Task fit.** For each candidate skill, judge its description against
   the task in one line: reviewing wants the review and hardening skills,
   shipping wants the pull-request and git skills, a design pass wants the
   prototyping and interface skills, and so on. [references/task-kinds.md](references/task-kinds.md)
   has a longer table of kind-to-skill matches if the task doesn't map
   cleanly.
3. **Stack fit.** Only link a stack-specific skill (a framework, a
   language, a deployment target) when the project folder shows real
   evidence for it in the catalogue's stack signals, not from the task
   description alone.
4. **Sets.** When a whole set covers what the task needs, name the set in
   the manifest rather than listing its members one by one, so the file
   stays short and reads as intent.
5. **Typed-only skills.** These cost nothing extra in context once linked,
   since they never fire on their own. Link one when the task will call
   for it by name; otherwise leave it out and mention it as a candidate in
   the report.

Split the chosen set by where each skill already lives. Anything already
linked into the user's home folder is available to every project without a
manifest entry; note it as "needed, already in home" rather than adding it
here. Everything else goes into `.agent-skills`. Anything chosen once and
not chosen this time is dropped by the sync in step 4; say what and why.

Done when: you have written out four short lists, one reason per entry:
what to link into the project, what is already covered from home, what
stays kept as-is, and what gets dropped.

## 4. Write the manifest and sync

Rewrite `.agent-skills` following this layout, carrying forward any
`# keep:` line already there along with whatever other comments the team
has added:

```text
# Skills for this project
# keep: house-style
# task: review the open pull request and fix what it finds (picked 2026-09-24)
house-style
review
cover
```

Then:

```bash
agent-skills sync
agent-skills status
```

`sync` clears every symlink this tool owns in `.claude/skills` and
`.agents/skills` and relinks from `.agent-skills` plus `.agent-skills.local`,
so a skill drops out simply by no longer being listed. Leave
`.agent-skills.local` alone; it holds one person's own extras and `sync`
reads it on its own.

Done when: `agent-skills status` shows the chosen set together with the
keep list, and no other entries besides those.

## 5. Write up the outcome

Cover, in order: the task summarised in one line; the complete set the task
draws on, broken into "linked into project" and "already available from
home" with a reason for each; anything dropped and the reason; anything
left as it was. Give the reader the full picture of what the task will
use, not a list limited to what changed this run.

Then, only as suggestions, never carried out without being asked:

- A skill this project links that plainly every project would want:
  suggest `agent-skills home add <skill>`.
- A skill already in home that only this task needed: suggest
  `agent-skills home remove <skill>` and note it belongs in the project
  manifest from now on instead.

Never edit the user's home links yourself; both directions above are lines
in the report, not actions you take.

Done when: the report fits on one screen and every line names a real skill
from the catalogue.

## Verify what you built

```bash
agent-skills status
```

Every entry traces back to a skill you picked in step 3, the number of
entries agrees with what the report said, and the manifest's `# task:`
line reflects today's task.

## It's working if

- Two runs against different tasks land on two different linked sets, and
  what `agent-skills status` shows lines up with whichever report is newer.
- A teammate can open `.agent-skills` in a fresh checkout and tell what the
  project is currently working on from the `# task:` line alone.
- Nothing links into a project's `.claude/skills` or `.agents/skills`
  without a matching line in `.agent-skills` (or `.agent-skills.local`).
