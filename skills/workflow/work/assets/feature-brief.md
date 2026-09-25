# Feature brief: <short name>

The shared contract between what product wants, what gets built, how it is
checked and who accepts it. Keep it short, and keep uncertainty in plain
sight.

## Document control

| Field | Value |
|---|---|
| Feature | <short name> |
| Source issue | <link or ABC-123> |
| Document status | Draft / Current / Superseded |
| Product owner | <name> |
| Engineering owner | <name> |
| Acceptance owner | <name> |
| Version | <number or date> |
| Readiness | Not ready / Ready with assumptions / Ready |
| Last updated | <date and time> |

## Problem

<The user or business problem. The proposed code is not the problem.>

## Evidence and context

- <customer evidence, operational issue, policy need or observed behaviour>
- <links, screenshots, support cases or data>

## Users and actors

| Actor | Need | Role or permission |
|---|---|---|
| <actor> | <what they need to do> | <role> |

## Desired outcome

<What becomes possible, and how you will know it worked.>

## Scope

**Included**

- <behaviour in this change>

**Not included**

- <related behaviour deliberately left out>

## Core journey

1. <starting state>
2. <what the user does>
3. <how the system responds>
4. <the successful outcome>

## Business rules

Stable ids let tests and decisions point at a rule.

| ID | Rule | Source or owner |
|---|---|---|
| BR-001 | <rule that must always hold> | <evidence or decision owner> |

## Permissions and tenant boundaries

- Which tenant does this data belong to?
- For each role: may it read, add, edit, delete or publish it?
- What is off limits to a user, both to look at and to alter?
- When someone is refused access, what do they get instead?

## Data, integrations and failure behaviour

| Area | Expected behaviour | When it fails |
|---|---|---|
| Data | <creation, updates, history, retention> | <safe response> |
| Integration | <internal or external dependency> | <timeout, retry, duplicate or outage handling> |
| Notification or queue | <expected side effect> | <retry and visibility> |

## Quality and compliance

- Accessibility: <keyboard, screen reader, contrast or wording needs>
- Security and privacy: <sensitive data, audit, access or retention needs>
- Performance: <a meaningful limit or expected response time>
- Reporting and analytics: <events, reports or audit entries>
- Compatibility: <browsers, devices or existing journeys that matter>

## Known facts, assumptions and decisions

**Known**

- <confirmed fact, with its source>

**Assumed for this version**

| ID | Assumption | Risk if wrong | Owner | Review date |
|---|---|---|---|---|
| AS-001 | <temporary assumption> | <impact> | <name> | <date> |

**Decision required**

| ID | Question | Why it matters | Practical options or constraints | Decision owner | Needed by |
|---|---|---|---|---|---|
| D-001 | <answerable question> | <product or technical consequence> | <options and what each costs> | <name> | <date> |

An unanswered product decision never hides inside an engineering assumption.

## Acceptance criteria

Observable behaviour only. Cover the normal journey, permissions,
validation, failures and the regressions that matter.

**AC-001: <outcome>**

- Given <starting state>
- When <action>
- Then <observable result>
- And <further result>

Example: Given a customer with a paid order, when they cancel within 14
days, then the order page shows "Refund requested".

## Evidence required

- Automated checks: <tests or checks>
- Browser QA: <scenario ids or journeys>
- Product evidence: <screenshots, wording or workflow sign-off>
- Specialist review: <payment, security, data, accessibility or migration>

## Release and rollback

- Release conditions: <what must be true>
- Feature flag or staged release: <if any>
- Rollback: <how to get back safely>
- Monitoring: <what will show success or failure>

## Readiness decision

Pick one:

- **Ready**: intent, scope and acceptance criteria are enough to proceed.
- **Ready with assumptions**: named assumptions are accepted for now and
  their risks are visible.
- **Not ready**: at least one open decision could reshape how this is built
  or how safe it is.

- Decision: <status>
- Product owner: <name>
- Date: <date>
