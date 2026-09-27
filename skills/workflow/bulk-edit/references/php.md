# PHP and PHPStan notes for sweeps

## Seeing every error

A PHPStan baseline hides existing errors. Remove the entries for the error
identifier you are targeting before capturing the baseline list, then run
over the whole project with JSON output: the `raw` formatter does not
print the error identifier (even with `-v`), so grepping it for
`identifier=` finds nothing to count.

```bash
vendor/bin/phpstan analyse --error-format=json --memory-limit=2G > /tmp/sweep-before.json
```

After the sweep, capture the same way into a second file and compare
counts per identifier. Do not regenerate the project's baseline for this:
`--generate-baseline` overwrites the real one, and its format differs from
this output, so the counts would not line up.

```bash
vendor/bin/phpstan analyse --error-format=json --memory-limit=2G > /tmp/sweep-after.json
for f in /tmp/sweep-before.json /tmp/sweep-after.json; do
  echo "== $f"
  jq -r '.files[].messages[].identifier // "no-identifier"' "$f" | sort | uniq -c | sort -rn | head -20
done
```

## Which fixes are safe to script

| Usually safe | Usually risky |
|---|---|
| Concrete value types the tool can see (`string`, `int`, date objects) | Eloquent relationship results: the related model can be null at runtime even when types say otherwise |
| Framework return types with well-known behaviour | `mixed` and other dynamic types |
| Renames with identical signatures | Chains like `$a->relation->property` |
| | Null-safe operators or checks that look redundant but guard real data |

## Pattern traps

- **Write context:** replacing `->` with `?->` inside an assignment target
  turns `$a->b = 1` into `$a?->b = 1`, a fatal error ("Can't use nullsafe
  operator in write context"). Skip lines where the pattern is followed by
  `=` (but not `==` or `=>`).
- **Multi-line expressions:** a regular expression that checks for `??` on
  the same line misses a `??` on the next line. Check the following line
  too, or skip.
- **Strings and comments:** a textual replace also hits strings, comments
  and docblocks. Exclude them, or use a parser-based tool (Rector) where one
  exists for the change.

## Prefer a real tool when there is one

Rector (PHP), ESLint with `--fix`, and IDE rename refactorings understand
the code's structure. Use them over regular expressions whenever they
support the change you need, and still follow the baseline, sample and
compare steps.
