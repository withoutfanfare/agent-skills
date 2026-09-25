# Operating model

Delivery loses most time to fuzzy intent, thin handovers, checks done
twice, evidence nobody trusts and sign-offs nobody can find. The answer
here: let systems carry coordination, shared knowledge and repeatable
checks; let AI carry out the work; save people's attention for intent and
judgement. Measure the whole journey rather than how much code appears:

```text
problem → intent and decisions → code → technical review → docs in plain
English → repeatable UAT with evidence → product sign-off → controlled
release with smoke checks → what was learnt, and the next decision
```

## Ownership

| Work | Owned by | What the system contributes |
|---|---|---|
| Product intent, priorities, business rules | product or management | spots ambiguity and turns it into answerable decisions |
| Analysing the specification | AI-assisted | separates facts from assumptions and decisions; drafts testable criteria |
| Building it | engineering, helped by AI | the smallest maintainable change inside the authorised scope |
| Automated checks | engineering and CI | behaviour that can be checked again and again |
| Handover and review analysis | AI-assisted | a map of change, risk, evidence and reading order |
| Documentation | AI-assisted | plain-English pages per reader, from current sources |
| Technical approval and accepting risk | a qualified engineering owner | a judgement on the code and whatever risk remains |
| Browser QA | AI-assisted | authorised scenarios run on known fixtures, with evidence captured |
| Product sign-off | a named product or management owner | confirmation that the result meets the need |
| Release and smoke checks | engineering and release tooling | the approved candidate released and its first health confirmed |

AI may assemble evidence and recommend. When an owner is away, their
approval does not pass to the AI by default; it counts only when that
owner gives it.

## Evidence labels

Tag every claim in a map or receipt with exactly one:

- **Inspected**: read directly just now, from a source you can name.
- **Run**: produced in the present context by a command or scenario you
  can name.
- **Inferred**: a conclusion drawn from evidence, with its uncertainty
  spelled out.
- **Unverified**: something the available access or evidence could not
  establish.

These tag evidence, not the stage. A finished document can still contain
an unverified claim.

## State statuses

Each state on the map gets one of: `Complete` (the current evidence
satisfies it), `In progress` (someone is working on it and it is not yet
satisfied), `Actionable now` (useful work can be done with today's access
and permissions), `Blocked` (a named operational prerequisite is missing),
`Awaiting a decision` (the outcome turns on an authorised person's call),
`Not applicable` (with the reason). These are summaries only; the result
words a mode defines are more precise and are never swapped for them.

## Proportionate controls

How deep to go depends on impact, how hard it is to undo, and how much is
uncertain.

| Kind of change | Least acceptable control |
|---|---|
| Wording or low-risk layout | targeted checks, a light review, a visual look |
| Everyday admin journey | clear acceptance criteria, automated checks, review, UAT, product sign-off |
| Report or export | fixed fixtures, figures reconciled, permissions reviewed, output signed off |
| Payment or subscription | thorough peer review, sandbox tests, idempotency and failure checks, rollback, explicit sign-off |
| Tenant or permission boundary | tests for isolation and authorisation, a security-minded review, evidence |
| Database migration | review of the data impact, a forward and a rollback plan, a rehearsal sized to the risk, operational approval |

Small changes stay light, while the controls that guard money, personal
data, tenant separation and uptime never weaken.

## Principles

Use whichever apply; they are not steps.

- Missing intent becomes precise questions. A made-up policy can pass for
  an approved one.
- Assumptions are written down, with an expiry when that helps.
- Claims cite current evidence and admit what that evidence leaves open.
- Decisions and useful artefacts live with the project, not just in a
  chat, wherever the project keeps such things.
- Changes are sized so a person can understand, check and undo them.
- Whether the code is correct and whether the product is accepted are two
  separate questions.
- Anything waiting shows who owns it and what happens next.
- Each rule has one home, and everything else links to it.
- Rules that keep coming up, and failures that repeat, turn into tests,
  checks, sharper guidance or safer defaults.

## Which source settles which question

- What should happen: accepted briefs and decision records.
- What does happen in code: the current code and configuration.
- What is checked today: the tests.
- What happened on one candidate in one environment: run evidence.
- Delivery context: issues and pull requests.
- Leads only, until someone records the decision properly: messages and
  meetings.

The project's own documents outrank generic examples. If two authoritative
sources contradict each other, show the contradiction and name who can
settle it. Ranking one above the other in silence would take away a
decision that owner still has to make.

## Freshness

An upstream change leaves downstream artefacts in place; mark only the
claims it affects and say what needs checking again.

| Change | Possibly out of date |
|---|---|
| Intent or acceptance criteria changed | what the code assumed, the handover, review, UAT, verification, sign-off |
| New code or a new pull request head | review, verification, sign-off evidence |
| Different build, environment, fixtures or feature flags | verification and sign-off evidence |
| Risk acceptance, release conditions or the delivery profile changed | sign-off, release preparation, and the map itself |

Then choose the evidence state again from whichever anchors are still
current ([stage map](stage-map.md)). The map never slides back on a hunch.

## What it is not

It does not demand long specifications, an approval meeting at each stage,
blind trust in generated output, or a filled-in copy of every template. It
is a handful of contracts that let anyone answer: what are we trying to
achieve, what exists, what changed, what has really been checked, what
still needs a judgement, whose decision is next, and what actually reached
users.
