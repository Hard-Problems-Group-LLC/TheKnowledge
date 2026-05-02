# ECR: Add Mock-Use Testing Standards To TheKnowledge

Status: Draft

Author: Codex

Date: 2026-04-22

Target: `TheKnowledge`

## Summary

Integrate a durable testing standard that explains when mocks are appropriate
and when they should be avoided. The standard should be explicit that
overusing mocks can create brittle, implementation-shaped tests and can be
especially risky in AI-driven coding, where an agent may satisfy mock-call
expectations without preserving real behavior.

## Source Guidance

Use `docs/specifications/testing-standards.md` in this repository as the
starting point. The local standard says:

- Prefer real local implementations when they are deterministic, cheap, and
  safe.
- Prefer deterministic fixtures or fakes before dynamic mocks.
- Reserve mocks for narrow external or hard-to-trigger boundaries.
- Pair important mocked behavior with real integration, contract, smoke, or
  browser coverage.
- Avoid mocking owned application logic inside integration tests.
- Review mocked tests for durable behavior assertions rather than incidental
  call-count assertions.

## Proposed TheKnowledge Changes

Add this guidance to TheKnowledge as one or both of:

- a dedicated standards document under
  `standards-and-practices/docs/testing/`;
- a concise rule and cross-reference in
  `standards-and-practices/docs/development-workflow.txt`.

The result should be reusable across consuming repositories and should fit
TheKnowledge's existing testing expectations: pessimistic coverage, edge
cases, failure modes, reusable fixtures, and scripted smoke checks.

## Rationale

Mocks are useful engineering tools, but excessive mocking weakens confidence
in tests. Integration tests that replace internal collaborators with mocks can
miss broken wiring, schema drift, rendering failures, filesystem problems, and
real command handling. The risk is amplified when AI agents use tests as the
main behavioral signal because call-shaped mock tests can reward code that
does not work in the real system.

## Acceptance Criteria

- TheKnowledge documents when mocks are appropriate.
- TheKnowledge documents when mocks are inappropriate.
- The guidance distinguishes unit, integration, and smoke/browser tests.
- The guidance recommends real-path coverage for important mocked behavior.
- The guidance encourages deterministic fakes and fixtures before mocks.

## Notes

This is an ECR rather than a direct submodule edit to preserve the
less-disruptive TheKnowledge change-control path adopted by this project.
