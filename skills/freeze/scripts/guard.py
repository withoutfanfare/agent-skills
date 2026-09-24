#!/usr/bin/env python3
"""PreToolUse hook for the freeze skill: allow file edits only inside the
paths listed in .claude/freeze-scope at the project root.

No scope file means no freeze. Exit 0 allows the edit; exit 2 blocks it and
sends the reason back to the agent.
"""
import json
import os
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if payload.get("tool_name") not in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        return 0
    tool_input = payload.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not target:
        return 0

    project = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    scope_file = os.path.join(project, ".claude", "freeze-scope")
    if not os.path.isfile(scope_file):
        return 0

    allowed = [line.strip() for line in open(scope_file, encoding="utf-8")
               if line.strip() and not line.startswith("#")]
    allowed.append(scope_file)  # the scope itself stays editable, to lift or widen it

    target = os.path.realpath(target)
    for entry in allowed:
        path = os.path.realpath(os.path.join(project, os.path.expanduser(entry)))
        if target == path or target.startswith(path.rstrip(os.sep) + os.sep):
            return 0

    print(
        f"Blocked by freeze: {target} is outside the agreed scope "
        f"({', '.join(allowed[:-1]) or 'nothing listed'}). Tell the user what you wanted "
        "to change and why; widen the scope only if they agree.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
