# Task kinds

A rough guide for step 3 when a task does not map cleanly onto a single
skill description. Judge from the catalogue's actual skill list each time;
not every skill named here exists in every library, and new ones may have
been added since this table was written.

| Kind | Tends to need | Rarely needs |
|---|---|---|
| Design | prototyping and interface-sketching skills, the project's front-end stack skill | test-writing, pull-request skills |
| Build | the stack's scaffolding or component skills, a test-writing skill | interface-sketching, changelog skills |
| Review | the review skill, a security-hardening skill, the stack's test skill | scaffolding, prototyping |
| Ship | pull-request and git-workflow skills, a changelog skill | design and prototyping skills |
| Docs | plain-English rewriting, documentation-sync skills | build and ship skills |
| Debugging | a triage or root-cause skill, the stack's test skill | design and ship skills |

A task touching authentication, payments or stored secrets usually wants a
security-hardening or threat-modelling skill whatever the kind above. A
mixed task (for example "build the feature and open the pull request") takes
the union of its rows rather than forcing one kind.

When a task names a specific framework or platform in the stack signals
(a Laravel install, a Nuxt front end, a Tauri desktop shell), prefer that
stack's own skill over a generic one with similar wording, and only when
the catalogue's stack signals actually show that framework in use.
