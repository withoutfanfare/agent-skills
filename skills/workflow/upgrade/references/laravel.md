# Laravel and PHP upgrade notes

The worked notes below cover Laravel 9 to 11. For any later jump, read the
official upgrade guide for the target version in full; do not extrapolate
from these notes.

## composer.json first

The version bump starts in `composer.json`. Update the `php` constraint and
`laravel/framework`, then let Composer work out the rest:

```json
{
    "require": {
        "php": "^8.3",
        "laravel/framework": "^<target>.0"
    }
}
```

Run `composer update laravel/framework --with-all-dependencies` rather than
a blanket `composer update`, so unrelated packages do not move at the same
time and muddy the diff. `composer outdated --direct` shows which of your
own dependencies still lag; `composer why-not laravel/framework ^<target>.0` shows
exactly which installed package is blocking the move.

## Laravel 10 to 11

The biggest change is optional, not mandatory: new applications get a
slimmer structure (a single `bootstrap/app.php` for middleware, routing and
exception handling, no `app/Http/Kernel.php`, no default `app/Console/Kernel.php`).
An existing application is not required to adopt this shape. Only migrate
into it deliberately, as its own piece of work, not as a side effect of the
version bump.

What every 10-to-11 upgrade does need:

- PHP 8.2 is now the floor.
- Several first-party packages (Sanctum, Cashier, Passport, Telescope) need
  their own major version bump alongside the framework, and no longer load
  their migrations automatically: publish them with `vendor:publish`. Check
  each one's own upgrade notes rather than assuming a patch bump covers it.
- A migration that modifies a column with `->change()` must now restate
  every modifier it wants to keep (`nullable`, `default`, `unsigned`,
  `comment`); anything left off is dropped.
- The `double` and `float` column types were rewritten and the
  `unsignedDecimal`/`unsignedDouble`/`unsignedFloat` helpers removed.
- SQLite 3.26.0 or newer is required.
- Passwords are rehashed on login when the hashing work factor has changed;
  a password column not called `password` needs `$authPasswordName`.
- The framework's own upgrade guide lists the rest by name and is short
  enough to read in full for this jump.

## Laravel 9 to 10

- PHP 8.1 becomes the floor.
- `$dates` on a model is removed; anything still using it needs the
  equivalent cast:

```php
// before
protected $dates = ['shipped_at'];

// after
protected $casts = [
    'shipped_at' => 'datetime',
];
```

- PHPUnit 10 becomes available but is optional. If you take it in the same
  jump, it changes how data providers and some assertions are declared; run
  the suite once after the bump purely to catch PHPUnit-level breakage
  before chasing application code.

## PHP 8.1 to 8.2

- Dynamic properties on a class not extending `stdClass` are deprecated. A
  class that relied on setting undeclared properties (common on quick
  value-object style classes) either declares them or gains the
  `#[\AllowDynamicProperties]` attribute as a stop-gap:

```php
class OrderTotals
{
    public function __construct(
        public readonly int $subtotal,
        public readonly int $tax,
    ) {}
}
```

## PHP 8.2 to 8.3

- Typed class constants and the `#[\Override]` attribute are new, not
  breaking; adopt them gradually rather than as part of the upgrade diff.
- `json_validate()` replaces the old `json_decode() === null` check for
  "is this valid JSON" without paying for the full decode.

## Common deprecation patterns worth grepping for

| Pattern | Why it surfaces during an upgrade |
|---|---|
| Manual `Carbon` timezone juggling | Default timezone handling has shifted more than once |
| Custom exception handler rendering | Moves between `Handler.php` and `bootstrap/app.php` in Laravel 11 |

## Automated fixes with Rector

Rector rewrites code for a target PHP or Laravel version, which turns a
long list of mechanical fixes into one reviewed diff:

```bash
composer require rector/rector driftingly/rector-laravel --dev
```

```php
// rector.php
use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use RectorLaravel\Set\LaravelSetList;

return RectorConfig::configure()
    ->withPaths([__DIR__ . '/app', __DIR__ . '/routes', __DIR__ . '/config'])
    ->withSets([
        LevelSetList::UP_TO_PHP_83,
        LaravelSetList::LARAVEL_110,
    ]);
```

```bash
vendor/bin/rector process --dry-run   # read the proposed diff first
vendor/bin/rector process             # apply it, then run the suite
```

Treat Rector's output as a draft, not a finished commit: read every file it
touched before running the suite against it.

## Rollback specifics

- `git switch --detach <pre-upgrade-tag>` plus `composer install` restores the
  dependency tree exactly, because `composer install` reads the committed
  `composer.lock` rather than resolving fresh.
- If a migration ran as part of the upgrade, test `php artisan
  migrate:rollback --step=1` against a copy of the data before you need it
  for real, not during an incident.
- A symlink-based deploy (releases directory plus a `current` symlink)
  makes the rollback a single `ln -sfn` back to the previous release, with
  no rebuild required.
