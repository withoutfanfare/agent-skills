# Decision-to-Live record

Tracks the full journey, starting when someone owns a product decision and
ending when production is verified to have it. Time spent working and time
spent waiting are logged apart.

## Control

| Field | Value |
| :-- | :-- |
| Change | <name> |
| Issue or specification | <link, for example ABC-123> |
| Decision timestamp | <when> |
| Release ID | <build, release or deployment ID> |
| Production deployment timestamp | <when> |
| Production smoke check timestamp | <when> |
| Release owner | <name> |
| Measurement owner | <name> |
| Risk class | Low / Medium / High / Critical |

## Stages

| Stage | Entered | Exited | Working | Waiting | Wait reason | Evidence |
| :-- | :-- | :-- | --: | --: | :-- | :-- |
| Specification | <time> | <time> | <duration> | <duration> | <code> | <link> |
| Development | <time> | <time> | <duration> | <duration> | <code> | <link> |
| Review | <time> | <time> | <duration> | <duration> | <code> | <link> |
| Staging and verification | <time> | <time> | <duration> | <duration> | <code> | <link> |
| Product acceptance | <time> | <time> | <duration> | <duration> | <code> | <link> |
| Deployment | <time> | <time> | <duration> | <duration> | <code> | <link> |

Wait codes:

- `DECISION`: nobody had yet given a needed product or policy answer.
- `HANDOVER`: context was lacking, or nobody clearly owned the work.
- `REVIEW`: work was ready but sat waiting for technical review.
- `REWORK`: evidence showed something had to be corrected.
- `ENVIRONMENT`: fixtures, staging or infrastructure could not be used.
- `ACCEPTANCE`: verified work sat waiting for product acceptance.
- `RELEASE`: approved work sat waiting for an operator or a release window.
- `EXTERNAL`: the critical path ran through a supplier or other third party.

## Measures

- Decision-to-Live time: <time of passing smoke check minus time of decision>
- Total working time: <sum>
- Total waiting time: <sum>
- Flow efficiency: <working time as a percentage of Decision-to-Live time>
- Rework loops: <count>
- Decision delays: <how many, and how long>
- First-run verification result (PASS / FAIL / NEEDS DECISION): <result>
- Production defect or rollback inside the observation period: Yes / No

## What the figures say

<Name the biggest source of delay or rework. The measure must never reward
delivery that was rushed or unsafe.>

## Improvement action

| Observation | Owner | Small system change | Review date |
| :-- | :-- | :-- | :-- |
| <bottleneck, with evidence> | <name> | <change to a template, automation, ownership or policy> | <date> |

## Outcome after release

<Evidence from users or the business on whether the original decision paid
off. Shipping it does not prove that.>
