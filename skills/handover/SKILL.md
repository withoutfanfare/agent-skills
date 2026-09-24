---
name: handover
description: >-
  Writes a self-contained brief so a colleague or another agent can pick up
  a task and start straight away: background, the task and its limits, what
  done looks like, what not to touch, the exact files, how to verify, and
  when to stop and ask. Use when the user wants to delegate or hand off a
  task, brief someone on work, or write a task for another agent.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Handover

Delegation usually fails on context, not on the task. The person picking
it up does not know why a file exists, which areas are fragile, or what was
already tried. A good brief gives them all of that up front, so they can
start in minutes rather than after an hour of archaeology or a meeting.

To pick up a project yourself after time away, use `catch-up` (if
installed); to capture what a session taught, use `takeaways` (if
installed).

## 1. Know the audience

A brief for an experienced colleague can leave room for judgement. A brief
for an agent must be explicit, because agents follow instructions
literally: every boundary written down, every check spelled out. Ask who
it is for if it is not obvious.

Done when: the audience is known and the level of detail is set.

## 2. Gather what the delegate will need

From the conversation and the code: the current state, recent changes in
the area, what has been tried, the relevant files and systems, and how the
work is tested. Read the files you will point at, so the paths and
descriptions are right.

Done when: every file and system you will mention has been checked to
exist.

## 3. Write the brief

```markdown
# Brief: <task>

## Background
<what the delegate must know first: current state, recent changes, why this
matters now, terms they might not know>

## The task
<the concrete outcome, not "improve" or "clean up"; the deliverable (a pull
request, a document, a deployed change); what is in scope and what is not>

## Done means
- <observable checks: what works, which tests pass, which numbers hold>

## Do not touch
- <files, modules or services off limits; patterns to keep even if they look odd;
  fragile areas; dependencies not to upgrade>

## Where things are
- <exact paths, services, tables, configuration, docs; where credentials are
  kept (never the credentials themselves)>

## How to check your work
<commands to run, manual steps, edge cases to try>

## Stop and ask when
<kinds of blocker worth raising; decisions not to make alone; how long to be
stuck before asking; who to ask and how>

## Already tried
<approaches that failed, and why, so they are not repeated>
```

Trim sections that add nothing for a small task, but keep the order: it is
the order in which someone builds understanding.

Done when: a person with no access to this conversation could start the
task from the brief alone.

## 4. Check it cold

Reread the brief as the delegate. Mark every place you would have to ask a
question, and answer it in the brief.

Done when: the cold read raises no questions the brief could have
answered.

## 5. Save or send

Save it where the delegate will find it: the issue, the pull request, a
`docs/briefs/` file, or the message to the agent. Report where it went.

## It's working if

- The delegate starts work without asking for context.
- They stop and ask at the right moments, not hours too late.
- Nothing outside the brief's scope changes in their work.
