---
name: Test-Driven Development Rule
scope: system
kind: testing
status: active
---

# Test-Driven Development Rule

Implementations MUST use test-driven development when the change has testable behavior or an observable acceptance criterion.

## Cycle

1. Write or update a failing test that expresses the intended behavior.
2. Implement the smallest change that makes the test pass.
3. Refactor while keeping the test passing.
4. Run the relevant tests and the project verification command before delivery.

## Applicability

Use TDD for executable behavior, interfaces, parsing, validation, state transitions, and other changes with repeatable observable outcomes.

For documentation-only, glossary-only, or structural Markdown changes without executable behavior, use the relevant verification checks instead. Do not create tests that only repeat file contents, wiring, or incidental formatting.
