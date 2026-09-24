# Verify mode

Acceptance rests on proof that a named build does what was intended when
someone actually uses it. Here you write a repeatable user acceptance
testing (UAT) plan, drive authorised browser QA on a named release
candidate, or organise evidence that already exists. A result is never made
up to fill a gap.

## Pick the operation

- **Plan**: scenarios and prerequisites only. No environment is needed.
- **Execute**: run the scenarios somewhere confirmed safe.
- **Report**: give shape to evidence from a current run, and leave missing
  results missing.
- **Plan and execute**: allowed only once every execution precondition
  holds.

For lasting artefacts, use the [UAT plan](../../assets/uat-plan.md), the
[verification report](../../assets/verification-report.md) and the
[evidence manifest](../../assets/evidence-manifest.md).

The profile's staging-review gate gets its evidence here too. That means
three things are true: the item has merged and reached the named
environment, a plan exists, and the run used that deployment rather than a
build on someone's machine.

**Hand-offs.** `road-test` (when installed) drives browser scenarios
through to a verdict; `test-plan` (when installed) drafts plan material
from code and docs. Results from any tool come back in this mode's terms:
`PASS`, `FAIL` or `NEEDS DECISION`, tied to a named release candidate, and
no verdict at all for work that never ran. A browser-testing skill such as
`road-test`, or any tool with its own result words, is translated
explicitly:

| Tool says | This mode records |
| :-- | :-- |
| passed | `PASS` |
| failed | `FAIL` |
| blocked because it could not get in, the feature was gated, or the environment got in the way | `NOT_RUN`, with the blocker named. Never a verdict. |
| blocked because intent is absent or contradicts itself | `NEEDS DECISION`, flagged on its own |

Proof from lower down the stack (tests, static analysis, HTTP checks, what
the database holds) only becomes a scenario verdict once it is linked to a
scenario and a release candidate. For each piece, say which scenario it
proves and which requirement it meets, and take the candidate's details
(commit, environment, deployment, test-data version) from the run itself.
No such tools installed? This file is the process.

## Plan

Collect: acceptance criteria as they stand, with the IDs of any business
rules; who the actors are, what they may do and what they own; the journeys
that matter (happy path, validation, failure, regression); anything about
flags, integrations, currency, locale, time or screen size; and limits on
privacy, safety and how long evidence is kept.

Planning needs no environment, build or deployed fixture. If they are
absent, write them down as prerequisites for execution.

Each step tightens what the previous one set out, so go in order:

1. Say what the plan is for and where its coverage stops.
2. Give each scenario an ID that will not change, and the requirement it
   comes from.
3. For every scenario write down who acts, a starting state that is the
   same every time, the steps, a result you can observe, the evidence
   wanted, and how to put things back.
4. Include scenarios for tenant walls, permissions, bad input, failure,
   accessibility, resilience and regression wherever they apply.
5. Name the synthetic accounts, the fixture version, and the sandbox
   responses that are safe to use.
6. Write the stop conditions, and what execution will leave out.
7. Set readiness to one of `Ready to execute`,
   `Ready after named prerequisites` or `Not ready`.

Done when: the scenarios can be run as written, the prerequisites are in
plain view, and no scenario has a verdict yet.

## Execution preconditions

Nothing is clicked and no data changes until all of these are confirmed.

**What is under test**

- the precise commit or build, and which deployment carries it;
- proof the deployed build includes that commit. Check the SHA last
  deployed, or the deploy log, against the merge commit. A URL that answers
  shows the site is running; it does not show it is running this change.

**Where it runs**

- an environment that is not production, with its URL;
- that URL, taken from the profile, really responds. When it does not, look
  in the repository's deploy workflows and smoke scripts for the actual
  host before blaming the network, and correct the profile in this same run rather
  than working round it;
- integrations pointed at sandboxes, and no more personal data than the
  test needs.

**Data and accounts**

