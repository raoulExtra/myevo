---
decision_id: DECI-001
scope: system
subject: glossary-relations
status: done
date: 2026-10-04
---

# Single-Source Relation Files

## Decision

Store each glossary relation as one Markdown file under `relation/<scope>/`.

## Reason

Duplicating a relation in both term files creates a consistency risk. One canonical relation file avoids conflicting updates.

## Consequences

- Relation files use `RELA-*` identifiers.
- Term files remain focused on definitions and metadata.
- Inverse relations are inferred rather than duplicated.
- Relation endpoints can be validated independently.

## Alternatives considered

- Store relations in both term files.
- Store relations in a database.
