---
name: hotspot
description: >-
  Finds out why a page, endpoint or job is slow and fixes the biggest cause
  first, with before and after measurements: repeated queries, missing
  indexes, oversized results, slow outside calls, missing caching. Use when
  the user says something is slow, asks to profile or speed up a request,
  mentions N+1 queries, or wants to know where the time goes.
license: MIT
allowed-tools: Bash Read Edit Write Grep Glob
---

# Hotspot

Slow code is rarely slow everywhere. Usually one thing takes most of the
time, and guessing which is how days go into optimising the wrong loop.
This skill measures first, fixes the largest cost, and measures again, so
every claim of "faster" comes with numbers.

## 1. Measure the baseline

Pick the exact request, command or job that is slow, and measure it the
same way you will measure it afterwards:

- total time (several runs, not one);
- number of database queries and their total time;
- outside calls and their time;
- memory, if the complaint is about memory.

Use what the project already has: a query log, a profiler or debug bar, an
APM tool, or simple timing around the code. Warm caches or cold, say which,
and keep it the same for the comparison.

Done when: there is a baseline table with the numbers and how they were
taken.

## 2. Find where the time goes

Rank the costs from the measurement. The usual suspects, roughly in order
of how often they turn out to be the culprit:

| Suspect | Sign |
|---|---|
| Repeated queries (N+1) | query count grows with the number of rows shown |
| Missing index | one query slow on its own; the query plan shows a full scan |
| Too much data | selecting every column or every row, then filtering in code |
| Slow outside calls | an API call per request, or per item, with no timeout |
| Work that belongs in the background | emails, exports or image processing inside the request |
| Repeated expensive work | the same calculation or lookup on every request, uncached |
| Heavy front end | the server is quick but the page is not; check assets and rendering |

Confirm the suspect with evidence (the query log, the query plan via
`EXPLAIN`, a timing around the call) before changing anything.

Done when: the single largest cost is named, with evidence.

## 3. Fix the biggest cost

One change at a time, starting with the largest:

- Repeated queries: load related data up front in one query.
- Missing index: add it through a migration, matching the query's filter
  and sort columns.
- Too much data: select the columns needed; paginate or stream large sets.
- Outside calls: add timeouts, batch them, cache results that can be
  cached, or move them to a background job.
- Background work: queue it and return early.
- Repeated work: cache it, with a clear rule for when the cache is cleared.

Add a guard against the problem coming back where the framework offers one
(for example, making lazy loading throw an error outside production).

Done when: the change is made and the tests for that area pass.

## 4. Measure again

Repeat step 1 exactly. Compare:

```text
                 Before    After
Time (median)    1,840 ms  210 ms
Queries          203       4
Query time       1,410 ms  38 ms
```

If the improvement is small, the diagnosis was wrong: go back to step 2
rather than stacking more changes. Stop when the request meets its target
or the remaining costs are not worth the complexity.

Done when: the before and after table is filled in from real runs.

Laravel specifics (query logging, eager loading, indexing, caching) are in
[references/laravel.md](references/laravel.md).

## It's working if

- Every speed claim comes with a before and after measurement taken the same
  way.
- Each fix targeted the largest remaining cost, with evidence.
- Nothing was cached without a rule for clearing it.
