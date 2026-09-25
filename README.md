# Agent skills

79 skills for AI coding agents, written for **Claude Code** and **Codex**,
with a small command that links the ones you need into each project.

A **skill** is a folder of instructions an agent reads before it starts a
job: how to review a pull request, run a post-mortem, size a feature, or
chase down a slow page. Write the method down once, and every session
follows it, with checks along the way so the agent can tell done from not
done.

## Quick start

```bash
git clone https://github.com/withoutfanfare/agent-skills.git
cd agent-skills && ./install.sh
```

Then, inside any project:

```bash
agent-skills list              # the sets, and how many skills there are
agent-skills add review        # link one skill (or a set) into this project
agent-skills status            # what is linked here
```

Restart your agent so it notices. In Claude Code, ask for a skill by name
with `/review`; in Codex, with `$review`. Most skills also start on their
own when a request matches them.

## Link skills per project, not all at once

Installing switches nothing on. Every skill an agent can start by itself
adds its description to every session, so linking a hundred makes agents
vaguer, not cleverer. Link the handful a project needs:

```bash
agent-skills add laravel       # a whole set
agent-skills init              # write .agent-skills so the team gets the same set
agent-skills sync              # make links match .agent-skills exactly
agent-skills home add careful  # link one everywhere (keep this list short)
```

Links go into `.claude/skills` for Claude Code and `.agents/skills` for
Codex. Each link points back at this repository, so `git pull` updates
every project at once. Personal extras for one project go in
`.agent-skills.local`.

Not sure what fits? `/pick <what you are about to do>` links the right few
for the task in hand, and `/which-skill` maps a situation to a skill and
what comes after it.

## What is in here

The full list, with one line each, is in [CATALOGUE.md](CATALOGUE.md).
Some highlights:

| If you want to | Use |
|---|---|
| Know where an issue or pull request really stands, and the next safe step | `work` |
| Review a change: "is it the right change?" and "is it built well?", separately | `review` |
| Prove a change works by running it, not by reading it | `prove-it` |
| Find out why something is slow, with before and after numbers | `speed-up` |
| Fix a red test suite without weakening a single assertion | `fix-tests` |
| Run a blameless post-mortem that ends in owned actions | `post-mortem` |
| Threat-model a feature before building it | `threat-model` |
| Turn technical detail into plain English for a chosen reader | `plainify` |
| Stop destructive commands for a risky session | `careful` |

Sets group skills for common kinds of work: `delivery`, `planning`,
`quality`, `operations`, `frontend` and `laravel`.

## How the skills are built and checked

- **One method per skill,** written as numbered steps, each ending with a
  "Done when" line the agent can check, and closing with "It's working if".
- **Tuned for current models** (Claude Opus 5.5, Fable 5.1 and Sonnet 5;
  GPT-6 in Codex): descriptions say what a skill does and when to use it in
  the words people actually use; instructions say what good looks like
  rather than shouting rules.
- **Works in both agents.** Skills that should only run when asked for by
  name carry both Claude Code's `disable-model-invocation` and Codex's
  `agents/openai.yaml` policy, and the linter checks the two agree.
- **Tested for triggering.** `tests/trigger.sh` runs real Claude Code
  sessions to confirm each skill starts on a realistic request and stays
  quiet on a near miss.
- **Linted.** `scripts/lint.py` checks names, descriptions, sizes, the
  typed-only settings, the router's coverage, sets and house style.

See [CONTRIBUTING.md](CONTRIBUTING.md) to add or improve a skill.

## Usage tracking (optional)

`agent-skills track` shows how to switch on a small local hook that logs
which skills you use; `agent-skills usage` reports on it, and
`/usage-audit` turns that into recommendations. Nothing leaves your
machine.

## Skills I use and recommend

Excellent work by other people, worth installing alongside these:

- [Laravel Boost](https://github.com/laravel/boost): Laravel's own
  guidelines and skills for AI agents.
- [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren
  Tan: workflow skills including `unslop`, `blast-radius` and
  `show-me-your-work`.
- [unlazy](https://github.com/Leonxlnx/unlazy) by Leon Lin: completion
  discipline through gate files and runnable checks.
- [Matt Pocock's skills](https://github.com/mattpocock/skills): grilling
  a plan, domain modelling and turning conversations into tickets.
- [Anthropic's skills](https://github.com/anthropics/skills) and
  [OpenAI's skills](https://github.com/openai/skills): the official
  collections, including web-app testing and moving setups to Codex.
- [LLM Council](https://github.com/karpathy/llm-council) by Andrej
  Karpathy: several models answering, then reviewing each other.

## Author

Written by [Danny Harding](https://github.com/withoutfanfare) of
Stuntrocket, who builds web apps with Laravel and Nuxt, and desktop apps
with Tauri and Swift.

## Licence

MIT. See [LICENSE](LICENSE).
