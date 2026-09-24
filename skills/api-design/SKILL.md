---
name: api-design
description: >-
  Designs a web API's resources, versioning, pagination, authentication and
  error format before or alongside implementation, so endpoints are
  consistent and predictable to any client. Use when designing new API
  endpoints, deciding on API versioning, standardising error responses, or
  the user asks about REST conventions or how an API should paginate or
  authenticate.
license: MIT
allowed-tools: Read Write Edit Grep Glob
---

# API design

An API that grows one endpoint at a time, each one designed on its own,
ends up with three different pagination shapes and two different error
formats before anyone notices. A client written against one endpoint then
breaks on the next. This skill fixes the shape of resources, versioning,
pagination, errors and auth once, so every endpoint added afterwards is a
copy of a working pattern rather than a fresh decision.

## 1. Name the resources

List the nouns the API exposes (orders, subscriptions, invoices), not the
actions on them. Give each one a plural, lowercase, hyphenated path
segment, and use the standard verb-to-method mapping so a client can guess
an endpoint it has never seen:

| Action | Method | Path | Meaning |
|---|---|---|---|
| List | GET | `/items` | collection |
| Show | GET | `/items/{id}` | one resource |
| Create | POST | `/items` | new resource |
| Replace | PUT | `/items/{id}` | full update |
| Partial update | PATCH | `/items/{id}` | partial update |
| Delete | DELETE | `/items/{id}` | remove |

Nest a resource under its parent only when it cannot exist independently
(`/orders/{id}/line-items`), and stop at one level of nesting; a second
level almost always means the child deserves its own top-level, filterable
path instead.

Done when: every planned endpoint maps to one row of this table, with no
verb in the path itself (no `/getOrders`, no `/order/cancel`).

## 2. Decide the versioning strategy up front

Put the version in the URL path (`/v1/orders`), not in a header or a query
parameter. A path segment is visible in every log line, every browser tab
and every curl command, which makes a client's mistake ("I'm still on v1")
obvious without inspecting request internals.

When a version is retired, do not remove it outright. Add a deprecation
period: return a `Deprecation` header giving the date it was deprecated
(`@` plus a Unix timestamp, such as `@1767225600`, never `true`) and a
`Sunset` header giving the removal date, and keep the old version serving real responses until that
date passes. Removing a version the moment a new one ships breaks every
client that has not yet migrated, silently, at a time you do not control.

Done when: the version is in the URL, and any retirement has a published
sunset date rather than a surprise removal.

## 3. Fix the error shape once

Every error, from every endpoint, returns the same envelope, so a client
writes one error handler instead of one per endpoint:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The request could not be processed.",
    "details": [
      { "field": "email", "message": "An email address is required." }
    ]
  }
}
```

Map failure categories to status codes once, centrally, rather than letting
each endpoint pick its own: `422` for invalid input, `401` for missing or
invalid credentials, `403` for a valid credential without permission,
`404` for a resource that does not exist (or that the caller cannot see,
if hiding existence matters), `429` for rate limiting, `500` only for a
genuine, unexpected server fault. `code` is a stable machine-readable
string a client can branch on; `message` is for a human; `details` carries
per-field information and can be omitted when there is none.

Done when: two different endpoints producing the same kind of error return
byte-for-byte the same shape and status code.

## 4. Fix pagination once

A collection endpoint that might return more than a page of results needs,
from the first version, a consistent paging shape:

```json
{
  "data": [ /* ... */ ],
  "meta": { "current_page": 2, "per_page": 25, "total": 143 },
  "links": { "first": "...", "prev": "...", "next": "...", "last": "..." }
}
```

Cap `per_page` server-side (do not trust a client-supplied number without a
ceiling) and make the default page size explicit in the documentation, not
just in behaviour.

Done when: every list endpoint returns `data`, `meta` and `links` in this
shape, even the ones nobody expects to page through yet.

## 5. Decide auth once, and apply it uniformly

Pick one primary scheme for the API (a bearer token, an API key header, or
OAuth2 scopes) and use it everywhere; mixing schemes per endpoint means a
client needs to know, endpoint by endpoint, which credential to send. State
which endpoints are public and which need auth as a table, not as an
implicit property of the route file, so it can be audited in one pass.

Done when: there is a single sentence describing how any client
authenticates to any endpoint, with named exceptions for public routes.

## 6. Return the right status for the outcome

`200` for a successful read or update that returns a body, `201` for a
create (with the created resource in the response and a `Location`
header), `202` for work queued rather than done synchronously, `204` for a
successful action with no body (typically delete). Getting these wrong
does not break most clients immediately, but it breaks any tooling that
inspects status codes to decide whether to retry, which is most HTTP
client libraries.

Done when: each endpoint's success status matches what it did, not
a copy-pasted `200` from a neighbouring endpoint.

## 7. Write it down where clients will find it

Document each endpoint's method, path, request shape, response shape and
possible error codes, either inline near the code (attributes or
docblocks a generator can read) or as a standalone OpenAPI document kept
next to the code it describes, so it is reviewed in the same pull request
as the change it documents rather than drifting out of date separately.

Done when: a new endpoint's documentation was written in the same change
that added the endpoint.

Laravel implementation detail (form requests, API resources, versioned
route groups, exception handler mapping): see
[references/laravel.md](references/laravel.md).

## It's working if

- A client can predict the path and method for an action it has not seen
  yet, from the table in step 1 alone.
- Every error response across the whole API can be handled by one piece of
  client code.
- A version can be retired on a published date without breaking anyone who
  has not migrated yet.
