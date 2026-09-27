# Swift concurrency in depth

## Reading a Swift 6 strict concurrency error

- **"Sending 'x' risks causing data races"**: a non-`Sendable` value is
  crossing into a `Task`, an actor, or another isolation domain. Either
  make the type `Sendable` (a `struct` of `Sendable` properties usually
  qualifies for free), or stop sending the value itself and send a copy or
  an identifier instead.
- **"Call to main actor-isolated instance method in a synchronous
  nonisolated context"**: something outside `@MainActor` is calling a
  method that touches the UI. Mark the caller `@MainActor` if it belongs on
  the main actor too, or `await` the call from an already-async, already
  isolated context.
- **"Stored property 'x' of 'Sendable'-conforming class is mutable"**: a
  `class` claims `Sendable` but has a `var`. Either make the properties
  `let`, move the mutable state behind an actor, or drop the `Sendable`
  conformance and confine the class to one isolation domain instead.

## @MainActor placement

Put `@MainActor` on the type (a view model class), not scattered across
individual methods, unless one method genuinely does heavy off-main work
(parsing, a network call) that the rest of the type should not wait on.
Mixing the two only when there is a real reason keeps the isolation
boundary at one place per type instead of a method-by-method puzzle.

## Actors do not make code fast

An actor removes data races on its own state by serialising access to it,
not by running work in parallel. Two calls into the same actor still queue
behind each other. If a screen feels slow because of an actor, the fix is
usually to do less work inside it or to move the work to a `Task` that
does not hold the actor, not to add more isolation.

## Task lifetime

A `Task` started inside a SwiftUI view's body or an `onAppear` keeps
running after the view disappears unless something cancels it. Use the
`.task { }` view modifier for work tied to a view's lifetime; SwiftUI
cancels it automatically when the view goes away. A `Task` stored on a
long-lived `@Observable` object needs its own explicit cancellation,
typically in a `deinit` or an explicit "stop" method.

## Migrating an existing project to Swift 6 mode

Turning on strict concurrency (`SWIFT_STRICT_CONCURRENCY=complete`, or the
Swift 6 language mode in the build settings) on an older SwiftUI codebase
usually surfaces dozens of warnings at once, mostly from singletons and
delegates written before `Sendable` existed. Fix them by isolation, not by
suppression: `@unchecked Sendable` is a last resort for a type you are
certain is safe by construction (immutable after init, or internally
locked), and reaching for it on every warning defeats the point of turning
strict mode on at all.
