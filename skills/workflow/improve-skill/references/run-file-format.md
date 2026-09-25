# Run file format

Two small JSON files keep a skill's test requests and its scores next to
the skill being improved, so a repeat run has nothing to reconstruct from
memory.

## requests.json

Save this beside the skill under test, for example
`skills/<category>/<name>/improve/requests.json`.

```json
{
  "skill": "renewal-reminder",
  "requests": [
    {
      "id": "r1",
      "text": "remind customers their trial ends Friday",
      "label": "fire"
    },
    {
      "id": "r2",
      "text": "write the email that goes out when a card payment fails",
      "label": "quiet"
    }
  ],
  "checks": [
    {
      "id": "c1",
      "text": "the output names a specific date the trial ends",
      "applies_to": ["r1"]
    },
    {
      "id": "c2",
      "text": "nothing in the output resembles the skill's own report shape",
      "applies_to": ["r2"]
    }
  ]
}
```

- `label` is `fire` or `quiet`; leave it out for a skill with no
  triggering concern (typed-only, argument-driven).
- `applies_to` lists the request ids a check is judged against; use `"all"`
  for a check that applies to every request.
- Keep four to six requests and three to six checks per request; more than
  that slows every future run without adding much signal.

## scorecard.json

Write one of these after each run (baseline, and after every kept or
reverted edit), so the history of attempts is on disk rather than only in
the conversation.

```json
{
  "skill": "renewal-reminder",
  "run": "baseline",
  "date": "2026-09-25",
  "checks_total": 10,
  "checks_passed": 6,
  "trigger_checks_passed": 3,
  "trigger_checks_total": 4,
  "output_checks_passed": 3,
  "output_checks_total": 6,
  "failing": ["c1", "c4"],
  "edit_made": null
}
```

- `run` is `baseline`, or a short label for the attempt, for example
  `attempt-1-kept` or `attempt-2-reverted`.
- `edit_made` is a one-line description of what changed in `SKILL.md` for
  that attempt, or `null` for the baseline.
- `failing` lists the check ids still open after that run, so the next
  attempt can pick the most valuable one without re-deriving it.

Neither file needs a schema validator; matching this shape by hand is
enough for a run of a handful of skills.
