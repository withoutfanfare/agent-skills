---
name: share-safe
description: >-
  Scans content that is about to leave the machine, such as code, docs,
  config, logs, a draft message, or a whole repository including its
  history, for secrets and personal data. Reports each finding by severity
  with the secret value masked, and offers a redacted copy rather than
  editing the original. Use when the user asks whether something is safe
  to send, wants a file or repo checked before sharing, or asks to scrub
  or redact content before it goes to a teammate, a client, or in public.
license: MIT
allowed-tools: Read Grep Glob Bash Write
---

# Share-safe

Once something leaves the machine, whether by email, chat, a public issue,
or a shared repository, it is out of reach. Someone else's inbox or an
indexed page keeps a copy long after the sender regrets it. This skill is
the check that runs before that line is crossed, not after.

## 1. Fix the audience

The same file can be fine for a teammate and reckless in public. Ask, if it
is not already clear, whether this is going to a colleague, a client or
partner, or somewhere public (a public repository, a support forum, a
shared public link). If the user will not say, review as if for the public
audience: it is the safer failure.

Done when: an audience is set, either stated or defaulted to public with
that noted in the report.

## 2. Gather what will actually travel

Read every file named, plus anything they point at: a config that loads
from an `.env`, a log that references a request ID worth pulling, a
message that says "see attached". If the request covers a repository
rather than a single file, treat its commit history as part of the
content: something removed in the latest commit but present three commits
back is still going out the moment the repository is shared.

```bash
git log --all -p -- <suspect file> | head -200
```

Done when: you have read the content itself, not just its current
top-level view.

## 3. Scan for what should not travel

Work down this list. Judge by context, not just pattern: a variable called
`API_KEY` holding the word `changeme` is not a finding; a 40-character
random string assigned to almost any name is.

- **Credentials**: API keys and tokens, passwords, private key blocks,
  connection strings or URLs with a password embedded in them.
- **Personal data**: real names, email addresses, phone numbers, postal
  addresses, dates of birth. These hide easily inside pasted logs and
  database exports, where one paste can carry hundreds of rows.
- **Infrastructure detail**: internal hostnames, IP addresses, server
  paths, bucket or queue names. Lower risk on their own, but they map the
  inside of a system to someone who should not have that map.
- **Sensitive but not secret**: figures, names or plans that are fine
  internally and wrong for the stated audience, such as a client's name in
  a message meant for the public.

Done when: every file and every piece of history pulled in step 2 has been
checked against this list.

## 4. Report by severity, values masked

Never print a secret in full. Show enough to identify it and no more, for
example the first and last few characters with the middle replaced.

| Severity | Meaning |
|---|---|
| high | a working credential or personal data that identifies someone |
| medium | infrastructure detail or a credential that looks inactive or expired |
| low | sensitive-but-not-secret content, wrong only for this audience |

For each finding: where it is (file and line, or commit), what it is, the
masked value, and what could happen if it shipped as-is.

Done when: every item from step 3 appears in the report with a severity,
or the report says plainly that nothing was found.

## 5. Offer a redacted copy

Never edit the user's original file. Write a new file (or a paste-ready
block, for pasted content) with each finding replaced by a placeholder
that keeps the surrounding content readable, for example:

```text
STRIPE_SECRET_KEY=<REDACTED: stripe secret key>
```

For a repository whose history carries the problem, redacting the working
copy is not enough; say so plainly and point to history-rewriting as the
only real fix, without attempting it unasked (it rewrites commit hashes
and needs a co-ordinated force-push everyone agrees to).

Done when: a redacted copy exists for every finding that can be fixed by
substitution, and history-only problems are called out separately.

## 6. Give a one-line verdict

End with exactly one of:

- "Safe to share with <audience>."
- "Not yet: N item(s) to fix first, redacted copy below."

Done when: the verdict matches the findings; a high-severity finding never
sits under a "safe" verdict.

## It's working if

- Nothing marked "safe" still contains a live credential.
- Every finding shows a masked value, never the real one.
- The user's original file is untouched; the fix is a new file or block.