- fixtures that are versioned and deterministic, with a reset that can run
  twice safely and has been shown to work;
- every fixture sitting in the **state the journey needs**. Existing is
  not enough: a record may be there yet be archived, past its date, still
  in draft, out of stock, or hidden behind a tenant flag that sends the
  user another way;
- synthetic accounts for each role.

**Settings and permission**

- feature flags, time zone, locale, browser and viewport;
- where evidence may be stored, and the privacy rules for it;
- authority to make the synthetic changes the plan involves.

Confirm every observable precondition in the plan *before* asking for
authority to execute: that the options the tenant has switched on actually
show on the page, that fixtures are in the right state, that browser
tooling is connected. If a precondition needs access you lack, ask for it
now rather than finding out mid-run.

With a completion-ledger skill installed (one checkbox per fact, each with
a shell check whose expected output is a literal token or summary line,
never prose), turn these preconditions into its checkboxes, one per
observable fact: the URL answers, the fixture is in the required state, the
flags are set. Run its checker before requesting execute authority, so the
pre-flight arrives as pasted output instead of an assertion. Those
checkboxes are separate from this mode's stage gate and its evidence
labels; do not mix them up.

Cannot confirm which target this is, that it is safe, or that it resets?
Then the run is `ABORTED`, and the operational reason is written down.
Unexecuted work gets no verdict, since that would be inventing a result.

## Scenario results

Three words only:

- **PASS**: on the named release candidate, the specified behaviour was
  seen, backed by current evidence that is good enough, and reached through
  the interface a user would touch. If that interface could not be driven,
  the scenario is `NOT_RUN` and the reason is given. A shortcut lower down
  never earns `PASS`, because it can work when the real screen would not.
- **FAIL**: the specified behaviour did not appear, or a defect in the
  product stopped the scenario getting to the end.
- **NEEDS DECISION**: the authoritative sources do not say what should
  happen, or they contradict one another.

A broken environment is never `NEEDS DECISION`. It is an execution blocker,
or a failure category.

The overall result takes the worst scenario still unresolved. One `FAIL`
anywhere gives `FAIL`. With no `FAIL` but at least one `NEEDS DECISION`,
the result is `NEEDS DECISION`. `PASS` needs every in-scope scenario run
and passed.

> **While any in-scope UAT scenario is `NOT_RUN`, acceptance is not the
> next action. Never invite a sign-off.** Do not put approval or the
> accepted state on the table, and do not hint that the item is close to
> it. An unrun scenario is evidence of nothing, in either direction. What
> comes next is running it, naming what stands in its way, or asking the
> acceptance owner outright whether they choose to accept the gap. Having a
> plan is not the same as having run it. Those are two separate gates, and
> acceptance can lean only on the second.

Run state sits apart from the result, as `COMPLETED` or `ABORTED`, and an
aborted run carries no overall result. The summary lists every scenario
that was planned. The ones that ran have a status. The ones that did not
show `execution: NOT_RUN`, `status: null` and a reason, never an invented
verdict.

## Execute

Take these in order. Each depends on the one before (reset confirmed before
running, something observed before evidence is taken, evidence in hand
before a verdict), and jumping ahead records results that nothing supports.

1. Pin down the run's context, and prove the reset really resets.
2. One scenario at a time, each from its known starting point, use the
   product the way a user does: click the actual button. Do not call the
   code underneath, trigger the app's internal events, or poke state
   directly to save time. Going beneath the interface bypasses what it
   enforces (a greyed-out button, an archived record, a validation rule),
   and that is frequently the very thing under test.
3. Watch what renders, along with validation, permission behaviour, the
   console, network traffic and any back-end signals you are allowed to
   see.
4. Take redacted evidence at the moment you observe.
5. Hold what you saw against the cited rule, and give one result.
6. Where you can, reproduce a failure once after a clean reset, and work
   out whether the fault lies in the product, the test or the environment.
7. Run a limited set of regressions, chosen for how likely the change is
   to have hit them.
