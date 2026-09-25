#!/usr/bin/env bash
#
# A guided setup procedure: walks a human through steps that need a person
# at the controls (a dashboard, a login, a one-off migration), one step at
# a time, and files away what they collect.
#
# Everything above the "STEPS" marker is shared plumbing used by every
# procedure built from this template. Do not hand-edit it; author your
# steps below the marker instead.

set -euo pipefail

# ---------------------------------------------------------------------------
# Plumbing: colour, progress, prompts, and idempotent writers.
# ---------------------------------------------------------------------------

_TTY=0
[[ -t 1 ]] && _TTY=1

# A terminal only earns colour codes when it is interactive AND tput itself
# reports at least a basic 8-colour palette; anything less gets plain text.
_terminal_supports_colour() {
  [[ "$_TTY" -eq 1 ]] || return 1
  command -v tput >/dev/null 2>&1 || return 1
  local palette
  palette=$(tput colors 2>/dev/null) || palette=0
  [[ "$palette" -ge 8 ]]
}

if _terminal_supports_colour; then
  C_BOLD=$(tput bold); C_DIM=$(tput dim); C_OFF=$(tput sgr0)
  C_CYAN=$(tput setaf 6); C_GREEN=$(tput setaf 2); C_AMBER=$(tput setaf 3)
else
  C_BOLD=""; C_DIM=""; C_OFF=""; C_CYAN=""; C_GREEN=""; C_AMBER=""
fi

# Every value this procedure writes (the env file and any CI secrets or
# variables) targets one project, resolved once, up front. The intro prints
# it, so a run from the wrong directory is caught before the first write.
PROJECT_ROOT="${PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
ENV_TARGET="${ENV_TARGET:-$PROJECT_ROOT/.env}"

_realdir() { (cd "$1" 2>/dev/null && pwd -P); }

_root_real=$(_realdir "$PROJECT_ROOT") || true
if [[ -z "$_root_real" ]]; then
  printf 'PROJECT_ROOT does not exist: %s\n' "$PROJECT_ROOT" >&2
  exit 1
fi
_env_dir_real=$(_realdir "$(dirname "$ENV_TARGET")") || true
if [[ -z "$_env_dir_real" ]]; then
  printf 'The folder for ENV_TARGET does not exist: %s\n' "$ENV_TARGET" >&2
  exit 1
