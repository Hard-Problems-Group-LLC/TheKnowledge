# Proposal Format

## Purpose
Use this format for proposals that require discussion before a full
specification. Keep prose concise, active-voice, and Chicago-style. Wrap text
at 78 columns unless a Markdown table or similar structure requires a wider
line. Use 118 columns for those structures when practical.

Store proposal records as Markdown (`.md`) files. Existing legacy proposal
records should be converted before substantive edits unless an operator
explicitly defers that migration.

## Header
Include the following metadata at the top:

| Field | Meaning |
| --- | --- |
| Title | A short, user-recognizable name. |
| Author | The primary drafter. |
| Date | ISO 8601 timestamp of authorship. |
| Status | Under Review, Approved, Rejected, or Deferred. |
| Reviewers | Names and roles of expected reviewers. |
| Related Work | Links to backlog items, bugs, or specifications. |

Store each proposal file in the matching status directory under
`project-management/proposals/`: `under-review/`, `approved/`, `rejected/`,
or `deferred/`.

## Problem Statement
Describe the user-facing problem and why current behavior is insufficient.
Note affected personas, environments, and measurable pain points.

## Goals
List the concrete outcomes the proposal must achieve. Keep each goal concise
and testable.

## Non-Goals
List items explicitly out of scope to prevent scope creep.

## Use Cases
Summarize representative scenarios that the solution must satisfy. Tie them to
users and environments.

## Constraints and Assumptions
Call out platform constraints, performance budgets, compatibility targets, and
assumptions that shape the design.

## Proposed Approach
Outline the intended solution. Break down major components, data flows, and
notable algorithms. Note observability, diagnostics, and operational support.

## Risks and Mitigations
Identify technical, operational, and usability risks. Pair each risk with
mitigations or fallbacks.

## Testing and Validation
Describe how the proposal will be validated: test strategy, fixtures,
benchmarks, and manual verification. Reference Joel Spolsky's guidance on
shipping only after thorough testing.

## Alternatives Considered
List competing options and why they were rejected.

## Open Questions
Enumerate unresolved questions with owners and expected decision dates.

## Milestones
Lay out deliverables with dates, owners, and dependencies. Include entry and
exit criteria per milestone.

## Adoption and Rollout
Explain rollout sequencing, compatibility plans, and user communication.

## Decision Log
Reserve space to capture accepted changes during review.
