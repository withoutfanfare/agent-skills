# Results

## 24 September 2026: rewrite equivalence run

The rewritten skill against the version it replaced. Both were run on the
same anonymised fixtures, with the same models, flags and scorer.

**Verdict:** the two versions behave the same. In Claude Code both pass
every run (75 of 75). In Codex they fail on the same fixture: 70 of 75 for
the rewrite, 69 of 75 for the previous version. Triggering is identical in
both harnesses. No run in either harness attempted a write.

### Setup

| Item | Value |
|---|---|
| Claude Code | 2.1.281, model `claude-fable-5-1`, `claude -p --setting-sources project --strict-mcp-config --no-session-persistence`, tools `Read Glob Grep` (plus `Skill` for trigger runs) |
| Codex CLI | 0.154.0, model `gpt-5.6-sol`, reasoning effort high, `codex exec --sandbox read-only --ephemeral`, a throwaway `CODEX_HOME` (login token plus a minimal config: web search, apps, plugins and MCP off, no MCP servers listed), `HOME` set to an empty folder |
| Scorer | `run_evals.py score`, judge `claude-opus-5-5` with no tools; any run that exits non-zero, gives an empty answer or attempts a write fails automatically |
| Fixtures | `fixtures.json`: 19 fixtures, 14 critical (5 runs each per harness), 5 others (1 run each); 75 runs per harness per version |
| Working folder | a fresh empty git repository. The skill under test was copied into `.claude/skills/work` and `.agents/skills/work`; for trigger runs every other library skill was copied in beside it |
| Network | Codex shell network is blocked by the sandbox (checked: a `curl` inside a run cannot resolve hosts). Claude runs had no shell tool |

### Classifier: runs passed

| Fixture | Critical | Claude, rewrite | Claude, previous | Codex, rewrite | Codex, previous |
|---|---|---|---|---|---|
| stage-in-review-entry-breach | yes | 5/5 | 5/5 | 5/5 | 4/5 |
| gate-complete-anchor-absent | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| acceptance-scope-changed-after-approval | yes | 5/5 | 5/5 | 1/5 | 2/5 |
| head-changed-after-checks-and-review | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| pr-closed-not-merged | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| merged-not-deployed | no | 1/1 | 1/1 | 1/1 | 1/1 |
| deployment-contains-merge-commit | no | 1/1 | 1/1 | 1/1 | 1/1 |
| optional-state-explicitly-inapplicable | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| optional-state-not-resolved | no | 1/1 | 1/1 | 1/1 | 1/1 |
| no-profile | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| legacy-profile-gates-only | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| board-state-missing-from-profile | yes | 5/5 | 5/5 | 4/5 | 5/5 |
| two-plausible-candidates | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| contradictory-deployment-sources | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| inferred-only-anchor | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| terminal-live | no | 1/1 | 1/1 | 1/1 | 0/1 |
| live-without-production-verification | no | 1/1 | 1/1 | 1/1 | 0/1 |
| earlier-gate-breach-behind-item | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| optional-state-unexamined | yes | 5/5 | 5/5 | 5/5 | 5/5 |
| **Total** | | **75/75** | **75/75** | **70/75** | **69/75** |

Attempted writes: 0 in all 300 runs.

### Triggers

Each prompt was run three times per harness. The skill counts as started
when the run calls it (Claude) or reads its `SKILL.md` or returns its map
(Codex).

| | Claude, rewrite | Claude, previous | Codex, rewrite | Codex, previous |
|---|---|---|---|---|
| Should invoke (started) | 15/15 | 15/15 | 15/15 | 15/15 |
| Should not invoke (stayed quiet) | 15/15 | 15/15 | 15/15 | 15/15 |
| Explicit `/work` or `$work` loads the skill | 1/1 | 1/1 | 1/1 | 1/1 |
| Attempted writes | 0 | 0 | 0 | 0 |

### Failures

- **`acceptance-scope-changed-after-approval`, Codex, both versions.** The
  stage, drift and gate are always right: Staging Review, `ahead`, and the
  gate to Approved with AC4 UAT and a current sign-off unmet. Most Codex
  runs fail on two scored fields. They fold the earlier AC1 to AC3 UAT
  passes into the unmet UAT line instead of listing them as met history.
  Some also propose asking for or building an AC4 implementation, which is
  not a gap the map shows. Both versions fail this way (rewrite 1/5,
  previous 2/5), so this is a model behaviour, not a difference between the
  versions. It is the one critical fixture below the 5 of 5 threshold in
  Codex.
- **Codex, rewrite, `board-state-missing-from-profile` run 4.** The map was
  correct. The proposed next step bundled running UAT with posting a
  sign-off request. It was only a proposal, nothing was attempted, but the
  judge marked it as crossing the authority line.
- **Codex, previous version.** `stage-in-review-entry-breach` run 5 used
  the Todo gate for the gate line, because the export did not show the
  impact field. `terminal-live` proposed a pointless re-inspection.
  `live-without-production-verification` reported Live although the smoke
  checks had not run.

### Known limitations

- The judge is a model. It applies the README's rules to each run's final
  text, and a failed run is read by hand before it is recorded. Borderline
  calls are noted in each run's score file, which is kept outside the
  repository.
- Codex cannot pin a model snapshot the way Claude's `--model` does. The
  model name is set in the command.
- Scenarios EVAL-001 to EVAL-020 and EVAL-029 have no executable fixture
  yet. They are checked by hand.
- Claude trigger runs have the whole library installed beside `work`.
  Codex trigger runs use the same library through `.agents/skills`.
- Before this run, the scorer's next-action rule briefly required the
  expected action's decision to appear in the receipt. That is stricter
  than the suite's rule, which is to close a displayed gap and stay within
  authority, and it failed the previous version on runs its own suite had
  passed. The rule was put back before any figures above were scored. No
  expected value in `fixtures.json` was changed.
