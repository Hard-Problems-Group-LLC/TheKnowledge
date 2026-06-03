# Accepted ECR List

This file lists imported ECR filenames that TheKnowledge has accepted,
implemented, or otherwise resolved. External projects can compare this list
against their own submitted ECR filenames without TheKnowledge recording the
source project name.

Keep entries ordered with the newest resolution first. Use the imported ECR
filename as the durable source-facing identifier. If two imported ECRs collide
on filename, ask the operator for a disambiguation strategy before renaming
or merging records.

## Accepted and Implemented
- `2026-04-22-testing-mock-standards.md`
  Resolution date: 2026-05-08.
  Notes: resolved by the approved mock-use testing standard, including
  guidance to prefer real local implementations, fixtures, and fakes before
  mocks, and to pair important mocked behavior with real-path coverage.
- `2026-04-22-cross-project-change-confirmation.md`
  Resolution date: 2026-05-08.
  Notes: resolved by the approved session-continuity and project-boundary
  guidance requiring explicit current-session confirmation before mutating
  outside the active project root.
- `2026-04-11-collision-resume-session-continuity.md`
  Resolution date: 2026-05-08.
  Notes: resolved by the approved session-continuity and project-boundary
  guidance preserving the literal `collision resume` directive and its
  operational meaning.
- `2026-04-16-codex-wrangler-pragmatic-edit-method-policy.md`
  Resolution date: 2026-05-08.
  Notes: resolved by the approved pragmatic edit-method policy that separates
  edit safety from edit transport and permits named-file or scripted edits
  for appropriate whole-file, generated, or mechanical changes.
- `pragmatic-edit-method-policy.md`
  Resolution date: 2026-05-08.
  Notes: duplicate edit-method topic resolved with the same pragmatic
  edit-method policy implementation.
- `2026-04-16-codex-wrangler-changelog-sop-and-pending-queue-preservation.md`
  Resolution date: 2026-05-08.
  Notes: resolved by the approved changelog and pending-queue preservation
  guidance, which keeps the queue short lived and recommends `CHANGELOG.md`
  for repositories with durable release or operator-history needs.
- `changelog-sop-and-pending-queue-preservation.md`
  Resolution date: 2026-05-08.
  Notes: duplicate changelog topic resolved with the same changelog and
  pending-queue preservation implementation.
- `update-helper-omits-install-entrypoints.txt`
  Resolution date: 2026-05-02.
  Notes: resolved by the consuming-project validation and wrapper contract
  implementation, including managed `.gitignore` refresh coverage and starter
  entrypoint refresh guidance.
- `standardized-commit-helper-wrapper-contract-drift.md`
  Resolution date: 2026-05-02.
  Notes: resolved by the consuming-project validation and wrapper contract
  implementation, including vendored helper-path resolution and public wrapper
  contract guidance.
- `2026-04-22-tool-environment-surprise-interrupt-standard.md`
  Resolution date: 2026-05-02.
  Notes: resolved by the consuming-project validation and wrapper contract
  implementation and related guidance updates that treat wrong-runtime and
  wrong-authority discoveries as interrupt-class conditions.
- `2026-04-22-knack-cache-path-and-ignore-guidance.md`
  Resolution date: 2026-05-02.
  Notes: resolved by Git-aware cache handling with `.cache/` fallback and
  corresponding documentation updates.
- `2026-04-22-consuming-project-steady-state-validation-guidance.md`
  Resolution date: 2026-05-02.
  Notes: resolved by the managed runtime-policy contract for consuming-project
  validation entrypoints.
- `2026-04-16-codex-wrangler-standardized-commit-helper-wrapper-contract-drift.md`
  Resolution date: 2026-05-02.
  Notes: duplicate wrapper-contract topic resolved with the same consuming-
  project validation implementation.
- `2026-04-11-consuming-repo-safe-timeout-wrapper-and-tripwire-controls.md`
  Resolution date: 2026-05-02.
  Notes: resolved by the consuming-project validation and wrapper contract
  implementation, including vendored helper resolution and safe non-Git cache
  behavior.
- `coding-and-documentation-standards-ecr.md`
  Resolution date: 2026-03-30.
  Notes: strengthened TheKnowledge's documentation and Python-version
  guidance.
- `ecr-directory-structure-for-read-only-upstream-feedback.md`
  Resolution date: 2026-03-30.
  Notes: added structured ECR intake guidance for read-only upstream
  feedback.
- `python-bootstrap-and-context-strategy-ecr.md`
  Resolution date: 2026-03-30.
  Notes: added the managed bootstrap/context strategy and starter behavior.
