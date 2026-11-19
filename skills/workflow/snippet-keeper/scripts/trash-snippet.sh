#!/usr/bin/env bash
# Move SnippetsLab snippets to the Bin by UUID, checking each one first and
# proving afterwards that it is gone. The Bin keeps them until it is emptied.
# Usage: trash-snippet.sh <uuid> [<uuid> ...]
set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
lab="$(command -v lab || echo /Applications/SnippetsLab.app/Contents/Helpers/lab)"
status=0 binned=0
previous="$(osascript -e 'tell application "System Events" to return name of (first process whose frontmost is true)' 2>/dev/null)"

for uuid in "$@"; do
  json="$("$lab" fetch --launch --format json --snippet "$uuid" 2>&1)" || {
    echo "SKIP $uuid: $json"; status=1; continue
  }
  title="$(printf '%s' "$json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["snippet"]["title"])')"

  result="$(osascript "$here/trash-snippet.applescript" "$uuid" "$title" 2>&1)"
  # An ABORT comes before any delete (often a focus change), so one retry is safe.
  if [[ "$result" == ABORT:* ]]; then
    sleep 2; result="$(osascript "$here/trash-snippet.applescript" "$uuid" "$title" 2>&1)"
  fi
  if [[ "$result" != OK:* ]]; then
    echo "FAIL $uuid \"$title\": $result"; status=1; continue
  fi

  if "$lab" fetch --snippet "$uuid" >/dev/null 2>&1; then
    echo "FAIL $uuid \"$title\": still in the library after Delete"; status=1
  else
    echo "BINNED $uuid \"$title\""; binned=$((binned + 1))
  fi
done
echo "$binned binned, $(($# - binned)) failed"

# Hand the screen back to whatever was in front before.
[[ -n "$previous" && "$previous" != "SnippetsLab" ]] && osascript -e "tell application \"$previous\" to activate" >/dev/null 2>&1

exit $status
