#!/usr/bin/env python3
"""Group a log file into fingerprints, ranked by how often each occurs.

A production log is mostly the same handful of problems happening over and
over, wearing different ids, numbers and timestamps as disguises. This
script strips those off, groups what is left by exception class, message
shape and the first in-app stack frame, and prints a markdown table ranked
by count, so a person (or the log-triage skill) can decide what to look at
first instead of reading thousands of near-duplicate lines.

Reads a Laravel/Monolog-style log (`[2026-09-27 10:15:32] production.ERROR:
message {"context":...}` with an optional stack trace on following lines)
or a generic `timestamp level message` log, one entry per line or spread
over several lines when a stack trace follows.

Usage:
    python3 fingerprint_log.py <log-file> [--since ISO8601] [--limit 20]
    python3 fingerprint_log.py -                 # read from stdin
    python3 fingerprint_log.py storage/logs/laravel.log --since 2026-09-20

Standard library only, no dependencies. Identifying values found in a
trailing JSON context blob (keys such as user_id, tenant, email) are
counted per fingerprint but never printed. The Message column is only
partly redacted (ids, emails, numbers), so names, tokens and other values
can still appear in it: redact it before sharing the table.
"""
import argparse
import json
import re
import sys
from collections import OrderedDict
from datetime import datetime

LINE_START = re.compile(
    r"^\[?(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)\]?"
    r"\s+(?:(?P<channel>[\w-]+)\.)?"
    r"(?P<level>DEBUG|INFO|NOTICE|WARNING|WARN|ERROR|CRITICAL|ALERT|EMERGENCY|FATAL)"
    r"\b:?\s*(?P<message>.*)$",
    re.IGNORECASE,
)

EXCEPTION_RE = re.compile(r"(?:[A-Za-z_][A-Za-z0-9_]*\\)*[A-Za-z_][A-Za-z0-9_]*(?:Exception|Error)\b")
FRAME_RE = re.compile(r"(?P<path>[\w./\\-]+\.(?:php|py|js|ts|rb|go))(?:\((?P<l1>\d+)\)|:(?P<l2>\d+))")
VENDOR_HINTS = ("vendor/", "node_modules/", "site-packages/", "/dist/")
IN_APP_ANCHORS = ("app/", "src/")

UUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
LONGHEX_RE = re.compile(r"\b[0-9a-f]{16,}\b", re.IGNORECASE)
NUMBER_RE = re.compile(r"(?<![A-Za-z_])\d+")  # also "5123ms", not "v2"

# Per-request keys (request_id, trace_id...) are unique per entry and would
# make one user's repeated error look widespread, so they are not counted.
IDENTIFYING_KEYS = re.compile(r"(_id|^id$|user|tenant|account|customer|email)", re.IGNORECASE)
PER_REQUEST_KEYS = re.compile(r"(request|trace|span|job|correlation)", re.IGNORECASE)
LEVEL_RANK = {name: rank for rank, name in enumerate(
    ("DEBUG", "INFO", "NOTICE", "WARN", "WARNING", "ERROR", "CRITICAL", "ALERT", "FATAL", "EMERGENCY"))}


def parse_entries(lines):
    """Yield (timestamp, level, raw_text) for each entry in the log, as soon
    as the next entry starts, so a large log is never held in memory."""
    current = None
    for line in lines:
        line = line.rstrip("\n")
        m = LINE_START.match(line)
        if m:
            if current is not None:
                yield current["ts"], current["level"], "\n".join(current["lines"])
            current = {"ts": m.group("ts"), "level": (m.group("level") or "").upper(),
                       "lines": [m.group("message")]}
        elif current is not None:
            current["lines"].append(line)
        # lines before the first recognised entry are ignored
    if current is not None:
        yield current["ts"], current["level"], "\n".join(current["lines"])


def parse_ts(text):
    """Parse a log or --since timestamp, whichever separator and zone it
    uses. A zone is dropped, so both sides compare as local wall time."""
    text = text.strip().replace("T", " ", 1).replace("Z", "+00:00")
    return datetime.fromisoformat(text).replace(tzinfo=None)


def top_exception(raw_text):
    m = EXCEPTION_RE.search(raw_text)
    return m.group(0) if m else ""


