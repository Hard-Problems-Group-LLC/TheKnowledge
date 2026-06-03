# Testing Mock Standards

| Field | Value |
| --- | --- |
| Title | Testing Mock Standards |
| Author | Codex |
| Date | 2026-05-02T00:42:40-07:00 |
| Status | Approved |
| Reviewers | Matt Heck, repository maintainer/operator; AI maintainers |
| Related Work | `internal/overrides/proposals/under-review/imported-ecrs/2026-04-22-testing-mock-standards.md`; `standards-and-practices/docs/development-workflow.txt` |

## Problem Statement
TheKnowledge's testing guidance is strong on pessimistic coverage and failure
mode thinking, but it does not currently say enough about when mocks are
appropriate and when they become brittle. That gap matters more in AI-driven
development, where call-shaped mocked tests can reward implementation-shaped
code that fails on the real integration path.

## Goals
- Define when mocks are appropriate and when they are not.
- Prefer deterministic fixtures and fakes before mocks where feasible.
- Require important mocked behavior to keep some real-path coverage.
- Turn the imported testing ECR into a top-level actionable proposal.

## Non-Goals
- Banning mocks outright.
- Replacing the broader testing-standards work in consuming projects.

## Use Cases
1. A repository needs clear guidance for unit, integration, and smoke tests.
2. An AI maintainer is deciding whether to mock owned collaborators or use a
   deterministic fake.

## Constraints And Assumptions
- Some boundaries really are expensive or unsafe enough to require mocks.
- The guidance must remain generic enough for multiple languages and testing
  stacks.

## Proposed Approach
Add a reusable testing standard that says:

- prefer real local implementations when they are deterministic, cheap, and
  safe;
- prefer fixtures and fakes before dynamic mocks;
- reserve mocks for narrow external or hard-to-trigger boundaries; and
- pair important mocked behavior with real integration, contract, smoke, or
  browser coverage.

When this proposal reaches a final disposition, move the originating
consuming-project ECR into `ECRs/TheKnowledge/closed/` with a note pointing
back to this proposal or the resulting implementation.

## Risks And Mitigations
- Risk: the guidance becomes too language- or framework-specific.
  Mitigation: keep the standard principle-based and cross-reference more
  detailed local docs only when needed.

## Testing And Validation
- Add doc-wiring coverage for the new mock-use standard if approved.

## Alternatives Considered
1. Leave mocks implicit in the general testing rules.
   Rejected because AI-driven maintenance benefits from a clearer signal.

## Open Questions
1. Should the standard live in a dedicated testing document or a shorter
   cross-reference from `development-workflow.txt`?

## Milestones
1. Approve the standard.
2. Add the guidance and tests.
3. Close the imported ECR.

## Adoption And Rollout
Land the new testing guidance in both TheKnowledge and starter docs so
consuming repositories inherit the same baseline.

## Decision Log
- 2026-05-02T00:42:40-07:00 - Promoted the imported testing-mocks ECR into
  one actionable TheKnowledge proposal.
- 2026-05-08T11:01:07-07:00 - Approved by the operator for implementation as
  part of the client-focused imported-ECR integration pass.
- 2026-05-08T11:03:32-07:00 - Implemented by adding the mock-use testing
  specification, reusable testing standard, direct guidance, managed
  downstream guidance, and documentation test coverage.
