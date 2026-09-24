---
name: harden
description: >-
  Audits an application for security weaknesses against the OWASP Top 10
  and hardens what it finds: access control, injection, authentication,
  secrets, configuration, uploads and outbound requests. Reports each issue
  with where it is, how it could be exploited and the fix. Use when the user
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
reviews and reports; fixes are applied only when the user asks.

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

For each category, look in the code for the evidence, not the intention:

| Category | What to look for |
|---|---|
| Broken access control | Every write and every record fetch checks this user may act on this record (not only that they are signed in). IDs in URLs cannot reach other users' data. |
| Cryptographic failures | Passwords hashed with a slow algorithm; sensitive fields encrypted at rest; HTTPS enforced; no home-made crypto. |
| Injection | Queries use bound parameters; shell commands never include user input; templates escape output by default and every unescaped output is justified. |
| Insecure design | Rate limits on sign-in, reset and expensive endpoints; business rules enforced on the server, not only in the interface. |
| Misconfiguration | Debug off in production; security headers set; CORS narrow; default credentials and sample routes gone; error pages leak nothing. |
| Vulnerable components | Dependency audit clean or triaged (`upkeep`, if installed). |
| Authentication failures | Session renewed at sign-in; secure, HTTP-only cookies; lockout or throttling; multi-factor for admin. |
| Integrity failures | Webhooks verify signatures; downloads and uploads verified; no unsafe deserialisation of user data. |
| Logging failures | Sign-ins, permission failures and sensitive actions are logged, without logging secrets or personal data. |
| Server-side request forgery | Any URL the app fetches on a user's behalf is checked against an allowlist; internal addresses are refused. |

Also check file uploads (type and size validated, random stored names,
stored outside the web root) and secrets (read from the environment, never
committed, never logged).

Done when: every category has findings or a line saying what was checked
and found sound.

## 3. Prove and rate each finding

For each issue: the file and line, the input an attacker would send, what
happens, and the fix. Rate severity (critical, high, medium, low) by what an
attacker gains and how easily. Mark anything not confirmed from the code as
"to verify" and say how.

Done when: every finding has a location, an exploit sketch and a fix.

## 4. Report

```markdown
# Security review: <app>
**Summary:** <critical n, high n, medium n, low n>; top three risks in one line each
| # | Severity | Category | Where | Issue | Fix |
## Details
<one short section per critical or high: vulnerable code, attack, fixed code>
## Checked and sound
<categories with no findings, and what was checked>
```

Framework specifics for Laravel are in
[references/laravel.md](references/laravel.md).

## It's working if

- Every critical or high finding comes with the exact input that exploits
  it.
- Categories with no findings still say what was checked.
- No fix was applied without the user asking.
