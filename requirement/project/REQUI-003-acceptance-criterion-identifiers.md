---
requirement_id: REQUI-003
scope: project
subject: acceptance-criterion-identifiers
status: active
---

# Acceptance Criterion Identifiers

Acceptance criteria MUST derive their identifier from the containing requirement identifier and extend it with `-ACC-###`.

## Format

`<requirement_id>-ACC-###`

## Acceptance criteria

- **REQUI-003-ACC-001** — Every acceptance criterion has a stable identifier.
- **REQUI-003-ACC-002** — The identifier starts with the containing requirement ID.
- **REQUI-003-ACC-003** — The identifier ends with a three-digit sequential `-ACC-###` suffix.
- **REQUI-003-ACC-004** — Acceptance criterion identifiers remain stable when the requirement filename or wording changes.
