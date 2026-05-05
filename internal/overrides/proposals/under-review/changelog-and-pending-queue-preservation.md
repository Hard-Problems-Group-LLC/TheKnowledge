# Changelog And Pending-Queue Preservation

| Field | Value |
| --- | --- |
| Title | Changelog And Pending-Queue Preservation |
| Author | Codex |
| Date | 2026-05-02T00:42:40-07:00 |
| Status | Under Review |
| Reviewers | Matt Heck, repository maintainer/operator; AI maintainers |
| Related Work | `internal/overrides/proposals/under-review/imported-ecrs/changelog-sop-and-pending-queue-preservation.md`; `internal/overrides/proposals/under-review/imported-ecrs/2026-04-16-codex-wrangler-changelog-sop-and-pending-queue-preservation.md`; `scripts/git_standard_commit_push.py`; `internal/overrides/state/pending-commit-changes.txt` |

## Problem Statement
TheKnowledge already standardizes a short-lived pending-commit queue, but it
does not define a durable changelog story for repositories that need
operator-facing or release-facing change history. That leaves consuming
projects to invent ad hoc changelog workflows and makes it easy for useful
queue content to disappear after commit.

## Goals
- Define when TheKnowledge-based repositories should keep a changelog.
- Clarify the relationship between `pending-commit-changes.txt`,
  `completed-tasks.txt`, and `CHANGELOG.md`.
- Decide whether changelog preservation belongs in the standard helper or in
  a documented manual pre-commit step.
- Close the duplicate imported ECRs under one actionable proposal.

## Non-Goals
- Forcing every small internal repository to publish release notes.
- Replacing `completed-tasks.txt` or the pending-commit queue.
- Designing a complete release-automation pipeline.

## Use Cases
1. A consuming project wants durable user-visible change notes without
   discarding the existing queue-based commit-body workflow.
2. A maintainer wants one standard answer for whether notable pending-queue
   entries must be copied into `CHANGELOG.md` before commit.
3. TheKnowledge needs one top-level proposal instead of two duplicate
   imported ECRs on the same topic.

## Constraints And Assumptions
- Some repositories that use TheKnowledge have no release process and may not
  need a changelog.
- The current standardized helper already consumes and clears the pending
  queue after local commit.
- Any helper-driven changelog sync must remain reviewable and avoid guessing
  categories from arbitrary prose.

## Proposed Approach
Adopt one proposal that resolves the duplicate imported ECRs and chooses a
single changelog policy. The current preferred direction is:

- require a top-level `CHANGELOG.md` only for repositories with durable
  operator-facing or user-facing release history needs;
- standardize the baseline changelog format when a changelog exists;
- document that `pending-commit-changes.txt` is short-lived commit-body
  input, not the durable history source; and
- either add an explicit helper path for changelog sync or define a required
  manual step before `ACP`.

When this proposal reaches a final disposition, move the originating
consuming-project ECRs that fed it into `ECRs/TheKnowledge/closed/` with a
note pointing back to this proposal or the resulting implementation.

## Risks And Mitigations
- Risk: mandatory changelogs add noise in repositories that do not need them.
  Mitigation: scope changelog requirements to repositories with durable
  release-history needs.
- Risk: helper-driven changelog updates create low-signal or wrong sections.
  Mitigation: prefer explicit categories, reviewable diffs, and opt-in helper
  behavior.

## Testing And Validation
- Add or update tests for starter guidance if the standard changelog policy
  changes managed files.
- Verify that queue-clearing behavior and changelog expectations are both
  documented in one place.

## Alternatives Considered
1. Keep the current queue-only model.
   Rejected because it leaves durable history undefined.
2. Require `CHANGELOG.md` everywhere.
   Rejected because some repositories do not need that overhead.

## Open Questions
1. Should changelog sync live inside the standard helper or in a separate
   wrapper?
2. Should the baseline changelog format follow Keep a Changelog exactly or a
   narrower local subset?

## Milestones
1. Choose the baseline changelog policy.
2. Update helper and starter guidance if needed.
3. Close the duplicate imported ECRs against the chosen outcome.

## Adoption And Rollout
If approved, update starter docs, managed guidance, and any helper behavior
in one pass so consuming projects inherit one clear rule.

## Decision Log
- 2026-05-02T00:42:40-07:00 - Promoted the duplicate imported changelog ECRs
  into one actionable TheKnowledge proposal.
