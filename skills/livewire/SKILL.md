---
name: livewire
description: >-
  Builds Livewire 4 components: forms, tables, modals and file uploads, with
  correct property hydration, validation and Alpine interop, then proves the
  interaction with a component test rather than a single browser glance. Use
  when the user works with wire:model, wire:click or Livewire Form Objects,
  or asks for interactive server-driven Laravel front-end work.
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Livewire

Livewire hides a full request cycle behind what looks like ordinary PHP
properties, and that illusion breaks in specific, repeatable ways: an ID
left unlocked can be edited in the browser, an untyped property arrives as a
string, a missing `:key` in a loop reuses the wrong child. This skill
builds components that avoid those traps and proves the interaction works
with a test, not just a look in the browser.

It targets Livewire 4, where `make:livewire` creates a single-file
component and `wire:model.blur` also delays the client-side value. On
Livewire 3, components are a class plus a Blade view, and the plain
`wire:model.blur` of v3 is `wire:model.live.blur` in v4; the rest of the
method is the same.

## 1. Decide what state the component owns

List the public properties the component needs and, for each one, whether
it is form input, display-only, or derived from something else. Anything
derived from other properties or from a query belongs behind
`#[Computed]`, not stored and recalculated by hand.

Public properties are serialised into the page and sent back on every
request, so never put a service object or anything carrying a secret in
one. An Eloquent model is fine: only its class and key reach the browser,
and Livewire locks it so the key cannot be swapped. It is re-fetched fresh
each request, though, so any `select()` or other query constraint is lost;
put a constrained query behind `#[Computed]` instead. If you store a bare
ID, mark it `#[Locked]`, or anyone can change it in the browser's
developer tools.

Done when: every public property is form input, a model, or a locked ID,
and nothing sensitive is among them.

## 2. Type every public property

An untyped public property hydrates whatever the browser sent as a string,
so `$this->quantity === 1` silently fails against the string `"1"`. Type
every public property, and Livewire will cast it correctly on the way back
in.

Done when: no public property is left untyped.

## 3. Build the form logic

For anything beyond a trivial form, put the fields and validation rules on
a Form Object rather than the component itself, and call it from the
component's action method. Use `wire:model` for input that only needs to
sync on submit (the default since Livewire 3), and reach for `wire:model.live`
only where the interface genuinely needs to react before that, since every
`.live` binding is a round trip on every keystroke.

Validate on submit with the form's own validation, and on a per-field basis
with an `updated{Property}()` hook calling `validateOnly()` where
field-level feedback matters.

Done when: validation rules live in one place, and a bad submission is
rejected with the field-level error the user actually needs to see.

## 4. Handle tables, modals and uploads deliberately

- **Tables**: keep search and sort state in `#[Url]`-bound properties so
  the view is shareable and survives a refresh; reset pagination whenever
  the search term changes; put the query itself behind a `#[Computed]`
  property so it only runs once per render.
- **Modals**: open them by dispatching and listening for a named event
  (`#[On('open-thing-modal')]`), and call `reset()` plus
  `resetValidation()` when they close, or stale input reappears next time.
- **File uploads**: validate with `image|max:...` or the equivalent, show
  `wire:loading` scoped to `wire:target="photo"` so only the relevant part
  of the page shows a spinner, and preview with `temporaryUrl()` before the
  record is saved.
- **Nested components in a loop**: always set `:key` to a stable, unique
  value. Without it, adding, removing or reordering items lets a child
  silently keep displaying another item's state.

Done when: each of these that the component uses behaves correctly after
an add, remove or reorder, not just on first render.

## 5. Prove the interaction with a test

Write a component test that sets the relevant properties, calls the
action, and asserts the resulting state, not just that it rendered without
error: `Livewire::test(Component::class)->set(...)->call(...)->assertSet(...)`
or `assertSee(...)`. For a form, also assert that bad input is rejected:
submit it and check `assertHasErrors([...])`.

Run the test and show the output. A component seen once in a browser tab
is not proven; a component with a passing interaction test is.

Done when: at least one test exercises the component's main action and
passes, shown by its output.

## 6. Report

The component built, the state it owns and why, the test that proves its
main interaction, and anything deliberately left for a fuller flow check.

For verification of the component inside its full route, auth and page
context, hand off to `prove-it` (if installed).

Gotchas and full worked examples: [references/patterns.md](references/patterns.md).

## It's working if

- No public property holds a service or a secret, and every ID the user
  must not change is `#[Locked]`.
- A component test exercises the main action and its output has been seen,
  not assumed.
- Reordering or removing items in a list of nested components does not mix
  up their state.
