---
name: nuxt
description: >-
  Builds and debugs Nuxt applications: file-based page and API routing,
  server routes and Nitro, data fetching with useFetch/useAsyncData, when to
  render on the server versus the client, runtime config and secrets, and
  which deployment target to build for. Use when the user mentions Nuxt,
  nuxt.config, server/api, useFetch, Nitro or nuxi build, or asks to add or
  fix a Nuxt page, layout or server route.
license: MIT
allowed-tools: Read Grep Glob Bash Write Edit
---

# Nuxt

Nuxt turns a folder structure into routes, middleware and an API, which is
convenient until the convention is broken without an error: a page nobody
can reach, a secret shipped to the browser, or a fetch that silently reuses
someone else's cached response. This skill covers Nuxt's own machinery,
routing, data fetching, rendering mode and deployment. For what happens
inside a component once it is mounted (component internals), hand off to
`vue` (if installed); for how a page should look, hand off to `tailwind`
or `sketch` (if installed).

Paths below use the Nuxt 4 layout, where `pages/`, `components/`,
`composables/`, `layouts/` and `app.vue` live inside `app/`, while
`server/`, `public/` and `nuxt.config.ts` stay at the root. A Nuxt 3
project keeps them all at the root; Nuxt 4 detects that layout and works
with it, so drop the `app/` prefix rather than moving files.

## 1. Let the file tree define the routes

A page under `app/pages/` is routed by its path and filename; there is no
router file to edit by hand. `[id].vue` captures one dynamic segment,
`[...rest].vue` catches everything below it, and a folder without an
`index.vue` has no route of its own. When a page seems unreachable, check
its file is actually where the URL implies before suspecting the router.

A server endpoint follows the same idea under `server/api/` (JSON) or
`server/routes/` (anything else), with the HTTP verb as a filename suffix:
`server/api/orders/[id].patch.ts` answers `PATCH /api/orders/:id`. A verb
mismatch between what the frontend calls and what the file is named
produces a 405, which reads like a routing bug but is a naming one.

Done when: every new page and endpoint sits at the file path its URL and
verb imply, with no route registered anywhere else.

## 2. Fetch data with the composable that matches the trigger

`useFetch` and `useAsyncData` exist to run during server-side rendering and
again on the client for hydration; use them for whatever a page needs as
soon as it loads. For data triggered by something a user does, a button, a
form, a filter change, call `$fetch` directly inside the handler instead.
Wiring a click handler to `useFetch` re-runs it on every reactive trigger
Nuxt tracks, not only the click, which is a common source of duplicate
requests.

Nuxt caches by key. `useFetch` builds its automatic key from the URL, the
options and the call site, so two calls with different parameters already
get separate entries. The trap is your own composable that wraps
`useAsyncData`: every caller runs the same line inside it, so without an
explicit key that includes the parameters, they all share one response.
Build the key from the inputs (`` `orders-${status}` ``). Pass a reactive parameter as a getter,
`() => filters.value.status`, not its current value, so a change to it
triggers a new request rather than being baked in at first render.

Done when: a change to a reactive input produces a new network request, and
two calls through the same composable with different parameters never show
the same data.

## 3. Keep server-only code out of what ships to the browser

Anything under `app/` (pages, components, `app.vue`) is bundled for the
client. Database access, third-party API keys and anything from
`server/utils/` belongs only in `server/`, never imported from a page or
component, even indirectly through a shared file. A stray import like this
produces no build error; it just puts a secret in a file anyone can view.

Done when: a search of the client build output for a server-only symbol or
secret finds nothing.

## 4. Decide server rendering per page, not by default

Server-side rendering is Nuxt's default, and it is wrong for anything that
depends on a browser-only API. Turn it off for a whole route in
`nuxt.config.ts` with `routeRules: { '/admin/**': { ssr: false } }`, or wrap the browser-only part in `<ClientOnly>` for a section of
one, rather than reaching for `window` or `localStorage` in code that also
runs on the server. A hydration mismatch warning in the console almost
always means the server-rendered markup and the first client render
disagree, usually because of exactly this.

Done when: the page's rendered HTML (viewed as the server sent it, not the
live DOM) contains what SSR is meant to provide, and the console shows no
hydration warning.

## 5. Put configuration where its exposure is deliberate

`runtimeConfig.public` in `nuxt.config.ts` reaches the browser; the
top-level `runtimeConfig` object does not. A value the client needs stuck
under the private half fails silently as undefined; a secret placed under
`public` by mistake fails just as silently by being exposed. Back each
value with an environment variable using Nuxt's naming (`NUXT_PUBLIC_X` for
public, `NUXT_X` for private) so the same build can move between
environments without a code change.

Done when: every value the client reads is under `public`, every secret is
not, and swapping the `.env` file changes behaviour without a rebuild of
the code.

## 6. Prove it with the framework's checks, then a real page load

Run the project's typecheck script (typically wrapping `nuxi typecheck`)
after any change to page props, server route bodies or composable return
types, and run a full `nuxi build` before calling anything finished, since
the dev server tolerates some things a production build does not, such as
an import that cannot be tree-shaken. Neither proves the page works; both
only prove it compiles. Load the actual page, in a real browser or the
project's own preview, and report what the network tab and console showed,
not what the code is supposed to do.

Done when: typecheck and build both complete without error, and you can
describe the requests and console output you actually saw for the page you
changed.

## 7. Match the deployment target to what the app needs at runtime

`nuxi generate` produces a static site with no working server: right for an
app with no `server/` routes in use at request time, wrong the moment one
is added later without anyone changing the deployment. `nuxi build`
produces a server build that keeps Nitro's API routes and any per-request
SSR working. Pick deliberately, and re-check the choice whenever a static
site grows its first API route, since a static rebuild will drop it without
a build failure to flag it.

Done when: the deployment command matches whether the app actually needs a
running server at request time.

## It's working if

- Every route, page and endpoint, is reachable at the URL its file path and
  filename suggest, with no manually registered route anywhere.
- `nuxi typecheck` and `nuxi build` (or the project's equivalents) both
  complete cleanly, and a real page load shows the expected requests with
  no hydration warning.
- Nothing server-only, a secret, a database call, appears in the client
  bundle.
