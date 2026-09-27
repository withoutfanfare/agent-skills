---
name: swift
description: >-
  Builds and changes native macOS and iOS apps in Swift and SwiftUI: state
  with the Observation framework (@Observable, @State, @Bindable,
  @Environment), a persistence choice, Swift concurrency (async/await,
  actors, @MainActor, Sendable, Swift 6 strict concurrency), AppKit interop,
  and building and testing from the command line. Use when the user is
  building or changing a SwiftUI screen, an Xcode project or a view model,
  or hits a Swift 6 concurrency or Sendable error. Not for Tauri apps (use
  `tauri`), and not for shipping or signing a build (use `notarise`).
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Swift

A SwiftUI screen is a function of state, so most bugs in one trace back to
state living in the wrong place or crossing a concurrency boundary
unsafely, not to the view code itself. This skill treats naming the owner
of each piece of state, and the isolation of each async call, as the
design step that comes before writing the view.

## 1. Give each piece of state one owner

Before writing a view, decide who owns each value:

- **`@State`** for a value only this view needs, that disappears when the
  view does (a text field's draft text, whether a sheet is showing).
- **`@Observable`** on a plain class for anything shared between views or
  that outlives one screen (a view model, a fetched list). Any property the
  class exposes is tracked automatically; a view reading it redraws only
  when that specific property changes, not on every mutation.
- **`@Bindable`** where a child view needs a two-way binding (`$model.name`)
  into an `@Observable` reference it was handed, not its own copy.
- **`@Environment`** for something effectively app-wide (a session, a
  colour scheme, a shared data store), injected once near the root with
  `.environment(_:)` rather than threaded through every initialiser.

Reach for `@Observable` over the older `ObservableObject` in new code; it
needs no `@Published` on every property and skips redraws for properties a
view never reads. Pick one persistence layer per store of truth: SwiftData
for an app shaped around model objects and queries, plain `Codable` plus
`FileManager` for a handful of settings, and avoid mixing both for the same
data, which invites two copies to disagree.

Done when: every new piece of state has exactly one owner, and no value is
duplicated in both a parent's `@State` and a child's own copy.

## 2. Isolate before you write the async call

Decide which actor a type runs on before writing its methods, not after a
compiler error forces the question. Mark anything that touches the UI
`@MainActor` (most view models qualify); leave work with no UI dependency
unisolated or on its own actor so it does not block the main thread. Swift
6's strict concurrency checking then turns a crossed boundary into a build
error instead of a runtime data race, which is a trade worth making even
though it front-loads some annotation work.

A type sent between isolation domains (across an `await` to another actor,
into a `Task`) must be `Sendable`. Prefer a `struct` or an `actor`, which
Swift can verify as `Sendable` on its own, over a plain `class` shared
across boundaries; a `class` that truly must cross needs its mutable state
protected some other way, which is usually the sign to make it an actor
instead.

Longer patterns and the specific errors Swift 6 mode raises, with the fix
for each, are in
[references/concurrency.md](references/concurrency.md).

Done when: the project builds under Swift 6 strict concurrency with no
suppressed warnings, and every type crossing an isolation boundary is
`Sendable` or confined to one actor.

## 3. Drop into AppKit only where SwiftUI has a real gap

Reach for `NSViewRepresentable` or `NSViewControllerRepresentable` when a
control genuinely has no SwiftUI equivalent (precise text layout, a custom
`NSView` from an existing framework, certain drag-and-drop or menu
behaviour), not as a default for anything that feels awkward in SwiftUI.
Keep the wrapper thin: it should marshal data in and out through its
`Coordinator`, not carry business logic that belongs in the model.

Done when: the wrapped view is the smallest AppKit surface that solves the
gap, and everything else in that screen stays SwiftUI.

## 4. Build and test from the command line

For an Xcode project or workspace:

```bash
xcodebuild -scheme <Scheme> -destination 'platform=macOS' build
xcodebuild -scheme <Scheme> -destination 'platform=macOS' test
```

Swap the destination for `platform=iOS Simulator,name=<device>` on iOS (list names with `xcrun simctl list devices available`)
targets. For a Swift package with no Xcode project:

```bash
swift build
swift test
```

Write new tests with Swift Testing (`import Testing`, `@Test`, `#expect`
and `#require`), which reads closer to plain assertions and runs tests in
parallel by default; keep existing `XCTest` cases as they are rather than
converting them, and reach for `XCTest` only where Swift Testing has no
equivalent yet (UI automation, performance measurement). The two can live
in the same target and both run under `xcodebuild test` or `swift test`.

Done when: the build and test commands both exit clean from the terminal,
not just from Xcode's own UI.

## 5. Prove the change by running the app

A green build and a passing test suite prove the code compiles and the
paths under test behave as written; neither proves the screen looks right
or the interaction feels right. Launch the app (`open` the built `.app`, or
run it from Xcode) and drive the exact change by hand: trigger the state
change, watch the view update, check the value actually persisted if that
was the point.

Traps that pass a clean build and only show up once the app is running are
in [references/gotchas.md](references/gotchas.md).

Done when: you can describe what you saw happen on screen, not what the
code is supposed to do.

## It's working if

- The project builds and tests pass from the command line, under Swift 6
  strict concurrency with no isolation warnings suppressed.
- Every piece of state has one named owner, and no `@Observable` value is
  duplicated in a second copy elsewhere.
- Running the built app shows the change happening on screen, not only in
  the test log.
