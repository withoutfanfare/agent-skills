# Shape of `design-system.md`

A rough guide, not a form to fill in mechanically. Drop a heading rather
than pad it with invented content; a shorter honest document beats a long
one padded with guesses. Aim for 300 to 500 lines: much shorter and there
is not enough to work from, much longer and the important rules get lost
in the rest.

**Every value traces back to code or a rendered page.** Resolve a
`clamp()` to a real pixel figure at a stated viewport. Check a claim
before writing it down, such as confirming a button label in the source
before calling it the standard one. A guessed rationale is worse than
leaving the line out, because whatever you write here gets followed.

## 1. What it looks and feels like

One paragraph, written last, after you have looked through the
screenshots. Light or dark, dense or spacious, and what does the visual
work: type, photography, illustration, data, white space. Say what the
product deliberately avoids as well as what it does.

This paragraph carries more weight than any table below it. It is what
keeps generated output from drifting toward a generic default look.

## 2. Colour

Start with backgrounds, layered darkest or lightest first, then the text
colours in their ramp, then accent colours in the order they are actually
used (which one carries the most weight, which is reserved for rare
moments). Where the code or docs record why a colour was chosen, include
it: a rationale tells a designer something a hex value cannot.

If there is a signature visual effect built from colour (a gradient wash,
a grain overlay, a glow around key elements), call it out here with the
real CSS. It is often the single most recognisable trait of the product
and the thing a plain token list leaves out.

## 3. Type

Each typeface and where it is used. The heading scale as a table of size,
weight, tracking and line height: it is the combination of these, not any
one value, that makes a set of pages read as one product. Note any rule
about sizes that keeps getting reintroduced by accident (two very close
sizes, like 21px and 21.6px, are a common way two pages end up feeling
like they were built by different people).

If a typeface was tried and dropped, say so, so it does not get proposed
again.

## 4. Space, corners and motion

Container widths and comfortable reading measures. Vertical rhythm,
resolved to a real pixel figure at a named viewport rather than left as a
raw `clamp()` expression. Corner radii as a scale. Named easing curves.

Describe how elements enter the page as a pattern (fade up on scroll,
stagger by list position, and so on) and where it is applied: whole
sections versus every element is a design decision, not an implementation
detail, and belongs here.

## 5. How pages are put together

The small number of decisions that make separate pages feel like the same
product: a fixed side rail or a full-width header, how the hero area is
treated, how sections are separated from each other (a background change,
a rule, whitespace alone), how a page tends to close. If there is a rule
like "no two sections next to each other share a background", state it and
what it prevents.

## 6. Components

Buttons in full detail, since they get reused more than anything else.
Then the one or two most common surface treatments (a card, a panel), with
real CSS for anything unusual. Where there is exactly one correct way to
build something, say so directly ("this is the one card treatment; do not
invent a second"), because otherwise variants creep in over time. List
anything else recurring by name only; the markup itself lives in the
`components/` folder of the pack.

## 7. Imagery

Group images by family (photography, illustration, icons and so on), and
for each one write down the subject matter, the lighting or rendering
style and how elements are framed in enough detail that a brief handed to
an illustrator or an image model would produce something on-brand without
further guidance. Note the usual crop ratio and where any caption sits.
Without this, generated pages default to generic stock imagery.

## 8. Voice, briefly

Only the parts of the writing style that affect layout and design: heading
capitalisation, banned phrasing, first- versus third-person, spelling
convention. Full copywriting guidance belongs in its own document, not
duplicated here.

## 9. What has been tried and rejected

The most useful section, and the one that is easiest to skip. Everything
above describes the target; this describes the dead ends, which is far
more actionable because it comes from this product's own history rather
than general best practice. A rule paired with the real decision that
produced it is far more useful than a list of dos, and it is the one part
a plain CSS scan can never produce on its own.

Look for it in commit messages describing a revert, review comments,
retrospectives, or a written changelog. Write each one as a short rule plus
the real instance that produced it:

> **A label repeated on every card carries no information and just adds
> noise.** One listing page put the same status word on 19 of 22 cards.
> Removing it, rather than restyling the card, was what actually calmed
> the page down.

If the project's history has nothing recorded, say that plainly rather
than inventing examples to fill the section.

## 10. Accessibility notes

Contrast requirements, focus-ring treatment, and any reduced-motion
handling, kept to what is specific to this system rather than restating
general guidance.
