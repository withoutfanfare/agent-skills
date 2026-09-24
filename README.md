# Agent skills

A library of skills for AI coding agents, written for Claude Code and Codex.

A **skill** is a folder of written instructions an agent reads before it
starts a job: how to review a pull request, run a post-mortem, or size a
feature. Write the method down once, and every session follows it.

> Work in progress: skills are being added in batches.

## Quick start

```bash
git clone https://github.com/withoutfanfare/agent-skills.git
cd agent-skills && ./install.sh
```

Then, inside any project:

```bash
agent-skills list              # what is available
agent-skills add <skill>       # link it for Claude Code and Codex
```

Installing switches nothing on. Skills are linked one project at a time,
so each session only carries the few it needs.

## Licence

MIT, copyright Danny Harding. See [LICENSE](LICENSE).
