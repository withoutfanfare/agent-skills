---
name: instruction-audit
description: Reviews an AGENTS.md or CLAUDE.md file (root and nested) against a size and usefulness budget, then proposes cuts before touching anything.
license: MIT
disable-model-invocation: true
allowed-tools: Read Grep Glob Bash Edit Write
---

# Instruction audit

An agent's instructions file gets read at the start of every session,
whether the task needs it or not, so every line in it is a standing tax on
that session's attention. Files grow by addition: a rule goes in after a
mistake, a fact gets pasted in and never updated, two files end up saying
almost the same thing in different words. None of that is ever undone on
its own. This skill reads what is actually there, sorts each passage into
a small number of outcomes, and proposes a smaller file, but it never
edits an instructions file without the person's go-ahead first.

This is not `project-setup` (if installed): that skill writes the one
block of hard facts (tracker, branch, commands, environments) a project
needs recorded once. This skill audits everything in the file, including
that block if it has drifted, but its job is trimming and correcting what
exists, not establishing the facts in the first place.

## 1. Collect every file in scope

Find the root instructions file (`AGENTS.md`, `CLAUDE.md`, or both if the
project keeps one pointing at the other) plus every nested one below it
(`git ls-files -- '**/AGENTS.md' '**/CLAUDE.md' 'AGENTS.md' 'CLAUDE.md'` or
an equivalent search if the project is not in git). For each, note where
it sits in the tree and which ones a session in a given subfolder would
have open at once (that pairing matters in step 4). Read every file in
scope in full before judging any of them; a rule that looks redundant
alone might be the one place a fact is actually stated.

Done when: you have the full path list, each file marked with what loads
alongside it, and you have read every one of them.

## 2. Take a baseline measurement

Record, per file: line count, and a rough split between prose instruction,
fenced code or command blocks, and anything that looks machine-generated
(a tool's setup banner, an auto-inserted marker, a table a script clearly
wrote). Compare sibling nested files with `diff` where two look alike;
near-identical blocks are worth flagging before you read either closely,
because the fix is usually mechanical (keep one copy, point to it) rather
than a judgement call.

Done when: you can state a before-total for lines in scope, split by
file, with the mechanically obvious duplication already flagged.

## 3. Sort every passage into one outcome

Work through each file section by section (or paragraph by paragraph for
files with no headings) and assign one outcome:

| Outcome | When it applies |
|---|---|
| Keep | A project-specific fact or rule nothing else would surface, stated once, still true |
| Shorten | The point is worth keeping but takes more words than it needs |
| Drop, model already does this | A capable agent follows the instruction without being told: general good practice, a well-known convention, an explanation of a widely used tool |
| Drop, environment already says it | A build script, a lint config, a README or `--help` output already carries the same fact more reliably, so the copy here can only go stale |
| Drop, no longer true | Names a file, command, branch or process check that has moved or gone |
| Move to a nested file | Only relevant to part of the repository, sitting in the root file where every session pays for it |
| Move to an on-demand reference | Detail a session needs rarely and in full, not as a constant reminder (a long checklist, a one-off migration note) |
| Merge | Restated with small variation somewhere else in scope |

For anything borderline, rate your confidence it is genuinely safe to
remove: certain (nothing in the file or repo still depends on it), likely
(strong signal, one thing left unchecked), or possible (a hunch worth the
person's own judgement). Leave a possible-confidence item for the report
rather than deciding it yourself.

Done when: every passage in every file has one outcome and, if it is a
drop or merge, a confidence rating.

## 4. Check pairs, not just single files

Re-read every set of files that would be open in the same session
together (the root file plus whichever nested ones apply to a given
folder) looking specifically for two rules that pull in different
directions, or one that quietly overrides another without saying so. This
is the check a single-file pass cannot do, because neither file looks
wrong on its own. Record each conflicting pair together, naming both
files and both rules, not as two separate single-file findings.

Rate a genuine conflict as blocker (the rules actively contradict, so a
session could follow either and be "right"), major (they overlap enough
to cause confusion but one is clearly subordinate), or minor (different
wording of the same intent, harmless but worth tidying).

Done when: you have looked at every co-loaded file pair and either listed
its conflicts or can say none were found.

## 5. Draft the proposal, do not apply it

Write the report below and show it to the person. Nothing in scope is
edited at this stage, including files you are completely confident about;
confidence changes how you present a recommendation, not whether you wait
for it to be accepted.

```markdown
## Instruction audit: <files in scope>

**Before:** <n files, n lines total>
**Proposed after:** <n files, n lines total (n% smaller)>

### Conflicts between co-loaded files
| Severity | Files | Rule A | Rule B | Proposed resolution |
|---|---|---|---|---|
| blocker | root, api/AGENTS.md | "always ask before deploying" | "deploy on every merge to main" | keep the api-folder rule, note the exception in root |

(state "none found" if step 4 found nothing)

### Proposed changes
| File | Passage | Outcome | Confidence | Reason |
|---|---|---|---|---|
| AGENTS.md | "Use conventional commits" | keep | certain | project-specific, not a default |
| AGENTS.md | explanation of what a pull request is | drop, model already does this | certain | standard knowledge |
| api/AGENTS.md | 40-line deployment checklist | move to reference | likely | needed occasionally, not every session |

### Proposed file contents
<the full replacement text for each file being edited, and for any new
reference file a "move" outcome creates>
```

Done when: the report is written and the person has seen it, with no file
in scope changed yet.

## 6. Apply only what is approved

Once the person responds, apply exactly the outcomes they accepted.
Where they reject an outcome, leave that passage untouched rather than
substituting your own compromise. Where a passage moves to a new
reference file, link it from the file it left with one line, so the fact
is still findable. Do not fold unrelated tidying into this pass; if you
notice something outside the agreed outcomes while editing, add it to the
report for next time instead of changing it now.

Done when: every accepted outcome is applied, every rejected one is
untouched, and the diff contains nothing the person did not agree to.

## 7. Recheck the result

Reread every edited file in full and confirm nothing marked "keep" was
lost in the edit, then recompute the line counts from step 2 so the
report's before and after figures are measured, not estimated.

Done when: the new line counts are recorded against the files you
actually saved, and a fresh read of each one still makes sense on its
own.

## It's working if

- The person can see, before any file changes, exactly what shrinks, what
  moves, and why, with nothing applied without their say-so.
- A conflict between two files gets one shared entry, not two separate
  ones that each look fine alone.
- The file that remains reads as true today, with nothing left in it that
  the agent would have done anyway.
