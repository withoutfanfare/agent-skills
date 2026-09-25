#!/usr/bin/env python3
"""Usage tracking for agent-skills: an optional hook, and a report.

    track.py log            hook mode: reads a PreToolUse payload on stdin and
                            appends one line per Skill call to the usage log
    track.py report [days]  prints use per skill for the last N days (default 30)
    track.py report --json  the same as JSON, for tools and the usage-audit skill

The log is a local file (one JSON object per line), never sent anywhere:
$AGENT_SKILLS_LOG, or ~/.local/share/agent-skills/usage.jsonl by default.
A "use" is one skill in one session, however many times it was called.
"""
import datetime as dt
import glob
import json
import os
import sys

LOG = os.environ.get("AGENT_SKILLS_LOG") or os.path.expanduser("~/.local/share/agent-skills/usage.jsonl")
LIBRARY = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def log():
    """Hook mode. Never blocks the tool call, whatever happens."""
    try:
        payload = json.load(sys.stdin)
        if payload.get("tool_name") != "Skill":
            return 0
        skill = (payload.get("tool_input") or {}).get("skill") or ""
        cwd = payload.get("cwd") or os.getcwd()
        entry = {
            "time": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "skill": skill,
            "project": os.path.basename(cwd.rstrip("/")),
            "session": payload.get("session_id", ""),
        }
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:  # a broken log must never stop the agent working
        pass
    return 0


def library_skills():
    """Every skill in the library, one or two folders below skills/."""
    skills = {}
    folder = os.path.join(LIBRARY, "skills")
    for pattern in ("*", "*/*"):
        for path in sorted(glob.glob(os.path.join(folder, pattern, "SKILL.md"))):
            name = os.path.basename(os.path.dirname(path))
            head = open(path, encoding="utf-8").read(2000)
            skills[name] = "disable-model-invocation: true" in head
    return skills


def report(args):
    as_json = "--json" in args
    numbers = [a for a in args if a.isdigit()]
    days = int(numbers[0]) if numbers else 30
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%Y-%m-%d")
    uses, projects, last = {}, {}, {}
    seen = set()
    if os.path.isfile(LOG):
        for line in open(LOG, encoding="utf-8"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("time", "")[:10] < since or not e.get("skill"):
                continue
            skill = e["skill"].split(":")[-1]  # plugin skills are logged as plugin:name
            key = (skill, e.get("session") or e.get("time"))
            if key in seen:
                continue
            seen.add(key)
            uses[skill] = uses.get(skill, 0) + 1
            projects.setdefault(skill, set()).add(e.get("project", ""))
            last[skill] = max(last.get(skill, ""), e["time"][:10])
    library = library_skills()
    unused = [s for s in library if s not in uses]
    if as_json:
        json.dump({"days": days, "log": LOG,
                   "skills": {s: {"uses": uses[s], "projects": len(projects[s]), "last_used": last[s],
                                  "in_library": s in library, "typed": library.get(s)}
                              for s in sorted(uses, key=lambda s: -uses[s])},
                   "unused": unused}, sys.stdout, indent=2)
        print()
        return 0
    if not uses:
        print(f"No skill use logged in the last {days} days.")
        print("Tracking is optional; see: agent-skills track")
        return 0
    print(f"Skill use, last {days} days ({sum(uses.values())} uses)\n")
    print(f"{'Skill':<28}{'Uses':>6}{'Projects':>10}  Last used")
    for s in sorted(uses, key=lambda s: (-uses[s], s)):
        note = "" if s in library else "  (not in this library)"
        print(f"{s:<28}{uses[s]:>6}{len(projects[s]):>10}  {last[s]}{note}")
    print(f"\nLibrary skills not used: {len(unused)} of {len(library)}")
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "report"
    sys.exit(log() if mode == "log" else report(sys.argv[2:]))
