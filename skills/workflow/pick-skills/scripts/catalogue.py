#!/usr/bin/env python3
"""Print what `pick-skills` needs to choose a matched set of skills for this project.

Run with no arguments from anywhere inside a project:

    python3 catalogue.py

It reports, for the current project (found by walking up to the nearest
`.git`, falling back to the current folder):

1. Stack signals found in the project folder.
2. The current `.agent-skills` and `.agent-skills.local` manifests, or a
   note that neither exists yet.
3. What is currently linked into `.claude/skills` and `.agents/skills`.
4. Every skill in the library, with its description and whether it is
   typed-only (`disable-model-invocation: true`).

No arguments are required and no external packages are used, only the
standard library.
"""
import re
import sys
from pathlib import Path


def library_root() -> Path:
    """Resolve the real library root from this file's own location.

    This script is normally reached through a symlink, e.g.
    <project>/.claude/skills/pick-skills/scripts/catalogue.py ->
    <library>/skills/<category>/pick-skills/scripts/catalogue.py. Path.resolve()
    follows symlinks; from there walk up to the folder that holds `skills/`.
    """
    real = Path(__file__).resolve()
    for candidate in real.parents:
        if (candidate / "skills").is_dir() and (candidate / "sets").is_dir():
            return candidate
    return real.parents[3]


def project_root() -> Path:
    """Walk up from the current folder to the nearest `.git`."""
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if (candidate / ".git").exists():
            return candidate
    return here


def frontmatter_field(text: str, field: str) -> str:
    """Pull one top-level frontmatter field, handling folded (`>-`) blocks."""
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return ""
    lines = m.group(1).split("\n")
    value_lines = []
    capturing = False
    for line in lines:
        top = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if top:
            if capturing:
                break
            if top.group(1) == field:
                capturing = True
                first = top.group(2).strip()
                if first not in (">-", ">", "|", "|-", ""):
                    value_lines.append(first.strip("'\""))
            continue
        if capturing and line.startswith((" ", "\t")):
            value_lines.append(line.strip())
        elif capturing:
            break
    return " ".join(value_lines).strip()


def library_skills(lib: Path):
    """Yield (name, description, typed_only) for every skill in the library."""
    skills_dir = lib / "skills"
    if not skills_dir.is_dir():
        return
    entries = sorted(skills_dir.iterdir()) + sorted(
        sub for cat in skills_dir.iterdir() if cat.is_dir() for sub in cat.iterdir())
    for entry in entries:
        skill_md = entry / "SKILL.md"
        if entry.name.startswith((".", "_")) or not skill_md.is_file():
            continue
        text = skill_md.read_text(errors="replace")
        description = frontmatter_field(text, "description") or "(no description)"
        typed_only = frontmatter_field(text, "disable-model-invocation").lower() == "true"
        yield entry.name, description, typed_only


STACK_CHECKS = {
    "artisan": "Laravel",
    "composer.json": "PHP/Composer",
    "package.json": "Node",
    "requirements.txt": "Python (pip)",
    "pyproject.toml": "Python",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
    "Package.swift": "Swift",
    "src-tauri": "Tauri",
    "nuxt.config.js": "Nuxt",
    "nuxt.config.ts": "Nuxt",
    "resources/views/livewire": "Livewire",
    "app/Filament": "Filament",
    "tailwind.config.js": "Tailwind",
    "tailwind.config.ts": "Tailwind",
    "tests/Pest.php": "Pest",
    "phpunit.xml": "PHPUnit/Pest",
    "Dockerfile": "Docker",
    "docker-compose.yml": "Docker",
    ".git": "git repository",
}


def stack_signals(root: Path):
    found = []
    for rel, label in STACK_CHECKS.items():
        if (root / rel).exists():
            found.append(label)
    return sorted(set(found))


def read_manifest(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(errors="replace").rstrip("\n")


def linked_names(root: Path):
    """Names of every symlinked skill in both tool folders, from any library."""
    names = set()
    for rel in (".claude/skills", ".agents/skills"):
        d = root / rel
        if not d.is_dir():
            continue
        for entry in d.iterdir():
            if entry.is_symlink():
                names.add(entry.name)
    return sorted(names)


def main() -> int:
    lib = library_root()
    root = project_root()

    print(f"# pick catalogue for {root}")
    print(f"library: {lib}\n")

    signals = stack_signals(root)
    print("## Stack signals")
    print(", ".join(signals) if signals else "(none found)")

    print("\n## .agent-skills")
    manifest = read_manifest(root / ".agent-skills")
    print(manifest if manifest else "(no .agent-skills file yet)")

    local_manifest = read_manifest(root / ".agent-skills.local")
    if local_manifest:
        print("\n## .agent-skills.local")
        print(local_manifest)

    print("\n## Currently linked")
    linked = linked_names(root)
    print(", ".join(linked) if linked else "(nothing linked)")

    skills = list(library_skills(lib))
    print(f"\n## Library ({len(skills)} skills; * = typed-only, only runs when asked for by name)")
    if not skills:
        print(f"(no skills found under {lib / 'skills'}; is this the right library root?)")
    for name, description, typed_only in skills:
        flag = "*" if typed_only else " "
        print(f"{flag} {name}: {description}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
