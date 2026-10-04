---
requirement_id: REQUI-001
scope: project
subject: project-folder-verification
status: active
command: python cli.py verify
---

# Verify Project Folder

The project MUST provide a read-only verification command for its Markdown records.

## Acceptance criteria

- **REQUI-001-ACC-001** — `python cli.py verify` verifies the current project folder.
- **REQUI-001-ACC-002** — Action records under `action/` MUST have `name`, `kind`, and `status` metadata.
- **REQUI-001-ACC-003** — The command checks required folders and Markdown frontmatter.
- **REQUI-001-ACC-004** — Relation records MUST use `RELA-*` identifiers and reference existing terms.
- **REQUI-001-ACC-005** — Decision records MUST use `DECI-*` identifiers.
- **REQUI-001-ACC-006** — Completed decisions MUST be under `decision/<scope>/DONE/` with `status: done`.
- **REQUI-001-ACC-007** — The command exits successfully only when no verification errors are found.
- **REQUI-001-ACC-008** — `python cli.py verify --verbose` reports filesystem operations and content checks without modifying files.
