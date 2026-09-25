# Delivery profile: <project>

The `work` skill reads this on every run. It tells any teammate's AI tool
how this project ships. Keep the headings; replace the content. Write
"none" under a heading rather than deleting it, and link to longer policy
documents instead of copying them. Save it as `docs/delivery-profile.md`.

## Lifecycle

List the board's states in board order, spelt exactly as the board shows
them. For each state give:

- **Applies when**: `always`, or the condition that brings an item through
  this state. A conditional state is not skippable: it applies until
  evidence proves the condition false.
- **Evidence anchor**: one fact that can be checked against the exact pull
  request, commit, deployment and acceptance scope, and that shows the item
  has arrived.
- **Gate to enter**: what should be true before the card moves in. A
  complete gate alone never places an item in a state.
- **Note on entry**: the update the board expects on arrival.
- **Mode**: the `work` mode that does the work for this state.

Assistants move a card only when the user asks, and only into a state
whose gate is fully met.

- Tracker route: `<one of: gh CLI against <owner/repo> and project <n> | the Jira CLI for project <KEY> | the connected tracker tool | none, paste the issue>`. One route only.
- Definition of Ready: `<link to the issue template or checklist>`.
- Tracker writes assistants may make: `<e.g. comments and pull request links when the user asks; state moves when the user asks and the gate is met; the approval state only once the acceptance owner's sign-off is on the issue; the live state only after production checks pass>`.
- WIP limits and staleness rules (reported only): `<link or none>`.

| State | Applies when | Evidence anchor | Gate to enter | Note on entry | Mode |
| --- | --- | --- | --- | --- | --- |
| `<Backlog>` | always | the issue exists and nothing later can be found in the repository or environments | issue meets the Definition of Ready | none | spec |
| `<Doing>` | always | commits for this issue exist on its branch or worktree `<or: the recorded start event>` | acceptance criteria agreed; owner, priority and cycle set | short progress comment | build |
| `<Integration>` | `<only if the diff touches <paths or shared contracts>, else not applicable>` | the exact head runs in `<integration environment>` | slice finished; deployed checks needed; merged to `<integration branch>` | evidence or notes | build |
| `<Code review>` | always | an open pull request into `<base>` carries the exact head | pull request raised into `<base>` with test notes; required checks passing on the head | comment linking the pull request | ship / review |
| `<Merged>` | always | the pull request shows a merge time and its merge commit is on `<base>` (closed, green or "merged" in a comment is not enough) | review comments resolved; checks passing; deploy notes written | none | review |
| `<On staging>` | always | `<staging>` reports the exact merge commit `<via a health endpoint, a release tag or a build id tied to the commit>`; a branch name is never proof | merged and deployed to staging; UAT plan written | progress comment | verify |
| `<Accepted>` | always | `<acceptance owner>` has recorded sign-off on the issue for this deployed candidate and the current criteria | every in-scope UAT scenario passed; sign-off recorded on the issue | none | accept |
| `<Live>` | always | production reports the exact accepted commit and the production smoke checks passed | released and checked in production | none | release |

## Branches and pull requests

- Repository default: `<main>`, protected; nobody pushes to it directly.
- Every pull request targets: `<develop>`. Never `<main>`.
- Branch and worktree naming: `<e.g. one branch per issue, named after its key>`.
- Creating a worktree: `<command or tool; files it copies in such as .env or built assets; steps to run afterwards if made by hand; whether the tool pushes the new branch when it creates it (fine while the branch still matches its base)>`.
- Pull request description: `<e.g. the problem first in plain words, then the fix, then how to check it>`. Template: `<path or none>`.
- Pull request title: `<e.g. conventional commit style plus the issue key>`.

## Commits and quality gates

- Commit style: `<e.g. conventional commits>`.
- Staging files: `<e.g. add named paths only>`.
- Before committing: `<lint command>`.
- Before pushing or opening a pull request: `<test command>`, `<static analysis command>`.
- Known failures to ignore: `<link or none>`.

## Artefact locations

| Artefact | Folder and filename pattern |
| --- | --- |
| Feature brief | `<docs/briefs/YYYY-MM-DD-<key>-<slug>.md>` |
| Decision records | `<inside the brief, or docs/decisions/>` |
| UAT plans and run reports | `<docs/uat/<area>/<date>-<key>.md>` |
| Evidence from runs | `<beside the UAT report, or none>` |
| Runbooks | `<docs/runbooks/>` |
| Plain-English docs | `<docs/developers/, docs/help/>` |

## Environments

| Environment | Address and how to reach it | What is allowed | Owner |
| --- | --- | --- | --- |
| Local | `<URL or start command>` | anything that can be undone | the developer |
| Staging | `<URL>` | UAT and smoke checks; `<how it is deployed>` | `<role>` |
| Production | `<URL>` | authorised releases and smoke checks only | `<role>` |

## Release

- Release branch and who merges to it: `<e.g. develop into main, merged by a person; assistants never merge or push there>`.
- Schedule and cut-off: `<e.g. Tuesdays and Thursdays, sign-off by 12:00>`. Eligible when: `<e.g. Accepted, in the current cycle, before the cut-off>`; otherwise it waits for the next release.
- Urgent route: `<who may release outside the schedule, and for how small a change>`.
- Deploy: `<what starts it, who may start it, where the announcement appears>`.
- Post-deploy smoke checks: `<URLs, commands or scenarios; how long to watch>`.
- Rollback: `<command or runbook link>`.
- Closing the issue: `<e.g. move to Live once the production checks pass; release notes go in docs/releases/>`.

## People and authority

- Product sign-off: `<name or role>`.
- Code review: `<who, and how they are assigned>`.
- Release authority: `<name or role>`.
- Accepting risk: `<name or role>`.

## Documentation

| Kind of change | Readers | `plainify` purpose | Saved to |
| --- | --- | --- | --- |
| Platform or infrastructure | developers | onboarding guide | `<docs/developers/...>` |
| Admin feature | admin users | help article | `<docs/help/...>` |
| Operational change | operators | runbook entry | `<docs/runbooks/>` |
| Customer-facing release | customers | release notes | `<where>` |

## Project traps

- `<links to the project's own guardrail docs>`.
- `<destructive commands that are forbidden, or that need a named person to confirm>`.
