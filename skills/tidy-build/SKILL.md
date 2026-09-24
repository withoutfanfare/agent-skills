---
name: tidy-build
description: >-
  Builds a Rust, Tauri, Node or Go project, reports where the output landed
  and how big it is, then removes the build caches to free disc space, but
  only after a successful build. Use when the user asks to build and clean,
  free disc space from builds, or clear out target or dist folders.
license: MIT
allowed-tools: Bash Read Glob Grep
---

# Tidy build

Build caches grow quietly: a Rust `target/` folder can pass ten gigabytes.
This skill builds the project, shows what was produced, measures the caches,
and clears them. It never cleans after a failed build, because a failed
build is exactly when the user wants the logs and intermediate files.

## 1. Work out what kind of project this is

| Evidence | Kind | Build | Caches to clear |
|---|---|---|---|
| `src-tauri/tauri.conf.json` | Tauri | the project's `tauri build` script | `src-tauri/target/` |
| `Cargo.toml` | Rust | `cargo build --release` | `target/` |
| `package.json` with a `build` script | Node | `npm run build` (or the lockfile's package manager) | `dist/`, `build/`, `.next/`, `node_modules/.cache/` |
| `go.mod` | Go | `go build ./...` | `go clean -cache` (shared across projects; ask first) |

Prefer the project's own scripts over the generic command when they exist.
If nothing matches, ask rather than guess.

Done when: the kind, the build command and the cache folders are named.

## 2. Build

Run the build with a generous timeout (builds of desktop apps can take
several minutes). Keep the warnings; they matter even when the build
succeeds.

If the build fails: stop here, clean nothing, and report the first real
error with its file and line.

Done when: the build succeeded, or the failure is reported and nothing was
removed.

## 3. Show what was built

List the outputs a person would actually use, with sizes: the app bundle
and installer for Tauri, the release binary for Rust and Go, the output
folder for Node.

Done when: each output path is listed with its size.

## 4. Measure, then clean

```bash
du -sh <each cache folder>
```

Remove only the cache folders named in step 1. Leave these alone whatever
happens:

- `node_modules/` (slow and costly to reinstall)
- the outputs listed in step 3, unless the user asked for them to go too
- source, configuration and `.git/`

If the user only wanted a clean, skip steps 2 and 3, but still measure
first.

Done when: the named caches are gone and the space freed is known.

## 5. Report

```text
Built:   <outputs with sizes>
Warnings: <count, or none>
Freed:   <total> (<folder>: <size>, ...)
```

## It's working if

- A failed build never loses its caches.
- The user sees what was built and how much space came back.
- `node_modules/` is still there afterwards.
