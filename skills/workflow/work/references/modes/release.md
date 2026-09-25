# Release mode

Putting accepted work into production deserves as much care as building
it, and every release is a chance to learn why delivery took as long as it
did. This mode gets a release ready, runs the production smoke checks it is
authorised to run, gathers evidence, and feeds the Decision-to-Live
measure. Preparing is always allowed. Deploying, or changing anything in
production, needs explicit authority and must go through the project's own
release controls.

Everything here comes from the **Release** section of the
[delivery profile](../delivery-profile.md). That section should say: which
branch releases are cut from and who is allowed to merge to it; the
schedule and its cut-offs; the rule for eligibility; the urgent route; what
triggers a deploy; which smoke checks run; how to roll back; and how an
issue gets closed. If the profile does not cover something, point that out
and ask. A release command, window or rollback method is never made up,
because a guess could sidestep the safety controls the project really
relies on.

Projects that keep durable measurement use the
[Decision-to-Live record](../../assets/decision-to-live.md); for many, the
tracker's history of status changes is enough. The measures themselves are
explained in [measurement](../measurement.md).

## Inputs

- the accepted candidate, with its exact build or commit;
- the product acceptance decision, and any limits attached to it;
- the review disposition, and how any open risk is being handled;
- verification results, and what they left out;
- runbooks for deploying, rolling back and handling incidents;
- who owns the release, which environment, the window, and anything it
  depends on;
- the monitoring needed and the production smoke scenarios;
- whatever Decision-to-Live timestamps exist so far.

## Eligibility

First, test the item against the eligibility rule in the profile, showing
each part as a tick. Typically that means: the tracker holds the state the
profile asks for (often `Approved`, with the acceptance owner's sign-off on
the issue); the item belongs to the current cycle; and it was approved
before the cut-off. Missing the cut-off means waiting for the next release.
Say so plainly; the schedule is not up for negotiation. The urgent route is
open only to an item with the profile's urgent priority, and only when the
release owner calls for it.

## Prepare

Keep to this order. Everything after step one describes the candidate step
one confirmed, and the go/no-go record depends on the rest being done.

1. Check that every piece of evidence refers to one and the same release
   candidate.
2. Write down the conditions for release, and who is authorised to meet
   each.
3. Find anything with ordering constraints: data jobs, integrations,
   flags, caches, queues, migrations, compatibility between versions.
4. Using the current runbook, set out when and how to roll back, or how to
   recover safely by going forward.
5. Write a few brief production smoke scenarios that show basic health and
   neither destroy anything nor reach outside the system.
6. Name what to monitor, who gets the alerts, and how long to watch.
7. Note the go/no-go decision still needed and where its evidence will be
   kept.
8. Draft release notes, or notes for stakeholders, if they would help.

Done when: a different authorised operator could take over knowing the
candidate, the order of steps, the safety checks, where rollback stops, and
what evidence to collect.

## Execute

Only deploy, or run checks against production, when this request plainly
authorises it and the project's release rules are satisfied. Just before
acting, confirm the target and the candidate once more. The profile names
who merges into the release branch; on most projects that is a person, and
it is never the assistant. What the skill does is get that merge ready (it
confirms the candidate, lists everything else going out with it, and drafts
the release note) and then hand it over.

Stop immediately if the candidate does not match, if a material risk has
no rollback path, if it is unclear whether live integrations will be hit,
if a migration does something unexpected, if credentials are exposed, or if
production starts doing something outside the approved scope. Continuing
could mean a production action with no way back.

Once an authorised release has gone out, follow this order. Each step
supplies the evidence for the next, and claiming success before the smoke
checks have run would misreport what happened.

1. Note the deployment's identifier and its timestamps.
2. Run the smoke checks that were named, none of them destructive.
3. Write down what the checks and monitoring actually showed.
4. When a stop condition appears, roll back or escalate as the runbook
   directs.
5. Attach the release evidence to the accepted candidate.

A deploy command that finished cleanly tells you nothing about whether
users can complete their journey in production.

### The Live gate

An item is closed only when production verification, as the profile
defines it, is complete: either the smoke checks in the Release section
have passed against what was deployed, or an authorised exception has been
written down. The issue then moves to the profile's last state, `Live`.
Moving it is a tracker write like every other, so it waits for the user's
word (see [tracker](../tracker.md)). A notice that a deploy happened is not
verification. The state never runs ahead of the evidence.

Done when: the release state, the evidence, the smoke result, who owns what
remains, and the Decision-to-Live record are all stated. Then go back to
the [stage map](../stage-map.md).

## Release states

These are plain statements of fact: `Prepared`, `Authorised`, `Deployed`,
`Smoke checks passed`, `Smoke checks failed`, `Rolled back`, `Unverified`.
Do not squash them into a single "done". Doing so hides which checks
really passed.

## Decision-to-Live learning

Capture the decision that started it, when each stage began and ended, how
much time was active against waiting, when the release and its smoke checks
finished, what caused any rework, and how production first behaved.

Aim for speed, but inside quality guardrails. The number must never be
improved by concealing waits, loosening gates, carving one outcome into
several, or letting failures through unresolved. A measure that has been
gamed no longer tells you how delivery went.

When the next worthwhile review comes round, choose one delay or source of
rework that keeps recurring, look at real cases, and try one small,
time-boxed improvement. Change shared guidance only once the lesson has
proved it will last. The loop is described in full in
[measurement](../measurement.md).

## Guardrails

- Approval of the product does not authorise a deploy, unless the
  project's policy explicitly says it does.
- Never make up an environment, a release command or a way to roll back.
  Getting one wrong can do something to production that cannot be undone.
- Smoke checks never use real transactions. Real money and real customers
  would be affected.
- Strip sensitive logs, personal data, tokens and credentials out of
  evidence, so that gathering it does not itself leak anything.
- Evidence from releases that failed or were rolled back is kept; it is
  what the learning draws on.

## Freshness

Preparation goes stale where the candidate, the acceptance decision, the
treatment of a risk, the runbook or the release environment has changed.
Confirm everything again immediately before executing.

## Report

A brief status note, not the runbook written out again. Give the release
state (one state from the list above), how the smoke checks went, any stop
condition that fired and what it set off, and who owns the next action.
Link to the Decision-to-Live record and the evidence instead of copying
them in.
