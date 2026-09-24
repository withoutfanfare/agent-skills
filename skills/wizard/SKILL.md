---
name: wizard
description: >-
  Generates an interactive bash script a person runs by hand to step
  through a manual procedure only they can do, confirming before anything
  irreversible and hiding secret input. Use when the user needs a guided
  script to provision infrastructure, set up credentials, walk a
  third-party dashboard, or run a migration that needs a human at the
  controls. Not for CI or deploy pipelines; use `launchpad`.
license: MIT
allowed-tools: Read Grep Glob Write Bash
---

# Wizard

Some setup work cannot be automated because the actions live behind a
login only a human holds: clicking "reveal key" on a dashboard, approving
a billing plan, copying a one-time code. Explaining those steps fresh in
chat every time is slow and easy to get wrong halfway through. This skill
turns the procedure into a small script: it opens the right page, says
exactly what to click, waits for the value, and files it away correctly.

The generated script does the talking to the human from then on, not this
skill. It should be safe to stop with Ctrl-C and run again later, picking
up where it left off.

## 1. Work out every step and every value

Before writing anything, read the project for what the procedure actually
needs: `.env` and `.env.example` files, README setup notes, CI workflow
files (search for the secrets and variables they reference), and any
existing setup scripts. For a migration or cutover, work out the current
state, the target state, and which actions in between cannot be undone.

List the steps in the order a human must do them, and for each captured
value note: where they get it, where it needs to end up (an env file, a CI
secret, both, or nowhere), and whether it is secret (needs hidden entry)
or fine to show on screen.

Show the user this list before writing the script, so they can add, drop
or reorder steps.

Done when: every step is named in order, and every value has a source, a
destination and a visibility.

## 2. Write the exact path for each step

For each step, spell out the concrete path through the interface: which
page, which menu, which button, in the order a stranger would need to
follow it. Where the current interface is unknown, say so and check the
project's docs, or ask, rather than inventing a plausible-looking path
that might not exist.

Done when: every step reads as a set of instructions someone unfamiliar
with the tool could follow without guessing.

## 3. Build the script from the template

Start from [assets/procedure.sh](assets/procedure.sh) and read it before
touching it: everything above its stages marker is fixed plumbing (colour
output, progress display, confirmation prompts, hidden secret entry, an
idempotent env-file writer, optional CI secret writer) and should not be
hand-edited. Below the marker, replace the sample step with one step per
item from step 1, in order, and update the step count.

Match the template's helpers to what each step needs: open the target page
before asking for a value, use the hidden-entry helper for anything
secret, write every value that belongs in the env file, only push to CI
what the workflow actually reads, and gate any irreversible action behind
a yes/no confirmation.

Keep the guard that refuses to write the env file anywhere outside the
project root; it is what stops a wrong working directory sending values to
the wrong place silently.

Done when: the script contains one step per item from step 1, in the same
order, with nothing from the template's plumbing altered.

## 4. Check it before handing it over

Run:

```bash
bash -n <script path>
```

Run `shellcheck <script path>` if it is available, and fix what it flags.
Do not run the script itself end to end: it opens a browser and waits on a
human, so instead trace it by eye, confirming every value from step 1 is
both asked for and written to the destination step 1 named.

Tell the user how to run it. A script built for a single occasion can stay
in a scratch location and be deleted after; one the user wants to keep for
future team members or future runs should be committed and linked from
setup docs.

Done when: `bash -n` passes, every captured value's destination has been
traced by eye, and the user knows how to run it.

## It's working if

- A person with no context on the procedure can run the script and finish
  it without asking a question.
- Running it twice is harmless: existing values show as defaults, and
  nothing destructive happens without an explicit yes.
- Nothing secret appears on screen or in shell history.
