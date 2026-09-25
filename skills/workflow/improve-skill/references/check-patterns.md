# Check patterns

Categories to draw checks from when testing a skill, with worked examples.
Every check must be answerable yes or no from the output alone; if two
readers could disagree, rewrite it or drop it.

## Trigger checks

Only needed when the skill is meant to start itself from a plain request
(not typed-only), or when you are proving a typed-only skill really stays
quiet.

| Request type | Check |
|---|---|
| A `fire` request | The skill's own steps or report shape are visible in the run, not a generic answer |
| A `quiet` request (near miss) | Nothing in the run shows the skill's steps or report shape |
| A `quiet` request, typed-only, tried by name in Codex | The skill still runs when called by its exact name, even though it stayed quiet unprompted |

Example pair for a subscription app's "renewal reminder" skill. Fire:
"remind customers their trial ends Friday". Quiet: "write the email
that goes out when a card payment fails" (a nearby but different job).

## Structure

| Skill says | Check |
|---|---|
| "group findings by severity" | Output has a separate heading or column for each severity used |
| "end with a plain-English summary" | The final section has no code and no bare identifiers like `ABC-123` |
| "list one file per row" | Every row names exactly one file path |

## Length

| Skill says | Check |
|---|---|
| "keep the summary short" | The summary section is under 60 words |
| "one line per finding" | No finding wraps a table row onto a second line |

## Required content

| Skill says | Check |
|---|---|
| "always give a severity" | Every finding has a severity word next to it |
| "quote the request it answers" | At least one line quotes or paraphrases the original request |
| "note the ticket if one exists" | The output names a ticket or explicitly says none was given |

## Banned content

| Skill says | Check |
|---|---|
| "no marketing language" | Output contains no exclamation marks and no words like "amazing" |
| "never invent a file that was not read" | Every file path mentioned was also read during the run |
| "no long dashes" | Output contains no em dash character |

## Step order

| Skill says | Check |
|---|---|
| "read the ticket before proposing anything" | A reference to the ticket appears before the first proposal |
| "run the check before reporting a fix" | Command output or its result appears before the fix is described |

## Writing new checks

Word each check as a full sentence a stranger could mark from the output
alone, for example "the report contains a table with a Severity column"
rather than "checks severity is there". One check should test one thing;
if answering it needs two separate readings of the output, split it into
two checks.
