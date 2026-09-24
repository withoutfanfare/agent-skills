---
name: herd-doctor
description: >-
  Diagnoses Laravel Herd sites on macOS that will not load: nginx stuck or
  serving a stale process, a site missing from the linked list, or a site
  running the wrong PHP version. Use when a .test site will not load,
  returns a 502, shows the wrong PHP version, or its domain cannot be
  found.
license: MIT
allowed-tools: Read Bash Grep Glob
---

# Herd doctor

Herd runs an nginx instance and a set of PHP versions in the background,
and most "the site is just broken" reports trace back to one of three
things: nginx itself is stuck, the site was never linked or secured
properly, or it is running under a PHP version the code was not written
for. Guessing which one it is wastes time; working the three checks in
order finds it in minutes.

This skill never assumes a specific site name, project folder or domain.
Ask which site is affected, or read it from the terminal error, before
running any command below; every example uses a placeholder domain.

## 1. Get the exact symptom

Reproduce the failure and capture what actually comes back, not a
paraphrase of it: a browser error screen, a connection refused, a 502, a
blank response, or the wrong content entirely. The exact wording narrows
which of the three causes below is likely before you touch anything.

```bash
curl -sv https://example-site.test/ 2>&1 | head -30
```

Done when: you have the real error text or status code, not "it doesn't
work".

## 2. Check whether nginx itself is the problem

Herd's nginx runs a master process as root and worker processes as the
logged-in user. A master process left in a bad state (after a crash, a
config change, or a system sleep) can keep serving stale behaviour
indefinitely.

```bash
ps aux | grep nginx | grep -v grep
```

If nginx looks stuck, absent, or you see errors in its log, restart all of
Herd's services first:

```bash
herd restart
```

If the old master process survives that, it needs killing with `sudo`,
which cannot answer a password prompt from inside an agent session. Ask
the user to run it in their own terminal, aimed only at Herd's nginx master
(its path in the `ps` output sits inside Herd's application folder), not
every nginx on the machine, then run `herd start`:

```bash
sudo kill <herd-nginx-master-pid>   # the user runs this
herd start
```

Killing the process is safe: Herd's start command brings a fresh master
and worker set up from its own configuration, so nothing is lost.

Done when: `ps aux | grep nginx` shows a fresh master and worker set, and
the symptom from step 1 either changes or is ruled out.

## 3. Check the site is actually linked and secured

A site that returns "not found" at the domain level, rather than an error
from the application, usually was never linked, or its link broke.

```bash
herd links
herd secured
```

If the site you are troubleshooting is missing from `herd links`, link it
from its project folder and re-secure it:

```bash
cd /path/to/the/project      # the site's own folder, not a fixed example path
herd link
herd secure
herd restart
```

A certificate or "not secure" warning on a site that is already linked
usually clears by running `herd secure` again from the site's folder.

Done when: the site under investigation appears in both `herd links` and,
if it should be served over https, `herd secured`.

## 4. Check the PHP version serving the site

A site written for one PHP version, served under another, tends to fail
with syntax or missing-function errors that look nothing like a PHP
version mismatch at first glance.

```bash
herd which-php
```

If it does not match what the project's `composer.json` `require.php`
constraint expects, isolate the correct version for that one site rather
than changing the global default (which would affect every other site):

```bash
herd isolate 8.3
```

Done when: `herd which-php`, run from inside the site's folder, matches
what the project declares it needs.

## 5. Confirm the fix, don't assume it

Re-run the same check from step 1 and read the actual output; a command
that exits without error is not proof the site now works.

```bash
curl -sv https://example-site.test/ 2>&1 | head -30
```

Done when: the response matches what a working site should return (the
expected status code and body), not just "no error was printed".

## It's working if

- You can point to the exact one of nginx, linking, or PHP version that
  was wrong, not a guess at which fix "probably" did it.
- The final check in step 5 was actually run and its real output read,
  not assumed from the fix having been applied.
- No site name, domain, or folder path from this session was hardcoded
  into anything left behind, so the same steps work unchanged for a
  different site next time.
