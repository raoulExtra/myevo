---
name: Documentation Metadata Rule
scope: system
kind: documentation
status: active
---

# Documentation Metadata Rule

Every system or project document MUST identify what it documents and which shared rules and terms it uses.

## Required metadata

- `document_id`: stable unique identifier.
- `subject_type`: `system`, `project`, or `component`.
- `subject`: name of the documented subject.
- `scope`: `system` or `project`.
- `status`: `draft`, `active`, or `archived`.

## Optional metadata

- `terms`: glossary terms used by the document.
- `rules`: system rules that govern the document.
- `source`: canonical source location.

Documentation stores the subject description. The glossary stores term definitions. The rule directory stores governing rules. Do not duplicate those definitions in the document.
