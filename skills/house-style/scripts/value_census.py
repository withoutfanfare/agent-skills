#!/usr/bin/env python3
"""Count how often colour and length values recur across a codebase.

A value declared once in a hundred files is probably an accident; a value
that shows up in a dozen unrelated files is almost certainly part of the
design system, even if nobody wrote it down as a named token. This script
does not try to understand CSS structure, it just tallies raw values so a
reviewer can tell the difference quickly, before reading component code
line by line.

Usage:
    python3 value_census.py <directory> [--kind colour|length|both] [--min 2]

    python3 value_census.py src/ --kind colour
    python3 value_census.py resources/ --min 3

Only colour (hex, rgb(a), hsl(a)) and length (px, rem, em) literals are
counted. CSS variable *declarations* like `--brand: #2563eb;` are counted
under the value they declare, so a well-tokenised codebase naturally shows
its tokens as the highest counts. Tailwind utility classes (`bg-blue-600`,
`p-4`) are not literals, so they are not counted.

Dependency and build folders (node_modules, vendor, dist, public/build,
.git) are skipped, so only the project's own code is counted.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

SKIP_DIRS = {"node_modules", "vendor", "dist", ".git"}

STYLE_EXTENSIONS = {".css", ".scss", ".sass", ".less", ".vue", ".jsx", ".tsx", ".js", ".ts", ".blade.php", ".html"}

COLOUR_PATTERN = re.compile(
    r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]+\)|hsla?\([^)]+\)"
)
LENGTH_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?(?:px|rem|em)\b"
)


def skipped(path: Path, root: Path) -> bool:
    folders = path.relative_to(root).parts[:-1]
    if SKIP_DIRS.intersection(folders):
        return True
    return any(a == "public" and b == "build" for a, b in zip(folders, folders[1:]))


def iter_style_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or skipped(path, root):
            continue
        name = path.name.lower()
        if any(name.endswith(ext) for ext in STYLE_EXTENSIONS):
            yield path


def normalise_colour(value: str) -> str:
    value = value.strip()
    if value.startswith("#"):
        return value.lower()
    return re.sub(r"\s+", "", value.lower())


def census(root: Path, kind: str) -> Counter:
    counts = Counter()
    for path in iter_style_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if kind in ("colour", "both"):
            for match in COLOUR_PATTERN.finditer(text):
                counts[("colour", normalise_colour(match.group()))] += 1
        if kind in ("length", "both"):
            for match in LENGTH_PATTERN.finditer(text):
                counts[("length", match.group().lower())] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--kind", choices=["colour", "length", "both"], default="both")
    parser.add_argument("--min", type=int, default=2, help="Only show values seen at least this many times (default 2)")
    args = parser.parse_args()

    root = Path(args.directory)
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        sys.exit(1)

    counts = census(root, args.kind)
    if not counts:
        print("No colour or length values found.")
        return

    likely_tokens = [(k, v) for k, v in counts.items() if v >= args.min]
    likely_tokens.sort(key=lambda item: (-item[1], item[0]))

    print(f"Values seen {args.min}+ times (likely part of the system):\n")
    for (kind, value), count in likely_tokens:
        print(f"  {count:>4}  {kind:<7} {value}")

    one_offs = sum(1 for v in counts.values() if v < args.min)
    print(f"\n{one_offs} distinct value(s) seen fewer than {args.min} time(s): check these by hand before calling them drift.")


if __name__ == "__main__":
    main()
