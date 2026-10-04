---
name: Single-Source Relation Rule
scope: system
kind: architecture
status: active
---

# Single-Source Relation Rule

Relations between glossary terms have one canonical source. A relation MUST NOT be duplicated in both term files.

## Storage

- Store each relation as one Markdown file under `relation/<scope>/`.
- Give the relation file YAML frontmatter containing `from`, `relation`, and `to`.
- Cross-scope relations MUST include `from_scope` and `to_scope`.
- Keep term files responsible only for their own definitions and metadata.

## Direction

- Store directional relations once, such as `component --broader--> part`.
- Store `has` relations once, such as `code --has--> checksum`.
- Infer their inverse when needed: `checksum --part_of--> code`.
- Infer the inverse when needed: `part --narrower--> component`.
- Store inheritance relations once, such as `code --inherits_from--> artifact`.
- Infer the inverse when needed: `artifact --inherited_by--> code`.
- Store symmetric `related` relations once using a stable filename order.

## Integrity

- Both referenced term files MUST exist.
- A relation MUST NOT reference the same term on both sides.
- A relation type MUST be defined before use.
- Relation changes MUST update only the canonical relation file.
