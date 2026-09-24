# Document mode

Tests show that a change works. Documentation lets everyone else learn what
it does without opening the diff. This mode writes plain-English pages for
the people who depend on the change (the admins and users who meet it, the
operators who keep it running, the developers who extend it) and files them
where the project keeps its docs, using `plainify` when installed.

You can call it directly with `work document <item>`. A `carry on` run also
reaches it after the build is finished, provided the delivery profile lists
audiences for this type of change. Documentation normally forms part of the
gate into staging or review.

## Sources

- the **Documentation** table in the [delivery profile](../delivery-profile.md),
  which says, per change type, who the audiences are, which `plainify`
  purpose suits each, and where it is saved;
- acceptance criteria, decision records and the brief or design;
- the pull request's diff and description, the files that matter, and any
  docs already covering this area;
- verification evidence and the UAT plan, if they exist;
- pages elsewhere that this change has made wrong.

Without a profile, ask one question covering both audience and location.
Alternatively, give the draft in the reply and name where it would be saved.

## Steps

Each step needs the one before: an audience has to be chosen before you
write for it, and a page has to exist before you can file it.

1. **Choose the audiences.** Go through the profile's table and keep only
   the readers this change genuinely affects; every other row gets
   `Not needed (reason)`. Typical pairings: customers who will notice the
   change get release notes, an admin feature gets a user guide, an ops
   change gets a runbook entry, and a platform change gets a developer guide.
2. **Look for existing pages.** Search the docs area for anything the change
   touches. Updating what is there beats adding a second page beside it. A
   page the change has made wrong is either corrected or flagged as stale.
3. **Stick to the sources.** Write from the code, tests, pull request and
   brief, not from recollection. Readers will act on whatever the page says,
   so leave out anything the sources do not show and mark the hole
   "Unverified".
4. **One plain-English pass for each audience.** With `plainify` installed,
   run it with the purpose that fits that audience. Without it, meet the same
   standard by hand. Operators and developers need exact detail; strip the
   jargon for everyone else. Write in British English and Markdown, with no
   long dashes.
5. **File it** in the location the profile gives, named the way the project
   names files, and list it in whatever index that area has (an index page,
   a tag list, a README).
6. **Link both ways.** The page points to the pull request and the brief;
   the pull request description points back to the page.
7. **A documentation plan** (from
   [the documentation plan template](../../assets/documentation-plan.md)) is
   only needed when there is more than one audience or some of the work is
   put off. In every other case the receipt covers it.

## Guardrails

- Pages reach far more people than the systems they describe. No
  credentials, tokens, secrets, or personal or production data beyond what
  is needed, may travel from code, config or the pull request into a page.
- Update the page that exists before you consider writing a new one.
- If the sources do not show a behaviour, it stays out of the page and the
  gap is marked "Unverified".

## Staleness

Once the decisions, criteria or code behind a page change, the page is out
of date. Name the page and the specific claim, and fix it next time round.

## Completion check

Done when: each audience in the profile's row ends with a new page, an
updated page, or a written `Not needed (reason)`; every page starts with what
the change means for its reader; and nothing on any page goes beyond what the
sources back up.

The reply is a short receipt; the pages stay where they were saved. Per
audience, say whether a page was saved or updated or marked `Not needed`
(with the reason), and give its location. Keep it to a few lines each. List
every "Unverified" gap still in the pages so the reader can see which claims
still lack a source.
