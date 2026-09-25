# Accept mode

Only a few questions genuinely need a person with authority to answer
them. This mode strips product acceptance down to those. Everything
mechanical arrives already summarised, so the owner never redoes QA, and
nothing here pretends an AI can accept a product.

For a lasting pack, use the [acceptance report](../../assets/acceptance-report.md)
and the [decision record](../../assets/decision-record.md).

## Inputs

- what the change is meant to achieve, and its acceptance criteria as they
  stand today;
- the candidate itself: environment, build and exact commit;
- the technical review: what it covered, what it found, and the
  disposition a human recorded;
- the evidence manifest and the verification report;
- rollback, exclusions, known limits, risks already accepted, and the
  conditions for release;
- who owns the product decision by name, and when it is needed.

## Ready to ask?

Only request approval once every one of these is true:

- intent, review and verification all talk about one candidate and one
  scope;
- the review's disposition has been given by someone with authority;
- the mechanical scenarios have all run, or anything left out is stated;
- nothing blocking has failed without being resolved;
- each `NEEDS DECISION` item has an owner with a name;
- the owner can open the evidence, and it is safe for them to see.

While any in-scope UAT scenario is `NOT_RUN`, acceptance is not the next
action: never invite a sign-off. The rule is set out in [verify](verify.md).

When the conditions fall short, do more than list what is missing, since a
bare list gives the user nothing to do. Go back into the main `work` loop,
finish whatever upstream analysis, planning or evidence gathering can
safely be done now, and then show the one gate still standing.

## Workflow

Each step narrows what came before, so the questions get fewer and sharper
until only one request remains. Keep to the order.

1. Check that intent, review, verification and the candidate agree.
2. Describe, in words a manager would use, the problem users had and what
   they will now see.
3. Boil the mechanical evidence down to counts and links.
4. Keep only questions that need judgement: how the workflow should go,
   wording, the user experience, policy, a limitation or risk to accept.
5. For each question, show why it matters, with its evidence alongside.
6. Leave release conditions, open risks, exclusions and limits where they
   can be seen.
7. Ask for a single explicit outcome for the named candidate.
8. Write down who decided, when, which commit, their comments, any changes
   required, and the next date. If the profile's lifecycle ties the
   approved state to a recorded sign-off, that record goes on the issue:
   you draft the comment, and the owner or the user posts it. The board
   moves to approved only after that record exists (see
   [tracker](../tracker.md)).
9. Feed accepted choices back into durable intent, tests, UAT and docs.

Done when: readiness has been stated outright, the mechanical evidence is
summarised faithfully, what remains is purely judgement, and a single named
owner has been asked for a single decision. Then go back to the
[stage map](../stage-map.md).

## The three outcomes

- **Approve**: this exact candidate does what was needed, inside the scope,
  limits and risks that were shown.
- **Request changes**: it falls short for now, and the changes wanted, with
  their reasons, are spelled out.
- **Defer**: it is not released. Something (priority, a decision, evidence)
  is not ready, and the next owner and date are written down.

A product is not accepted by silence, by the passing of time, by an AI's
recommendation, by engineering sign-off, or because the release is under
pressure.

## When verification is mixed

- A `PASS` backs up the one mechanical claim it matches, and nothing more.
- A blocking `FAIL` that is still open means no approval request goes out.
- A `FAIL` judged non-blocking stays in view. Before approval, someone with
  authority decides how it is handled, on both the technical and product
  side.
- If no one with authority has said whether a `FAIL` blocks, do not send
  the request. Name the technical or product owner who must classify it,
  and never assume it down: it may well be blocking.
- A `NEEDS DECISION` turns into a specific product question with an owner.
- An aborted scenario, or one never run, is a gap in readiness. It is not a
  pass, and it is not a product ambiguity.

## Decision block

```yaml
feature: "<feature and version>"
environment: "<named environment>"
release_candidate_commit: "<full commit>"
decision_owner: "<named person or role>"
decision: "PROPOSED | APPROVE | REQUEST_CHANGES | DEFER"
decided_at: null # ISO-8601 timestamp once an authorised decision exists
accepted_limitations: []
required_changes: []
next_review_at: null
evidence:
  verification_report: "<link>"
  technical_review: "<link>"
  specification: "<link>"
```

Until the owner has actually answered, the block says `decision: PROPOSED`
with `decided_at: null`. Filling in an outcome nobody gave would let a
release through with no decision behind it.

## Guardrails

- Someone should be able to read the main pack in five to ten minutes.
- Failed checks, exclusions and risks stay visible even when hiding them
  would make acceptance easier. An owner can only accept responsibly with
  everything in front of them.
- Missing product intent belongs to the named owner. It is not handed to
  engineering by default.
- Nobody accepts on behalf of an owner who has not been named or cannot be
  reached. An acceptance that no person gave is no decision.
- Evidence must come from this candidate in this environment; evidence from
  anywhere else proves nothing here.
- Where release has its own gate, product acceptance does not double as
  permission to deploy. That gate is still checked on its own (see
  [release](release.md)).
- Keep credentials and any personal data that is not needed out of the
  pack, so it can be shared safely.

## Output

A lasting pack holds: what decision is being asked for; what problem is
solved and what visibly changed; the mechanical evidence; the product
questions; limits, risk and exclusions; the conditions for release; and the
decision record, proposed or authorised.

Open with the decision needed and the questions only the owner can answer.
Evidence sits underneath, as counts and links, so the whole thing stays a
five-to-ten-minute read. End on the decision block, so the owner sees
exactly what they are signing.

## Freshness

If intent, the candidate, the review disposition, verification or the way a
risk is handled changes, only the acceptance claims that depend on it go
stale. Earlier decisions stay as history. When the boundary of what was
accepted has moved, ask for acceptance again.
