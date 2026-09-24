---
name: freeze
description: Limits file edits to an agreed set of files or folders for the rest of the session.
license: MIT
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: "Edit|Write|MultiEdit|NotebookEdit"
      hooks:
        - type: command
          command: >-
            sh -c 'for d in ${CLAUDE_SKILL_DIR:+"$CLAUDE_SKILL_DIR"}
            "$CLAUDE_PROJECT_DIR/.claude/skills/freeze" "$HOME/.claude/skills/freeze";
            do [ -f "$d/scripts/guard.py" ] && exec python3 "$d/scripts/guard.py"; done;
            echo "freeze: guard script not found, edits are NOT being checked" >&2; exit 0'
---

# Freeze

For the moments when the task is narrow and the temptation to "just fix"
something nearby is strong: adding logging without touching the logic,
changing one module while others are mid-review. While a freeze is on,
edits outside the agreed paths are refused.

Claude Code only. Codex does not run hooks declared by a skill.

## 1. Agree the scope

Use the paths the user named ("only touch `src/billing`"). If they did not
name any, ask one short question. Paths can be folders or single files.

Done when: the user has agreed a list of paths.

## 2. Write the scope file

Write the paths, one per line, to `.claude/freeze-scope` in the project
root. Relative paths are read from the project root. Create the `.claude`
folder if needed, then read the file back.

Done when: the file exists and lists exactly the agreed paths. Tell the
user what is frozen and what is open, then carry on.

## 3. When an edit is refused

Explain which file needed changing and the reason. If it genuinely
matters, offer to extend the freeze to cover it, and extend it only once
the user says yes, by adding the path to the scope file. Never write files through the shell
to get round the freeze.

Done when: the user has widened the scope or decided the change can wait.

## 4. Lift the freeze

When the user says to lift or end the freeze, or agrees the task is done,
delete `.claude/freeze-scope` and confirm. A refused edit is not a reason
to lift it.

## Limits

- Only the editing tools are checked. Shell commands (`sed -i`, redirects,
  `tee`) can still change files, and `careful` (if installed) does not catch them either,
  so the rule in step 3 is what holds.
- The scope file belongs to the project root of this session. In a git
  worktree, that is the worktree, not the main checkout.
- Deleting the scope file lifts the freeze silently, which is why the file
  is read back in step 2.

## It's working if

- Every change in the session's diff sits inside the agreed paths.
- Refused edits reached the user as questions, not workarounds.
