#!/usr/bin/env python3
"""Check every skill in skills/ before it is committed.

    python3 scripts/lint.py

Checks each skill against the open Agent Skills format and this library's
house rules:

- name: lowercase letters, digits and single hyphens, at most 64
  characters, matching the folder name, without the reserved words
  "anthropic" or "claude"
- description: present, at most 1024 characters, no angle brackets
- SKILL.md: at most 500 lines
- a typed-only skill (disable-model-invocation: true) also has
  agents/openai.yaml with policy.allow_implicit_invocation: false, so Codex
  treats it the same way, and the reverse
- no em dashes (house style)
- no private terms: if a file called .lint-private-terms exists at the
  repository root (it is git-ignored), each non-blank line in it is a
  case-insensitive regular expression that must not appear anywhere in the
  repository's text files; a line starting with `!` names a file (glob,
  relative to the root) that the terms do not apply to, such as LICENSE

Exit code 0 = clean, 1 = findings.
"""
import fnmatch
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TEXT_EXT = {".md", ".txt", ".py", ".sh", ".yaml", ".yml", ".json", ".mjs", ".js", ""}
SKIP_DIRS = {".git", "__pycache__", "node_modules"}


def frontmatter(text):
    """Return (fields, body) from a SKILL.md, reading top-level keys only.

    Handles `key: value` and folded or literal blocks (`key: >-`). Nested
    maps (metadata, hooks) are recorded as present with an empty value.
    """
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    fields, key, block = {}, None, []
    for line in m.group(1).split("\n"):
        top = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if top:
            if key is not None and block:
                fields[key] = " ".join(block).strip()
            key, value, block = top.group(1), top.group(2).strip(), []
            if value in (">", ">-", "|", "|-", ""):
                fields[key] = ""
            else:
                fields[key] = value.strip("'\"")
                key = None
        elif key is not None and line.startswith((" ", "\t")):
            block.append(line.strip())
    if key is not None and block:
        fields[key] = " ".join(block).strip()
    return fields, m.group(2)


def private_terms():
    """Return (patterns, exempt file globs) from .lint-private-terms."""
    path = os.path.join(ROOT, ".lint-private-terms")
    if not os.path.isfile(path):
        return [], []
    lines = [l.strip() for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]
    return ([re.compile(l, re.I) for l in lines if not l.startswith("!")],
            [l[1:] for l in lines if l.startswith("!")])


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f == ".lint-private-terms":
                continue
            path = os.path.join(base, f)
            if os.path.splitext(f)[1] in TEXT_EXT and not os.path.islink(path):
                yield path


def check_skill(folder, findings):
    rel = f"skills/{folder}"
    path = os.path.join(SKILLS, folder, "SKILL.md")
    if not os.path.isfile(path):
        findings.append(f"{rel}: no SKILL.md")
        return False
    text = open(path, encoding="utf-8").read()
    fields, body = frontmatter(text)
    if fields is None:
        findings.append(f"{rel}/SKILL.md: no frontmatter block")
        return False

    name = fields.get("name", "")
    if name != folder:
        findings.append(f"{rel}: name '{name}' does not match the folder")
    if not NAME_RE.match(name) or len(name) > 64:
        findings.append(f"{rel}: name must be lowercase words joined by single hyphens, 64 characters at most")
    if re.search(r"anthropic|claude", name):
        findings.append(f"{rel}: name may not contain the reserved words 'anthropic' or 'claude'")

    desc = fields.get("description", "")
    if not desc:
        findings.append(f"{rel}: description missing")
    elif len(desc) > 1024:
        findings.append(f"{rel}: description is {len(desc)} characters (1024 at most)")
    if "<" in desc or ">" in desc:
        findings.append(f"{rel}: description contains angle brackets")

    lines = text.count("\n") + 1
    if lines > 500:
        findings.append(f"{rel}/SKILL.md: {lines} lines (500 at most; move detail into references/)")

    typed = fields.get("disable-model-invocation", "").lower() == "true"
    yaml_path = os.path.join(SKILLS, folder, "agents", "openai.yaml")
    yaml_text = open(yaml_path, encoding="utf-8").read() if os.path.isfile(yaml_path) else ""
    implicit_off = re.search(r"^\s*allow_implicit_invocation:\s*false\s*$", yaml_text, re.M)
    if typed and not implicit_off:
        findings.append(f"{rel}: typed-only skill needs agents/openai.yaml with allow_implicit_invocation: false")
    if implicit_off and not typed:
        findings.append(f"{rel}: agents/openai.yaml turns off implicit use, but SKILL.md does not")
    return typed


def main():
    findings, typed_count = [], 0
    folders = sorted(d for d in os.listdir(SKILLS)
                     if os.path.isdir(os.path.join(SKILLS, d)) and not d.startswith("."))
    for folder in folders:
        typed_count += bool(check_skill(folder, findings))

    terms, exempt = private_terms()
    for path in text_files():
        rel = os.path.relpath(path, ROOT)
        file_terms = [] if any(fnmatch.fnmatch(rel, g) for g in exempt) else terms
        try:
            lines = open(path, encoding="utf-8").read().split("\n")
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, 1):
            if "—" in line and rel.endswith(".md"):
                findings.append(f"{rel}:{n}: em dash (use a comma, colon or full stop)")
            for term in file_terms:
                if term.search(line):
                    findings.append(f"{rel}:{n}: private term /{term.pattern}/")

    if findings:
        print(f"{len(findings)} finding(s):")
        for f in findings:
            print(f"  x {f}")
        sys.exit(1)
    note = f", {len(terms)} private terms checked" if terms else ", no .lint-private-terms file"
    print(f"ok: {len(folders)} skills clean ({typed_count} typed-only){note}")


if __name__ == "__main__":
    main()
