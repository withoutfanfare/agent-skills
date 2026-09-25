---
name: feature-flags
description: >-
  Adds or manages a feature flag: a descriptive name, a condition that
  handles the logged-out case, a staged rollout plan, and consistent checks
  across code, templates and routing, followed by full removal once the
  flag has served its purpose. Use for 'feature flag', 'toggle this behind
  a flag', 'percentage rollout', 'canary release', or cleaning up an old
  flag.
license: MIT
allowed-tools: Read Grep Glob Edit Write Bash
---

# Flags

A feature flag is a small promise: the same code path can be switched on
for some visitors and off for others, without a deploy. The promise breaks
in three common ways: the name stops meaning anything after the second
flag with a similar purpose, the condition forgets that half of visitors
are not logged in and crashes for them, or the flag outlives the rollout
and quietly clutters the codebase for months. This skill covers naming,
the condition (including anonymous visitors), staged rollout, consistent
checks, testing both states, and full removal.

## 1. Name the flag for what it changes, not who asked for it

Use a short, descriptive, kebab-case name that says what behaviour it
gates: `new-checkout-flow`, `bulk-export`, `dark-mode`. Avoid a name tied
to a ticket number, a team or a date (`abc-123`, `growth-q3`), because
those stop being meaningful the moment the ticket closes and the flag
stays.

Check the flag store or codebase for an existing flag with an overlapping
name before adding a new one; two flags gating the same feature under
different names is a common source of confusion.

Done when: the name describes the behaviour on its own, and no existing
flag already covers it.

## 2. Write the condition, including the anonymous case

Decide, explicitly, what the flag returns for a visitor who is not signed
in. Most flagging systems pass a `null` or missing user/scope for guests;
if the condition only handles a real user object, it will throw or behave
unpredictably for every anonymous request. Write the anonymous branch on
purpose, not as a side effect of a default case:

```text
define('early-access-banner', scope):
    if scope is null:
        return false          # guests never see it
    if scope.is_beta_tester:
        return true
    return false
```

Also decide what a signed-in user with no matching attribute gets (a
default, not an exception), and whether the flag needs a user, an
account, or some other scope such as a team or a region.

Done when: the condition has a named branch for "no user" and a named
default for "user with none of the matched attributes".

## 3. Plan the rollout in stages

Roll a new behaviour out by tightening or loosening one condition, not by
writing a new flag per stage:

1. **Internal only**: restrict to a small, clearly fake test account or
   email domain, for example `@internal.example`, never a real
   colleague's address.
2. **Opted-in testers**: add a `beta_tester` style attribute alongside the
   internal check.
3. **Percentage rollout**: add a random or hashed percentage for everyone
   else, keyed by a stable identifier (user ID, not session ID) so the
   same visitor gets a consistent result across requests.
4. **Full rollout**: the condition returns true unconditionally as a
   deliberate, temporary step before removal (step 6).

Record which stage is live somewhere a teammate would find it (the flag's
description, a linked note, or a commit message), since a percentage sat
at 10% with no note looks identical to one stuck there by accident.

Done when: the current stage and the next planned stage are both written
down somewhere other than your memory.

## 4. Check the flag in the same way everywhere it appears

A flag checked with a plain string in some places and a constant or a
typo'd name in others drifts out of sync. Search the codebase for
every place the new behaviour needs to branch: server-side logic,
templates/views, client-side code, and routing or middleware. Use one
canonical name or constant for the flag and reference it, rather than
re-typing the string at each call site.

Done when: every place the feature could show up has been searched for,
not just the one call site you started from.

## 5. Test both states

Write or update tests that set the flag on and off for the same scenario
and assert the difference in outcome. For a flag whose condition depends
on the visitor, cover an anonymous request as its own case rather than
assuming the logged-in test covers it.

Done when: a test fails if the on-branch and off-branch behaviour were
swapped by accident.

## 6. Remove the flag fully once the rollout is complete

Once a flag has been at 100% for long enough to trust it, remove it
completely rather than leaving it at "always true" indefinitely: delete
the flag's definition, delete every check and its now-dead alternate
branch, and clear any stored per-user values the flagging system kept.
Leaving a permanently-true flag in place costs a reader time working out
whether it is still a real toggle.

Done when: a search for the flag's name finds nothing left in the
codebase or the flagging system's stored state.

Laravel projects using Pennant: [references/laravel.md](references/laravel.md).

## It's working if

- A new flag's anonymous-visitor behaviour was a deliberate decision, not
  an accident discovered in production.
- Turning the flag off restores the exact previous behaviour, proven by a
  test.
- No flag past full rollout still has a definition, a check, or stored
  values anywhere in the project.
