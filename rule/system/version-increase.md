---
name: Version Increase Rule
scope: system
kind: versioning
status: active
---

# Version Increase Rule

When an executable artifact changes, its embedded semantic version MUST increase relative to the version in the previous Git revision.

## Enforcement

- Use `MAJOR.MINOR.PATCH` version format.
- A changed executable with an equal or lower version MUST fail artifact verification.
- A new executable MUST contain version metadata.
- An unchanged executable does not require a version change.
- Documentation-only changes do not require executable version changes.
