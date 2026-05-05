# Pragmatic Edit Method Policy

| Field | Value |
| --- | --- |
| Title | Pragmatic Edit Method Policy |
| Author | Codex |
| Date | 2026-05-02T00:42:40-07:00 |
| Status | Under Review |
| Reviewers | Matt Heck, repository maintainer/operator; AI maintainers |
| Related Work | `internal/overrides/proposals/under-review/imported-ecrs/pragmatic-edit-method-policy.md`; `internal/overrides/proposals/under-review/imported-ecrs/2026-04-16-codex-wrangler-pragmatic-edit-method-policy.md`; `AGENTS.md`; `templates/AGENTS-footer.md` |

## Problem Statement
TheKnowledge currently tends to treat one edit transport as the safety rule.
That is too rigid. Patch-style edits are valuable for small localized
changes, but a universal patch-only rule becomes counterproductive when the
edit shape is whole-file documentation, generated content, mechanical
multi-file work, or an environment where the patch helper itself is
unreliable.

## Goals
- Keep patch-style edits as the preferred default for small localized work.
- Permit safer alternatives for whole-file records and other non-localized
  changes.
- Preserve the real safety rules: scoped edits, diff review, validation, and
  protection of unrelated user work.
- Collapse the duplicate imported ECRs into one actionable proposal.

## Non-Goals
- Encouraging opaque one-liners that hide the affected file set.
- Removing diff review or validation requirements.
- Replacing existing user-change protection rules.

## Use Cases
1. A documentation-heavy update needs whole-file creation or replacement.
2. A mechanical multi-file transformation is safer as a small script or
   codemod than as dozens of hand-applied patches.
3. The patch helper fails in a particular environment and should not be
   retried indefinitely.

## Constraints And Assumptions
- Small localized edits still benefit from patch-style application.
- The project must keep a reviewable Git diff regardless of edit transport.
- Repo-local tool reliability should be remembered rather than rediscovered
  repeatedly by later sessions.

## Proposed Approach
Adopt a transport-neutral safety policy:

- prefer patch-style edits for small localized manual changes;
- allow explicit named-file writes or short scripts for whole-file records,
  generated content, and mechanical transformations;
- require `git diff` review and appropriate validation either way; and
- require repeated transport failure to be surfaced as a bug or local
  reliability note instead of retried endlessly.

When this proposal reaches a final disposition, move the originating
consuming-project ECRs that fed it into `ECRs/TheKnowledge/closed/` with a
note pointing back to this proposal or the resulting implementation.

## Risks And Mitigations
- Risk: broad wording invites sloppy direct edits.
  Mitigation: keep the policy explicit about named files, reviewable diffs,
  and unchanged protection rules.

## Testing And Validation
- Update guidance tests to ensure starter docs stop implying one mandatory
  edit transport for every manual change.

## Alternatives Considered
1. Keep a patch-only rule.
   Rejected because it conflates safety with transport.
2. Allow any edit transport without guidance.
   Rejected because the safe use cases still need explicit boundaries.

## Open Questions
1. Should TheKnowledge formalize a local reliability record path for flaky
   transports?

## Milestones
1. Approve the policy.
2. Update agent guidance and tests.
3. Close the duplicate imported ECRs.

## Adoption And Rollout
Land the guidance and test updates together so TheKnowledge and consuming
projects inherit the same policy.

## Decision Log
- 2026-05-02T00:42:40-07:00 - Promoted the duplicate imported edit-policy
  ECRs into one actionable TheKnowledge proposal.
