# Measurement and shared knowledge

The speed of typing code is a poor guide to delivery. The useful questions
are how long it takes for a decision someone owns to become verified in
production, where that time was spent, and whether quality survived the
trip. This file sets out that measure, the ones that support it, a small
loop for improving, and how delivery knowledge lives beside the code.

Decision records, and the statuses they move through, follow the
[decision record template](../assets/decision-record.md).

## Decision-to-Live

This measures the full journey from a decision to working production, not
how quickly code was written.

- **The clock starts** once someone with authority has recorded a decision
  that carries enough intent for delivery to begin.
- **The clock stops** once the accepted candidate is running in production,
  its required smoke checks there have passed (or an authorised exception
  has been written down), and the first evidence has been linked.

For every stage, log when it started and ended, and split its time into
active and waiting:

| # | Stage |
| :-- | :-- |
| 1 | Deciding and specifying |
| 2 | Building |
| 3 | Review |
| 4 | Staging and verification |
| 5 | Product acceptance |
| 6 | Release, with its smoke checks |

Use the [Decision-to-Live template](../assets/decision-to-live.md) to keep
the record.

## Core measures

| Measure | What to report |
| :-- | :-- |
| Decision-to-Live time | The median and the 85th percentile, broken down by type of change and level of risk. |
| Waiting share | Share of the total spent waiting, broken down into waits for clarification, for review, for an environment, for acceptance, and for release. |
| Decision latency | How long it takes from a material question being raised to an answer being authorised and recorded, and how old the still-open decisions are. |
| Review lead time and burden | Time from asking for review to the first substantial response, and on to a disposition; how many rounds it took; how much effort went on reconstructing context. |
| Verification readiness | Of the candidates that matter, how many arrive with up-to-date acceptance criteria, a plan that can be repeated, structured evidence, and fixtures where they are needed. |
| Acceptance latency | Time the decision spent waiting, and time spent actively deciding, shown separately. |
| First-pass outcome | Whether rework that could have been avoided happened, and its cause. |
| Quality guardrails | Defects that escaped and how severe they were, rollbacks and hotfixes, and any effect on security, privacy, payments, tenancy or support. |

Some numbers look like progress but prove nothing: story points, lines of
code, how many prompts or pull requests there were, how many tests or
documents exist, and `PASS` counts that have no evidence under them.

## Improvement loop

Run it as often as is useful:

1. pick the delay or source of rework that keeps costing the most;
2. study a handful of real cases of it;
3. work out whether it calls for clearer intent, better ownership, more
   capacity, shared knowledge, automation, or a safer control;
4. try one experiment with clear limits;
5. watch quality and speed side by side;
6. decide to keep the experiment, adjust it, or drop it;
7. change the shared system only once the lesson has shown it will last.

Individuals are never ranked. Waiting and rework mostly come from how the
system is designed, how work is shaped, and how ownership is set up.

## Docs as code

Every rule has exactly one home. Knowledge that changes along with the code
sits close to the repository, and prompts point to it through a brief map
instead of carrying copies.

A document that claims to be authoritative makes clear:

- what it is for and what it covers;
- whether it describes intent, how things are built today, or a procedure;
- who owns it and what should prompt a review;
- its rules and invariants, and the failure cases worth knowing;
- the decisions, code, tests and operational evidence it relates to;
- where it stops, and which record replaces it, if any.

Begin with knowledge that is risky, that people need again and again, or
that would be hard to piece back together. Sensible places to start are
permissions and tenancy, payments and subscriptions, idempotent queues,
fixtures, and the review, UAT, release and rollback routines.

Inexpensive checks can show that links work, that required metadata is
there, that no two decisions share an ID, that paths mentioned really
exist, that replaced records point to their successor, and that risky
changes trigger the right documentation review. Only promote a warning to a
gate after the rule and its exceptions have settled down.

Shared knowledge never holds credentials, tokens, production sessions,
real customer data, personal material nobody needs, or sensitive logs that
have not been redacted.
