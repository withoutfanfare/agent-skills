---
name: tenancy
description: >-
  Designs and implements multi-tenant data isolation: choosing between
  shared tables and separate schemas, resolving the current tenant from the
  request, scoping every query automatically, and proving two tenants
  cannot see each other's data. Use when building a SaaS application, adding
  tenant isolation, wiring up subdomain or workspace routing, or the user
  mentions multi-tenancy, tenant scoping or cross-tenant data leaks.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Tenancy

A multi-tenant application serves many customers from one codebase, and
every query that forgets to filter by tenant is a data leak waiting to
happen. The leak rarely shows up in testing, because a single developer
account only ever sees its own data; it shows up when a real customer
reports seeing someone else's invoice. This skill treats tenant isolation
as a property to build in and prove, not a filter to remember.

## 1. Choose an isolation strategy

Pick one, and say why, before writing any code:

| Strategy | How it works | Isolation | Cost |
|---|---|---|---|
| Shared tables, tenant column | Every tenant-owned row carries a `tenant_id`; one database, one schema | Depends entirely on every query filtering correctly | Cheapest to run and migrate |
| Separate schema per tenant | One database, one schema per tenant, same tables | Stronger: a forgotten filter still hits the wrong schema, not another tenant's data | More migration and connection overhead |
| Separate database per tenant | Each tenant gets its own database | Strongest, and the usual answer for regulatory or contractual isolation requirements | Most operational overhead: backups, migrations and connections all multiply |

Shared tables with a tenant column suit most products: it is the cheapest
to build and scales well until a specific tenant needs contractual or
regulatory isolation. Reach for separate schemas or databases only when
that requirement is real, not as a default for safety, since it multiplies
every migration and backup task by the tenant count.

Done when: the strategy is named along with the reason (scale, compliance,
cost) and written down where the team will find it again.

## 2. Resolve the current tenant once, early

Work out which tenant a request belongs to in one place, as early in the
request lifecycle as possible (middleware, a request filter, an interceptor),
and hold the result somewhere every later step can read it without
re-resolving it. Common ways to identify the tenant:

- **Subdomain**: `acme.example.com` maps to the tenant with slug `acme`.
- **Custom domain**: the tenant configured a domain, looked up directly
  against the request host.
- **Path prefix**: `/t/acme/dashboard`, useful when subdomains are not
  available.
- **The signed-in user's own tenant**: the user record carries which
  tenant they belong to.

Whichever method you pick, resolve it from the host matched against
tenants you know, or from the authenticated user, never from a value the
client can freely set such as a form field or query string. The host is
client-supplied too, so it only selects a tenant; it grants nothing. After
resolving, confirm the signed-in user actually belongs to that tenant, or
anyone can point a request at `other-tenant.example.com` with their own
session. A request claiming `?tenant_id=4` proves nothing.

If resolution fails, fail closed: return a not-found or unauthorised
response rather than falling back to a default tenant or no tenant at all.

Done when: one piece of code resolves the tenant, every other layer reads
that result, and no path accepts a client-supplied tenant id at face value.

## 3. Scope every query automatically, not by convention

Relying on every developer to remember `WHERE tenant_id = ?` on every query
fails the first time someone forgets, and code review will not catch every
instance forever. Push the scoping into the data layer instead, so a query
written without thinking about tenancy is still safe:

- An ORM global scope, query filter or default predicate that applies to
  every read and write for tenant-owned models.
- On write, auto-populate the tenant id from the resolved tenant rather
  than trusting a value passed in.
- Reserve an explicit bypass (an "unscoped" or "across tenants" call) for
  genuine cross-tenant work such as admin tooling, and keep it easy to grep
  for so it never hides inside ordinary application code.

Index the tenant column (or lead with it in a composite index) on every
table it appears on: a query correctly scoped to one tenant out of
thousands is still a full table scan without one.

Done when: a query written with no special effort is scoped by default, and
every place that deliberately reads across tenants is a named, searchable
exception.

## 4. Carry the tenant into background work

Background jobs, scheduled tasks and queue workers do not inherit whatever
resolved the tenant for a web request, because they run outside it. Pass
the tenant explicitly into the job (an id or the resolved record) and have
the job re-establish tenant context for itself at the start of its work,
the same way the request middleware would.

A job that silently runs unscoped either does nothing useful (the global
scope finds no tenant and returns nothing) or, worse, touches every
tenant's data at once. Check any code that catches "no tenant resolved" and
treats it as "all tenants" rather than an error.

Done when: every background job that touches tenant-owned data receives
its tenant explicitly and sets that context before it queries anything.

## 5. Prove the isolation, don't assume it

Write a test that creates two tenants, puts data under each, and asserts
that operating as one tenant never returns or affects the other's rows.
Cover both directions: reading (a list only shows the current tenant's
records) and writing (a new record is stamped with the current tenant, and
an attempt to update another tenant's record by id fails).

```text
given tenant A and tenant B each have a record
when acting as tenant A and listing records
then only tenant A's record appears

when acting as tenant A and updating tenant B's record by its id
then the request is refused, not silently ignored
```

Run this test whenever the scoping mechanism changes, not only once at
launch: a refactor of the data layer is exactly when an automatic scope
gets dropped by accident.

For separate schema or database isolation, also test that the schema or
database switch happens for every request and never leaks a connection
into the next one (a pooled connection carrying tenant A's schema into a
request for tenant B is the same leak with a different cause).

Done when: an automated test fails if tenant isolation breaks, and it has
been run and seen passing against the real scoping mechanism.

## 6. Separate tenant routes from operator routes

Admin or operator tooling that manages tenants from outside any single
tenant needs its own routes, guarded by its own authorisation, and must
not sit behind the same middleware that resolves and enforces a single
tenant. Mixing the two means either the admin panel cannot see across
tenants, or a tenant route accidentally inherits admin-level reach.

Done when: tenant-scoped routes and cross-tenant admin routes are visibly
separate, each with the guard that matches its purpose.

Laravel specifics (global scopes, traits, middleware, dynamic database
connections, named packages): [references/laravel.md](references/laravel.md).

## It's working if

- A query written by someone who never thought about tenancy is still
  scoped correctly.
- The two-tenant isolation test exists, runs in the normal test suite, and
  has been seen to fail when the scoping is deliberately broken.
- No code path trusts a tenant id supplied by the client without checking
  it against the resolved tenant.
