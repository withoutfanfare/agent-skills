---
name: launchpad
description: >-
  Sets up continuous integration and deployment for a web application:
  pipeline checks, deploy steps for staging and production, zero-downtime
  releases, environment configuration, health checks and a rehearsed
  rollback. Use when the user wants a CI or CD pipeline, GitHub Actions
  workflows, a deploy script, zero-downtime deploys, or a rollback plan.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Launchpad

A deploy should be boring: the same checks every time, the same steps
every time, and a way back that has actually been tried. This skill builds
that path from a commit to production, using the project's hosting and
tools, with nothing that only works on one person's laptop.

## 1. Survey what exists

Find the current pipeline files (`.github/workflows/`, other CI
configuration), deploy scripts or hosting settings, how releases happen
today, the environments that exist, the test and quality commands, and
where secrets are kept.

Done when: you can describe today's path from commit to production,
including every manual step.

## 2. Build the checks (CI)

On every pull request, run in this order so the cheap checks fail first:
install with the lockfile, formatting, static analysis, tests (with a
throwaway database and services), then build. Cache dependencies. Fail on
any error; never mark a failing step "continue on error" to get green.
If tests render pages that load built front-end assets, run the build
before the tests, or have the tests stub those assets.

Done when: a pull request with a failing test shows a red check, and a
clean one shows green (try both).

## 3. Build the deploy (CD)

Deploy from the main line, to staging first, then production:

1. Build once, and promote the same build between environments.
2. Run database migrations in a backwards-compatible way: the old version
   must still run against the new schema while the release switches over.
3. Switch traffic to the new release in one step (a symlink, a container
   swap, a platform deploy), so there is no half-deployed moment.
4. Warm caches and restart workers so they pick up new code.
5. Run a smoke test against the live release.

Keep secrets in the platform's secret store, never in the repository or
workflow files.

Done when: a deploy to staging runs end to end from a merge, with the smoke
test passing.

## 4. Health checks

Add a health endpoint that checks the essentials (database, cache, queue,
critical outside services) and returns an error status when any fails.
Point the platform's health check and the smoke test at it.

Done when: stopping a dependency makes the health check fail.

## 5. The way back

Write the rollback: switch back to the previous release, and what to do
about migrations (prefer roll-forward fixes for data; keep the previous
release able to run on the new schema). Rehearse it on staging.

Done when: a rollback has been performed on staging, and the time it took
is recorded.

## 6. Production safety checklist

- Debug mode off; unique application key per environment.
- HTTPS enforced; secure cookies.
- Secrets only in the secret store; `.env` files ignored by git.
- Least-privilege deploy credentials.
- Deploys cannot run with failing checks.

Laravel specifics (Forge, Envoyer or Deployer, artisan steps, example
workflow) are in [references/laravel.md](references/laravel.md).

## It's working if

- Deploying is one action, and it is the same action every time.
- A failed check blocks the deploy.
- Rollback has been rehearsed, and everyone knows how long it takes.
