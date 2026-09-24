#!/usr/bin/env bash
# Does each skill start when it should, and stay out of the way when it
# should not? Runs real Claude Code sessions, so it costs a little usage.
#
#   bash tests/trigger.sh                 every case in tests/triggers.tsv
#   bash tests/trigger.sh review sweep    only cases for these skills
#   JOBS=6 bash tests/trigger.sh          six cases at a time (default 4)
#
# tests/triggers.tsv has one case per line: skill, fire|quiet, prompt
# (tab-separated). A "fire" case passes when the session invokes that
# skill; a "quiet" case passes when it does not. Each case runs in a fresh
# throwaway project with every library skill linked, only project settings
# loaded, no MCP servers, and no tools that could change anything.

set -uo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd -P)
cases="$repo/tests/triggers.tsv"
only=" $* "

jobs="${JOBS:-4}"
results=$(mktemp -d)
trap 'rm -rf "$results"' EXIT

run_case() {
    local index="$1" skill="$2" expect="$3" prompt="$4" project used fired result shown
    project=$(cd "$(mktemp -d)" && pwd -P)
    git -C "$project" init -q
    (cd "$project" && "$repo/bin/agent-skills" add $("$repo/bin/agent-skills" list skills) >/dev/null)

    used=$(cd "$project" && timeout 300 claude -p "$prompt" \
            --output-format stream-json --verbose --max-turns 3 \
            --setting-sources project --strict-mcp-config --no-session-persistence \
            --disallowedTools Bash Edit Write NotebookEdit WebFetch WebSearch Agent 2>/dev/null |
        python3 -c '
import json, sys
for line in sys.stdin:
    try:
        event = json.loads(line)
    except ValueError:
        continue
    message = event.get("message") if isinstance(event, dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    for block in content if isinstance(content, list) else []:
        if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
            print((block.get("input") or {}).get("skill", ""))
')
    rm -rf "$project"

    fired=no
    grep -qx "$skill" <<< "$used" && fired=yes
    if { [ "$expect" = fire ] && [ "$fired" = yes ]; } || { [ "$expect" = quiet ] && [ "$fired" = no ]; }; then
        result="pass"
    else
        result="FAIL"
    fi
    shown=${used//$'\n'/, }
    echo "$result  $skill  expected $expect, used: ${shown:-nothing}  | $prompt" > "$results/$index"
}

index=0
while IFS=$'\t' read -r skill expect prompt; do
    [ -n "$skill" ] && [ "${skill:0:1}" != "#" ] || continue
    [ "$only" = "  " ] || [[ "$only" == *" $skill "* ]] || continue
    index=$((index + 1))
    while [ "$(jobs -rp | wc -l)" -ge "$jobs" ]; do sleep 1; done
    run_case "$(printf '%04d' "$index")" "$skill" "$expect" "$prompt" &
done < "$cases"
wait

cat "$results"/* 2>/dev/null
pass=$(cat "$results"/* 2>/dev/null | grep -c '^pass')
fail=$(cat "$results"/* 2>/dev/null | grep -c '^FAIL')
echo
echo "$pass passed, $fail failed"
[ "$fail" = 0 ]
