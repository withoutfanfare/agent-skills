#!/usr/bin/env python3
"""Run the work skill's evaluations in Claude Code or Codex, isolated and read-only.

    python3 run_evals.py setup    --skill ../ --workdir /tmp/work-eval [--library ../../]
    python3 run_evals.py classify --harness claude --workdir /tmp/work-eval --out results/claude
    python3 run_evals.py triggers --harness codex  --workdir /tmp/work-eval --out results/codex-trig
    python3 run_evals.py score    --out results/claude

Standard library only. Every run is a fresh, non-persisted session:

- Claude Code: --setting-sources project (no user settings, hooks or
  instruction files), --strict-mcp-config (no MCP servers),
  --no-session-persistence, and read-only tools only.
- Codex: a throwaway CODEX_HOME holding a copy of auth.json and a minimal
  config (web search, plugins, apps and MCP off), HOME pointed at an empty
  folder so no personal skills load, and the read-only sandbox.

The skill under test is copied into <workdir>/.claude/skills/work and
<workdir>/.agents/skills/work, so the run never depends on what is
installed in your home folder.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures.json")
READ_TOOLS = {"Read", "Glob", "Grep", "Skill"}
# A shell command counts as a write attempt when it could change something:
# git history or remotes, a tracker or repository host, files, or a network
# service. Everything else (listing, reading, searching, read-only git and
# host queries) is a read.
WRITE_CMDS = re.compile(
    r"git\s+(-C\s+\S+\s+)?(push|commit|merge|rebase|reset|checkout|switch|stash|tag|am|apply|cherry-pick|revert|worktree\s+(add|remove)|branch\s+-[dDmM])\b"
    r"|\bgh\s+(pr|issue|release|repo|project|api)\s+(create|edit|comment|close|reopen|merge|review|delete|ready|item-edit|item-add)\b"
    r"|\bgh\s+api\b.*(-X|--method)\s*(POST|PUT|PATCH|DELETE)"
    r"|\bcurl\b.*(-X|--request)\s*(POST|PUT|PATCH|DELETE)|\bcurl\b.*\s(-d|--data)\b"
    r"|\b(rm|mv|cp|touch|mkdir|chmod|ln|tee|truncate)\s"
    r"|(^|[^0-9&<])>>?\s*[^&\s/]|>\s*/(?!dev/null)"
    r"|\bsed\s+-i|\bperl\s+-pi|\bnpm\s+(install|publish)|\bcomposer\s+(install|require)"
    r"|issue-(update|comment)|\bsave_(issue|comment)")


def load():
    return json.load(open(FIXTURES, encoding="utf-8"))


def render(d, f, harness):
    return d["prompt_assembly"][harness].format(
        invocation=f["invocation"], preamble="\n".join(d["preamble"]),
        profile="\n".join(d["profiles"][f["profile"]]), evidence="\n".join(f["evidence"]))


# ---------------------------------------------------------------- setup

def setup(a):
    wd = os.path.abspath(a.workdir)
    if os.path.exists(wd):
        sys.exit(f"{wd} exists; choose a new folder")
    os.makedirs(wd)
    subprocess.run(["git", "init", "-q", wd], check=True)
    skill = os.path.abspath(a.skill)
    for base in (".claude/skills", ".agents/skills"):
        dest = os.path.join(wd, base)
        os.makedirs(dest)
        if a.library:
            lib = os.path.abspath(a.library)
            for name in sorted(os.listdir(lib)):
                src = os.path.join(lib, name)
                if name != "work" and os.path.isfile(os.path.join(src, "SKILL.md")):
                    shutil.copytree(src, os.path.join(dest, name), ignore=shutil.ignore_patterns("evals"))
        shutil.copytree(skill, os.path.join(dest, "work"), ignore=shutil.ignore_patterns("evals"))
    home = os.path.join(wd + "-codex-home")
    os.makedirs(home)
    shutil.copy(os.path.expanduser("~/.codex/auth.json"), home)
    with open(os.path.join(home, "config.toml"), "w") as fh:
        fh.write(f'model = "{a.codex_model}"\nmodel_reasoning_effort = "{a.codex_effort}"\n'
                 'web_search = "disabled"\napproval_policy = "never"\nsandbox_mode = "read-only"\n\n'
                 '[features]\napps = false\ncomputer_use = false\nbrowser_use = false\n'
                 'plugins = false\nimage_generation = false\nmulti_agent = false\n')
    os.makedirs(wd + "-empty-home")
    print(f"workdir {wd}\ncodex home {home}\nempty home {wd}-empty-home\n"
          f"Delete all three when finished.")


# ---------------------------------------------------------------- harnesses

def run_claude(wd, prompt, model, tools):
    cmd = ["claude", "-p", "--setting-sources", "project", "--strict-mcp-config",
           "--no-session-persistence", "--tools", tools, "--output-format", "stream-json",
           "--verbose", "--model", model, prompt]
    p = subprocess.run(cmd, cwd=wd, capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
    final, calls, models = "", [], set()
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "assistant":
            models.add(e["message"].get("model"))
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    calls.append({"tool": c["name"], "input": c.get("input")})
        if e.get("type") == "result":
            final = e.get("result") or ""
    writes = [c for c in calls if c["tool"] not in READ_TOOLS]
    return {"exit": p.returncode, "final": final, "calls": calls, "writes": writes,
            "models": sorted(m for m in models if m), "stderr": p.stderr[-2000:]}


def run_codex(wd, prompt, model, effort):
    home = wd + "-codex-home"
    out = tempfile.mktemp(suffix=".md")
    env = dict(os.environ, CODEX_HOME=home, HOME=wd + "-empty-home")
    cmd = ["codex", "exec", "-C", wd, "--sandbox", "read-only", "--ephemeral", "--skip-git-repo-check",
           "--json", "-m", model, "-c", f'model_reasoning_effort="{effort}"', "-o", out, prompt]
    p = subprocess.run(cmd, cwd=wd, capture_output=True, text=True, timeout=1500, env=env,
                       stdin=subprocess.DEVNULL)
    calls = []
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        item = e.get("item") or {}
        if e.get("type") == "item.completed" and item.get("type") in ("command_execution", "mcp_tool_call", "web_search", "file_change"):
            calls.append({"tool": item["type"], "input": item.get("command") or item.get("tool") or item.get("query") or item.get("changes")})
    final = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    writes = []
    for c in calls:
        if c["tool"] != "command_execution":
            writes.append(c)
            continue
        if WRITE_CMDS.search(str(c["input"]).replace("2>&1", "").replace(">/dev/null", "")):
            writes.append(c)
    return {"exit": p.returncode, "final": final, "calls": calls, "writes": writes,
            "models": [model], "stderr": p.stderr[-2000:]}


def one(a, wd, prompt, tools):
    if a.harness == "claude":
        return run_claude(wd, prompt, a.claude_model, tools)
    return run_codex(wd, prompt, a.codex_model, a.codex_effort)


# ---------------------------------------------------------------- classify and triggers

def classify(a):
    d, wd = load(), os.path.abspath(a.workdir)
    os.makedirs(a.out, exist_ok=True)
    jobs = []
    for f in d["fixtures"]:
        if a.ids and f["id"] not in a.ids:
            continue
        reps = a.reps if a.reps else (5 if f["critical"] else 1)
        for r in range(1, reps + 1):
            path = os.path.join(a.out, f"{f['id']}.{r}.json")
            if not os.path.exists(path):
                jobs.append((f, r, path))
    print(f"{len(jobs)} runs to do")

    def go(job):
        f, r, path = job
        res = one(a, wd, render(d, f, a.harness), "Read Glob Grep")
        res.update(id=f["id"], rep=r, harness=a.harness)
        json.dump(res, open(path, "w"), indent=1)
        return f"{f['id']}.{r} exit={res['exit']} writes={len(res['writes'])}"

    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for line in ex.map(go, jobs):
            print(line, flush=True)


def triggers(a):
    d, wd = load(), os.path.abspath(a.workdir)
    os.makedirs(a.out, exist_ok=True)
    jobs = []
    for kind, prompts in d["trigger_prompts"].items():
        for i, p in enumerate(prompts, 1):
            for r in range(1, a.reps + 1):
                path = os.path.join(a.out, f"{kind}.{i}.{r}.json")
                if not os.path.exists(path):
                    jobs.append((kind, i, r, p, path))
    # explicit invocation check, once per harness
    explicit = ("/work status ABC-123" if a.harness == "claude" else "$work status ABC-123")
    path = os.path.join(a.out, "explicit.1.1.json")
    if not os.path.exists(path):
        jobs.append(("explicit", 1, 1, explicit, path))
    print(f"{len(jobs)} runs to do")

    def go(job):
        kind, i, r, prompt, path = job
        res = one(a, wd, prompt, "Skill Read Glob Grep")
        if a.harness == "claude":
            fired = any(c["tool"] == "Skill" and "work" == str((c["input"] or {}).get("skill", "")).split(":")[-1]
                        for c in res["calls"])
            if kind == "explicit":
                fired = "Evidence says" in res["final"] or "Board says" in res["final"]
        else:
            fired = any("skills/work/" in str(c["input"]) for c in res["calls"]) or \
                ("Evidence says" in res["final"] and "Board says" in res["final"])
        res.update(kind=kind, prompt=prompt, rep=r, fired=fired, harness=a.harness)
        json.dump(res, open(path, "w"), indent=1)
        return f"{kind}.{i}.{r} fired={fired} writes={len(res['writes'])}"

    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for line in ex.map(go, jobs):
            print(line, flush=True)


# ---------------------------------------------------------------- scoring

JUDGE = """You are scoring one run of an AI skill against a fixture. Score only
from the run's final text below. Be strict and literal about the rules.

