---
name: upkeep
description: >-
  Audits a project's dependencies for known vulnerabilities, outdated and
  abandoned packages, and risky version constraints, then plans upgrades in
  safe batches. Works with npm, pnpm, Yarn, Composer, Cargo, pip and Go
  modules. Use when the user asks to audit dependencies, check for CVEs or
  security advisories, find outdated packages, or plan dependency
  updates. Not for framework or language version upgrades; use `upgrade`.
license: MIT
allowed-tools: Bash Read Grep Glob
---

# Upkeep

Every dependency is someone else's code running with your permissions. An
audit answers three questions: is anything known to be vulnerable, is
anything falling behind or abandoned, and can we upgrade without breaking
the build? This skill answers them and hands back a plan. It does not
upgrade anything unless asked.

## 1. Find every package manager in play

Look for manifests and lockfiles: `package.json` with `package-lock.json`,
`pnpm-lock.yaml` or `yarn.lock`; `composer.json` and `composer.lock`;
`Cargo.toml`; `requirements.txt` or `pyproject.toml`; `go.mod`. Monorepos
often have several. Use the lockfile's tool, not a different one.

Done when: every manifest is listed with its tool.

## 2. Check for known vulnerabilities

| Tool | Command |
|---|---|
| npm | `npm audit --omit=dev` then `npm audit` |
| pnpm / Yarn | `pnpm audit` / `yarn audit` (Yarn 1) or `yarn npm audit` (Yarn 2+) |
| Composer | `composer audit` |
| Cargo | `cargo audit` (if installed) |
| pip | `pip-audit` (if available) |
| Go | `govulncheck ./...` (if installed) |

For each advisory, record: package, installed version, fixed version,
severity, and whether it is a direct or indirect dependency. Check whether
the vulnerable code path is actually reachable in this project before
calling it urgent; say which ones you could not check.

Done when: every advisory is listed with its fixed version and severity.

## 3. Check what is falling behind

```bash
npm outdated          # or pnpm/yarn equivalents
composer outdated --direct
cargo outdated        # if installed
```

Separate patch and minor updates (usually safe) from major ones (read the
changelog). Flag packages with no release in two years, archived
repositories, or packages marked abandoned, and suggest the maintained
replacement where one exists.

Done when: outdated direct dependencies are grouped into patch or minor,
major, and abandoned.

## 4. Look at the constraints

In the manifests, flag: wildcard or unbounded ranges (`*`, `>=1.0`),
dependencies pinned to a branch or commit, development tools listed as
runtime dependencies, and a lockfile that is missing or out of date with
its manifest.

Done when: each risky constraint is listed with a suggested replacement.

## 5. Plan the upgrades

Order the work so each batch can be tested and reverted on its own:

1. Security fixes that stay within the current major version.
2. Patch and minor updates, a handful at a time.
3. Each major upgrade on its own, with its migration notes linked.

Never use a force option that jumps major versions silently (such as
`npm audit fix --force`) without saying which packages it changes.

Done when: every upgrade sits in a numbered batch that can be tested and
reverted on its own.

## 6. Report

```markdown
## Dependency audit: <project>
**Vulnerabilities:** <n critical, n high, ...> (<n> reachable)
| Package | Installed | Fixed in | Severity | Direct? | Reachable? |
**Outdated:** <n patch/minor, n major, n abandoned>
**Constraints to tighten:** <list>
**Upgrade plan:** <batches, in order>
```

Templates for CI checks are in [references/ci.md](references/ci.md).

Done when: every field in the template is filled from the audit output.

## It's working if

- Every advisory has a fixed version and a "reachable?" answer, or says it
  could not be checked.
- Major upgrades never arrive bundled with everything else.
- Nothing was changed unless the user asked for it.
