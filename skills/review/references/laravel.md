# Laravel review notes

Extra checks for Laravel applications. Each is a mistake that is easy to
make and easy to miss.

| Check | Why it matters | What good looks like |
|---|---|---|
| Models guard mass assignment | `Model::create($request->all())` lets a user set any column, including admin flags | `$fillable` on every model, and `create($request->validated())` |
| Validated input only | `$request->all()` skips the validation rules entirely | Form Requests, and only `validated()` data passed on |
| Authorisation on every write | Being signed in is not permission to change this record | A policy check (`authorize`, `can`) in every action that changes data |
| Relationships loaded up front | A relationship used inside a loop runs one query per row | `with()` for relationships, `withCount()` for counts |
| Related writes in a transaction | A failure halfway leaves orphaned rows | `DB::transaction()` around writes that belong together |
| Jobs safe to run twice | Queued jobs are retried; a payment job could charge twice | An idempotency key or unique constraint, and a `failed()` method |
| `env()` only in config files | It returns null once configuration is cached | `config()` everywhere else |
| Timeouts on HTTP calls | A slow service hangs the request or worker | `Http::timeout()` on every outside call |
| Scoped route binding | Implicit binding finds any record by ID | Scoped bindings or a policy on the bound model |
| No empty `catch` blocks | Swallowed exceptions hide real failures | Log, rethrow or handle a specific exception |

Useful tools, where the project already has them: Larastan or PHPStan for
types, Pint for formatting, and the test suite run with coverage for the
changed files. Leave anything these catch to them.
