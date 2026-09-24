# Laravel testing notes

## Keep the test database throwaway

Check both places that decide which database tests use. `.env.testing`
takes precedence over `phpunit.xml`:

```bash
grep -E 'DB_CONNECTION|DB_DATABASE' .env.testing 2>/dev/null
grep -E 'DB_CONNECTION|DB_DATABASE' phpunit.xml
```

Safe answers are `DB_CONNECTION=sqlite` with `DB_DATABASE=:memory:` or a
dedicated test file such as `database/testing.sqlite`. Anything else (MySQL,
PostgreSQL, a development database file) means stop and ask. Tests that use
`RefreshDatabase` wipe the database they connect to.

If configuration is cached, tests may ignore the test settings entirely.
Clear it first: `php artisan config:clear`.

## Conventions

- Run tests with the project's Composer script when there is one
  (`composer test`), otherwise `php artisan test`.
- Pest: group with `describe()`, write cases with `it()` or `test()`, share
  setup in `beforeEach()`. PHPUnit: use the `#[Test]` attribute rather than
  the old `/** @test */` comment.
- Build data with model factories and their states rather than inserting
  rows by hand.
- Fake outside effects: `Mail::fake()`, `Queue::fake()`, `Event::fake()`,
  `Notification::fake()`, `Http::fake()`, `Storage::fake()`.
- Act as a user with `actingAs($user)`; test permissions with a second user
  who must be refused.
- Livewire components: `Livewire::test(Component::class)->set(...)->call(...)->assertSee(...)`.

## Useful assertions

| Checking | Assertion |
|---|---|
| Status | `assertOk()`, `assertCreated()`, `assertForbidden()`, `assertNotFound()` |
| Validation | `assertSessionHasErrors('field')`, `assertJsonValidationErrors('field')` |
| Database | `assertDatabaseHas()`, `assertDatabaseMissing()`, `assertModelExists()` |
| Redirects | `assertRedirect(route('name'))` |
| JSON | `assertJsonPath('data.id', $id)`, `assertJsonStructure([...])` |
| Fakes | `Mail::assertSent()`, `Queue::assertPushed()`, `Http::assertSent()` |

## Useful commands

```bash
php artisan test --filter="refuses a guest"      # one test by name
php artisan test tests/Feature/OrderTest.php     # one file
php artisan test --parallel                      # faster suites
php artisan test --coverage --min=80             # coverage with a floor
```
