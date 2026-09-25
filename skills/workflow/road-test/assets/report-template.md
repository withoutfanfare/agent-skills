# Acceptance test: <target>

| | |
|---|---|
| Date | <date> |
| Goal | <what this run proves> |
| Environment | <local / staging>, <URL> |
| Version | <branch and commit> |
| Accounts used | <roles, not passwords> |

## Acceptance criteria

- <what must be true for this to pass>

## Preflight

| Check | Result |
|---|---|
| Site responds | |
| Environment as expected | |
| Workers and scheduler running (if needed) | |
| Front-end assets current | |
| Outside services in test mode | |

## Scenarios

| # | Scenario | Priority | Verdict | Evidence |
|---|---|---|---|---|
| 1 | | must | | |

Verdicts: passed · failed · blocked (what is needed) · needs a decision
(the question).

## Findings

### F1: <title>
- Scenario: <#> · URL: <url>
- Steps: 1. … 2. …
- Expected: <…> (source: code / spec / plain sense)
- Actual: <…>
- Evidence: <path>
- Severity: <blocker|major|minor|polish> · Cause: <bug|missing|content|environment|flaky|by design>
- Proposed fix: <smallest change, file and line>

## Records created

- <accounts, orders, uploads to clean up>

## Summary

Passed <n> · Failed <n> · Blocked <n> · Needs a decision <n>
