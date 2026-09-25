# Pull request handover

Accuracy here is the author's responsibility, even for parts an AI drafted
from the diff and the issue.

## Control

| Field | Value |
| :-- | :-- |
| Pull request | <link or number> |
| Author | <name> |
| Issue and specification | <links> |
| Base and head | <branches> |
| Head commit | <full SHA> |
| Status | Draft / Ready for review / Changes requested |
| Last refreshed | <when> |

## Why

<What problem users or the business have, and why it is being fixed now.>

## What changed

- <change>

## What did not change

- <nearby behaviour deliberately left as it was>

## Key decisions

| Decision | Reason | Record |
| :-- | :-- | :-- |
| <choice> | <why> | <link> |

## Areas affected

Rate each as Low / Medium / High / Critical, or write "None" if untouched.

| Domain | Change | Risk |
| :-- | :-- | :-- |
| Database | <summary> | <risk> |
| Permissions | <summary> | <risk> |
| Tenancy | <summary> | <risk> |
| Payments | <summary> | <risk> |
| Subscriptions | <summary> | <risk> |
| Personal data | <summary> | <risk> |
| Queues and integrations | <summary> | <risk> |
| User interface | <summary> | <risk> |

## Migrations, compatibility and rollback

- Data change or migration: <none, or what>
- Compatibility with older versions: <effect>
- Order of deployment: <if it matters>
- Rolling back: <the safe route, and any catch>
- Staged release or feature flag: <if used>

## Verification already done

List only what was really exercised.

| Check | Command or journey | Result | Evidence |
| :-- | :-- | :-- | :-- |
| Tests | <exact scope> | Pass / Fail | <run or link> |
| Static analysis | <exact scope> | Pass / Fail | <run or link> |
| In the browser | <scenario> | Pass / Fail / Needs decision | <evidence> |

## Where to look first

1. <the riskiest file, rule or behaviour, and why>
2. <the next place>
3. <an assumption about design or product that deserves a challenge>

## UAT and product acceptance

- Where the candidate runs: <URL or environment name>
- Roles and fixtures required: <details>
- Key journeys: <scenario IDs>
- Product decisions still to make: <IDs, or none>

## Known limits and follow-up

- <a deliberate limit, with its issue, such as ABC-123>

## Reviewability

| Signal | Value |
| :-- | :-- |
| Files changed | <n> |
| Hand-written lines changed | <n> |
| Risk domains touched | <n, and which> |
| Separate behaviours changed | <n> |
| Generated or vendored files kept separate | Yes / No / Not applicable |

When one review cannot reasonably take this in, explain what stops it being
split and suggest a route.

- Why it stays whole: <reason, or not applicable>
- Order to read it in: <files or domains>

## Stale-draft refresh

Complete when the pull request has been idle for a while, or its base has
moved on a lot.

- Is the original intent still wanted: Yes / No / Needs decision
- Base brought up to date: <when, and outcome>
- Conflicts resolved and dead code taken out: <outcome>
- Dependency and security assumptions checked again: <outcome>
- Tests run again on the head commit: <outcome>
- Screenshots and handover updated: <outcome>
- Owner and review date confirmed again: <who, and when>

## Author declaration

I confirm this describes the current head commit, names the risks I know
of, and does not pass off anything an AI generated as verified fact.

- Author: <name>
- Date: <date>
