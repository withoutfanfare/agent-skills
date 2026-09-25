# Tauri gotchas

Each of these compiles cleanly and only fails once the app is running.

- **The invoke string has drifted from the command.** Renaming a Rust
  command breaks every `invoke('old_name')` on the frontend, and the build
  still passes. The call fails at run time with a "command not found"
  style error. Grep the frontend for the old name after any rename, which
  is one more reason to route every call through a typed wrapper.
- **Arguments sent in snake_case.** Rust's `order_id` is expected as
  `orderId` from JavaScript unless the command sets
  `#[tauri::command(rename_all = "snake_case")]`. A wrong key reaches Rust
  as a missing argument.
- **A plugin call with no capability.** Tauri 2 blocks plugin and core
  calls (file system, dialogs, the shell) unless a file in
  `src-tauri/capabilities/` grants the permission for that window. Your own
  commands are allowed by default, so this bites only when a command
  starts using a plugin.
- **A frontend-only dev server.** Every `invoke()` fails there because no
  Rust process is running. If the wrapper swallows the error, the screen
  looks finished while every value on it is empty or default. Use the full
  dev command that starts both sides.
