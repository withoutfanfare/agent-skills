---
name: vue
description: >-
  Builds and reviews Vue 3 components and composables written with the
  Composition API and script setup syntax: where state should live, typed
  props and emits, reactivity traps that silently stop working, and tests
  with Vitest and Vue Test Utils. Use for "build this component", "write a
  composable", "why isn't this reactive", or "review this Vue code".
license: MIT
allowed-tools: Read Edit Write Grep Glob Bash
---

# Vue

A Vue component can look finished and still be wrong in ways the compiler
never flags: a value that stops updating because it was pulled out of a
reactive object, a loading spinner that never clears because the user
navigated away mid-request, a prop typed so loosely that a bad value only
surfaces at runtime. This skill is about getting the component's shape and
behaviour right. For how it should look, hand off to a design-focused skill
instead.

## 1. Decide what the component owns

Before writing anything, work out which state belongs to this component and
which belongs to its parent, a store, or a route. A component that both
fetches its own data and accepts that same data as a prop cannot be reused
somewhere else. A rule that holds well: state that only this component cares
about lives here; state more than one component needs lives in a shared
store or gets passed down.

Done when: every prop has a reason to be a prop rather than internal state,
and no piece of internal state duplicates something a parent should be
passing in.

## 2. Type the public interface

Declare props and emitted events with `defineProps<T>()` and
`defineEmits<T>()` using TypeScript types, not the runtime array or object
form. The typed form catches a missing required prop or a wrongly shaped
emit payload while building, rather than leaving it to show up as `undefined`
in production.

Done when: the project's type check (its `typecheck` script, or `vue-tsc
--noEmit` where there is no such script) passes after the component's public
interface changes.

## 3. Pull out a composable when logic repeats or piles up

Move logic into a composable once it is used by two or more components, or
once one component's `<script setup>` is doing more than one job (fetching
data and also validating a form, say). A composable should read like a
small, named capability, callable from anywhere, not a grab bag of
leftover code.

Done when: the extraction changes no visible behaviour, confirmed by
running the component's existing tests before adding new ones for the
composable itself.

## 4. Keep async state honest when the user leaves early

A `loading` or `saving` flag set to `true` before an async call must be
cleared on every path that follows, including the one where the component
is unmounted, or the user navigates elsewhere, before the response arrives.
Put the flag's clear in a `finally` block, not only in the success branch
and the `catch`, so an early `return` in the success path cannot skip it.
For work that should stop rather than just be ignored once it is stale,
capture an `AbortController` or a request token when the call starts, and
check it is still current before touching shared state in the response
handler.

Done when: for a flag held in a store or other shared state (a local flag
resets on remount anyway), starting the action and immediately leaving the
screen, then returning, shows the flag cleared and the screen usable, not
stuck loading.

## 5. Check the common reactivity traps

- Destructuring a `reactive()` object breaks the link between the extracted
  variable and future updates; destructuring a `ref` loses the `.value`
  wrapper it needs. Pull fields out with `toRefs()` (or `toRef()` for a
  single field) so they stay wired up, and use the store's equivalent
  (commonly `storeToRefs()`) when pulling fields from shared state, wrapped
  around the store itself, not around a plain object copied from it.
- A `watch()` given a destructured primitive, rather than a ref, a reactive
  object, or a getter function (`() => someObject.field`), will not fire
  when the source changes.
- State read by only one component belongs in that component, not in a
  shared store; move it to a store only once a second component needs it.

Done when: changing the underlying source updates every place that reads
it, verified by changing the source and watching the consuming template.

## 6. Write tests that outlive a refactor

Mount the component with Vue Test Utils and assert on what it renders and
what it emits, not on internal variables, so a rename inside the component
does not break the test. Test a composable directly, ideally with its own
test file beside it, rather than only through a component that happens to
use it. Run the project's test command after each change, and treat a test
that just turned red as the thing to fix next, not a note for later.

Where an element is interactive, give it an accessible name (visible text,
`aria-label`, or a linked `<label>`) and check that a menu or dialogue box
traps and returns keyboard focus correctly, as part of the same change.

Done when: the test command's output for the changed files is pass, and
each interactive element added or changed has an accessible name.

## 7. Report what you verified

State the test command run and its result, and, for any fix to a loading
or busy flag, describe leaving the screen mid-request and confirming the
flag cleared on return, not just that the code looks right.

Done when: the report names the command run and what it showed, not just
what changed.

## It's working if

- The type check and test suite both pass for the changed files.
- Leaving a screen mid-request and coming back never leaves it stuck loading.
- Every value shown in the template still updates when its source changes.
