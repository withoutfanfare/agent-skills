# Design brief for one interface option

Give this brief to each designer (a parallel helper, or yourself in turn),
with one assigned direction.

---

You are designing a deeper interface for one area of a codebase.

**Area:** <modules and files>
**Why it is shallow today:** <the evidence from exploration>
**Real call sites:** <two or three paths to code that uses it now>
**Your direction:** <for example: "a single object that owns the whole
lifecycle" / "plain functions over plain data" / "events and handlers">

Produce:

1. **The public interface:** names and signatures only, as small as you can
   make it while still serving every call site.
2. **What it hides:** the details callers no longer need to know.
3. **Call sites rewritten:** how each real call site reads with your
   interface.
4. **Costs:** what becomes harder, slower or less flexible, stated
   plainly.
5. **Migration:** the first two or three steps to get there without
   breaking anything.

Stay within your direction even if another seems better; the value is in
comparing different shapes. Keep it under a page.
