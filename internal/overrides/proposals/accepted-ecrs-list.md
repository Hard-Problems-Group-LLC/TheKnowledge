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
