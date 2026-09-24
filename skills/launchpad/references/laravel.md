# Laravel deployment notes

## Example CI workflow

```yaml
name: CI
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: "8.3"
          coverage: none
      - uses: actions/cache@v4
        with:
          path: vendor
          key: composer-${{ hashFiles('composer.lock') }}
      - run: composer install --no-interaction --prefer-dist
      - run: cp .env.example .env && php artisan key:generate
      - run: vendor/bin/pint --test
      - run: vendor/bin/phpstan analyse --no-progress
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci && npm run build
      - run: php artisan test --parallel
        env:
          DB_CONNECTION: sqlite
          DB_DATABASE: ":memory:"
```

The build runs before the tests because any test that renders a page using
`@vite` fails without the built manifest; the alternative is calling
`$this->withoutVite()` in those tests. `--parallel` needs the
`brianium/paratest` dev dependency; drop the flag if the project does not
have it.

## Deploy steps

In order, for a release directory or platform deploy:

```bash
composer install --no-dev --optimize-autoloader --no-interaction
npm ci && npm run build
php artisan migrate --force
php artisan optimize          # caches config, routes, events and views
php artisan queue:restart     # workers pick up the new code
php artisan storage:link      # every deploy if each release gets a fresh folder
```

- **Forge:** put these in the deploy script; enable "quick deploy" only
  for staging if production needs a manual promote.
- **Envoyer or Deployer:** zero-downtime by design (a new release folder,
  then a symlink switch); share `.env` and `storage/` between releases.
- **Vapor:** set up environments in `vapor.yml`; run migrations with the
  deploy hook.

Avoid `php artisan down` for routine deploys; zero-downtime switching makes
it unnecessary. Keep it for long, risky migrations.

## Health endpoint

Laravel 11 and later include a `/up` route (set in `bootstrap/app.php`).
Extend it with a listener on the `DiagnosingHealth` event, or add your own
route that checks the database, cache and queue connection and returns a
503 on failure.

## Rollback

Switch the `current` symlink back to the previous release (or redeploy the
previous tag on a platform), then `php artisan optimize` and
`php artisan queue:restart`. Only roll back a migration if it is known to
be safe and reversible; otherwise ship a forward fix.
