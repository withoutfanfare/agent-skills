#!/usr/bin/env bash
#
# http-smoke.sh -- check a list of routes against expected status codes.
#
# Usage:
#   http-smoke.sh <base-url> <routes-file>
#   http-smoke.sh <base-url> --json <routes.json>
#
# routes-file: one route per line, "METHOD PATH EXPECTED_STATUS".
#   Blank lines and lines starting with # are skipped. Example:
#     GET  /login       200
#     POST /login       419
#     GET  /account     302
#   (a web POST without a CSRF token gets 419; a guest on a protected
#   page is redirected to the login page with 302)
#
# --json mode reads a JSON file shaped: [{"method":"GET","path":"/login","status":200}, ...]
#
# Exits non-zero if any route does not match its expected status.

set -u

fail() { echo "error: $*" >&2; exit 2; }

[[ $# -lt 2 ]] && fail "usage: http-smoke.sh <base-url> <routes-file | --json routes.json>"

base_url="${1%/}"
shift

if [[ "$1" == "--json" ]]; then
  json_file="${2:-}"
  [[ -f "$json_file" ]] || fail "json file not found: $json_file"
  routes="$(python3 -c '
import json, sys
data = json.load(open(sys.argv[1]))
for r in data:
    print(r.get("method", "GET").upper(), r["path"], r["status"])
' "$json_file")" || fail "could not parse $json_file"
else
  routes_file="$1"
  [[ -f "$routes_file" ]] || fail "routes file not found: $routes_file"
  routes="$(grep -Ev '^\s*(#|$)' "$routes_file")"
fi

[[ -n "$routes" ]] || fail "no routes to check"

pass=0
fail_count=0

while read -r method path expected; do
  [[ -z "${method:-}" ]] && continue

  # API-shaped paths get an Accept header so a failure returns a JSON body
  # instead of an HTML error page that would defeat a JSON assertion later.
  accept="text/html"
  [[ "$path" == /api/* || "$path" == *.json ]] && accept="application/json"

  # -g/--globoff: a path containing [ ] or { } (e.g. from a route template)
  # would otherwise be parsed by curl as URL globbing syntax and rejected.
  actual="$(curl -sgk -o /dev/null -w '%{http_code}' -X "$method" \
    -H "Accept: $accept" --max-time 15 "${base_url}${path}" 2>/dev/null)"
  curl_rc=$?

  # A non-zero curl exit means the transfer itself failed (timed out, was
  # reset, etc). curl can still have written a %{http_code} from the
  # headers it received before that happened, so trust that code only when
  # curl actually succeeded - otherwise this reports a stall as a pass.
  if [[ "$curl_rc" -ne 0 ]]; then
    actual="000"
  else
    actual="${actual:-000}"
  fi

  if [[ "$actual" == "$expected" ]]; then
    printf 'ok    %-6s %-40s -> %s\n' "$method" "$path" "$actual"
    pass=$((pass + 1))
  else
    note=""
    [[ "$actual" == "000" ]] && note="  (no response -- is the app running?)"
    (( curl_rc != 0 )) && note="  (curl exit $curl_rc -- transfer failed or timed out)"
    printf 'FAIL  %-6s %-40s expected %s, got %s%s\n' "$method" "$path" "$expected" "$actual" "$note"
    fail_count=$((fail_count + 1))
  fi
done <<< "$routes"

echo "----"
echo "$pass passed, $fail_count failed (base: $base_url)"

[[ "$fail_count" -eq 0 ]]
