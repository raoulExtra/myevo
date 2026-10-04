---
name: Python Package Layout Rule
scope: system
kind: architecture
status: active
---

# Python Package Layout Rule

Python implementation code MUST be stored under `src/myevo/` and Python tests MUST be stored under `tests/`.

## Placement

- `src/myevo/` contains the importable `myevo` package and its implementation modules.
- `tests/` contains repeatable tests for package behavior.
- Repository-root Python files MAY be executable entry points, but MUST delegate implementation to `src/myevo/`.
- Tests MUST exercise observable behavior and MUST NOT merely repeat source text, wiring, or incidental formatting.

## Package requirements

- `src/myevo/__init__.py` identifies the package.
- Package modules contain their own required version metadata.
- Entry points and tests use the package modules rather than duplicating implementation.
