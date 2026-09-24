---
name: review
description: >-
  Reviews a diff, branch or pull request before it merges, answering two
  questions separately: does it do what was asked, and is it safe, reliable,
  fast and maintainable? Every finding carries a severity and a confidence
  rating. Use when the user asks to review changes, check a pull request,
  look for bugs before merging, or asks whether the code matches the ticket.
license: MIT
context: fork
background: false
effort: high
allowed-tools: Read Grep Glob Bash
---

# Review

A good review answers two different questions, and a weak one blurs them.
**Is this the right change?** checks it against what was asked for. **Is the
change built well?** checks security, reliability, performance and upkeep.
Beautiful code that builds the wrong thing fails the first; the right
feature with an injection hole fails the second. Keep the two answers apart
all the way to the report, so one never hides the other.

## 1. Check you are reviewing the right thing

Before reading any code, confirm the target exists and has content. For a
branch or commit range, resolve the base and look at the size of the diff
against the merge base:

```bash
git rev-parse <base>
git diff <base>...HEAD --stat
```

A wrong base or an empty diff should stop the review here, in seconds.
Skip whatever the project's tooling already enforces (formatters, type
checkers, linters). Spend attention on what only a reviewer can see.

Done when: you know the exact set of files and commits under review, and it
is not empty.

## 2. Write down the intent

Find what the change was supposed to do, in this order: an issue or ticket
referenced in the branch name, commits or pull request description; a spec
or plan the user pointed you at; the user's own request in this
conversation. If none exists, ask once. If there truly is none, say so and
review for quality only.

Write the intent as one short paragraph in your own words. Every finding is
judged against it, and it leads the report so the reader can correct a
misunderstanding before reading anything else.

Done when: the intent paragraph is written, or "no spec available" is
recorded.

## 3. Is this the right change?

Compare the diff with the intent and list three kinds of gap, quoting the
line of the spec each one rests on:

- **Missing or partial:** asked for, not (fully) there.
- **Unasked for:** behaviour nothing requested. Sometimes welcome, always
  worth naming.
- **Built differently:** looks done, but contradicts what was asked.

Done when: each requirement in the intent is marked met, partial or
missing.

## 4. Is the change built well?

Read the whole diff, then follow data from where it enters (requests, files,
queues, webhooks) to where it leaves (responses, logs, emails, exports).
Every entry point is a security surface. Work in severity order, so blockers
surface before anyone reads about naming:

1. **Security:** input validation, output encoding, authorisation on every
   write, secrets, injection of any kind.
2. **Reliability:** error paths, partial writes, retries that repeat side
   effects, race conditions, timeouts on outside calls.
3. **Performance:** queries inside loops, missing indexes, unbounded
   results, work that belongs in a background job.
4. **Upkeep:** naming, coupling, dead code, and tests that would fail if the
   behaviour broke.

Check who else uses what changed. A change to shared code carries more risk
than a new leaf. [references/checklist.md](references/checklist.md) has the
long list for deep reviews. For Laravel projects, also work through
[references/laravel.md](references/laravel.md).

Done when: every changed file has been read and every entry point traced.

## 5. Rate every finding

Give each finding two ratings:

| Severity | Meaning |
|---|---|
| blocker | must be fixed before merge |
| major | should be fixed; merge only with a reason |
| minor | worth doing, not worth delaying for |

| Confidence | Meaning |
|---|---|
| certain | visible in the code itself |
| likely | strong evidence, depends on runtime behaviour |
| possible | a smell worth checking; say what would confirm it |

If there are blockers, lead with them and trim the minors to a short list.
A security blocker is never mixed in with style notes.

Some findings are only true at a point in time. Debug logging may be right
while a feature is being tested and wrong at merge. Say which applies:
"remove before merge; fine on the feature branch".

Done when: every finding has a severity, a confidence and a file and line.

## 6. Report

```markdown
# Review: <what was reviewed>

**Intent:** <one paragraph>
**Verdict:** blocked / changes needed / ready

## Is this the right change?
<missing, unasked-for and built-differently items, each quoting the spec, or "no spec available">

## Is it built well?
| ID | Severity | Confidence | Where | Finding | Suggested fix |
|---|---|---|---|---|---|
| R1 | blocker | certain | src/Search.php:45 | User input joined into SQL | Bind the parameter |

## Notes
<one short section per blocker or major: the code, the fix, what it prevents>
```

Size the report to the job: a quick look gets the verdict and a short list;
a full review gets the table and notes.

For a high-stakes or disputed change, end by suggesting the same review on
a different model. A finding both reviews raise is almost certainly real;
one only a single review raises should be checked against the code before
anyone acts on it.

Done when: the report follows the template, with the two questions answered
separately.

## It's working if

- The reader can tell within ten seconds whether the change can merge, and
  why.
- Scope problems and code problems appear under separate headings, never
  in one ranked list.
- Every finding points to a file and line and says how sure the reviewer is.
