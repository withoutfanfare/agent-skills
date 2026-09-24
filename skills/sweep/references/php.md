# PHP and PHPStan notes for sweeps

## Seeing every error

A PHPStan baseline hides existing errors. Remove the entries for the error
identifier you are targeting before capturing the baseline list, then run
over the whole project with raw output:

```bash
vendor/bin/phpstan analyse --error-format=raw --memory-limit=2G > /tmp/sweep-before.txt
```

After the sweep, capture the same way into a second file and compare
counts per identifier. Do not regenerate the project's baseline for this:
`--generate-baseline` overwrites the real one, and its format differs from
the raw output, so the counts would not line up.

```bash
vendor/bin/phpstan analyse --error-format=raw --memory-limit=2G > /tmp/sweep-after.txt
for f in /tmp/sweep-before.txt /tmp/sweep-after.txt; do
  echo "== $f"; grep -o 'identifier=[^]]*' "$f" | sort | uniq -c | sort -rn | head -20
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
