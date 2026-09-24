# Analogies and templates

## Analogies that hold up

| Concept | Analogy | Where it breaks |
|---|---|---|
| API | a restaurant menu: you order from a fixed list, the kitchen is hidden | real APIs can change the menu between versions |
| Cache | a note on your desk instead of a trip to the filing room | a note can go out of date; caches need clearing |
| Queue | a ticket system at a deli counter: jobs wait their turn | some queues have several counters (workers) at once |
| Database index | the index at the back of a book | every new page means updating the index too, which slows writes |
| Load balancer | a host seating guests across several waiters | it can also check whether a waiter is still working |
| Encryption in transit | a sealed envelope in the post | the recipient can still read it once opened |
| Hashing a password | a fingerprint: easy to check, impossible to turn back into a finger | weak passwords can still be guessed and checked |
| Container | a shipping container: the same box runs on any ship | containers share the host's kernel, unlike virtual machines |
| Webhook | a doorbell: the other service rings you when something happens | if nobody answers, the ring may be lost unless retried |
| Race condition | two people editing the same paper form at once | the loser's changes vanish silently |

## Layer template

```markdown
**In one sentence:** <what it is>

**The picture:** <what it does, why it exists, when to use it>

**Key ideas**
1. <idea>: <analogy or example>
2. ...

**How it works:** <step by step, with a real example>

**In practice:** use it when … · avoid it when … · people often get wrong …

**Want more?** <offer the deep dive on a named aspect>
```

## Comparison template

| | Option A | Option B |
|---|---|---|
| Best at | | |
| Weak at | | |
| Choose it when | | |
| Cost to run | | |