fi
# Refuse to write outside the project: a stray ENV_TARGET would otherwise
# send the env file to one project while CI secrets land on another.
if [[ "$_env_dir_real" != "$_root_real" && "$_env_dir_real" != "$_root_real"/* ]]; then
  printf 'ENV_TARGET (%s) sits outside PROJECT_ROOT (%s).\n' "$_env_dir_real" "$_root_real" >&2
  printf 'Point PROJECT_ROOT at the project this run is for, so both land together.\n' >&2
  exit 1
fi
PROJECT_ROOT="$_root_real"
ENV_TARGET="$_env_dir_real/$(basename "$ENV_TARGET")"

STEP_COUNT=0
STEP_TOTAL=0
ENV_KEYS_WRITTEN=()
CI_NAMES_WRITTEN=()
LEFT_FOR_LATER=()

_wipe_screen() {
  [[ "$_TTY" -eq 1 ]] || return 0
  local has_tput=0
  command -v tput >/dev/null 2>&1 && has_tput=1
  if [[ "$has_tput" -eq 1 ]]; then
    tput clear
    return
  fi
  # No tput on this box: fall back to the raw ANSI "clear screen + scrollback" sequence.
  printf '\033[2J\033[3J\033[H'
}

# intro "Title" - opening frame, then waits for the human to say go.
intro() {
  _wipe_screen
  printf '\n%s%s%s%s\n' "$C_BOLD" "$C_CYAN" "$1" "$C_OFF"
  printf '%s%s steps - writing to %s%s\n\n' "$C_DIM" "$STEP_TOTAL" "$ENV_TARGET" "$C_OFF"
  printf '%sYou do the clicking; this script tells you where and captures what you\n' "$C_DIM"
  printf 'copy back. Ctrl-C is safe at any point - run it again later and it will\n'
  printf 'offer what you already saved as the default.%s\n' "$C_OFF"
  wait_for_enter "Ready?"
}

# begin_step "Name" - clears the screen and prints the step header with
# progress, so only the current step is ever on screen at once.
begin_step() {
  _wipe_screen
  STEP_COUNT=$((STEP_COUNT + 1))
  printf '\n%s%s[%s/%s] %s%s\n' "$C_BOLD" "$C_CYAN" "$STEP_COUNT" "$STEP_TOTAL" "$1" "$C_OFF"
}

explain()  { printf '  %s\n' "$1"; }
instruct() { printf '  %s->%s %s\n' "$C_CYAN" "$C_OFF" "$1"; }
aside()    { printf '  %s%s%s\n' "$C_DIM" "$1" "$C_OFF"; }
caution()  { printf '  %s!! %s%s\n' "$C_AMBER" "$1" "$C_OFF"; }

# visit URL - opens it in the human's default browser; falls back to
# printing it if nothing on this machine can open a browser.
visit() {
  local url="$1" opener found=0
  printf '  %s>> %s%s\n' "$C_GREEN" "$url" "$C_OFF"
  for opener in xdg-open open wslview explorer.exe; do
    if command -v "$opener" >/dev/null 2>&1; then
      "$opener" "$url" >/dev/null 2>&1 && found=1 || true
      break
    fi
  done
  [[ "$found" -eq 1 ]] || caution "could not launch a browser - open this manually: $url"
}

wait_for_enter() {
  printf '  %s%s%s ' "$C_DIM" "${1:-Press Enter when you are ready}" "$C_OFF"
  read -r _ || true
}

# confirm_or_skip "question" - yes/no gate for anything that cannot be
# undone. Success (0) means yes.
confirm_or_skip() {
  local answer=""
  printf '  %s?? %s [y/N] %s' "$C_AMBER" "$1" "$C_OFF"
  read -r answer || true
  [[ "$answer" =~ ^[Yy] ]]
}

# _saved_value KEY - the current value for KEY already in ENV_TARGET, if
# any, unquoted. Lets re-runs offer the real value as a default.
_saved_value() {
  [[ -f "$ENV_TARGET" ]] || return 1
  local raw
  raw=$(grep -E "^${1}=" "$ENV_TARGET" | tail -n1) || return 1
  raw="${raw#*=}"
  if [[ "$raw" == \"*\" ]]; then
    raw="${raw#\"}"; raw="${raw%\"}"
    raw="${raw//\\\"/\"}"; raw="${raw//\\\$/\$}"; raw="${raw//\\\\/\\}"
  fi
  printf '%s' "$raw"
}

# _input_closed - input ended (Ctrl-D, or a pipe ran dry) before a
# required answer arrived. Stop, rather than re-prompt forever.
_input_closed() {
  printf '\n'
  caution "input closed before this was answered - stopping; run it again to carry on"
  exit 1
}

# collect VAR "Prompt" - visible input, re-prompting until non-empty; Enter
# alone keeps a previously saved value.
collect() {
  local var="$1" prompt="$2" saved answer
  saved=$(_saved_value "$var" || true)
  while :; do
    if [[ -n "$saved" ]]; then
      printf '  %s%s%s %s[Enter keeps the saved value]%s ' "$C_BOLD" "$prompt" "$C_OFF" "$C_DIM" "$C_OFF"
    else
      printf '  %s%s%s ' "$C_BOLD" "$prompt" "$C_OFF"
    fi
    read -r answer || [[ -n "$answer" ]] || _input_closed
    [[ -z "$answer" && -n "$saved" ]] && answer="$saved"
    [[ -n "$answer" ]] && break
    caution "that cannot be empty - try again"
  done
  printf -v "$var" '%s' "$answer"
}

# collect_hidden VAR "Prompt" - same as collect, but nothing is echoed.
collect_hidden() {
  local var="$1" prompt="$2" saved answer
  saved=$(_saved_value "$var" || true)
  while :; do
    if [[ -n "$saved" ]]; then
      printf '  %s%s%s %s[Enter keeps the saved value]%s ' "$C_BOLD" "$prompt" "$C_OFF" "$C_DIM" "$C_OFF"
    else
      printf '  %s%s%s ' "$C_BOLD" "$prompt" "$C_OFF"
    fi
    read -rs answer || [[ -n "$answer" ]] || _input_closed
    printf '\n'
    [[ -z "$answer" && -n "$saved" ]] && answer="$saved"
    [[ -n "$answer" ]] && break
    caution "that cannot be empty - try again"
  done
  printf -v "$var" '%s' "$answer"
}

# env_upsert KEY VALUE - write or replace KEY="VALUE" in ENV_TARGET.
# Idempotent: running it twice with the same value leaves the file
# unchanged aside from ordering. Refuses a value containing a newline
# rather than writing a broken line.
# _quote_for_env VALUE - backslash-escape the three characters that would
# otherwise break a double-quoted dotenv line, in the order that keeps the
# escaping reversible (backslashes first, or a later pass would double-escape
# the backslashes just introduced for the quote and dollar cases).
_quote_for_env() {
  local out="$1"
  out=${out//\\/\\\\}
  out=${out//\"/\\\"}
  out=${out//\$/\\\$}
  printf '%s' "$out"
}

env_upsert() {
  local key="$1" value="$2" scratch rc=0
  if [[ "$value" == *$'\n'* ]]; then
    caution "not writing $key - the value has a newline in it"
    LEFT_FOR_LATER+=("$key in $ENV_TARGET (multiline value, add by hand)")
    return
  fi
  touch "$ENV_TARGET"
  scratch=$(mktemp)
  # grep exits 1 when every line matched the key (nothing to keep); only
  # 2 or more means it failed, and moving that output in would lose the file.
  grep -vE "^${key}=" "$ENV_TARGET" > "$scratch" || rc=$?
  if (( rc > 1 )); then
    rm -f "$scratch"
    caution "could not read $ENV_TARGET - $key not saved"
    LEFT_FOR_LATER+=("$key in $ENV_TARGET (the file could not be read)")
    return
  fi
  printf '%s="%s"\n' "$key" "$(_quote_for_env "$value")" >> "$scratch"
  mv "$scratch" "$ENV_TARGET"
  ENV_KEYS_WRITTEN+=("$key")
  printf '  %s** saved%s %s -> %s\n' "$C_GREEN" "$C_OFF" "$key" "$ENV_TARGET"
}

# _gh_ready - true when the gh CLI is on PATH and already logged in. Both
# ci_secret and ci_variable check this first, so a missing or signed-out gh
# always falls through to the same "do it by hand" path rather than each
# helper failing differently.
_gh_ready() {
  command -v gh >/dev/null 2>&1 || return 1
  gh auth status >/dev/null 2>&1
}

# ci_secret NAME VALUE - set a repository secret via the gh CLI, run from
# PROJECT_ROOT so it lands on the same repository as the env file. Records
# a follow-up instead of failing if gh is not ready.
ci_secret() {
  local name="$1" value="$2" ok=1
  _gh_ready || ok=0
  if [[ "$ok" -eq 1 ]]; then
    printf '%s' "$value" | (cd "$PROJECT_ROOT" && gh secret set "$name") >/dev/null 2>&1 || ok=0
  fi
  if [[ "$ok" -eq 1 ]]; then
    CI_NAMES_WRITTEN+=("$name")
    printf '  %s** set%s repository secret %s\n' "$C_GREEN" "$C_OFF" "$name"
    return
  fi
  LEFT_FOR_LATER+=("repository secret $name (gh secret set $name)")
  caution "could not set $name - gh is not ready; do it later"
}

# ci_variable NAME VALUE - as ci_secret, for a non-secret repository
# variable.
ci_variable() {
  local name="$1" value="$2" ok=1
  _gh_ready || ok=0
  if [[ "$ok" -eq 1 ]]; then
    (cd "$PROJECT_ROOT" && gh variable set "$name" --body "$value") >/dev/null 2>&1 || ok=0
  fi
  if [[ "$ok" -eq 1 ]]; then
    CI_NAMES_WRITTEN+=("$name")
    printf '  %s** set%s repository variable %s\n' "$C_GREEN" "$C_OFF" "$name"
    return
  fi
  LEFT_FOR_LATER+=("repository variable $name")
  caution "could not set $name - gh is not ready; do it later"
}

# wrap_up - final summary of what was written and what still needs doing.
wrap_up() {
  _wipe_screen
  printf '\n%s%sDone%s\n' "$C_BOLD" "$C_GREEN" "$C_OFF"
  if (( ${#ENV_KEYS_WRITTEN[@]} )); then
    aside "saved ${#ENV_KEYS_WRITTEN[@]} value(s) to $ENV_TARGET: ${ENV_KEYS_WRITTEN[*]}"
  fi
  if (( ${#CI_NAMES_WRITTEN[@]} )); then
    aside "set ${#CI_NAMES_WRITTEN[@]} repository secret/variable(s): ${CI_NAMES_WRITTEN[*]}"
  fi
  if (( ${#LEFT_FOR_LATER[@]} )); then
    printf '\n'
    caution "still to finish by hand:"
    for item in "${LEFT_FOR_LATER[@]}"; do
      aside "  - $item"
    done
  fi
  printf '\n'
}

# ---------------------------------------------------------------------------
# STEPS - author this section. One begin_step() per action the human takes.
# Replace the sample step below and set STEP_TOTAL to match.
# ---------------------------------------------------------------------------

STEP_TOTAL=1

intro "Example service setup"

# -- Sample step: replace with the real procedure -------------------------
begin_step "Example service - API keys"
explain "This collects the API keys and saves them for local use and CI."
visit "https://example.com/dashboard/api-keys"
instruct "Copy the publishable key shown on that page."
collect EXAMPLE_PUBLISHABLE_KEY "Paste the publishable key:"
instruct "Click Reveal secret key, then copy it."
collect_hidden EXAMPLE_SECRET_KEY "Paste the secret key:"
env_upsert EXAMPLE_PUBLISHABLE_KEY "$EXAMPLE_PUBLISHABLE_KEY"
env_upsert EXAMPLE_SECRET_KEY "$EXAMPLE_SECRET_KEY"
ci_secret EXAMPLE_SECRET_KEY "$EXAMPLE_SECRET_KEY"   # only if CI actually reads it
# ---------------------------------------------------------------------------

wrap_up
