---
name: sweep
description: >-
  Makes one automated change safely across many files: static-analysis
  fixes, renames, deprecation replacements or pattern rewrites. Captures a
  baseline, dry-runs the script, samples a few files, then scales and checks
  nothing new broke. Use when a change touches ten or more files, or the
  user asks to fix all the linter or type errors, rename something
  everywhere, or apply a pattern across the codebase.
license: MIT
allowed-tools: Bash Read Edit Write Grep Glob
---

# Sweep

A script that edits two hundred files can fix two hundred problems or
create two hundred subtle ones. The difference is process: a baseline to
compare against, a dry run you read, a small sample before the
full run, and a count afterwards that proves nothing new appeared.

For restructuring one area by hand, use `reshape` (if installed).

## 1. Capture the baseline

Before changing anything, save the full current list of problems as
`file:line:message`, for the whole codebase rather than a subset:

```bash
<analysis tool> > /tmp/sweep-before.txt 2>&1
wc -l /tmp/sweep-before.txt
```

If the tool has a baseline or ignore file that hides existing errors,
remove the relevant entries first so everything is visible.

Done when: the baseline file exists and you know its count per error type.

## 2. Sort safe from risky

Group the problems by type, then decide which types a script can fix
reliably. Safe: the fix is the same every time and the tool's claim is
certainly true (a concrete type it can see, a renamed function with an
identical signature). Risky: the tool could be wrong at runtime (values
that might be null despite what the types say, dynamic data, defensive code
that was deliberate). When unsure, keep the defensive code: a warning costs
less than a crash.

Done when: each error type is marked "script", "by hand" or "leave".

## 3. Write the script with a dry run

The script prints every change it would make, as before and after lines,
without writing. It also logs every case it chose to skip (writes rather
than reads, multi-line expressions, anything unusual), because the skipped
cases are usually the risky ones.

Run it in dry-run mode and read the output. Anything surprising means fixing
the script, not trusting it.

Done when: you have read the whole dry run and the skip log.

## 4. Sample, then scale

Apply to three to five representative files. Run the analysis tool on just
those files and read the diff:

```bash
git diff -- <file1> <file2> <file3>
```

If the sample is clean, apply to everything. If a pattern still resists a
safe script after two attempts, fix it by hand: editing fifteen files by
hand costs less than one bad automated edit in two hundred.

Done when: the sample diff held no surprises, and the full run completed.

## 5. Prove nothing new broke

Run the analysis tool again over everything and compare with the
baseline, per error type:

```bash
<analysis tool> > /tmp/sweep-after.txt 2>&1
```

Every targeted count should fall. Any count that rose, or any error type
that did not exist before, means stop: find the files responsible, revert
just those, and handle them by hand. Then run the test suite.

Done when: no error type increased, no new type appeared, and the tests
pass.

## 6. Commit with a scope statement

The commit message says what was fixed, what was deliberately left and
why, and the before and after counts.

Stack-specific traps (PHP and PHPStan examples) are in
[references/php.md](references/php.md).

Done when: the commit message states what was fixed, what was left and why,
and the before and after counts.

## It's working if

- Every automated edit was seen in a dry run before it was written.
- The after-count is lower than the baseline for every targeted type, and
  higher for none.
- Skipped cases are listed, not silently dropped.
