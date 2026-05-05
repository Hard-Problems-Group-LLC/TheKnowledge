# Session Continuity And Cross-Project Boundary Guards

| Field | Value |
| --- | --- |
| Title | Session Continuity And Cross-Project Boundary Guards |
| Author | Codex |
| Date | 2026-05-02T00:42:40-07:00 |
| Status | Under Review |
| Reviewers | Matt Heck, repository maintainer/operator; AI maintainers |
| Related Work | `internal/overrides/proposals/under-review/imported-ecrs/2026-04-11-collision-resume-session-continuity.md`; `internal/overrides/proposals/under-review/imported-ecrs/2026-04-22-cross-project-change-confirmation.md`; `AGENTS.md` |

## Problem Statement
Two operator-safety issues surfaced in imported ECRs and they reinforce each
other. First, a replacement session can resume the wrong stale context when
multiple remote or Codex sessions exist for one workspace. Second, a session
can infer that a requested change belongs to another repository and mutate it
without an explicit cross-project confirmation in the current session. Both
cases need stronger boundary rules.

## Goals
- Preserve the `collision resume` continuity rule as a durable standard.
- Require explicit cross-project confirmation before mutating outside the
  active project root.
- Encourage active-writer detection when crossing project boundaries.
- Collapse the two related imported ECRs into one actionable proposal.

## Non-Goals
- Blocking read-only inspection needed to discover project ownership.
- Preventing explicitly authorized cross-project work.
- Replacing other escalation or sandbox approval rules.

## Use Cases
1. An operator reconnects from another machine and the newest session is not
   the correct one to resume.
2. A user sends a change request to the wrong terminal tab and the requested
   target belongs to another active project.

## Constraints And Assumptions
- Operators often work across multiple terminals, editor panes, and Codex
  sessions at once.
- Some cross-project changes are legitimate, but they need intent-level
  confirmation rather than inference.

## Proposed Approach
Promote both safeguards together:

- preserve `collision resume` and its non-compressible operational meaning in
  managed guidance; and
- add a cross-project boundary rule that requires explicit confirmation in
  the current session before mutating another project, service, or deployment
  surface.

When this proposal reaches a final disposition, move the originating
consuming-project ECRs that fed it into `ECRs/TheKnowledge/closed/` with a
note pointing back to this proposal or the resulting implementation.

## Risks And Mitigations
- Risk: the extra confirmation step feels slow during obvious cross-project
  work.
  Mitigation: permit bounded read-only inspection before asking and allow the
  operator to authorize the crossing explicitly.

## Testing And Validation
- Update managed guidance tests for `collision resume` and cross-project
  confirmation wording.

## Alternatives Considered
1. Keep the rules separate.
   Rejected because both are workspace-boundary safeguards and should be
   reviewed together.

## Open Questions
1. Should active-writer detection remain guidance or become a stronger
   requirement before cross-project edits?

## Milestones
1. Approve the combined safety rule.
2. Update guidance and tests.
3. Close the mapped imported ECRs.

## Adoption And Rollout
Land the wording changes in TheKnowledge and starter guidance together so the
same boundary rules propagate downstream.

## Decision Log
- 2026-05-02T00:42:40-07:00 - Promoted the session-continuity and
  cross-project-confirmation imported ECRs into one actionable proposal.
