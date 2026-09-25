---
name: project-setup
description: Records a project's working facts (tracker, base branch, commands, environments) where every agent session will see them.
license: MIT
disable-model-invocation: true
allowed-tools: Read Grep Glob Bash Edit Write
---

# Project setup

Several skills need the same handful of facts about a project: which issue
tracker it uses, which branch pull requests go to, how to run the tests,
where staging lives, which domain must never be tested against. Without
them, each session guesses or asks again. This skill finds those facts once
and writes them into the project's agent instructions file, which Claude
Code and Codex both load at the start of every session, so every skill sees
them without looking.

Run it once per repository, and again when something changes. To choose
which skills a project links, use `pick-skills` (if installed) instead.

## 1. Find the instructions file

Use the file the project already has: `AGENTS.md` (read by Codex and many
other agents) or `CLAUDE.md` (read by Claude Code). If there is only
`CLAUDE.md` and the team also uses Codex, suggest adding `AGENTS.md` and
pointing one at the other, rather than keeping two copies. If neither
exists, create `AGENTS.md`.

Done when: you know which file gets the facts.

## 2. Discover before asking

Work out everything you can from the repository:

| Fact | Where to look |
|---|---|
| Base branch for pull requests | where recent merged pull requests went (`gh pr list --state merged --limit 10`), the default branch |
| Commit style | recent commit subjects |
| Test, lint and build commands | package scripts, Composer scripts, Makefile, CI workflow steps |
| Issue tracker | issue links in commits and pull requests, CI or bot configuration |
| Local URL | environment example files, dev-server configuration |
| Staging and production | deploy configuration, CI workflows, README |

Done when: every fact is either found (with where it came from) or marked
as a question for the user.

## 3. Ask once

Put everything you could not find, plus anything you found but are unsure
of, into one numbered list of questions, each with your suggested answer,
so the user can reply "yes to all but 3". Typical questions: the tracker
project or team; which labels mean what; the production domain that must
never be tested against.

Done when: the user has answered or accepted every question.

## 4. Write the section

Add or update one section in the instructions file. If it already exists,
update it in place; never add a second copy.

```markdown
## Project facts

Kept current by the project-setup skill. Skills rely on these; fix a wrong
line rather than working around it.

- Issue tracker: <GitHub Issues in owner/repo | Jira project KEY | Linear team NAME | none>
- New issues: <default labels or project, if any>
- Pull requests go to: <branch>
- Commit style: <for example conventional commits>
- Tests: `<command>` · Lint: `<command>` · Build: `<command>`
- Local: <URL>
- Staging: <URL or none>
- Production (never test against): <domain>
```

Leave out lines that do not apply rather than writing "none" everywhere.
Keep the section short: it is loaded into every session.

Done when: the section exists once, and each line is a fact a skill will
use.

## 5. Show and commit

Show the user the section and suggest committing it, so everyone's
sessions benefit.

Done when: the user has seen the section and the suggestion to commit it.

## It's working if

- The next session raises pull requests against the right branch and runs
  the right test command without asking.
- Nothing in the section is aspirational; every line is true today.
