---
name: alpine
description: >-
  Builds client-side interactivity with Alpine.js: dropdowns, modals, tabs,
  toggles, and state shared between components with a store or synced to a
  backend component with x-model or an entangle-style binding. Use when the
  user asks for a dropdown, modal, accordion, tab set or toggle, mentions
  Alpine.js, x-data, x-show or $dispatch, or wants interactivity without a
  full frontend framework.
license: MIT
allowed-tools: Read Grep Glob Write Edit
---

# Alpine

Alpine.js adds behaviour straight into markup: a menu that opens, a modal
that traps focus, a tab set that remembers which tab is active. It is easy
to reach for `x-show` and stop there, which leaves a component that a mouse
user can operate but a keyboard or screen reader user cannot, that flashes
open before Alpine has loaded, and that leaks state into every element that
touches it. This skill builds the component properly the first time:
accessible, free of flash, and with state kept where it belongs.

## 1. Place the state deliberately

Decide before writing markup: local `x-data` for anything only one
component cares about (a dropdown's open flag, a form field's validity), an
`Alpine.store()` for state two or more unrelated components read or change
(a cart count in a header and a mini-cart in a sidebar), or a binding to the
backend component's own state when the value must round-trip to the server
(a saved preference, a record being edited).

Reaching for a store because it is convenient, when only one component
needs the value, buries state that a reader would expect to find in the
markup right next to where it is used. Keep `x-data` objects to the
handful of fields and methods one component needs; when several components
would otherwise duplicate the same object, that is the signal to promote it
to a store instead.

Done when: you can say in one sentence why the state lives where it does,
and no `x-data` object holds fields an unrelated part of the page needs.

## 2. Build the markup with the right directives

Write the component with `x-show` or `x-if` for conditional rendering,
`x-model` for two-way bound inputs, `x-bind`/`:` for dynamic attributes,
`x-on`/`@` for events, and `x-transition` for enter/leave animation. Use
`@click.outside` to close on an outside click and `@keydown.escape` to
close on Escape, both attached to the element that owns the open state.

Reach for `x-if` over `x-show` when the hidden content should not exist in
the DOM at all (heavy content, or content that must not be reachable by a
screen reader or Tab key while closed); use `x-show` when toggling is
frequent and losing the element's state on each hide would be wasteful.

Done when: the component opens, closes and updates using Alpine directives
alone, with no manual DOM queries or manual class toggling.

## 3. Guard against flash and motion

Add `x-cloak` to any element hidden on load until Alpine initialises, and
pair it with the CSS rule below (Alpine does not ship this rule itself):

```css
[x-cloak] {
    display: none !important;
}
```

Wrap transition classes in a reduced-motion check so a user with that
system preference gets an instant show or hide rather than an animation:

```html
<div
    x-show="open"
    x-transition:enter="motion-safe:transition motion-safe:ease-out motion-safe:duration-150"
    x-transition:enter-start="motion-safe:opacity-0 motion-safe:scale-95"
    x-transition:enter-end="motion-safe:opacity-100 motion-safe:scale-100"
>
```

Without a utility framework's `motion-safe` variant, check
`window.matchMedia('(prefers-reduced-motion: reduce)').matches` in the
component's `x-init` and skip setting transition classes when it is true.

Done when: nothing flashes open before Alpine runs, and a reduced-motion
system setting removes the animation rather than just slowing it.

## 4. Make it usable without a mouse

Every interactive element needs a role and state that matches what it
does: `aria-expanded` on a toggle button, `aria-hidden` on content that is
visually hidden, `role="dialog"` and `aria-modal="true"` on a modal,
`role="tablist"`/`role="tab"`/`role="tabpanel"` on tabs. Trap focus inside
an open modal so Tab cannot escape to the page behind it, return focus to
the trigger on close, and make sure every action reachable by click is also
reachable by keyboard (Enter/Space to activate, Escape to dismiss, arrow
keys where a native equivalent would use them, such as a tab set or menu).

Done when: you can operate the whole component using only Tab, Enter,
Space, arrow keys and Escape, and a screen reader announces the open and
closed states.

## 5. Wire up events without leaking them

Dispatch custom events with `$dispatch('cart:updated', detail)`, namespaced
with a prefix so they cannot collide with another component's event of the
same short name, and listen for them with `@cart:updated.window="..."` on
whichever element needs to react. Clean up anything set up in `x-init`
(timers, external listeners, subscriptions) in a `destroy()` method on the
same data object, which Alpine calls before it cleans the component up, so
that removing the element does not leave orphaned work running.

Done when: an event fired by one component is picked up only by the
listeners meant for it, and nothing keeps running after its element is
removed from the page.

## 6. Check it in the browser

Load the page and click through the interaction once, then repeat it using
only the keyboard. Reload with a slow network throttle (or check the
markup by eye) to confirm nothing hidden by `x-cloak` is visible before
Alpine has run. If the component talks to a backend, trigger a save or
toggle and confirm the state after a refresh matches what was shown before
it.

Done when: the interaction works by mouse and by keyboard, nothing flashes
on load, and any state meant to persist still holds after a reload.

Full worked examples (dropdown, modal, tabs, accordion, store, backend
binding) are in [references/patterns.md](references/patterns.md). A ready
to copy dropdown is in
[assets/dropdown.html](assets/dropdown.html), and a store skeleton is in
[assets/store.js](assets/store.js).

## It's working if

- The component works fully by keyboard, with visible focus and correct
  ARIA state at every step.
- Nothing hidden by `x-cloak` is visible for even a moment before Alpine
  initialises.
- Shared state lives in exactly one place (a store, or the backend
  component) and every component reading it stays in sync.
