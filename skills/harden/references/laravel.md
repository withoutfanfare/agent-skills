# Laravel hardening notes

## Access control

- Every model that users act on has a Policy, and every controller action
  that reads or writes a record calls it (`$this->authorize()`, `Gate`,
  `can` middleware).
- Route model binding finds any record by ID. Scope it to the user or
  check the policy.
- Admin routes sit behind their own middleware group.

## Input and output

- Validation in Form Requests; only `$request->validated()` passed on.
- `$fillable` on every model; no `Model::unguard()`.
- Blade `{{ }}` escapes. Every `{!! !!}` must output trusted, sanitised
  HTML; search for them.
- Raw SQL (`DB::raw`, `whereRaw`, `selectRaw`, `DB::select`) uses `?`
  bindings, never string joins.
- CSRF: `@csrf` in every form; `X-CSRF-TOKEN` header for JavaScript
  requests; any route excluded from CSRF has a reason (such as a signed
  webhook).

## Configuration

```bash
grep -E '^(APP_DEBUG|APP_ENV|SESSION_SECURE_COOKIE|SESSION_HTTP_ONLY)=' .env.example
grep -rn "env(" app routes --include=*.php   # env() outside config breaks with cached config
```

- `APP_DEBUG=false` and `APP_ENV=production` in production.
- `SESSION_SECURE_COOKIE=true`, `http_only` true, `same_site` lax or strict.
- Security headers via middleware: Content-Security-Policy,
  Strict-Transport-Security, X-Content-Type-Options, Referrer-Policy.
- `config/cors.php` allows only known origins.

## Authentication

- Throttle sign-in and password reset (`throttle:` middleware or
  `RateLimiter`).
- Regenerate the session at sign-in (the built-in auth does; custom flows
  must call `$request->session()->regenerate()`).
- Signed URLs (`URL::signedRoute`) for one-off links, with an expiry.

## Uploads

- Validate with `mimes:` or `mimetypes:` and `max:`; do not trust the
  client's file name or type.
- Store with `store()` (random name) on a private disk; serve through a
  controller that checks permission.

## Useful commands

```bash
composer audit
php artisan route:list --except-vendor   # check middleware on every route
```
