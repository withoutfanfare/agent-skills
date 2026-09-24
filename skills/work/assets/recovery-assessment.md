# Recovery assessment: <module or journey>

Fill this in before changing inherited, unfinished or poorly understood
work. Keep what you observed apart from what you inferred and what is
unknown.

## Assessment control

| Field | Value |
|---|---|
| Module or journey | <name> |
| Source issue or request | <link or ABC-123> |
| Repository and branch | <repository / branch> |
| Commit assessed | <full commit> |
| Environment observed | Local / test / staging |
| Assessor | <name, or tool plus the human owner> |
| Assessment date | <date and time> |
| Confidence | High / Medium / Low |

## Intended purpose

**Confirmed intent**

- <requirement backed by an authoritative source>

**Inferred intent**

- <inference, and the evidence behind it>

**Missing intent**

- <question the evidence cannot answer>

## Sources examined

- <issue, spec or decision record>
- <pull requests and review history>
- <routes, code, schema, jobs and UI>
- <automated tests>
- <behaviour observed safely>
- <logs or docs>

## Implementation map

| Area | What exists | Evidence | Status |
|---|---|---|---|
| Entry points (routes, commands) | <summary> | <URL or path> | Working / Incomplete / Broken / Unverified |
| Screens and UI | <summary> | <evidence or path> | <status> |
| Rules and logic | <summary> | <path> | <status> |
| Stored data | <summary> | <schema or migration> | <status> |
| Tenancy and access | <summary> | <observed behaviour or policy> | <status> |
| Background jobs, integrations | <summary> | <evidence or path> | <status> |
| Automated tests | <summary> | <run or test path> | <status> |

### What the statuses mean

Specification state:

- **Defined**: an authorised source spells out what should happen, precisely
  enough to judge against.
- **Missing**: no authoritative expected behaviour exists.
- **Conflicting**: authoritative sources disagree on the expected behaviour.

Implementation and evidence status:

- **Working**: the expected behaviour is known and current evidence supports
  it.
- **Incomplete**: some or all of the defined behaviour is absent or
  unfinished.
- **Broken**: evidence contradicts the known expected behaviour.
- **Unverified**: no verdict is possible; the specification state and
  evidence must show whether the intent, the execution evidence or both fall
  short.

A `Defined` specification state is the precondition for `Working`,
`Incomplete` or `Broken`.

## Behaviours checked

| ID | Journey or rule | Specification state | Expected | Observed | Status | Evidence | Confidence |
|---|---|---|---|---|---|---|---|
| REC-001 | <behaviour> | Defined / Missing / Conflicting | <expectation, or not specified> | <observation> | Working / Incomplete / Broken / Unverified | <reference, and why unverified if so> | High / Medium / Low |

## Risks

| Severity | Area | Concern backed by evidence | Impact | Action needed |
|---|---|---|---|---|
| Critical / High / Medium / Low | <area> | <concern> | <consequence> | <action> |

Always look at: money and payments; access rules and keeping tenants apart;
personal data; schema migrations and rollback; queued jobs and outside
integrations; anything that deletes or overwrites.

## Missing tests and evidence

- <important behaviour with no reliable coverage>
- <behaviour that could not be exercised safely>

## Decisions required

| ID | Decision | Options | Why it matters | Owner |
|---|---|---|---|---|
| D-001 | <question> | <practical choices> | <consequence> | <name> |

## Recovery options

For each route, note when it suits, what it gains and what it risks.

| Route | Suits when | Benefits | Risks |
|---|---|---|---|
| Complete the existing implementation | <conditions> | <benefits> | <risks> |
| Repair or refactor selected areas | <conditions> | <benefits> | <risks> |
| Replace selected areas or restart | <conditions> | <benefits> | <risks> |
| Stop or defer | The need, ownership, safety or evidence does not justify recovery yet | Avoids unowned or unsafe work | Delay, unsupported current behaviour, later replacement cost |

## Recommendation

<The route you recommend, why it is safer or cheaper, and how confident you
are.>

- Confidence: High / Medium / Low
- Recovery risk: Low / Medium / High / Critical
- Estimated implementation completeness: <optional range weighted by capability, with its basis and confidence, or Not assessed>

## Next steps

1. <decision or safety action that has to come first>
2. <small, testable delivery step>
3. <verification step>
4. <acceptance step>

## Recovery gate

- [ ] Every product decision able to change the outcome has someone who owns it.
- [ ] Each critical data, privacy or security risk has a safe answer.
- [ ] Which recovery route was chosen is stated plainly.
- [ ] One reviewer could check the first change in a single sitting.
- [ ] Current behaviour that has to survive is listed.

- Date: <date>
- Gate owner: <name>
- Gate result: Proceed / Proceed with named constraints / Do not proceed
