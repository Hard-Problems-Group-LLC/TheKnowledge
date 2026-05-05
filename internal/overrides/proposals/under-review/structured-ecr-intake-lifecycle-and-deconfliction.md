# Structured ECR Intake Lifecycle And Deconfliction

| Field | Value |
| --- | --- |
| Title | Structured ECR Intake Lifecycle And Deconfliction |
| Author | Codex |
| Date | 2026-05-02T00:49:43-07:00 |
| Status | Under Review |
| Reviewers | Matt Heck, repository maintainer/operator; AI maintainers |
| Related Work | `internal/overrides/proposals/under-review/replace-feedback-branch-with-feedback-ecrs-intake.md`; `internal/overrides/proposals/under-review/imported-ecrs/ecr-directory-structure-for-read-only-upstream-feedback.md`; `internal/overrides/proposals/under-review/imported-ecrs/deconfliction-map.md`; `standards-and-practices/docs/specifications/read_only_upstream_ecr_directory_structure.txt`; `standards-and-practices/docs/specifications/theknowledge_submodule_workflows.txt` |

## Problem Statement
TheKnowledge now has two separate intake pressures that are related but not
yet governed by one lifecycle. Consuming projects need a standard local place
to draft upstream requests when their active `TheKnowledge/` checkout is
read-only. Separately, writable TheKnowledge maintenance needs a clean way to
import those raw ECRs, deconflict duplicates, promote actionable work into
top-level proposals, and record when the original source ECRs are resolved.

The current flat `ECRs/TheKnowledge/` convention is an improvement over ad
hoc notes, but it does not say when a request is merely drafted, actively
under upstream handling, or fully resolved. The raw imported intake under
`internal/overrides/proposals/under-review/imported-ecrs/` has the same
problem.

## Goals
- Define one status-based lifecycle for consuming-project ECR directories.
- Define how raw imported ECRs are deconflicted into top-level actionable
  TheKnowledge proposals.
- Require closure notes that point from the source ECR to the TheKnowledge
  record that resolved it.
- Keep branch-policy questions related but separable from directory lifecycle
  questions.

## Non-Goals
- Forcing every cross-project note through one specific Git branch.
- Deleting raw imported ECRs immediately after promotion.
- Replacing TheKnowledge's normal proposal, backlog, or bug records.

## Use Cases
1. A consuming project drafts a TheKnowledge change request before it can be
   carried into a writable upstream checkout.
2. A writable TheKnowledge checkout imports multiple ECRs on overlapping
   topics and needs to promote them into a smaller actionable proposal set.
3. An operator wants to know which local ECRs are still open, which are in
   flight upstream, and which are closed.

## Constraints And Assumptions
- Source-project names should not appear in tracked TheKnowledge prose.
- Consuming projects may have read-only TheKnowledge submodules and writable
  parent repositories.
- Some imported ECRs duplicate each other or map cleanly onto existing
  top-level proposals.

## Proposed Approach
Adopt a structured lifecycle centered on the existing `ECRs/TheKnowledge/`
subtree:

- draft new local upstream requests under `ECRs/TheKnowledge/open/`;
- move them to `ECRs/TheKnowledge/in-progress/` when active upstream handling
  begins or when the request is imported into a writable TheKnowledge
  checkout; and
- move them to `ECRs/TheKnowledge/closed/` once an upstream proposal,
  implementation, rejection, or deferral record exists.

Inside TheKnowledge itself:

- keep `internal/overrides/proposals/under-review/imported-ecrs/` as the raw
  neutral intake inbox;
- promote actionable work into top-level proposals under
  `internal/overrides/proposals/under-review/`;
- maintain a deconfliction map that records which raw ECRs feed which
  top-level proposal; and
- when a source ECR is fully dealt with, require a closure note in the
  originating `ECRs/TheKnowledge/closed/` record that points to the
  top-level proposal, accepted-ECR entry, commit, or rejection/deferral note
  that resolved it.

## Risks And Mitigations
- Risk: maintainers keep using the raw intake directory as the actionable
  queue.
  Mitigation: document the distinction clearly and keep the deconfliction map
  current.
- Risk: closed ECRs lose the trail back to the TheKnowledge record.
  Mitigation: require closure notes with explicit references.

## Testing And Validation
- Update starter-scaffolding tests for the new `open/`, `in-progress/`, and
  `closed/` ECR layout.
- Update doc-wiring tests for the ECR lifecycle guidance and deconfliction
  language.

## Alternatives Considered
1. Keep the flat `ECRs/TheKnowledge/` directory.
   Rejected because it does not expose lifecycle state.
2. Use only Git branch state without local ECR status directories.
   Rejected because many requests are drafted before a writable upstream
   session is active.

## Open Questions
1. Should the current `Feedback` branch survive, be renamed, or be retired
   after the directory lifecycle is in place?
2. Should raw imported ECRs gain their own archive or closure subtree later,
   or is the deconfliction map sufficient?

## Milestones
1. Approve the ECR lifecycle and deconfliction model.
2. Update docs, starter scaffolding, and tests.
3. Reconcile the branch-policy proposal against the approved lifecycle.

## Adoption And Rollout
Land the directory-structure, doc, and test updates together. Then resolve
the narrower branch-policy question with the clearer lifecycle already in
place.

## Decision Log
- 2026-05-02T00:49:43-07:00 - Promoted the imported ECR-directory-structure
  request into a broader lifecycle and deconfliction proposal.
