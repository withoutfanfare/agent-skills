# Pull request review report

## Control

| Field | Value |
| :-- | :-- |
| Pull request | <link or number> |
| Head commit reviewed | <full SHA> |
| Specification | <link and version> |
| Reviewer | <person, or tool with its human owner> |
| Review date | <when> |
| Scope | <files and domains covered, and what was left out> |

## Summary

- Purpose: <one sentence>
- Overall risk (Low / Medium / High / Critical): <rating>
- Recommendation (Approve / Comment / Request changes / Not reviewable yet): <one>
- Verification confidence: High / Medium / Low
- Blocking findings: <n>
- Product decisions: <n>

## Change map

| Domain | Behaviour changed | Risk | Files or components |
| :-- | :-- | :-- | :-- |
| <domain> | <what now behaves differently> | <risk> | <paths> |

## Reviewability

- Does the scope fit its purpose (Yes / No / Partly): <answer>
- Can it be read as a single review unit: Yes / No
- Recommended reading order: <order>
- Needs splitting or refreshing first: <why, or none>

## Findings

Worst first. One entry per root cause. Neutral wording where you disagree.

Severity scale:

- **Blocker**: severe harm to money, security, privacy or service is credible and could happen now.
- **Major**: probably a serious defect, such as one tenant reaching another's data, lost data, money handled wrongly, or a core journey that cannot finish.
- **Minor**: a genuine correctness, reliability, accessibility or maintainability problem whose reach is limited.
- **Polish**: worth doing, but hurts little today.

### RF-001: <Blocker / Major / Minor / Polish> <short title>

- Finding ID: RF-001
- Location: `<file:line>`
- Trigger: <what input, state or sequence sets it off>
- Observed evidence: <what the code or behaviour shows now>
- Impact: <effect on users, data, money, security or operations>
- Why it matters here: <the rule or spec it breaks>
- Recommended change: <least change that fixes it>
- Verification: <test or reproduction proving the fix>
- Disposition: Open / Fixed / Accepted risk / Not applicable / Already addressed / Deferred with owner / Rejected with evidence
- Confidence: High / Medium / Low

## Missing evidence or tests

- <behaviour or risk without enough coverage>

## Product decisions the review surfaced

| ID | Owner | Question | Why the code cannot settle it |
| :-- | :-- | :-- | :-- |
| D-001 | <name> | <question> | <reason> |

## Checked and handled

- <a risk examined and found to be dealt with>

## Next action

1. <blocking fix or decision>
2. <how it will be verified>
3. <what the follow-up review covers>

A clean report does not prove the change is right. State what was covered
and where doubt remains.
