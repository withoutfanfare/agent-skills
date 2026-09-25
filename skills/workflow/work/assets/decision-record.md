# Decision record: <short title>

Write one when a choice materially shapes how the product behaves, the
architecture, data, compliance, release risk, or a rule the team will
keep applying. Keep it short enough that someone will maintain it.

Keep questions, assumptions and decisions apart. An open question needs an
answer from a named owner; an assumption is a temporary working basis with a
consequence and a review trigger. A record then moves through these states:

- **Proposed**: a prepared recommendation, not yet authorised. An agent may
  draft this.
- **Accepted**: chosen by an authorised owner. Only that owner sets it.
- **Superseded**: replaced by a later record, linked below.
- **Reversed**: deliberately undone, with the reason and consequences.

Once accepted, carry the choice into the brief, tests, UAT, docs and release
conditions it affects.

| Field | Value |
|---|---|
| Decision ID | DEC-<number> |
| Status | Proposed / Accepted / Superseded / Reversed |
| Date | <date> |
| Decision owner | <person or group> |
| Participants | <names> |
| Related issue or feature | <link or ABC-123> |
| Scope | <users, tenants, modules or releases affected> |
| Review trigger | <date, event, evidence threshold, or Not required with reason> |
| Supersedes | <decision id or none> |
| Superseded by | <decision id or none> |

## Context

<What forced a choice, including the constraint or evidence.>

Example: an online shop's refund emails fail silently when the mail provider
is down, and support cannot tell which customers were told.

## Decision

<The choice, in one clear sentence.>

## Scope

<Where it applies, and any boundary where it does not.>

## Reason

<Why this option won.>

## Options considered

| Option | Benefits | Costs and risks | Why chosen or rejected |
|---|---|---|---|
| <option> | <benefits> | <costs> | <reason> |

## Consequences

- Product behaviour: <impact>
- Users and accessibility: <impact>
- Data, security and privacy: <impact>
- Engineering and operations: <impact>
- Verification and acceptance: <impact>

## Resulting changes

- Spec or acceptance criteria: <change and link>
- Implementation: <change and link>
- Docs or automated checks: <change and link>
- Follow-up review date: <date or not required>

## Evidence and links

- Feature brief or issue: <link>
- Implementation and pull request: <link>
- Verification or policy source: <link>

## When to revisit

- Trigger: <date, event, evidence threshold, or Not required with reason>
- Review owner: <name or role>
- Evidence that would justify changing it: <description>
