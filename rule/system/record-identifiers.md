---
name: Record Identifier Rule
scope: system
kind: naming
status: active
---

# Record Identifier Rule

Stable identifiers are required for records that may be referenced by other files.

## Prefixes

- `RELA-###` identifies a glossary relation.
- `DECI-###` identifies a decision.
- `REQUI-###` identifies a project requirement.
Completed decisions MUST be stored under `decision/<scope>/DONE/`.

Identifiers are unique within their record type, remain stable after renaming, and appear in YAML frontmatter. Filenames SHOULD include the identifier and a readable slug.
