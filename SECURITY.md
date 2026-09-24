# Security

Some skills here run shell commands, register hooks or write files on the
machine that uses them. If you find a way a skill could be made to do
something harmful (running unexpected commands, leaking secrets, writing
outside the project), please report it privately rather than opening a
public issue.

## Reporting

Use GitHub's private vulnerability reporting on this repository (the
**Security** tab, then **Report a vulnerability**). Include the skill, what
an attacker would need to control, and the steps to reproduce.

You can expect an acknowledgement within a week, and a fix or a plan within
a month for confirmed issues.

## Using skills safely

- Read a skill before linking it, as you would any script you run.
- Skills with hooks (`careful`, `freeze`) run their own scripts before tool
  calls; review those scripts once.
- Skills never need your secrets in their files. Keep credentials in your
  environment or a secret store.
