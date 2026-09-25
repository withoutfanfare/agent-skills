# UAT plan

A plan for user acceptance testing (UAT) and browser QA. It connects the
specification to browser checks anyone can repeat, and to a short list of
product questions.

## Control

| Field | Value |
| :-- | :-- |
| Feature and version | <name / version> |
| Specification | <link and version> |
| Release-candidate commit | <full SHA, or "Not deployed: planning only"> |
| Environment | <name and URL, or "Not available: planning only"> |
| Plan readiness | Ready to execute / Ready after named prerequisites / Not ready |
| Acceptance owner | <named person> |
| Plan owner | <name> |
| Planned date | <date> |

## Objective

<What running this plan will show, and what it cannot show.>

## Coverage

In scope:

- <journey, rule or risk>

Out of scope:

- <area, the reason it is left out, and its owner>

## Deterministic preconditions

Live payment credentials and real personal data from production are never
used.

| Item | Required state | Reset or confirmation |
| :-- | :-- | :-- |
| Tenant | <synthetic tenant for UAT> | <how it is reset> |
| User roles | <for example customer, viewer, editor, administrator> | <where the accounts come from> |
| Seed data | <records and their IDs> | <test-data version> |
| Clock and time zone | <fixed, or recorded> | <how> |
| Payment provider | <sandbox, and which scenario> | <reset or test approach> |
| Flags and configuration | <exact values> | <how confirmed> |
| Browser and viewport | <exact target> | <how confirmed> |

## Result words

- **PASS**: the behaviour is specified, it was seen on the named release candidate, and the evidence is sufficient.
- **FAIL**: the behaviour is specified, yet it did not appear, or a defect stopped the check from finishing.
- **NEEDS DECISION**: no requirement says what is right, or authoritative sources disagree. Never guess.

## Scenarios

### UAT-001: <scenario name>

- Requirement: <acceptance criterion or rule ID>
- Actor: <role>
- Starting state: <fixture state>
- Risk covered: <risk>

Steps:

1. <action>
2. <action>

Expected:

- <what the browser or system visibly does>
- <any data change or side effect that can safely be checked>

Evidence to capture: <screenshot, URL, log, network response or database assertion>

Reset afterwards: <how>

## Regression

- <an existing journey this change might break>

## Accessibility and resilience

- Focus and keyboard use: <checks>
- Names and semantics for screen readers: <checks>
- Recovering from validation errors: <checks>
- A dependency that is slow or fails: <safe scenario>
- Retries and double submission: <safe scenario>

## Product questions

| ID | Question needing judgement | Evidence to show | Owner |
| :-- | :-- | :-- | :-- |
| PD-001 | <question> | <journey or screenshot> | <name> |

## Stop conditions

Stop and escalate when a check might reach production, reveal personal
data, charge real money, delete data others rely on, step across a tenant
boundary it should not, or run on a build nobody has confirmed.

## Ready to execute when

- each scenario points to a requirement or risk with a stable ID;
- the actor, the steps, the expected result and a repeatable starting state are all spelled out;
- the reset method and the evidence to collect are set;
- the candidate, environment, fixture version and accounts can all be confirmed;
- stop conditions and exclusions can be seen;
- every open product question has a named owner.

Results and evidence references never go in this plan. They belong in the
[verification report](verification-report.md) and the
[evidence manifest](evidence-manifest.md).
