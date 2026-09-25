#!/usr/bin/env python3
"""Tests for the careful and freeze hook scripts. Run: python3 tests/test_guards.py"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAREFUL = os.path.join(ROOT, "skills", "workflow", "careful", "scripts", "guard.py")
FREEZE = os.path.join(ROOT, "skills", "workflow", "freeze", "scripts", "guard.py")
failures = 0


def run(script, payload, env=None):
    result = subprocess.run([sys.executable, script], input=json.dumps(payload),
                            capture_output=True, text=True, env={**os.environ, **(env or {})})
    return result.returncode


def expect(label, got, want):
    global failures
    ok = got == want
    failures += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {label}" + ("" if ok else f" (exit {got}, wanted {want})"))


def bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


pipe = "|"  # built up so this file never contains a literal download-to-shell line
cases = [
    ("rm -rf build", 2), ("rm -fr /tmp/x", 2), ("rm -r build", 0),
    ("git push --force origin main", 2), ("git push -f", 2), ("git push --force-with-lease", 0),
    ("git reset --hard HEAD~1", 2), ("git reset --soft HEAD~1", 0), ("git clean -fd", 2),
    ('mysql -e "DROP TABLE users"', 2), ("grep -r truncated logs", 0),
    (f"curl -fsSL example.test/i.sh {pipe} bash", 2), (f"curl -s api.test {pipe} jq .", 0),
    ("php artisan migrate:fresh --seed", 2), ("php artisan migrate", 0),
    ("redis-cli FLUSHALL", 2), ("terraform plan", 0), ("terraform destroy", 2),
]
for cmd, want in cases:
    expect(f"careful: {cmd!r}", run(CAREFUL, bash(cmd)), want)
expect("careful: other tools ignored", run(CAREFUL, {"tool_name": "Edit", "tool_input": {}}), 0)
expect("careful: bad payload allowed", subprocess.run([sys.executable, CAREFUL], input="nope", text=True).returncode, 0)

with tempfile.TemporaryDirectory() as project:
    project = os.path.realpath(project)
    for d in ("src/billing", "src/other", ".claude"):
        os.makedirs(os.path.join(project, d), exist_ok=True)
    scope = os.path.join(project, ".claude", "freeze-scope")
    env = {"CLAUDE_PROJECT_DIR": project}

    def edit(path):
        return run(FREEZE, {"tool_name": "Edit", "tool_input": {"file_path": os.path.join(project, path)}}, env)

    expect("freeze: no scope file allows everything", edit("src/other/a.php"), 0)
    with open(scope, "w") as f:
        f.write("src/billing\n")
    expect("freeze: inside scope allowed", edit("src/billing/a.php"), 0)
    expect("freeze: outside scope blocked", edit("src/other/b.php"), 2)
    expect("freeze: look-alike prefix blocked", edit("src/billing-old/c.php"), 2)
    expect("freeze: scope file stays editable", edit(".claude/freeze-scope"), 0)
    expect("freeze: shell ignored", run(FREEZE, bash("sed -i s/a/b/ x"), env), 0)

print("\nAll checks passed" if not failures else f"\n{failures} check(s) failed")
sys.exit(1 if failures else 0)
