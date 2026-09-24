# Dependency checks in CI

Run audits on every pull request and on a schedule, so a new advisory for
an unchanged dependency is still noticed.

## GitHub Actions example

```yaml
name: Dependency audit
on:
  pull_request:
  schedule:
    - cron: "0 6 * * 1"   # Mondays at 06:00

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm audit --omit=dev --audit-level=high
      - uses: shivammathur/setup-php@v2
        with:
          php-version: "8.3"
      - run: composer install --no-interaction --no-progress
      - run: composer audit
```

`--audit-level=high` fails the job on high and critical advisories only.
Start there, then tighten once the backlog is clear.

## Automated update pull requests

Dependabot or Renovate can open update pull requests for you. Group patch
and minor updates to keep the noise down, and keep majors as separate pull
requests:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule: { interval: weekly }
    groups:
      minor-and-patch:
        update-types: [minor, patch]
  - package-ecosystem: composer
    directory: /
    schedule: { interval: weekly }
```
