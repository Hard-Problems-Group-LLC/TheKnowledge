# Obsolete Or Superseded Proposal Lifecycle State

| Field | Value |
| --- | --- |
| Title | Obsolete Or Superseded Proposal Lifecycle State |
| Author | Codex |
| Date | 2026-05-02T00:42:40-07:00 |
| Status | Under Review |
| Reviewers | Matt Heck, repository maintainer/operator; AI maintainers |
| Related Work | `internal/overrides/proposals/under-review/imported-ecrs/2026-04-22-proposal-obsolete-lifecycle-state.md`; `standards-and-practices/docs/specifications/status_subdirectories_for_proposals_and_bugs.txt`; `standards-and-practices/docs/format-for-proposals.md` |

## Problem Statement
The current proposal lifecycle directories do not cleanly represent a record
that was reasonable when written but is no longer actionable because later
architecture or implementation superseded its assumptions. Leaving such a
record in `approved/` makes the queue misleading, while `rejected/` or
`deferred/` can say the wrong thing.

## Goals
- Decide whether TheKnowledge should add a narrow `obsolete/` or
  `superseded/` proposal lifecycle state.
- Keep `approved/` limited to still-actionable approved work.
- Preserve traceability when a proposal is historically relevant but no
  longer executable as written.

## Non-Goals
- Creating a dumping ground for vague or low-priority work.
- Replacing `deferred/`, `rejected/`, or `approved/` for their normal uses.

## Use Cases
1. A historical proposal was partially absorbed by later work and should no
   longer appear as executable approved scope.
2. A repository needs a traceable archival state without pretending the old
   proposal was rejected on its merits.

## Constraints And Assumptions
- The state should be rare and explicitly justified.
- Any added directory must stay aligned across docs, starter templates, and
  tests.

## Proposed Approach
Evaluate whether TheKnowledge should add one rare proposal lifecycle state for
obsolete or superseded records. If adopted, the state should:

- require a short supersession rationale;
- remain rare and explicitly documented as such; and
- move source and any rendered companions together.

When this proposal reaches a final disposition, move the originating
consuming-project ECR into `ECRs/TheKnowledge/closed/` with a note pointing
to this proposal or the resulting lifecycle decision.

## Risks And Mitigations
- Risk: maintainers misuse the state instead of making a harder decision.
  Mitigation: require explicit rationale and warn that the state is rare.

## Testing And Validation
- Add doc and index-generation coverage if a new lifecycle directory is
  approved.

## Alternatives Considered
1. Continue using `approved/` for superseded work.
   Rejected because it weakens queue signal.
2. Reuse `deferred/` or `rejected/`.
   Rejected because both can misstate intent.

## Open Questions
1. Should the directory be named `obsolete/` or `superseded/`?
2. Should starter templates add the directory immediately or only after a
   real repository use case exists?

## Milestones
1. Decide whether the extra lifecycle state is justified.
2. Update docs, templates, and tests if approved.

## Adoption And Rollout
If approved, land the lifecycle addition with matching doc and test updates in
one change.

## Decision Log
- 2026-05-02T00:42:40-07:00 - Promoted the imported obsolete-lifecycle ECR
  into one actionable TheKnowledge proposal.
