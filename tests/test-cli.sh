#!/usr/bin/env bash
# End-to-end test of bin/agent-skills against a throwaway library, project
# and home folder. Run: bash tests/test-cli.sh

set -uo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd -P)
tmp=$(cd "$(mktemp -d)" && pwd -P)
trap 'rm -rf "$tmp"' EXIT

lib="$tmp/library"
mkdir -p "$lib/bin" "$lib/skills" "$lib/sets"
cp "$repo/bin/agent-skills" "$lib/bin/"
for s in alpha beta gamma; do
    mkdir -p "$lib/skills/$s"
    printf -- '---\nname: %s\ndescription: Test skill %s.\n---\nBody.\n' "$s" "$s" > "$lib/skills/$s/SKILL.md"
done
mkdir -p "$lib/skills/group/delta"   # a skill inside a category folder
printf -- '---\nname: delta\ndescription: Test skill delta.\n---\nBody.\n' > "$lib/skills/group/delta/SKILL.md"
printf 'alpha\nbeta # a comment\n' > "$lib/sets/pair.txt"

export HOME="$tmp/home"
mkdir -p "$HOME/bin"
ln -s "$lib/bin/agent-skills" "$HOME/bin/agent-skills"   # run through a symlink, as installed
cli="$HOME/bin/agent-skills"

project="$tmp/project"
mkdir -p "$project/sub"
git -C "$project" init -q

fails=0
check() {
    if eval "$2"; then echo "ok   $1"; else echo "FAIL $1"; fails=$((fails + 1)); fi
}
ours() { [ -L "$1" ] && [[ "$(readlink "$1")" == "$lib/skills/"* ]]; }

cd "$project/sub"   # commands work from a subfolder of the project
"$cli" add pair >/dev/null
check "set adds to Claude folder" 'ours "$project/.claude/skills/alpha" && ours "$project/.claude/skills/beta"'
check "set adds to Codex folder" 'ours "$project/.agents/skills/alpha" && ours "$project/.agents/skills/beta"'
check "unknown skill reported" '"$cli" add nope > "$tmp/s3"; grep -q "no such skill" "$tmp/s3"'
check "list set shows only its skills" '[ "$("$cli" list pair | tr "\n" " ")" = "alpha beta " ]'
check "list skills shows all" '[ "$("$cli" list skills | grep -c .)" = 4 ]'

"$cli" add delta >/dev/null
check "skill in a category folder links" 'ours "$project/.claude/skills/delta" && [ -f "$project/.claude/skills/delta/SKILL.md" ]'
"$cli" remove delta >/dev/null

mkdir -p "$project/.agents/skills/gamma"   # the user's own Codex copy
"$cli" add gamma >/dev/null
check "own copy left alone" '[ -d "$project/.agents/skills/gamma" ] && [ ! -L "$project/.agents/skills/gamma" ]'
check "Claude link still made" 'ours "$project/.claude/skills/gamma"'
check "status flags half-linked" '"$cli" status > "$tmp/s1"; grep -q "gamma.*Claude Code only" "$tmp/s1"'
rm -rf "$project/.agents/skills/gamma"

ln -s /elsewhere "$project/.claude/skills/foreign"
"$cli" remove alpha >/dev/null
check "remove clears both folders" '[ ! -e "$project/.claude/skills/alpha" ] && [ ! -e "$project/.agents/skills/alpha" ]'

"$cli" init --force >/dev/null
check "init records linked skills" 'grep -qx beta "$project/.agent-skills" && ! grep -qx alpha "$project/.agent-skills"'

printf 'alpha\n' > "$project/.agent-skills"
printf 'gamma\n' > "$project/.agent-skills.local"
"$cli" sync >/dev/null
check "sync matches manifest plus local" 'ours "$project/.claude/skills/alpha" && ours "$project/.claude/skills/gamma" && [ ! -e "$project/.claude/skills/beta" ]'
check "sync leaves foreign links alone" '[ -L "$project/.claude/skills/foreign" ]'

"$cli" home add beta >/dev/null
check "home add links both" 'ours "$HOME/.claude/skills/beta" && ours "$HOME/.agents/skills/beta"'
"$cli" home remove beta >/dev/null
check "home remove unlinks both" '[ ! -e "$HOME/.claude/skills/beta" ] && [ ! -e "$HOME/.agents/skills/beta" ]'

mkdir -p "$lib/skills/private/mine"   # a personal, git-ignored skill
printf -- '---\nname: mine\ndescription: Test skill mine.\n---\nBody.\n' > "$lib/skills/private/mine/SKILL.md"
check "list marks private skills" '"$cli" list skills | grep -qx "mine (private)"'
"$cli" add mine beta >/dev/null
check "private skill links" 'ours "$project/.claude/skills/mine" && ours "$project/.agents/skills/mine"'
check "status marks private skills" '"$cli" status > "$tmp/s4"; grep -q "mine.*(private)" "$tmp/s4"'
"$cli" init --force >/dev/null
check "init keeps private skills out of the shared file" '! grep -qx mine "$project/.agent-skills" && grep -qx beta "$project/.agent-skills"'
check "init puts private skills in the local file" 'grep -qx mine "$project/.agent-skills.local"'
"$cli" init --force >/dev/null
check "init adds a private skill to the local file once" '[ "$(grep -cx mine "$project/.agent-skills.local")" = 1 ]'
"$cli" sync >/dev/null
check "sync keeps private skills from the local file" 'ours "$project/.claude/skills/mine"'

rm -rf "$lib/skills/gamma"
check "status reports a removed skill" '"$cli" status > "$tmp/s2"; grep -q "gamma.*broken" "$tmp/s2"'

echo
if [ "$fails" = 0 ]; then echo "All checks passed"; else echo "$fails check(s) failed"; exit 1; fi
