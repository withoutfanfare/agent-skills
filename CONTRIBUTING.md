# Contributing

Thank you for wanting to improve these skills. This guide covers what fits,
how a skill is written here, and the checks a pull request must pass.

## What fits

Skills that help an agent do a real engineering, delivery or communication
job well, and that work for anyone: no dependence on one company's tools,
names or private systems. Improvements to existing skills (sharper
descriptions, better steps, fixed gotchas) are just as welcome as new ones.

Before writing a new skill, open an issue describing the job it does and
who would use it, so nobody spends an evening on something that overlaps
an existing skill.

## How a skill is laid out

```text
skills/<name>/
├── SKILL.md            required: frontmatter and instructions
├── references/         optional: detail loaded only when needed
├── scripts/            optional: code the skill runs
├── assets/             optional: templates the skill fills in
└── agents/openai.yaml  only for typed-only skills (see below)
```

Start from [docs/skill-template/](docs/skill-template/).

## Frontmatter

```yaml
---
name: <folder name>
description: >-
  What it does, in the third person, specific. Then "Use when ..." with the
  words a user would actually say.
license: MIT
allowed-tools: Read Grep Glob Bash
---
```

- `name`: lowercase words joined by single hyphens, matching the folder.
- `description`: this is how an agent decides to use the skill, so lead
  with what it does and include real trigger phrases. At most 1024
  characters.
- **Typed-only skills** (run only when someone asks for them by name) add
  `disable-model-invocation: true`, keep the description to one plain line,
  and include `agents/openai.yaml` with
  `policy.allow_implicit_invocation: false` so Codex behaves the same way.

## Writing the body

- Open with one paragraph on why the skill exists.
- Numbered steps, each ending with a **Done when:** line the agent can
  check.
- Say what good looks like; keep prohibitions for hard guardrails.
- Leave out what `--help` or the docs already say; write down the method,
  the judgement calls and the traps.
- End with **It's working if** and two or three observable signs.
- Aim for 60 to 160 lines in `SKILL.md` and put long material in
  `references/`; the linter rejects anything over 500.
- British English; commas, colons and full stops rather than long dashes.
- Rate severity as blocker, major or minor, and confidence as certain,
  likely or possible; the same words in every skill so reports can be read
  side by side.
- Start a report template's headings at `##`, so the report reads the same
  whichever skill wrote it.

## Checks

Run these before opening a pull request:

```bash
python3 scripts/lint.py          # frontmatter, names, typed-only settings, style
python3 scripts/catalogue.py     # regenerates CATALOGUE.md
bash tests/test-cli.sh
bash tests/test-lint.sh
python3 tests/test_guards.py
```

For a new or changed skill, add two lines to `tests/triggers.tsv`: a
realistic request that should start it, and a nearby one that should not.
If you have Claude Code installed, run them:

```bash
bash tests/trigger.sh <skill-name>
```

## Borrowed material

Only contribute what you have the right to share. Ideas can be credited
with a line such as "inspired by …". Text or code adapted from someone
else's work must keep its licence and copyright notice, and be credited in
the skill.

## Sign-off

Please sign off every commit (`git commit -s`). It adds a
`Signed-off-by` line confirming you wrote the change or have the right to
submit it, under the [Developer Certificate of
Origin](https://developercertificate.org/).

## Licence

Contributions are accepted under the repository's [MIT licence](LICENSE).

## Pull requests

Describe the problem first, then the change, then how you checked it. I
aim to review within a week; small, focused pull requests are reviewed
fastest.
