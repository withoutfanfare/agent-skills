#!/usr/bin/env python3
"""PreToolUse hook for the careful skill: refuse destructive shell commands.

Reads the hook payload on stdin. Exit 0 lets the command run; exit 2 blocks
it and sends the reason back to the agent.
"""
import json
import re
import sys

# Keeps a match inside one command, so flags from the next command in a chain
# (after ;, && or |) are not counted.
ARGS = r"[^;&|\n]*"

# Zero or more git global options between `git` and its subcommand, e.g.
# `git -C /path reset --hard` or `git --git-dir=/x/y push -f`. Each iteration
# is a short option (`-C /path`, `-c x=y`) or a long one (`--git-dir=/x/y`,
# `--paginate`), so the subcommand-matching rules below still find their
# subcommand however many of these come first.
GIT_GLOBAL = r"(?:\s+(?:-[A-Za-z](?:[ =]\S+)?|--[A-Za-z][\w-]*(?:=\S+)?))*"

RULES = [
    (r"(?<![\w-])rm\b(?=" + ARGS + r"\s(-\w*r|--recursive\b))(?=" + ARGS + r"\s(-\w*f|--force\b))",
     "recursive force delete"),
    (r"\bfind\b.*\s-delete\b", "find -delete"),
    (r"\bgit" + GIT_GLOBAL + r"\s+push\b" + ARGS + r"(\s--force(?!-with-lease|-if-includes)\b|\s-\w*f\w*\b|\s\+\S)",
     "git force push"),
    (r"\bgit" + GIT_GLOBAL + r"\s+push\b" + ARGS + r"(\s--delete\b|\s-d\b|\s:\S)", "deleting a remote branch"),
    (r"\bgit" + GIT_GLOBAL + r"\s+reset\b" + ARGS + r"\s--hard\b", "git hard reset"),
    (r"\bgit" + GIT_GLOBAL + r"\s+clean\b" + ARGS + r"\s(-\w*f|--force\b)", "git clean -f"),
    (r"\bgit\s+(checkout(\s+--)?|restore)\s+\.(\s|$)", "discarding all uncommitted changes"),
    (r"\bgit\s+branch\s+-D\s+(main|master|develop)\b", "deleting a main branch"),
    (r"\bdrop\s+(table|database|schema)\b", "DROP TABLE or DATABASE"),
    (r"\btruncate\s+(table\b|[\w.`\"]+\s*(;|[\"']|$))|(^|[;&|]\s*)truncate\s+-", "TRUNCATE"),
    (r"\bartisan\s+(migrate:fresh|migrate:reset|migrate:refresh|db:wipe)\b", "wiping the database"),
    (r"\b(flushall|flushdb)\b", "flushing Redis"),
    (r"\bkubectl\s+delete\b", "kubectl delete"),
    (r"\bterraform\s+(-chdir=\S+\s+)?(destroy|apply\b.*-auto-approve)", "terraform destroy or unattended apply"),
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