8. Undo side effects and note whether that worked.
9. Anything excluded or not run is written down where it will be seen.

Done when: each planned scenario has either a result or a visible unrun
state, the limits of the evidence are stated, resets are logged, and the
next owner is clear from the outcome. Then go back to the
[stage map](../stage-map.md).

### Fixtures

- Tenants and users are synthetic, named, and hold known roles.
- Fixture data carries a version, and every run logs which one it used.
- Resets are safe to repeat, and their result is checked each time.
- Pin or record viewport, flags, currency, locale and time whenever they
  affect the outcome.
- Only provider sandboxes and published test values.
- Isolate scenarios from each other, or reset between them.
- Build every scenario on its own fixtures and never rely on whatever
  data happens to be on staging: another run can change or remove it, and
  the result would quietly stop meaning anything.

### Evidence

File names follow `<run>-<scenario>-<step>-<type>`. For each artefact note
the actor, the commit, the environment, the URL, the time, and what it
demonstrates. Before-and-after captures help when state changes. Redact
payment details, personal data, headers, tokens and credentials.

Every artefact has limits, so name them. A screenshot cannot show that a
row was written, and a row in the database cannot show what appeared on
screen.

Before calling anything an anomaly, rule out your own tooling. Whatever you
added to watch the product (a stub, a proxy, a console hook, a listener) is
part of the rig, not the product. If a result smells like a defect, reload
the page or restart the session, attach the instrumentation once only, and
try again. Doubled events, missing events and values that cannot be real
usually come from a listener attached twice, a hook that outlived a soft
navigation, or a stub nobody removed, not from the product. Only report it
if the clean retry shows it again, and say which run the evidence is from.

## Machine-readable summary

Key order does not matter; the keys and value sets do.

```json
{
  "run_id": "<stable-run-id>",
  "run_state": "COMPLETED|ABORTED",
  "abort_reason": null,
  "release_candidate": {
    "environment": "<non-production environment>",
    "commit": "<full-commit>",
    "browser": "<browser and viewport>",
    "deployment": "<build-or-deploy-id>",
    "fixture_version": "<fixture-version>"
  },
  "overall_status": "PASS|FAIL|NEEDS_DECISION|null",
  "recommended_next_step": "acceptance|correction|decision|rerun",
  "decisions_required": [],
  "coverage_exclusions": [],
  "scenarios": [
    {
      "id": "UAT-001",
      "requirement": "AC-001",
      "execution": "RUN|NOT_RUN",
      "not_run_reason": "<null, or why it was not executed>",
      "status": "PASS|FAIL|NEEDS_DECISION|null",
      "expected": "<observable result>",
      "observed": "<what was seen, or null when NOT_RUN>",
      "failure_category": "product|test|environment|null",
      "evidence": ["EV-001"],
      "reset_confirmed": true
    }
  ]
}
```

## Guardrails

- Production is off limits for any QA that changes data; nothing there can
  be safely undone.
- Test runs use no real customer records, no shared logins and no live
  payment methods. A leak or a charge during testing is still real.
- Halt the moment you see one tenant's data from another, sensitive data
  on show, a live integration firing, or a candidate you cannot confirm.
  Pressing on risks a genuine breach, or a verdict about the wrong build.
- The product stays untouched while you verify it. Editing it until a
  scenario passes produces a verdict for something nobody will ship.
- An older run is history, not today's `PASS`. The code may have moved on.
- An AI judging a screenshot is not product acceptance. That decision
  belongs to a person or a policy.

## Freshness

Verification can go stale when the acceptance rule, the commit, the
deployment, the fixtures or an important setting changes. Keep the earlier
run as history, and list what now has to run again.

## Report

Write the story of the plan or the run, then the summary block filled in
for this run. The plan is not reprinted. Prose is for deviations, aborts
and the suggested next step; scenario detail belongs in the block and the
evidence. Usually that is a few short paragraphs and the block.
