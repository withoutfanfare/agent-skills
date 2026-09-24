---
name: adversary
description: >-
  Threat-models a feature or system before it is built, using STRIDE: maps
  what is worth protecting, how data flows and where trust changes, then
  rates realistic threats and proposes specific mitigations. Use when the
  user asks for a threat model, wants to think through the attack surface or
  trust boundaries of a design, or asks how someone could abuse a feature
  before it exists.
license: MIT
effort: high
allowed-tools: Read Grep Glob Bash Write
---

# Adversary

A security hole found in a design costs a conversation; found in
production, it costs an incident. This skill thinks like an attacker while
the feature is still on paper: what is valuable, how data moves, where
trust changes hands, and what a motivated person would try at each of
those points.

For auditing code that already exists, use `harden` (if installed).

## 1. Describe the system

From the design, the conversation and the surrounding code, write a short
description the user can check:

- **Assets:** what has value. Personal data, credentials, payment details,
  business data, money-moving actions, capacity, reputation.
- **Data flows:** from input to storage and back out: browser to server,
  server to database, to queues and workers, to outside services, to
  exports and emails.
- **Trust boundaries:** where the level of trust changes. The internet and
  the app, anonymous and signed-in users, users and admins, your code and a
  third party's, one tenant and another.
- **Actors:** who could attack, and with what access (anonymous visitor,
  customer, compromised account, disgruntled insider, compromised
  dependency).

Done when: the user confirms the description matches what they intend to
build.

## 2. Walk each boundary with STRIDE

At every boundary and flow, ask the six questions, keeping only threats
that are realistic here:

| Letter | Threat | Ask |
|---|---|---|
| S | Spoofing | Can someone pretend to be another user or system? |
| T | Tampering | Can someone change data, requests or files they should not? |
| R | Repudiation | Could someone deny an action because it was not recorded? |
| I | Information disclosure | Can someone see data they should not? |
| D | Denial of service | Can someone exhaust a resource or block others? |
| E | Elevation of privilege | Can someone do more than their role allows? |

Eight real threats are worth more than fifty theoretical ones.

Done when: every boundary has been walked, and each threat names the
boundary and the attacker.

## 3. Rate them

Score **likelihood** (1: needs insider access or unusual conditions; 2:
moderate skill or access; 3: any motivated attacker) and **impact** (1:
minor, contained; 2: significant breach or outage; 3: full compromise,
legal or regulatory consequences). Risk is likelihood times impact:
6 or more must be mitigated before release; 3 or 4 are mitigated or
explicitly accepted with monitoring. On the shared severity scale, 6 to 9
is a blocker, 3 or 4 major, and 1 or 2 minor.

Done when: every threat has both scores and a risk.

## 4. Mitigate specifically

For each threat scoring 3 or more: the control to build (concrete: "verify
the webhook signature with the provider's secret", not "add security"),
where it goes, rough effort, and what risk remains afterwards. Order by
risk removed per unit of effort.

Done when: every threat scoring 6 or more has a mitigation, and every one
scoring 3 or 4 is mitigated or has an owner who accepted it.

## 5. Write the threat model

Save it with the project's design documents (ask, or use
`docs/threat-models/`):

```markdown
# Threat model: <feature>
Date · Scope · Status: draft|reviewed|accepted

## System
<assets, flows, boundaries, actors>

## Threats
| # | STRIDE | Boundary | Threat | L | I | Risk | Mitigation | Owner |

## Accepted risks
<each with who accepted it and what is monitored>

## Before release
<the mitigations that must land first, as a checklist>
```

## It's working if

- Each threat is specific enough that a developer knows where the fix goes.
- Blocker risks are either mitigated or explicitly accepted by a named person.
- The model is written before the code, and updated when the design moves.
