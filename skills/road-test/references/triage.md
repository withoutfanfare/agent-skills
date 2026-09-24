# Triage guide

## Severity

| Severity | Means | Examples |
|---|---|---|
| Blocker | a core journey cannot be finished, or money, data or security is at risk | checkout fails; wrong total; another user's data visible; signed-out access to an admin page |
| Major | a core journey finishes but badly, or a secondary journey is broken | confirmation email never arrives; error not shown, leaving the user stuck; unusable on a phone |
| Minor | works, but wrong | cosmetic breakage, wrong wording, missing empty state, console error with no visible effect |
| Polish | an improvement, not a defect | awkward copy, rough transition |

Two automatic escalations: anything touching money or a price is a blocker
until shown otherwise; anything letting one user see or change another's
data is a blocker.

## Cause

| Class | Means | Who acts |
|---|---|---|
| Bug | the code is wrong; trace it to a file and line | developers |
| Missing feature | never built | a scope decision for the owner |
| Content | wording, images, translations | often not engineering |
| Environment | configuration, keys, workers, seed data; say whether production would be affected | whoever runs the environment |
| Flaky | happened once, would not repeat | record, do not raise |
| By design | works as intended; the tester was wrong | record, so nobody retests it |

## Every finding carries

1. The scenario number.
2. The exact URL.
3. Numbered steps from a known starting state.
4. Expected result, and where that expectation came from (code, spec, or
   plain sense).
5. Actual result, quoted where possible.
6. Evidence: a screenshot path, console message, failed request or log
   excerpt.
7. Severity and cause class.
8. The smallest proposed fix, with file and line for bugs.

A finding without evidence is an opinion: capture the evidence or remove
it.
