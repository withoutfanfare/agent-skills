# Verification report

## Release candidate

| Field | Value |
| :-- | :-- |
| Feature and version | <name / version> |
| Specification | <link and version> |
| Commit verified | <full SHA> |
| Environment and URL | <name / URL> |
| Test-data version | <ID> |
| Browser and viewport | <details> |
| Started / finished | <when> |
| Executor | <tool, and the person responsible> |

## Run state

**COMPLETED / ABORTED**

Abort reason: <what made it unsafe, unreachable or impossible to reset, or not applicable>

If the run aborted, scenarios that never ran get no verdict.

## Overall result

**PASS / FAIL / NEEDS DECISION / Not applicable: run aborted**

The single worst scenario sets the overall result:

- **PASS**: all in-scope scenarios showed the specified behaviour, with evidence.
- **FAIL**: one or more did not.
- **NEEDS DECISION**: none failed, but one or more found the intended behaviour undefined or contradictory, so a person has to decide.
- An aborted run gets no overall result.

| Result | Count |
| :-- | --: |
| PASS | <0> |
| FAIL | <0> |
| NEEDS DECISION | <0> |
| Total | <0> |

## Scenario results

### UAT-001: <scenario>

- Result: PASS / FAIL / NEEDS DECISION
- Requirement: <criterion or rule ID>
- Expected: <what the spec says should happen>
- Observed: <what actually happened>
- Evidence: <manifest IDs>
- Side effects reset: Yes / No / Not applicable
- Notes: <follow-up or decision required>

## Failures

| Scenario | Owner | Cause | Defect | Reproduction | Impact |
| :-- | :-- | :-- | :-- | :-- | :-- |
| <ID> | <name> | By design / Product bug / Test or environment issue / Missing feature | <how it differed> | <shortest steps> | <what it costs> |

## Decisions required

| Scenario | Decision owner | Missing or conflicting intent | Options |
| :-- | :-- | :-- | :-- |
| <ID> | <name> | <question> | <choices and their consequences> |

## Regression and risk checks

| Area | Evidence or exclusion | Result |
| :-- | :-- | :-- |
| Existing journeys | <reference> | <result> |
| Accessibility | <reference> | <result> |
| Tenant boundaries | <reference> | <result> |
| Permissions | <reference> | <result> |
| Payments and duplicates | <reference> | <result> |
| Personal data | <reference> | <result> |

## Console, network and log notes

- <only what matters, redacted>

## Exclusions and limits

- <what this run could not establish, and why>

## Recommendation

Choose one:

- Proceed to product acceptance (every in-scope scenario ran and passed)
- Return for correction (a failure needs fixing)
- Obtain decisions before continuing (intent is missing or contradictory)

Reason: <brief explanation grounded in the evidence>
