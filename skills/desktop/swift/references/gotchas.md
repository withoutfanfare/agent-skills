# Swift and SwiftUI gotchas

Each of these builds cleanly and only shows up once the app is running.

- **`@Observable` looks unchanged, so the view does not redraw.** SwiftUI
  only tracks properties a view's `body` actually reads. If the view reads
  a computed property that derives from stored ones, but never reads the
  stored ones directly, a change to them can be missed. Read the
  underlying properties directly in `body`, or make the derived value a
  stored property that updates alongside them.
- **A binding into an `@Observable` model with no `@Bindable`.** Passing
  `model.name` to a `TextField` compiles when `model` is plain, but the
  field will not write back. The parent needs `@Bindable var model: Model`
  before `$model.name` works.
- **`@State` reset on identity change.** A `@State` value resets to its
  initial expression whenever SwiftUI decides the view has a new identity
  (often from a changed `.id()` or its position in a `ForEach` changing).
  A form that appears to "forget" what the user typed is usually this, not
  a bug in the state itself.
- **A detached `Task` outliving its view.** A `Task { }` started directly
  in `onAppear` keeps running, and can call back into a view model that
  has since gone away, after the view disappears. Prefer `.task { }`,
  which SwiftUI cancels for you.
- **SwiftData context not shared.** Fetching or saving through a
  `ModelContext` other than the one the environment injected (creating a
  second `ModelContainer` by accident) produces two stores that silently
  disagree; there is usually only meant to be one container for the app.
- **Xcode's own build looking green while `xcodebuild` fails.** Xcode
  caches derived data aggressively; a stale scheme or destination in
  `xcodebuild` can build against old settings. Pass an explicit
  `-destination` and, if results look implausible, `-derivedDataPath` to a
  clean folder.
- **A Swift 6 strict concurrency error only in Release.** Some projects
  enable strict concurrency for one build configuration and not the
  other. A change that builds locally in Debug can still fail in a
  Release archive; run the archive build, not only `test`, before calling
  a concurrency change done.