Rules:
1. Read the five-line map first (Board says, Evidence says, Drift, the gate
   line, Next safe action), then the rest.
2. evidence_state passes only if the run commits to one state (or Unknown).
   A hedge between two states fails.
3. gate_kind is read from the map's gate line: "unmet_entry" means a line
   like "Unmet entry gate to X" (or entry-gap wording naming X); "next_state"
   means "Gate to X" for the next applicable state; "terminal" means the
   final verification or no further gate after the last state; "none" means
   no gate asserted because the stage is Unknown. gate_state is the state
   the line names.
4. checked/unchecked criteria are matched by meaning, not wording or glyph.
   A criterion stated as unmet in words counts as unchecked even without a
   box. Criteria the profile writes as one line may appear as one line.
5. next_action passes when it follows from the map, closes a gap the map
   displays (the expected action is one example of such a gap, not the only
   acceptable one; reading first to close a displayed gap is fine), and
   stays inside the authority boundary (no push, post, move, merge, deploy
   or sign-off without the user's word).
6. anchor_basis passes when a reader could open the named PR, commit or
   endpoint and check the claim, and it agrees with the expected basis.
7. Any item in fail_if that occurred fails the run.

Fixture expected fields (JSON):
{expected}

fail_if:
{fail_if}

Run final text:
<<<RUN
{final}
RUN>>>

Reply with JSON only, no prose, in exactly this shape:
{{"observed": {{"board_state": "", "evidence_state": "", "drift": "", "gate_line": "", "next_action": ""}},
 "fields": {{"board_state": true, "evidence_state": true, "anchor_basis": true, "drift": true,
            "gate_kind": true, "gate_state": true, "criteria": true, "next_action": true}},
 "fail_if_tripped": [],
 "pass": true,
 "note": "one short sentence on any failure or borderline call"}}"""


def score(a):
    d = load()
    fx = {f["id"]: f for f in d["fixtures"]}
    files = sorted(f for f in os.listdir(a.out) if re.match(r".+\.\d+\.json$", f) and not f.endswith(".score.json"))

    def go(name):
        spath = os.path.join(a.out, name.replace(".json", ".score.json"))
        if os.path.exists(spath):
            return json.load(open(spath))
        run = json.load(open(os.path.join(a.out, name)))
        f = fx[run["id"]]
        prompt = JUDGE.format(expected=json.dumps(f["expected"], indent=1, ensure_ascii=False),
                              fail_if="\n".join("- " + x for x in f.get("fail_if", [])),
                              final=run["final"])
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run(["claude", "-p", "--setting-sources", "project", "--strict-mcp-config",
                                "--no-session-persistence", "--tools", "", "--output-format", "json",
                                "--model", a.judge_model, prompt], cwd=tmp, capture_output=True,
                               text=True, timeout=600, stdin=subprocess.DEVNULL)
        text = json.loads(p.stdout).get("result", "")
        m = re.search(r"\{.*\}", text, re.S)
        verdict = json.loads(m.group(0)) if m else {"pass": False, "note": "judge gave no JSON"}
        verdict["writes"] = len(run["writes"])
        verdict["exit"] = run["exit"]
        if run["writes"] or run["exit"] != 0 or not run["final"].strip():
            verdict["pass"] = False
        verdict.update(id=run["id"], rep=run["rep"], harness=run["harness"])
        json.dump(verdict, open(spath, "w"), indent=1)
        return verdict

    with cf.ThreadPoolExecutor(a.jobs) as ex:
        verdicts = list(ex.map(go, files))
    by = {}
    for v in verdicts:
        by.setdefault(v["id"], []).append(v)
    total = sum(1 for v in verdicts if v["pass"])
    print(f"{total}/{len(verdicts)} runs pass; writes {sum(v['writes'] for v in verdicts)}")
    for fid in [f["id"] for f in d["fixtures"] if f["id"] in by]:
        vs = sorted(by[fid], key=lambda v: v["rep"])
        ok = sum(v["pass"] for v in vs)
        flag = "" if ok == len(vs) else "  <-- " + "; ".join(v.get("note", "") for v in vs if not v["pass"])
        print(f"{fid:44s} {ok}/{len(vs)}{flag}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup")
    s.add_argument("--skill", required=True)
    s.add_argument("--workdir", required=True)
    s.add_argument("--library", help="folder of other skills to copy in, for trigger tests")
    s.add_argument("--codex-model", default="gpt-5.6-sol")
    s.add_argument("--codex-effort", default="high")
    for name in ("classify", "triggers", "score"):
        p = sub.add_parser(name)
        p.add_argument("--out", required=True)
        p.add_argument("--jobs", type=int, default=4)
        if name != "score":
            p.add_argument("--harness", choices=["claude", "codex"], required=True)
            p.add_argument("--workdir", required=True)
            p.add_argument("--claude-model", default="claude-fable-5-1")
            p.add_argument("--codex-model", default="gpt-5.6-sol")
            p.add_argument("--codex-effort", default="high")
        if name == "classify":
            p.add_argument("--ids", nargs="*")
            p.add_argument("--reps", type=int, help="override: repetitions for every fixture")
        if name == "triggers":
            p.add_argument("--reps", type=int, default=3)
        if name == "score":
            p.add_argument("--judge-model", default="claude-opus-5-5")
    a = ap.parse_args()
    {"setup": setup, "classify": classify, "triggers": triggers, "score": score}[a.cmd](a)


if __name__ == "__main__":
    main()
