# Evidence manifest

Links each artefact back to the scenario, the environment and the release
candidate it came from. Artefacts live somewhere the team has approved and
the public cannot reach.

## Control

| Field | Value |
| :-- | :-- |
| Feature and version | <name / version> |
| Commit | <full SHA> |
| Environment | <name and URL> |
| Test-data version | <ID> |
| Run ID | <unique ID> |
| Retention or deletion date | <date or policy> |

## Naming

```text
<run>-<scenario>-<step>-<evidence-type>.<extension>
```

For instance: `run-12-uat-003-step-04-validation.png`

## Entries

| ID | Scenario | Step | Type | Actor | URL or route | Captured at | Location | Redacted | What it proves |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EV-001 | UAT-001 | <n> | <type> | <role> | <URL or route> | <time> | <path or link> | Yes / No / Not needed | <the specific observation> |

Good evidence can be a network response, console output, a URL, a
screenshot, a short screen recording, a visible timestamp, a log excerpt
that is safe to share, or a controlled check against the database. None of
it proves more than it shows; a screenshot cannot speak for what happened
behind the scenes.

## Privacy and security

- [ ] Nothing contains secrets or production credentials.
- [ ] Personal data appears only where it is needed.
- [ ] Synthetic IDs are used wherever that is practical.
- [ ] Payment details, email addresses, headers and tokens are redacted.
- [ ] Storage is an approved place, with access to match.
- [ ] Someone owns retention or deletion.

## Gaps

- <a claim with no evidence, the reason, and who owns the next step>
