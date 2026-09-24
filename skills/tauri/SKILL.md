---
name: tauri
description: >-
  Builds and changes Tauri desktop apps: designs Rust commands and their
  error types, wraps every invoke() call in a typed frontend function,
  decides which side of the Rust/JS boundary owns each piece of state, and
  keeps secrets out of logs and plain files. Use for 'tauri', 'desktop app',
  'src-tauri', 'invoke command', a Rust backend paired with a web frontend,
  or packaging a Tauri build for release.
license: MIT
allowed-tools: Read Grep Glob Bash Edit Write
---

# Tauri

A Tauri app is two programs pretending to be one: a Rust backend and a
web frontend, talking only through `invoke()` calls and events. Most bugs
in these apps live at that seam, not inside either side alone, because
nothing forces the two to agree on a shape, a name or an error format.
This skill treats the boundary as the thing to design first.

## 1. Give the command an error shape before writing its body

Decide what a command returns on failure before writing the happy path.
A bare `String` error forces the frontend to parse prose to know what
went wrong; a small struct with a stable `code` and a readable `message`
lets the frontend branch on `code` and show `message` to the user. Search
`src-tauri/src` for an existing error type first and extend it rather
than inventing a second shape next to it.

Done when: the command's `Result<T, E>` has an `E` the frontend can match
on without string comparison.

## 2. Keep the command a thin wrapper

Put validation and the actual work in a plain Rust function the command
calls, so the logic can be unit tested without going through IPC (Tauri's
message-passing layer between the two processes) at all. The `#[command]`
function itself should do little more than check its inputs and call that
function.

Register the command by name in the app's invoke handler list, then grep
both the registration and the function's own name to confirm they match
exactly. A mismatch compiles fine and fails at the moment it is called,
which is a much harder bug to place.

Done when: `cargo test` exercises the delegated function with no Tauri
runtime in scope, and the registered name and the function name are
identical by grep.

## 3. Never call invoke() directly from a component

Write one typed wrapper function per command, living next to (or named
after) the command it calls, and have every call site go through it. Copy
the Rust return type into the frontend's type system by hand if the
project has no generator for it, so a change on one side shows up as a
mismatch on the other the next time the type checker runs.

Pick one failure convention for the whole project: wrappers either throw
so callers use try/catch, or they return a result object so callers can
show a field-level error. Mixing the two means every call site needs to
remember which kind it is calling.

Done when: no component file contains the literal text `invoke(`, and the
type checker passes against the current Rust signatures.

## 4. Assign an owner to every piece of shared state

For each value the UI depends on, decide once whether Rust or the
frontend owns it. Rust should own anything that must survive a page
reload or be visible to more than one window: managed state, or a plugin
that persists to disk. The frontend's own state store should own things
that are only ever about the current screen. A value written from both
sides drifts out of sync silently, so when in doubt, make one side the
source of truth and have the other side read or subscribe to it.

For anything long-running, have Rust emit progress events rather than
have the frontend poll for status: polling adds constant load and can
race against the moment the work actually finishes. Make sure any event
listener is removed when its component goes away, or navigating back and
forth leaves a growing pile of listeners each reacting to the same event.

Done when: for every shared value you touched, one side is named as
owner, and any listener you added has a matching cleanup.

## 5. Treat secrets and file paths as hostile input

Never write a secret (an API key, a token, a saved password) to an
ordinary file in the app's data directory; that directory is not
encrypted at rest on most machines. Store secrets through the operating
system's own credential store instead, and keep only non-secret details
(an account name, whether something is connected, a timestamp) in a
plain settings file.

Any file path a command receives from the frontend needs the same
suspicion as a path from the open internet: reject anything containing
null bytes or shell metacharacters, and resolve it to a canonical path so
a `../` sequence cannot walk it outside the folders the app expects.

Done when: a test proves a path outside the app's own directories is
rejected rather than followed, and no secret value appears in a log line,
an error message, or a file written in plain text.

## 6. Decide what closing the window actually does

A menu-bar style app that people expect to keep running usually hides its
window on close and stays alive in the tray; a document-style app usually
quits outright. Wire the choice explicitly in the window's close handler
rather than leaving the platform default in place, and check the result
by closing the window and looking for the process afterwards, not by
reading the code.

Wire the handler for a new tray or menu item in the same change that adds
the item. An item with no handler compiles and shows up in the menu but
does nothing when clicked, and that only becomes visible by clicking it.

Done when: closing the window behaves as intended and the process is
present or absent to match, and every menu or tray item you added does
something when clicked.

## 7. Prove it with the real app, not just a green build

Run the Rust test suite from the backend's own folder after any change to
a command, a validator or an error type, before touching the frontend.
Use the full dev command that runs both sides together for anything
involving `invoke()`; a frontend-only dev server will let the UI render
but silently no-op every `invoke()` call, which looks like a working
screen with no real data behind it.

A passing test suite and a clean build only prove the code compiles and
the paths under test behave as written. Launch the actual app, trigger
the exact change by hand and watch the result appear on screen before
calling it done. For a release build on macOS, remember that "it built"
and "it will open on someone else's Mac" are different claims: without a
valid signing identity and, for wider distribution, notarisation, a build
that runs locally will still be blocked by Gatekeeper elsewhere.

Done when: you can describe what you actually saw happen in the running
app, not what the code is supposed to do.

## Gotchas

- A command whose registered name and function name have drifted apart
  fails at call time with a vague "command not found", never at compile
  time; re-check both after any rename.
- A frontend-only dev server accepts every `invoke()` call and returns
  nothing useful, so a screen can look finished while every value on it
  is empty or default.

## It's working if

- The backend test suite passes for the changed command, and the
  frontend type checker passes for its wrapper.
- Driving the change in the full dev build (both processes running
  together) shows the expected result on screen.
- No secret value turns up in a log, an error message, or a plain file on
  disk, and a path outside the app's own folders gets rejected rather
  than followed.
