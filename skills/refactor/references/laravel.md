# Laravel refactoring patterns

Where each kind of logic usually lives in a Laravel application, and the
refactoring that moves it there.

| Move this | Out of | Into |
|---|---|---|
| Validation rules | Controllers | A Form Request class |
| Authorisation checks | Controllers and views | A Policy, called with `authorize()` or `can` |
| A reusable business operation | Controllers, jobs, commands | A service class (several related operations) or an action class (one operation with an `execute` or `handle` method) |
| Repeated `where` clauses | Many queries | A local query scope on the model |
| A concept stored as a primitive (money, email address, status) | Scattered strings and integers | A value object, with an Eloquent cast |
| Response shaping | Controllers | An API Resource |
| Side effects after something happens (emails, logs, syncing) | The main operation | An event and listeners, or a queued job |
| Switching on a type string | `if` and `match` chains | An enum with methods, or one class per type behind an interface |

## Keep controllers thin

A controller method should read: validate (Form Request), authorise
(Policy), call one service or action, return a response or resource.
Anything more is a candidate to move.

## Repositories: only with a reason

Eloquent is already a data-access layer. Add a repository only when there
is a real need: complex queries reused in many places, or a data source
that might change. Otherwise, scopes and query objects are
lighter.

## Useful checks while refactoring

```bash
php artisan test --filter=<AreaUnderChange>   # fast loop on the area
vendor/bin/phpstan analyse <paths>            # if the project uses it
vendor/bin/pint --test <paths>                # formatting, if used
```
