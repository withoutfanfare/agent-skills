# Deep review checklist

For full reviews. Work through the sections that apply to the change; skip
the rest. Each line is a question to answer yes, no or not applicable.

## Security

- Is every value from outside the system validated before use?
- Is output encoded for where it lands (HTML, SQL, shell, URLs, logs)?
- Does every action that changes data check the user may do it, on that
  specific record, not just that they are signed in?
- Could a user reach another user's record by changing an ID?
- Are secrets read from configuration, never written into code, logs or
  error messages?
- Are file uploads checked for type and size, and stored outside the web
  root?
- Are new dependencies necessary, maintained and free of known advisories?

## Reliability

- What happens when an outside call times out, fails or returns nonsense?
- Do related writes happen together or not at all (a transaction or its
  equivalent)?
- If a background job runs twice, is the result still correct?
- Can two requests at the same moment corrupt shared state?
- Are errors logged with enough context to diagnose, and shown to users in
  plain words?
- Do edge values behave: empty, zero, negative, very large, missing,
  non-ASCII text?

## Performance

- Does any query or outside call run once per item in a loop?
- Do new queries filter and sort on indexed columns?
- Is any result set unbounded (no limit, no pagination)?
- Is slow work (emails, exports, image processing) done in the background?
- Is anything cached, and is the cache cleared when the data changes?

## Upkeep

- Do names say what things are and do?
- Is new logic in the layer where the project puts that kind of logic?
- Is anything duplicated that already exists elsewhere in the codebase?
- Would the tests fail if the new behaviour broke?
- Is there dead code, commented-out code or a leftover debug statement?

## Data and migrations

- Can the migration run on a large table without locking it for long?
- Can the previous release still run against the new schema during a
  deploy?
- Is there a way back if the migration has to be reversed?
