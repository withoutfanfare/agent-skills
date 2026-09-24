# Laravel verification notes

## Clear stale state before verifying

```bash
php artisan optimize:clear
```

Config, route and view caches can serve pre-change behaviour, making a
verification run pass or fail against last week's code.

## Rung 1: targeted tests

```bash
php artisan test --filter=NameOfTheThing
vendor/bin/pest --dirty          # only test files with uncommitted changes
```

`--dirty` picks test files, not source files: a change to `app/` alone runs
nothing. When only source has changed, name the tests with `--filter`.

## Rung 2: static analysis and style

```bash
vendor/bin/phpstan analyse app/Path/To/Changed
vendor/bin/pint --test           # style check only, does not rewrite files
```

## Rung 3: HTTP smoke pass

The script lives in this skill's own `scripts/` folder, not the project's,
so call it by that path (in Claude Code, `${CLAUDE_SKILL_DIR}`; in other
agents, wherever the skill is installed):

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/http-smoke.sh" https://your-app.test routes.txt
```

Local `.test` domains served over HTTPS with a self-signed certificate need
`curl -k`; the bundled script already does this. Hitting an API route
without an `Accept: application/json` header returns the HTML error page on
failure, not the JSON body, so an assertion against JSON silently fails for
the wrong reason.

If the frontend build has not run, pages throw a manifest-not-found error
that looks like an application bug but is really a missing `npm run build`.

## Rung 4: database state

```bash
php artisan tinker --execute="dd(Order::find(1)->status);"
```

Or a direct Pest assertion:

```php
$this->assertDatabaseHas('orders', ['id' => $order->id, 'status' => 'shipped']);
```

A queued side effect (a job, a queued notification, a queued listener)
never fires in a normal development environment unless a worker is
running. Run `php artisan queue:work --once` during verification, or check
`jobs` and `failed_jobs` directly, rather than assuming a queued action
happened because the request returned 200.

A freshly migrated, near-empty test database hides pagination bugs, N+1
queries and scoping mistakes that only show up with realistic data volume.
For anything data-sensitive, also check against a seeded or copied
database, not only the test suite's throwaway one.

## Rung 5: browser-driven flow

Livewire and admin-panel interactions are JavaScript-dependent: a 200 from
`curl` only proves the page shell rendered, not that the interactive part
works. Use the browser automation tools available to click through the
actual flow, or fall back to a component-level test
(`Livewire::test(Component::class)->set(...)->call(...)->assertSee(...)`)
when a full browser run is not warranted.

Save one screenshot per step to a dated run folder so the evidence survives
the conversation.

## A per-project verification map

Larger apps benefit from a small checked-in config naming the base URL, the
test command, the routes worth smoke-checking and their expected statuses,
and the two or three flows that must never break. Keep it small: a handful
of routes and flows that matter, not an exhaustive site map.
