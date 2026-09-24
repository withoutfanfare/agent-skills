---
name: careful
description: Switches on a guard for this session that refuses destructive shell commands.
license: MIT
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: >-
            sh -c 'for d in "$CLAUDE_PROJECT_DIR/.claude/skills/careful" "$HOME/.claude/skills/careful";
            do [ -f "$d/scripts/guard.py" ] && exec python3 "$d/scripts/guard.py"; done; exit 0'
---

# Careful

A seatbelt for sessions near things that cannot be undone: production
data, shared branches, live infrastructure. While this skill is active,
every shell command is checked before it runs, and destructive ones are
refused with the reason.

It is a skill rather than an always-on setting on purpose: most sessions
need no seatbelt, and one that fires all day gets ignored.

Claude Code only. Codex does not run hooks declared by a skill, so in Codex
this skill is a reminder, not a guard.

## When switched on

Tell the user the guard is active and what it covers, then carry on with
the task.

## When a command is refused

1. Stop. A refusal means this action needs a person, not a cleverer
   command. Never reword or split a command to slip past the check.
2. Show the user the exact command and the reason it was refused.
3. Offer a reversible alternative where one exists: archive instead of
   delete, `--dry-run` first, `git stash` instead of `git reset --hard`,
   `--force-with-lease` instead of `--force`.

Done when: the user has run the command themselves, approved an
alternative, or dropped it.

## What is refused

Recursive force deletes, `find -delete`, git force pushes (plain `--force`,
not `--force-with-lease`), hard resets, `git clean -f`, deleting a main
branch, `DROP TABLE` or `DROP DATABASE`, `TRUNCATE`, framework commands
that wipe a database, Redis flushes, `kubectl delete`, `terraform destroy`
or unattended apply, and piping a download straight into a shell. The list
lives in [scripts/guard.py](scripts/guard.py); add patterns as new hazards
appear.

## Limits

- The guard reads command text, not intent. Destructive SQL inside a
  script file, an interactive console or a heredoc is not seen. When
  working on production data, confirm every write with the user even when
  the guard is quiet.
- A script is checked only by the command that runs it
  (`bash deploy.sh`), not by its contents. Read a script before running it.
- The guard lasts for this session only.

## It's working if

- Every refused command reached the user, word for word.
- No refused command was re-attempted in another form.
- The session still got its real work done.
