---
name: harden
description: >-
  Audits an application for security weaknesses against the OWASP Top 10:
  access control, injection, authentication, secrets, configuration,
  uploads and outbound requests. Reports each issue with where it is, how
  it could be exploited and the fix; it does not change code. Use when the user
  asks for a security audit or review, asks whether code is safe, or wants
  to harden an app before launch.
license: MIT
context: fork
background: false
effort: high
allowed-tools: Read Grep Glob Bash
---

# Harden

Most breaches go through a small number of well-known doors: a missing
permission check, input glued into a query, a secret in the wrong place, a
debug page left on. This skill checks those doors systematically, proves
each finding with the code that causes it, and says how to close it. It
reviews and reports without changing code; the user or another session
applies the fixes.

For a review of one change, `review` (if installed) covers security as part
of a wider review. For content leaving the machine, use a scanning tool for
secrets instead.

## 1. Map the attack surface

List every way data and people get in: routes and endpoints, forms, file
uploads, webhooks, queue consumers, scheduled commands that read outside
data, admin areas, and outbound calls the app makes on a user's behalf.
Note which require sign-in and which do not.

Done when: there is a list of entry points, each marked public or
authenticated.

## 2. Work through the Top 10

The categories follow the OWASP Top 10:2025. For each one, look in the
code for the evidence, not the intention:

| Category | What to look for |
|---|---|
| A01 Broken access control | Every write and every record fetch checks this user may act on this record (not only that they are signed in). IDs in URLs cannot reach other users' data. Any URL the app fetches on a user's behalf is checked against an allowlist, and internal addresses are refused (server-side request forgery now sits here). |
| A02 Security misconfiguration | Debug off in production; security headers set; CORS narrow; default credentials and sample routes gone. |
| A03 Software supply chain failures | Dependency audit clean or triaged (`upkeep`, if installed); lock files committed; packages from trusted sources only; build and deploy pipeline secrets scoped and actions pinned. |
| A04 Cryptographic failures | Passwords hashed with a slow algorithm; sensitive fields encrypted at rest; HTTPS enforced; no home-made crypto. |
| A05 Injection | Queries use bound parameters; shell commands never include user input; templates escape output by default and every unescaped output is justified. |
| A06 Insecure design | Rate limits on sign-in, reset and expensive endpoints; business rules enforced on the server, not only in the interface. |
| A07 Authentication failures | Session renewed at sign-in; secure, HTTP-only cookies; lockout or throttling; multi-factor for admin. |
| A08 Software or data integrity failures | Webhooks verify signatures; downloads and uploads verified; no unsafe deserialisation of user data. |
| A09 Security logging and alerting failures | Sign-ins, permission failures and sensitive actions are logged and someone is alerted, without logging secrets or personal data. |
| A10 Mishandling of exceptional conditions | Errors fail closed (a failed permission or payment check denies, never allows); error pages and API errors leak no stack traces or internals; unexpected input cannot exhaust memory, disk or connections. |

Also check file uploads (type and size validated, random stored names,
stored outside the web root) and secrets (read from the environment, never
committed, never logged).

Done when: every category has findings or a line saying what was checked
and found sound.

## 3. Prove and rate each finding

For each issue: the file and line, the input an attacker would send, what
happens, and the fix. Rate severity by what an attacker gains and how
easily, on the same blocker/major/minor scale as `review` (if installed):

| Severity | Meaning |
|---|---|
| blocker | must be fixed before this ships |
| major | should be fixed; a real weakness |
| minor | worth fixing, low risk |

Rate confidence as certain (confirmed from the code), likely or possible.
Mark anything not confirmed from the code as possible and say how to
confirm it.

Done when: every finding has a location, an exploit sketch and a fix.

## 4. Report

```markdown
## Security review: <app>
**Summary:** <blocker n, major n, minor n>; top three risks in one line each
| # | Severity | Confidence | Category | Where | Issue | Fix |
### Details
<one short section per blocker or major: vulnerable code, attack, fixed code>
### Checked and sound
<categories with no findings, and what was checked>
```

Framework specifics for Laravel are in
[references/laravel.md](references/laravel.md).

## It's working if

- Every blocker or major finding comes with the exact input that exploits
  it.
- Categories with no findings still say what was checked.
- The code is unchanged, and every finding carries a fix someone else can
  apply.
