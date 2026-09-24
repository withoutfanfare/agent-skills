#!/usr/bin/env python3
"""PreToolUse hook for the careful skill: refuse destructive shell commands.

Reads the hook payload on stdin. Exit 0 lets the command run; exit 2 blocks
it and sends the reason back to the agent.
"""
import json
import re
import sys

RULES = [
    (r"\brm\s+(-\w*r\w*f|-\w*f\w*r)\w*\b", "recursive force delete"),
    (r"\bfind\b.*\s-delete\b", "find -delete"),
    (r"\bgit\s+push\b.*(\s--force(?!-with-lease)\b|\s-f\b)", "git force push"),
    (r"\bgit\s+reset\s+--hard\b", "git hard reset"),
    (r"\bgit\s+clean\s+-\w*f", "git clean -f"),
    (r"\bgit\s+branch\s+-D\s+(main|master|develop)\b", "deleting a main branch"),
    (r"\bdrop\s+(table|database|schema)\b", "DROP TABLE or DATABASE"),
    (r"(^|[^a-z])truncate(\s+table)?\s", "TRUNCATE"),
    (r"\bartisan\s+(migrate:fresh|migrate:reset|db:wipe)\b", "wiping the database"),
    (r"\b(flushall|flushdb)\b", "flushing Redis"),
    (r"\bkubectl\s+delete\b", "kubectl delete"),
    (r"\bterraform\s+(destroy|apply\b.*-auto-approve)", "terraform destroy or unattended apply"),
    (r"\b(curl|wget)\b[^|]*\|\s*(sudo\s+)?(ba|z)?sh\b", "piping a download into a shell"),
]


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if payload.get("tool_name") not in (None, "Bash"):
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    for pattern, reason in RULES:
        if re.search(pattern, command, re.I):
            print(
                f"Blocked by careful mode ({reason}). Show the user the exact command "
                "and ask them to run or approve it. Do not reword it to get past this check.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
