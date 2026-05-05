# Consuming-Project Validation And Wrapper Contracts

| Field | Value |
| --- | --- |
| Title | Consuming-Project Validation And Wrapper Contracts |
| Author | Codex |
| Date | 2026-05-02T00:42:40-07:00 |
| Status | Approved |
| Reviewers | Matt Heck, repository maintainer/operator; AI maintainers |
| Related Work | `internal/overrides/proposals/approved/theknowledge-tool-runtime-isolation-and-bootstrap-reliability.md`; `internal/overrides/proposals/approved/project-root-dot-local-for-local-operator-state-and-tooling.md`; `internal/overrides/proposals/under-review/imported-ecrs/2026-04-11-consuming-repo-safe-timeout-wrapper-and-tripwire-controls.md`; `internal/overrides/proposals/under-review/imported-ecrs/2026-04-16-codex-wrangler-standardized-commit-helper-wrapper-contract-drift.md`; `internal/overrides/proposals/under-review/imported-ecrs/standardized-commit-helper-wrapper-contract-drift.md`; `internal/overrides/proposals/under-review/imported-ecrs/2026-04-22-consuming-project-steady-state-validation-guidance.md`; `internal/overrides/proposals/under-review/imported-ecrs/2026-04-22-tool-environment-surprise-interrupt-standard.md`; `internal/overrides/proposals/under-review/imported-ecrs/2026-04-22-knack-cache-path-and-ignore-guidance.md`; `internal/overrides/proposals/under-review/imported-ecrs/update-helper-omits-install-entrypoints.txt` |

## Problem Statement
TheKnowledge's consuming-project validation story is split across too many
partial contracts. Runtime selection, wrapper entrypoints, timeout-wrapper
path resolution, cache placement, and managed refresh behavior each have
their own raw intake ECRs. The result is the same class of breakage in
multiple forms: consuming projects cannot reliably tell which command family
is authoritative, which runtime should own validation, or which generated
paths are safe in non-Git and submodule-heavy environments.

## Goals
- Define one coherent consuming-project validation contract.
- Make runtime selection explicit and interrupt on wrong-runtime surprises.
- Resolve helper-script paths and cache locations safely in vendored or
  non-Git contexts.
- Ensure managed starter refresh helpers install the same entrypoints the
  docs promise.
- Replace the overlapping imported ECR pile with one actionable proposal.

## Non-Goals
- Replacing direct-checkout TheKnowledge runtime-isolation work.
- Forcing every consuming project to use one packaging tool or one exact
  wrapper filename.
- Eliminating narrow project-local validation helpers where they are useful.

## Use Cases
1. A consuming project wants one declared validation entrypoint rather than
   ambient `python ...` examples.
2. A maintainer needs wrapper behavior that remains correct when TheKnowledge
   is vendored below another repository root.
3. A non-Git or pre-Git consuming project needs safe validation caches that
   do not create fake `.git/` state.
4. A submodule updater should refresh the same starter entrypoints that the
   docs and drift report name.

## Constraints And Assumptions
- Some consuming projects are no-VCS or pre-Git during early bootstrap.
- Some consuming projects need repo-local validation helpers rather than raw
  vendored-script invocation.
- TheKnowledge already distinguishes bootstrap and steady-state runtimes in
  several places, but the consuming-project guidance is not yet consistent.

## Proposed Approach
Resolve the imported ECR cluster under one contract:

- require each consuming project to name one steady-state validation
  entrypoint and stop treating ambient `python` as authoritative by default;
- define wrong-runtime, wrong-scope, and wrong-authority discoveries as
  interrupt conditions that must be reported and corrected before clearance;
- make vendored helper resolution safe by either standardizing explicit
  repo-root wrappers or by resolving sibling helper scripts from the
  TheKnowledge checkout consistently;
- make validation caches Git-aware, with safe non-Git fallbacks such as
  `.cache/`;
- make the submodule updater refresh every managed starter entrypoint that
  the docs and drift report advertise; and
- keep all of that aligned with the direct-checkout runtime-isolation work
  rather than letting the two contracts drift apart.

When this proposal reaches a final disposition, move the originating
consuming-project ECRs that fed it into `ECRs/TheKnowledge/closed/` with a
note pointing back to this proposal or the resulting implementation.

## Risks And Mitigations
- Risk: this proposal is broader than one script fix.
  Mitigation: keep the implementation split into small helper, docs, and test
  milestones while preserving one contract document.
- Risk: managed wrappers and direct vendored-script invocation remain
  inconsistent.
  Mitigation: require the final approved approach to pick one supported
  public contract and test it end to end.

## Testing And Validation
- Add fixture coverage for non-Git, separate-git-dir, and submodule-style
  invocation paths.
- Add doc-wiring tests for runtime-selection and interrupt guidance.
- Add regression coverage for managed refresh of starter install entrypoints.

## Alternatives Considered
1. Fix each imported ECR independently.
   Rejected because the breakages all touch the same contract surface.
2. Leave consuming projects to choose their own local workaround.
   Rejected because TheKnowledge should provide the shared contract.

## Resolved Questions
1. The public consuming-project interface remains
   `python {{THEKNOWLEDGE_ROOT}}/scripts/run_tool_with_timeout.py ...` for
   direct validation calls and
   `python {{THEKNOWLEDGE_ROOT}}/scripts/run_quality_gate_cached.py --repo-root .`
   for cached quality-gate runs, with hook wrappers and repo-local wrapper
   fallbacks resolving through the TheKnowledge checkout when needed.
2. Cache paths stay Git-private when a real Git directory exists and fall
   back to project-visible ignored `.cache/` paths when a repository is
   pre-Git, non-Git, or otherwise lacks usable Git metadata.

## Milestones
1. Choose the public validation-entrypoint contract.
2. Update wrapper resolution, cache behavior, and managed refresh logic.
3. Update starter guidance and tests.
4. Close the mapped imported ECRs against the final outcome.

## Adoption And Rollout
Land the contract change with tests and doc updates together so consuming
projects inherit one coherent story instead of another partial patch.

## Decision Log
- 2026-05-02T00:42:40-07:00 - Promoted the overlapping imported validation,
  wrapper, cache, and refresh ECRs into one actionable TheKnowledge
  proposal.
- 2026-05-02T13:32:00-07:00 - Approved and implemented. TheKnowledge now
  refreshes a managed `.gitignore` block in consuming projects, resolves
  vendored helper paths safely through the TheKnowledge checkout, uses
  runtime-policy resolution for non-Black tools, falls back to `.cache/`
  when Git-backed cache paths are unavailable, and keeps wrong-runtime and
  wrong-authority discoveries documented as interrupt-class conditions.
