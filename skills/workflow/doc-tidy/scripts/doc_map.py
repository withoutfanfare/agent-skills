#!/usr/bin/env python3
"""Map a markdown docs folder: broken internal links, broken anchors, and
files nothing else links to.

    python3 doc_map.py <docs-dir> [--ext .md,.mdx]

This does not fix anything or judge staleness; it only builds the link
graph and prints what it finds. Read the output, then decide what to do
about each item.

Output is plain text in three sections: broken links, broken anchors,
orphaned files (no incoming internal link and not named index/readme).
Exits 1 if it found any broken link or anchor, so it can gate a check.
"""
import argparse
import os
import re
import sys
from urllib.parse import unquote

# A destination is either <in angle brackets, spaces allowed> or bare.
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((<[^>]*>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")
# Reference-style: [text][ref] or the shortcut [text][], resolved against a
# [ref]: target definition elsewhere in the file.
REF_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\[([^\]]*)\]")
REF_DEF_RE = re.compile(r"^[ \t]{0,3}\[([^\]]+)\]:\s*(<[^>]*>|\S+)", re.M)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*$", re.M)
# A setext heading: a text line underlined with = (h1) or - (h2).
SETEXT_RE = re.compile(r"^[ \t]{0,3}(\S.*?)[ \t]*\n[ \t]{0,3}(=+|-+)[ \t]*$", re.M)
ANCHOR_ID_RE = re.compile(r'<a\s+[^>]*\b(?:id|name)\s*=\s*["\']([^"\']+)["\']', re.I)
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")
FOLDER_PAGES = ("readme", "index")


def slugify(heading):
    """Turn a heading into the anchor slug GitHub produces: lowercase,
    strip punctuation but keep Unicode letters, one hyphen per space."""
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s", "-", text)
    return text


def strip_code_fences(text):
    # Replace with the same number of newlines, not an empty string, so
    # line numbers after the fence are unaffected.
    return FENCE_RE.sub(lambda m: "\n" * m.group().count("\n"), text)


def heading_slugs(text):
    """Slugs for every heading (ATX and setext) plus explicit <a id>/name
    anchors. A repeated heading gets -1, -2 and so on, as GitHub and most
    renderers do."""
    slugs, seen = set(), {}
    headings = [heading for _, heading in HEADING_RE.findall(text)]
    headings += [heading for heading, _ in SETEXT_RE.findall(text)]
    for heading in headings:
        base = slugify(heading)
        count = seen.get(base, 0)
        seen[base] = count + 1
        slugs.add(base if count == 0 else f"{base}-{count}")
    slugs.update(ANCHOR_ID_RE.findall(text))
    return slugs


def ref_definitions(text):
    """Map of reference label (lowercased, per CommonMark) to raw target."""
    defs = {}
    for label, target in REF_DEF_RE.findall(text):
        defs[label.lower()] = target
    return defs


def folder_page(folder, exts):
    """The README or index page a link to a folder shows, if there is one."""
    for name in sorted(os.listdir(folder)):
        stem, ext = os.path.splitext(name)
        if stem.lower() in FOLDER_PAGES and ext in exts:
            return os.path.join(folder, name)
    return None


def find_docs(root, exts):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for name in filenames:
            if os.path.splitext(name)[1] in exts:
                yield os.path.join(dirpath, name)


def load(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docs_dir")
    parser.add_argument("--ext", default=".md,.markdown", help="comma-separated extensions to scan")
    args = parser.parse_args()

    root = os.path.abspath(args.docs_dir)
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    exts = {e if e.startswith(".") else f".{e}" for e in args.ext.split(",")}

    docs = sorted(find_docs(root, exts))
    if not docs:
        print(f"no {', '.join(exts)} files under {root}")
        return 0

    anchors_by_file = {}
    ref_defs_by_file = {}
    for path in docs:
        text = strip_code_fences(load(path))
        anchors_by_file[path] = heading_slugs(text)
        ref_defs_by_file[path] = ref_definitions(text)

    incoming = {path: 0 for path in docs}
    broken_links, broken_anchors = [], []

    def check_target(path, target, lineno):
        if target.startswith("<"):
            target = target[1:-1]
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
            return  # scheme link (http, mailto, tel...): not ours to check
        file_part, _, anchor = unquote(target).partition("#")
        if not file_part:
            if anchor and slugify(anchor) not in anchors_by_file[path]:
                broken_anchors.append((path, lineno, target))
            return
        candidate = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
        if os.path.isdir(candidate):
            candidate = folder_page(candidate, exts) or candidate
        if not os.path.isfile(candidate):
            broken_links.append((path, lineno, target))
            return
        if candidate in incoming:
            incoming[candidate] += 1
        if anchor and candidate in anchors_by_file and slugify(anchor) not in anchors_by_file[candidate]:
            broken_anchors.append((path, lineno, target))

    for path in docs:
        text = strip_code_fences(load(path))
        for lineno, line in enumerate(text.splitlines(), start=1):
            cleaned = CODE_SPAN_RE.sub("", line)
            for target in LINK_RE.findall(cleaned):
                check_target(path, target, lineno)
            for label, ref in REF_LINK_RE.findall(cleaned):
                key = (ref or label).lower()
                target = ref_defs_by_file[path].get(key)
                if target is None:
                    broken_links.append((path, lineno, f"[{label}][{ref}]"))
                    continue
                check_target(path, target, lineno)

    orphaned = [
        p for p in docs
        if incoming[p] == 0 and os.path.splitext(os.path.basename(p))[0].lower() not in {"index", "readme"}
    ]

    def rel(p):
        return os.path.relpath(p, root)

    print(f"Scanned {len(docs)} file(s) under {root}\n")

    print(f"## Broken links ({len(broken_links)})")
    for path, lineno, target in broken_links:
        print(f"  {rel(path)}:{lineno}  ->  {target}")

    print(f"\n## Broken anchors ({len(broken_anchors)})")
    for path, lineno, target in broken_anchors:
        print(f"  {rel(path)}:{lineno}  ->  {target}")

    print(f"\n## Orphaned files, no incoming internal link ({len(orphaned)})")
    for path in orphaned:
        print(f"  {rel(path)}")

    return 1 if (broken_links or broken_anchors) else 0


if __name__ == "__main__":
    sys.exit(main())
