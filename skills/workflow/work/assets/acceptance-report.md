# Product acceptance report

Written for whoever decides if this release candidate (the precise build up
for release) does what the product needed. The technical and automated
checks should be finished before this reaches them.

## Decision requested

- **Feature:** <name and version>
- **Release candidate:** <commit and environment>
- **Specification:** <link and version>
- **Technical review:** <link, commit reviewed, status>
- **Verification run:** <link, commit verified, status>
- **Freshness checked:** <when, and by whom>
- **Decision owner:** <named person>
- **Decision needed by:** <date and time>
- **Estimated review time:** <minutes>

Pick one:

- **Approve**: within the scope and risks shown, this candidate meets the need.
- **Request changes**: say which changes are needed and why each matters.
- **Defer**: it is not released. Note what information is missing or how priority changed, and when the decision will next be made.

Saying nothing does not approve it. Nor does the decision pass to
engineering by default.

## The problem this solves

<Two or three sentences anyone could follow.>

## What changed

- <what users will notice>

## What was verified

| Check | Result | Evidence |
| :-- | :-- | :-- |
| Engineering review | <status> | <review> |
| Browser QA | PASS / FAIL / NEEDS DECISION, with counts | <report> |
| Automated checks | <summary> | <link> |
| Specialist checks | <status, or not applicable> | <evidence> |

## Product questions

Each one specific enough to answer, with its evidence next to it.

### 1. <question>

- Why a person must judge this: <reason>
- Evidence: <staging link, screenshot or short recording>
- Decision: Approve / Request changes: <comment>

## Known limits and risks

- <the limit, its effect, and who accepts it>

## Not in this release

- <a related request left out on purpose>

## Release conditions

- <condition met, or still needed before release>

## Decision record

- Decision: Approve / Request changes / Defer
- Decision owner: <name>
- Date and time: <timestamp>
- Release-candidate commit: <full SHA>
- Comments: <text, or none>
- Required changes: <list, or none>
- Accepted limitations: <list, or none>
- Next review date, if deferred: <date>

Evidence behind it:

- Verification report: <link and commit verified>
- Technical review: <link and commit reviewed>
- Specification: <link and version>

```yaml
feature: "<feature and version>"
environment: "<environment>"
release_candidate_commit: "<full SHA>"
decision_owner: "<named person>"
decision: "PROPOSED | APPROVE | REQUEST_CHANGES | DEFER"
decided_at: null # ISO-8601 timestamp once an authorised decision exists
accepted_limitations: []
required_changes: []
next_review_at: null
evidence:
  verification_report: "<link and commit verified>"
  technical_review: "<link and commit reviewed>"
  specification: "<link and version>"
```
