#!/usr/bin/env bash
# Test scripts/lint.py against a throwaway library with known problems.
# Run: bash tests/test-lint.sh

set -uo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd -P)
tmp=$(cd "$(mktemp -d)" && pwd -P)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/scripts" "$tmp/skills"
cp "$repo/scripts/lint.py" "$tmp/scripts/"

skill() {  # skill <folder> <frontmatter lines> [body]
    mkdir -p "$tmp/skills/$1"
    printf -- '---\n%b\n---\n%b\n' "$2" "${3:-Body.}" > "$tmp/skills/$1/SKILL.md"
}

fails=0
check() {
    if eval "$2"; then echo "ok   $1"; else echo "FAIL $1"; fails=$((fails + 1)); fi
}

skill good 'name: good\ndescription: >-\n  Does a thing. Use when the user asks for the thing.'
python3 "$tmp/scripts/lint.py" > "$tmp/out" 2>&1
check "clean library passes" '[ $? = 0 ] && grep -q "ok: 1 skills clean" "$tmp/out"'

skill Bad-Name 'name: Bad-Name\ndescription: Something.'
skill mismatch 'name: other\ndescription: Something.'
skill nodesc 'name: nodesc'
skill typed 'name: typed\ndescription: Typed.\ndisable-model-invocation: true'
skill loose 'name: loose\ndescription: Loose.'
mkdir -p "$tmp/skills/loose/agents"
printf 'policy:\n  allow_implicit_invocation: false\n' > "$tmp/skills/loose/agents/openai.yaml"
skill dashes 'name: dashes\ndescription: Dashes.' 'One \xe2\x80\x94 two.'
skill secret 'name: secret\ndescription: Mentions acmecorp here.'
printf 'acmecorp\n!NOTES.md\n' > "$tmp/.lint-private-terms"
printf 'acmecorp is fine here\n' > "$tmp/NOTES.md"

python3 "$tmp/scripts/lint.py" > "$tmp/out" 2>&1
code=$?
check "findings exit non-zero" '[ "$code" = 1 ]'
check "bad name caught" 'grep -q "skills/Bad-Name: name must be lowercase" "$tmp/out"'
check "folder mismatch caught" 'grep -q "skills/mismatch: name .other. does not match" "$tmp/out"'
check "missing description caught" 'grep -q "skills/nodesc: description missing" "$tmp/out"'
check "typed without Codex policy caught" 'grep -q "skills/typed: typed-only skill needs" "$tmp/out"'
check "Codex policy without typed caught" 'grep -q "skills/loose: agents/openai.yaml turns off" "$tmp/out"'
check "em dash caught" 'grep -q "skills/dashes/SKILL.md:5: em dash" "$tmp/out"'
check "private term caught" 'grep -q "skills/secret/SKILL.md:3: private term" "$tmp/out"'
check "exempt file not flagged" '! grep -q "NOTES.md" "$tmp/out"'
check "good skill not flagged" '! grep -q "skills/good" "$tmp/out"'

echo
if [ "$fails" = 0 ]; then echo "All checks passed"; else cat "$tmp/out"; echo "$fails check(s) failed"; exit 1; fi
