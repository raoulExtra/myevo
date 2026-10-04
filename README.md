# myevo

`myevo` is a read-only Markdown project system for maintaining a controlled vocabulary and the records that govern a project.

## Purpose

The project stores glossary terms, rules, relations, decisions, requirements, and actions as Markdown records with YAML frontmatter. It keeps those records in one source-controlled project structure.

## Structure

- `glossary/` — system and project terms.
- `rule/` — rules governing records and project conventions.
- `relation/` — canonical relations between terms and records.
- `decision/` — recorded decisions, including completed decisions under `decision/<scope>/DONE/`.
- `requirement/` — project requirements and acceptance criteria.
- `action/` — reusable project actions.
- `src/myevo/` — importable Python package implementation.
- `tests/` — repeatable tests for executable behavior.
- `cli.py` — root entry point for project structure verification.
- `artifact_verify.py` — root entry point for executable artifact verification.
 
## Code placement

Executable implementation code is placed under `src/myevo/`. Root-level Python files are entry points only and delegate to the package.

Markdown records remain in their domain directories under `glossary/`, `rule/`, `relation/`, `decision/`, `requirement/`, and `action/`.

## Test phases

Changes follow these phases:

1. **Plan** — define the intended change, affected records, acceptance criteria, and verification steps.
2. **Implement** — update the required code or Markdown records.
3. **Test** — run checks relevant to the changed behavior.
4. **Verify** — run `python cli.py verify` and confirm the project structure and records are valid.
5. **Commit** — commit the reviewed, verified change.

The `test` phase does not replace the `verify` phase; they cover different risks.
 
For executable changes, the test phase uses TDD and checks that the embedded version increases relative to the previous Git revision.

## Verification

Run the project structure verification from the repository root:

```bash
python cli.py verify
```

Show filesystem operations and content checks:

```bash
python cli.py verify --verbose
```

Verify executable artifact metadata and checksums:

```bash
python artifact_verify.py
```
 
Run the test suite:
 
```bash
python -m unittest discover -s tests -v
```
 
Checksum values remain required and format-checked, but checksum content verification is temporarily disabled.

The verification commands are read-only and do not modify project files.
