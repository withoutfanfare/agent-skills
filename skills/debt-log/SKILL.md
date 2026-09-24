---
name: debt-log
description: >-
  Keeps a technical-debt register for a project: finds debt in the code,
  records each item with what it costs to keep and to fix, scores it, and
  produces a prioritised list worth acting on. Use when the user asks for a
  tech debt audit, wants to track or record some debt, or asks which debt to
  pay down first.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Debt log

Every team knows it has technical debt; few can say which piece costs the
most. Without a register, the loudest debt gets fixed and the most
expensive debt keeps charging interest quietly. This skill makes debt
visible and comparable, so paying it down becomes a choice about return,
not volume.

## Where the register lives

`docs/tech-debt.md` in the repository, unless the project keeps it
elsewhere (issues with a label, a wiki page). Each item has a stable ID
(`TD-001`, `TD-002`, ...) so it can be referenced in commits and pull
requests.

## Kinds of debt

| Kind | Examples |
|---|---|
| Design | a class that knows everything, logic in the wrong layer, boundaries in the wrong place |
| Code | duplication, magic values, tangled conditionals |
| Test | untested areas, flaky or brittle tests, over-mocking |
| Dependencies | end-of-life frameworks, unpatched advisories, abandoned packages |
| Documentation | undocumented APIs, stale setup guides |
| Operations | manual deploy steps, missing monitoring, hard-coded configuration |

## Find debt (audit)

Look for friction, not just smells: very large files, `TODO`, `FIXME` and
`HACK` comments (`git grep -n -E "TODO|FIXME|HACK"`), duplicated blocks,
areas with frequent bug fixes in `git log`, missing tests beside busy code,
outdated or vulnerable dependencies, manual steps in deployment docs.

Prefer debt that causes pain now over old debt nobody touches. Present
findings with kind, location and the friction it causes, and let the user
choose which to add.

Done when: each finding has a location and a concrete cost, and the user
has picked which to record.

## Record an item

```markdown
### TD-007: <searchable title>
Kind · Where: <files or modules> · Added: <date> · Status: open
Impact: 1-3 · Risk: 1-3 · Effort: 1-3 · Priority: <score>

**Why it exists:** <deadline, changed requirements, known trade-off>
**Cost of keeping:** <specific: "every new payment method means editing four files">
**Cost of fixing:** <hours or days>
**Fixing unlocks:** <what becomes easier>
```

Score each from 1 to 3: **impact** (annoyance, regular friction, blocks
work or causes bugs), **risk** (stable, slowly worsening, getting worse
fast), **effort** (hours, days, weeks). Priority is
`(impact × 2 + risk × 2) ÷ effort`. It is a guide for discussion, so show
the three scores beside it.

Done when: the item is in the register with all three scores and a
specific cost of keeping.

## Prioritise

Sort open items by priority, then pick out:

- **Quick wins:** high priority, effort 1.
- **Worsening:** risk 3, whatever the effort.
- **Unblockers:** items whose fix makes several others cheaper.

Suggest a small set for the next cycle, and link each to the work it would
speed up.

Done when: the user has a short, ordered list with reasons.

## Keep it honest

When an item is fixed, mark it done with the date and the commit or pull
request. When debt turns out to be harmless, close it with a note. An
occasional review removes items nobody would fix.

## It's working if

- Every item states a specific, observable cost of keeping it.
- The top of the list changes as work lands and new debt appears.
- Debt fixes can be traced back to register IDs.
