---
requirement_id: REQUI-002
scope: project
subject: executable-artifact-verification
status: active
command: python artifact_verify.py
---

# Verify Executable Artifacts

Every executable code file MUST contain its own version, version date, and checksum metadata.

## Acceptance criteria

- **REQUI-002-ACC-001** — `python artifact_verify.py` scans executable code in the project folder.
- **REQUI-002-ACC-002** — Each executable code file contains exactly one embedded artifact metadata set.
- **REQUI-002-ACC-003** — Each metadata set contains `version`, `version-date`, and `checksum`.
- **REQUI-002-ACC-004** — The checksum matches the canonical file contents, excluding the checksum value itself.
- **REQUI-002-ACC-005** — The command exits nonzero when metadata is missing or stale.
- **REQUI-002-ACC-006** — `python artifact_verify.py --version` shows the path, version, version date, and checksum for every executable code file.
- **REQUI-002-ACC-007** — `python artifact_verify.py --verbose` shows each verification step for every executable code file.
- **REQUI-002-ACC-008** — `python artifact_verify.py --verbose` reports filesystem scanning, file discovery, file reads, checksum reads, and that no files are modified.
