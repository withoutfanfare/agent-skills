# Adding a skill

From idea to a skill that agents can find, in one pass. The writing rules
live in [CONTRIBUTING.md](../CONTRIBUTING.md); this page is the checklist
around them, so a new skill is surfaced, tested and switched on, not just
written.

## 1. Check it is new

```bash
agent-skills list skills
```

Then ask `/which-skill` about the situation the skill is for. If an
existing skill covers most of it, improve that one instead (`/improve-skill`
tests an edit against real prompts).

Done when: no existing skill does the job, or you have chosen one to
extend.

## 2. Public or private

- **Public** (`skills/<category>/<name>`): works for anyone, with no
  dependence on your own tools, folders, accounts or clients. Pick the
  category it is tied to: `workflow`, `laravel`, `frontend` or `desktop`.
- **Private** (`skills/private/<name>`): leans on something only your
  machine has. The folder is git-ignored, never linted and never
  published; see its own `README.md` if you keep one there.

A private skill can be promoted later by rewriting it without the personal
parts and moving it into a category folder.

Done when: the folder path is decided.

## 3. Name it

Short, lowercase, hyphenated, and saying what it does (`log-triage`, not
`helper`). Names are unique across the whole library, private ones
included, because every skill links into one flat folder; the linter
refuses a clash.

Done when: `agent-skills list skills` shows no skill with that name.

## 4. Write it from the template

```bash
cp -R docs/skill-template skills/<category>/<name>
```

Fill in `SKILL.md` following CONTRIBUTING. Decide whether it should start
on its own or only when typed; a typed-only skill keeps
`agents/openai.yaml` from the template, a model-invoked one deletes it.

Done when: the skill has a description with real trigger phrases,
numbered steps ending in "Done when", and "It's working if".

## 5. Make it findable

For a public skill, all of these:

- **Router:** add it to `skills/workflow/which-skill/SKILL.md` under the
  section that fits, marked *(typed)* if it is typed-only. The linter
  fails until you do.
- **Set:** add its name to the `sets/*.txt` file it belongs with, if any,
  so `agent-skills add <set>` brings it in.
- **Trigger cases:** add a `fire` and a `quiet` line to
  `tests/triggers.tsv`. Make the quiet line one a neighbouring skill
  should catch, so the pair proves the boundary between them.
- **Catalogue:** run `python3 scripts/catalogue.py`.
- **README:** add it to the highlights table only if it is one of the
  handful a newcomer should know about.

A private skill needs none of these. `/pick-skills` reads private skills
along with the rest, so a clear description is what surfaces it.

Done when: `python3 scripts/lint.py` is clean.

## 6. Test it

```bash
python3 scripts/lint.py
bash tests/test-cli.sh
bash tests/test-lint.sh
bash tests/trigger.sh <name> <neighbour> <neighbour>
```

Run the trigger cases for the new skill and for the neighbours its quiet
lines point at, since a new description can steal their requests.

Done when: every command passes, including the neighbours' trigger cases.

## 7. Switch it on

```bash
agent-skills add <name>          # this project
agent-skills home add <name>     # every project (keep this list short)
```

Restart the agent so it sees the new skill.

Done when: `agent-skills status` (or `ls ~/.claude/skills`) shows the
link, and a fresh session starts the skill on its `fire` prompt.

## Retiring a skill

Remove it from the router, its set and `tests/triggers.tsv`, then delete
the folder and regenerate the catalogue. For a private skill, move the
folder to `skills/private/.archive/` instead, which keeps it out of every
listing without losing it.
