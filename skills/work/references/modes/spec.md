# Spec mode

Before anyone builds, someone has to agree what "done" looks like. This mode
turns a request into that agreement, or reopens an agreement on purpose when
intent shifts. It points at the gaps; it does not quietly fill them. A sound
issue should pass through in a minute and go straight back to the main
`work` loop.

## Usually, the issue is enough

Most items need no separate document. Compare the issue with the project's
Definition of Ready or issue template (the Lifecycle section of the
[delivery profile](../delivery-profile.md) names it; see
[tracker](../tracker.md)) and suggest the fields it lacks. Reach for
[the feature brief template](../../assets/feature-brief.md) only when the user
asks, or when the change is so large or risky that an issue cannot hold all
its rules, decisions and acceptance criteria.

## Sources

Start with whatever you can find; a gap in one place never stops the first
pass.

- the request or issue itself, quoted word for word;
- who is affected, and what shows the problem is real;
- related behaviour already live, plus existing product rules and past
  decisions;
- journeys someone has watched, screenshots, routes and designs;
- the risky edges: payments, personal data, migrations, tenancy, access;
- the owners for acceptance, engineering and product;
- the deadline, and what makes it urgent.

A source you could not find is logged as a gap. Never paper over it with a
likely-sounding guess.

## Steps

Go in order, because later steps lean on earlier ones. Who the actors are
(step 3) shapes which rules you examine (step 5), and how you label each
claim (step 6) decides what you still need to ask (step 7).

1. Read the issue against the Definition of Ready. For each field it lacks,
   say so and draft wording from the evidence; anything that depends on a
   product rule gets the label `Decision required`. Offer to update the issue
   with the draft, and only do so once the user agrees.
2. Separate the problem (for the user or the business) from any fix someone
   has already suggested.
3. List the actors, what each wants to achieve, and where ownership or tenant
   boundaries fall.
4. Draw three lines: what is in scope, what sits next to it, and what is
   deliberately out.
5. Scale your scrutiny to the risk. Consider the business rules,
   permissions and validation;
   the data and its failure modes; security, privacy and accessibility;
   integrations, reporting and performance; rollback; and how UAT will
   judge it.
6. Tag each claim that matters with one of three labels: `Known`,
   `Assumed for this version` or `Decision required`.
7. Only ask a question if its answer could change what gets built. Pair it
   with what depends on it and the person who decides.
8. Number the business rules and acceptance criteria that matter, and keep
   those numbers stable.
9. Write acceptance criteria someone could watch pass: the happy path, plus
   whichever validation, access, failure and regression cases apply.
10. For each important outcome, name how it will be proven: a test, a
    browser scenario, a specialist's review or a person's decision.
11. If this is a revisit, set the new contract beside the code and anything
    already produced from the old one.

Done when: each claim that matters carries one of the three labels, every
open question names its owner, and you have picked a readiness result.

## Readiness result

Choose one, and only one:

- **Ready**: nothing material is unclear for the next bounded step.
- **Ready with assumptions**: progress rests on assumptions that are written
  down and owned, and none of them masks a choice that would alter safety or
  architecture.
- **Not ready**: an authorised decision is still missing, and its answer
  would change the architecture, the user experience, safety, data or the
  outcome itself.

A result of `Ready` closes this stage and nothing more. It does not license
code changes or a release.

## Logging open questions

One row per material question:

```markdown
| ID | Question | Why it matters | Practical options or constraints | Decision owner | Needed by |
| --- | --- | --- | --- | --- | --- |
| D-001 | Can a subscriber pause twice in one year? | Changes billing dates | Allow / cap at one / ask support | Product owner | Before build |
```

If the choice will outlive this item, also draft a record from
[the decision record template](../../assets/decision-record.md) and set its
status to `Proposed`. Accepting it is its owner's call alone; never flip it
yourself.

If the user settles a question in chat, update the decision table (in the
brief or the issue) and the readiness line before the turn ends. Decisions
parked for later get lost. Questions that surface while building get the
following `D-` number and a safe default that is stated out loud (see
[build](build.md)).

## Writing acceptance criteria

Number each one and phrase it so an outsider could confirm it. Use
`Given / When / Then` when it sharpens the meaning; a wording tweak on a
button does not need it.

Describe what someone sees or can check, never the mere existence of code.
"A `PauseSubscription` class exists" fails the test; "the account page shows
the pause end date" passes.

## Guardrails

- Spend detail where the risk and uncertainty are, and nowhere else.
- Leave unknowns looking unknown. A guess presented as a sensible default
  reads later as a decision nobody made.
- How to build it is engineering's choice, unless the requested outcome
  itself pins it down.
- Where the risk is high, spell out the rules and the evidence needed.
- A brief is read by more people than the systems it covers, so leave out
  secrets and any personal or production data it does not need.
- If a single open question could change what a safe build looks like, the
  item is not ready. Saying otherwise is how the wrong thing gets built.

## Reply

When a durable brief earns its keep, it holds these sections:

```text
Document control; Problem; Evidence and context; Users and actors; Desired
outcome; Included and excluded scope; Core journey; Business rules;
Permissions and ownership boundaries; Data, integrations and failure
behaviour; Quality and compliance; Known facts, assumptions and decisions;
Acceptance criteria; Evidence required; Release and rollback; Readiness
decision.
```

A small or already healthy issue needs no brief. Give a short note instead:
how it measures against the Definition of Ready, what it still lacks, and the
readiness result.

Put the readiness result and open decisions first; the brief or note goes
below. Let the size of the issue set the size of the reply. Report what moved
or what is still absent rather than reciting the issue.

## When intent changes

Say precisely which pieces may now be out of step: assumptions baked into
code, reviews, hand-overs, UAT scenarios, evidence already gathered, and the
conditions for acceptance or release. Anything the change does not touch
keeps its evidence.

Done when: each claim that matters is known, assumed or a named decision;
every criterion can be watched passing; the readiness result matches what is
still uncertain; and any knock-on staleness is spelled out. Then go back to
the [stage map](../stage-map.md).