def top_in_app_frame(raw_text):
    candidates = FRAME_RE.finditer(raw_text)
    fallback = None
    for m in candidates:
        path = m.group("path")
        lineno = m.group("l1") or m.group("l2") or ""
        if any(v in path for v in VENDOR_HINTS):
            continue
        for anchor in IN_APP_ANCHORS:
            idx = path.find(anchor)
            if idx != -1:
                short = path[idx:]
                return f"{short}:{lineno}" if lineno else short
        if fallback is None:
            fallback = f"{path}:{lineno}" if lineno else path
    return fallback or ""


def normalise_message(message):
    text = message.split("\n", 1)[0].strip()
    # Drop the trailing context blob ("message {...} []"); it is read separately.
    text = re.split(r"\s\{\s*\"", text, maxsplit=1)[0]
    text = re.sub(r"\s\[\]$", "", text)
    text = UUID_RE.sub("<uuid>", text)
    text = EMAIL_RE.sub("<email>", text)
    text = LONGHEX_RE.sub("<id>", text)
    text = NUMBER_RE.sub("<n>", text)
    return re.sub(r"\s+", " ", text).strip()


def trailing_json(raw_text):
    """Return the last top-level {...} blob in the text, parsed, or None."""
    depth, start = 0, None
    for i, ch in enumerate(raw_text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                blob = raw_text[start:i + 1]
                try:
                    # strict=False: Laravel writes raw line breaks inside the trace string.
                    return json.loads(blob, strict=False)
                except ValueError:
                    start = None
    return None


def identifying_values(obj):
    """Return (key, value) pairs for fields that look like they identify a
    user or tenant, so the caller can count distinct ones without printing
    the raw value anywhere."""
    found = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                found.extend(identifying_values(value))
            elif IDENTIFYING_KEYS.search(str(key)) and not PER_REQUEST_KEYS.search(str(key)):
                found.append((str(key), str(value)))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(identifying_values(item))
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("logfile", help="Log file to read, or - for stdin")
    parser.add_argument("--since", help="Only count entries at or after this ISO8601 timestamp")
    parser.add_argument("--limit", type=int, default=25, help="Show at most this many fingerprints (default 25)")
    args = parser.parse_args()

    since = parse_ts(args.since) if args.since else None
    handle = sys.stdin if args.logfile == "-" else open(args.logfile, encoding="utf-8", errors="replace")

    groups = OrderedDict()
    skipped_unparsed = 0
    with handle:
        for ts, level, raw_text in parse_entries(handle):
            if since and parse_ts(ts) < since:
                continue
            exc = top_exception(raw_text)
            frame = top_in_app_frame(raw_text)
            message = normalise_message(raw_text)
            # Key on the frame's file, not its line: an edit above it moves the
            # line number and would split one known issue across a deploy.
            key = (exc, re.sub(r":\d+$", "", frame), message)
            group = groups.setdefault(key, {
                "count": 0, "level": level, "frame": frame, "first": ts, "last": ts, "affected": set(),
            })
            group["count"] += 1
            # Keep the worst severity seen, so a CRITICAL is not shown as INFO.
            if LEVEL_RANK.get(level, -1) > LEVEL_RANK.get(group["level"], -1):
                group["level"] = level
            group["last"] = max(group["last"], ts)
            group["first"] = min(group["first"], ts)
            ctx = trailing_json(raw_text)
            if ctx is not None:
                group["affected"].update(identifying_values(ctx))

    if not groups:
        print("No log entries recognised (expected `[timestamp] channel.LEVEL: message` or "
              "`timestamp LEVEL message`).")
        return

    ranked = sorted(groups.items(), key=lambda kv: kv[1]["count"], reverse=True)[:args.limit]

    print("| Count | First seen | Last seen | Level | Exception | Frame | Affected | Message |")
    print("|---|---|---|---|---|---|---|---|")
    for (exc, _, message), g in ranked:
        affected = str(len(g["affected"])) if g["affected"] else ""
        print(f"| {g['count']} | {g['first']} | {g['last']} | {g['level']} | {exc or '-'} | "
              f"{g['frame'] or '-'} | {affected} | {message} |")


if __name__ == "__main__":
    main()
