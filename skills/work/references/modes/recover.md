# Recover mode

Work that was inherited, abandoned halfway, left to go stale or never
properly understood needs a safe footing before anyone chooses what to do
with it. This mode finds that footing. It produces an assessment, and it
does not drift into writing code.

If the assessment has to survive past this conversation, fill in
[the recovery assessment template](../../assets/recovery-assessment.md).

## Sources

- what the handover asks for, and by when;
- the spec as it stands, with its decisions and acceptance notes;
- the code: its repository, branch, precise commit, related history and any
  pull requests;
- how it is built: configuration, policies, UI, background jobs,
  integrations, business logic, data and entry points;
- which automated checks exist and how they fare today;
- a local or staging environment you can use without harm;
- neighbouring modules, support tickets and past incidents;
- the owners for product, engineering and acceptance.

Note every source you could not get at. A tidy file name, a helpful comment,
a passing build or a page that renders is no proof that a journey works end
to end.

## Steps

The order matters. You cannot follow a journey you have not mapped, and you
cannot choose a route until you know what is specified and what actually
runs.

1. Pin the target so it cannot move underneath you: environment, repository,
   branch and full commit hash.
2. Work out what the thing was meant to do from the best current sources,
   and split that into what is confirmed, what is inferred and what is
   missing.
3. Map it: tests, queues, UI and operations; permissions, ownership
   boundaries and validation; data and business logic; entry points and
   integrations.
4. Follow each important journey end to end: what goes in, what gets stored,
   what else it triggers, what the user sees, and how it copes with failure.
5. Judge two things independently: how well the behaviour is specified, and
   what the implementation evidence shows.
6. Weigh the hazards: money, tenancy, permissions, security and privacy;
   migrations and rollback; destructive actions and effects on outside
   systems; idempotency (whether repeating an action is safe).
7. Be clear about what today's tests and observations prove and where they
   stop proving anything.
8. Keep choices that belong to product separate from engineering tasks.
9. Weigh finishing it, repairing it, replacing it or stopping.
10. Recommend one of those, giving its risk, how sure you are, and the first
    bounded change that can be verified by itself.

Done when: the target is pinned to a full commit and every source that
could not be reached is recorded.

## Status vocabulary

For how well behaviour is specified, use one of:

- **Defined**: an authorised source says what should happen, clearly enough
  to judge against.
- **Missing**: nothing authoritative says what should happen.
- **Conflicting**: authoritative sources say different things.

For what the implementation evidence shows, use one of:

- **Working**: today's evidence backs up the defined behaviour.
- **Incomplete**: part of the defined behaviour is absent or not finished.
- **Broken**: today's evidence goes against the defined behaviour.
- **Unverified**: neither intent nor evidence is strong enough for a verdict;
  name what is lacking.

Only use `Working`, `Incomplete` or `Broken` where the expectation is
`Defined`. However untidy it makes the summary, `Unverified` never gets
promoted to `Working`, because the evidence would not bear that out.

## Behaviour record

```markdown
| ID | Journey or rule | Specification state | Expected | Observed | Status | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REC-001 | Customer applies a discount code at checkout | Defined | Total drops by the code's value | Total unchanged on the staging basket | Broken | Staging run today; one code tried | Medium |
```

Should an overall completeness figure help, derive it from named
capabilities and how confident you are in each, and give it as a range.
Never manufacture an exact percentage.

## Guardrails

- Look before you touch. Unless implementation has its own separate go-ahead,
  do not edit, so the assessment reflects what you found rather than what
  you altered.
- Leave history and any unrelated uncommitted files alone; they may be a
  colleague's work in progress.
- While assessing, keep away from live payments, writes to production,
  sweeping data fixes and anything destructive. An assessment must never
  cause the harm it is meant to uncover.
- Treat old tickets and drafts as background on how the work was delivered.
  They only speak for today's product once someone confirms them, since
  intent may have changed.
- Report the current state in neutral terms. Whoever wrote it before had
  context and pressures you cannot see.
- If there is a credible sign of leaked credentials, lost data, one tenant
  seeing another's data, a dangerous migration or a live payment, stop and
  escalate. A person has to decide before anything else goes ahead.

## Reply

A durable assessment includes: the pinned target; intent split into
confirmed, inferred and missing; the sources; a map of the implementation;
the behaviour records; risks; gaps in the evidence; decisions; the recovery
options; a recommendation; the first bounded change; and the recovery gate.

Close it with this block, fields and values unchanged:

```yaml
recommended_route: "Complete | Repair selected areas | Replace selected areas | Stop or defer"
implementation_completeness: "Capability-weighted range and basis | Not assessed"
recovery_risk: "Low | Medium | High | Critical"
confidence: "High | Medium | Low"
first_bounded_change: "One reviewable outcome"
```

Start the reply with the route you recommend and its first bounded change.
Behaviour records and risks follow as the supporting case, trimmed to the
journeys and rules that actually shape the recommendation. Finish with the
recovery gate, so it is obvious what needs deciding before anyone carries on.

## Staying current

A pull-request handover or review written earlier only counts once it has
been regenerated, or checked against the recorded head. If reviewability
analysis is also safe to do, carry straight on into it within the same
`work` run instead of asking the user to choose.

Done when: the target is pinned, each status carries its evidence and a
confidence, product decisions stand apart from engineering work, and the next
bounded route is spelled out. Then go back to the
[stage map](../stage-map.md).
