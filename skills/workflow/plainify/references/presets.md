# Presets

Load the entries that match the chosen reader, shape and (if given)
purpose. House style always applies on top: markdown, British English, a
warm voice, commas and colons rather than long dashes.

## Readers

| Reader | Already knows | Cares about | Jargon | Tone | Depth | Default shape |
|---|---|---|---|---|---|---|
| Executive | little technology | outcome, risk, cost, time, the decision they must make | none | crisp, confident | shallowest | briefing |
| Manager | the product, some technology | status, blockers, effort versus impact, what to pass on | minimal, explained | clear, practical | enough to decide | one-pager |
| Non-technical colleague | the product, not the technology | what changed and how it affects their work | none | friendly | light | short summary |
| Designer | product and UX, some technology | what users will experience, flows, states, edge cases | light | collaborative | medium, user-facing | one-pager |
| Client | their business, not the technology | value, progress, anything affecting them, next steps | none | warm, professional, reassuring; problems framed with the plan | light to medium | email |
| Customer | how to use the product | what they can do now and how | none | helpful, upbeat | task-level | help article |
| Developer | the technology in depth | what changed, why, where, what to do | full precision | direct | as deep as needed | full documentation |
| Operator | systems and operations | what to run, what to watch, how to recover | full precision | direct, calm | step level | runbook-style steps |
| Product admin | the product's settings | what to configure and the effect | light, explained | clear | task-level | help article |
| Website visitor | nothing about you | why they should care, what to do next | none | inviting, plain | shallow | web copy |

## Shapes

| Shape | Structure |
|---|---|
| Briefing | headline; three bullets (what, so what, what now); one line on the decision needed |
| One-pager | headline; short summary; three to five key points; optional detail under a heading; next steps |
| Short summary | one-line summary; bullets; nothing else |
| Chat message | first line is the whole message; a few bullets; a link for more; under about 120 words |
| Email | subject line; greeting; the point in the first sentence; short paragraphs; a clear ask or next step; sign-off |
| Full documentation | title; overview; sections by task or concept; examples; troubleshooting |
| Release notes | version and date; highlights; grouped changes written as benefits; any action needed |
| FAQ | questions in the reader's words, most common first; short direct answers |
| Status update | status in one word or colour; what changed since last time; risks; next milestone |
| Help article | the task as the title; when you would do it; numbered steps with what you should see; troubleshooting |

## Purposes (set reader and shape together)

| Purpose | Reader | Shape | Notes |
|---|---|---|---|
| UAT script | client or customer | numbered test steps | each step: action, expected result, pass or fail box |
| User guide | customer | help article | one task per section |
| Developer onboarding | developer | full documentation | setup, architecture tour, conventions, first task |
| Operator guide | operator | runbook-style steps | trigger, checks, fix, confirm, escalate |
| Marketing copy | website visitor | web copy | benefit-led headline, proof, one call to action |
| Release notes | customer | release notes | benefits over implementation |
| Status page notice | customer | status update | what is affected, what we are doing, next update time |
| Help-centre article | customer | help article | plain task title people would search for |
| In-app announcement | customer | chat message | one benefit, one action |
| Client progress update | client | email | progress, anything needing them, next steps |
