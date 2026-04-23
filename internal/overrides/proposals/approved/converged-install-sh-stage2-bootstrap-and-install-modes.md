# Converged install.sh Bootstrap and Install Modes

Title: Engineering Change Request: Converged `install.sh` Bootstrap and
Install Modes
Author: Codex
Date: 2026-03-31T21:28:54-07:00
Status: Approved
Reviewers: operator (repository maintainer), AI maintainers
Related Work: Direct operator request on 2026-03-31; existing
`bootstrap.sh` and `bootstrap-stage2.py` starter templates; local
`codex-wrangler` `install.sh` and `scripts/install-stage-2.py` flow;
`python_bootstrap_and_context_strategy.txt`

## Problem Statement
TheKnowledge's current managed starter and `codex-wrangler`'s stronger local
bootstrap each solve different parts of the same problem. TheKnowledge ships
managed pinned-context files, starter refresh machinery, and drift checking,
but its default POSIX bootstrap still assumes too much host state and leans
on `pyenv-virtualenv`. `codex-wrangler` proved a better Rocky-and-Ubuntu
operator flow with a minimal stage 1, user-scoped `pyenv` setup, repo-local
`.venv`, editable install, and mandatory `direnv`, but that flow lives only
as a local override. New consuming projects therefore inherit an incomplete
default, while improved behavior remains hard to propagate safely.

## Goals
- Make `install.sh` the canonical managed POSIX bootstrap entry point.
- Provide one Python 3.9-safe managed stage-2 installer at
  `scripts/install-stage-2.py`.
- Keep the managed `python-environments.json`, `.python-version`, context
  scripts, and starter refresh machinery.
- Make `pyenv` plus repo-local `.venv` the new default steady-state model.
- Support both standard and development project-install modes.
- Require `direnv` for managed developer installs.
- Preserve compatibility wrappers for existing `bootstrap.sh`,
  `bootstrap-stage2.py`, and legacy prerequisite entry points.

## Non-Goals
- Remove Windows-specific compatibility shims in this change.
- Remove all legacy wrappers in the same release.
- Force every project to support a user-global installer.
- Change the requirement that bootstrap/setup code remain Python 3.9-safe.

## Use Cases
1. A newly created consuming project runs `./install.sh` on Ubuntu or Rocky
   and gets a known-good developer environment.
2. A maintainer reruns the managed bootstrap after starter drift and receives
   the same result as a fresh checkout.
3. A project that still uses distinct `pyenv-virtualenv` names continues to
   work while newer projects use plain pinned versions.
4. TheKnowledge's own repository uses the same managed default it prescribes
   to consuming projects.

## Constraints and Assumptions
- Managed stage-2 logic must stay stdlib-only and Python 3.9-safe.
- Managed starter refresh must remain deterministic and reviewable.
- Compatibility shims should remain thin wrappers, not competing workflows.
- `direnv` installation and shell-hook updates must be idempotent.

## Proposed Approach
Add `install.sh` and `scripts/install-stage-2.py` to the managed starter and
shift documentation to treat them as canonical. Keep `bootstrap.sh` as a
shim to `install.sh`, and keep `bootstrap-stage2.py` as a shim to
`scripts/install-stage-2.py`.

Update the shared bootstrap helper layer so the default config in
`python-environments.json` declares pinned bootstrap and runtime Python
versions whose selection names match the version strings. In that default
case, stage 2 installs those versions through `pyenv`, writes
`.python-version`, and builds a repo-local `.venv` without requiring
`pyenv-virtualenv`. When a legacy project still declares a distinct
environment name, the helper may continue to use `pyenv-virtualenv` as a
compatibility path.

Make stage 2 perform the rest of the managed developer or standard install:
submodule initialization when relevant, `pyenv` installation or update,
managed shell-hook blocks, `.venv` creation through `scripts/dev_setup.py`,
generic project installation, optional project hook delegation, and mandatory
`direnv` setup for developer mode.

Fix the submodule-update helper to load the managed refresh template set from
the adopted TheKnowledge revision instead of from the pre-update import.

## Risks and Mitigations
- Risk: starter refresh still lands only part of the new surface.
  Mitigation: update both the managed template list and the submodule-update
  import timing, and add regression coverage.
- Risk: compatibility wrappers hide migration drift too long.
  Mitigation: document `install.sh` as canonical immediately and keep wrapper
  bodies visibly minimal.
- Risk: managed docs and tests drift from starter behavior.
  Mitigation: update template, repository, and specification assertions in
  the same change.
- Risk: automatic `direnv` and `pyenv` shell edits feel intrusive.
  Mitigation: use clearly marked managed blocks and stable idempotent writes.

## Testing and Validation
- Extend bootstrap helper tests to cover the plain-`pyenv` default path and
  any legacy `pyenv-virtualenv` compatibility branch.
- Update initial-setup and managed-drift tests for the new file set and
  canonical commands.
- Validate wrapper entry points so `bootstrap.sh` and `bootstrap-stage2.py`
  still delegate correctly.
- Run TheKnowledge's required tool suite before staging.

## Alternatives Considered
1. Keep `bootstrap.sh` as canonical and copy only selected local behavior.
   Rejected because `install.sh` is clearer and already validated here.
2. Move entirely to `pyenv-virtualenv`.
   Rejected because plain `pyenv` plus `.venv` is simpler for most
   repositories.
3. Leave improved bootstrap behavior as a consuming-project override.
   Rejected because it defeats the point of a managed default.

## Open Questions
1. Whether TheKnowledge should eventually template an explicit project
   install-hook stub instead of only documenting the optional hook.
   Owner: AI maintainers and operator.
   Target date: 2026-04-07.
2. Whether Windows should receive a first-class stage-1/stage-2 analogue or
   continue using the compatibility installer path.
   Owner: TheKnowledge maintainers.
   Target date: 2026-04-14.

## Milestones
1. Approve the converged managed-bootstrap direction.
   Target date: 2026-03-31.
   Owners: operator, AI maintainers.
   Dependencies: direct design discussion.
   Entry criteria: proposal drafted.
   Exit criteria: operator approves option 3.
2. Update managed starter files, helper scripts, docs, and tests.
   Target date: 2026-03-31.
   Owners: AI maintainers.
   Dependencies: milestone 1.
   Entry criteria: approved proposal.
   Exit criteria: managed starter reflects the new canonical flow.
3. Adopt the converged starter in active consuming projects.
   Target date: 2026-03-31.
   Owners: AI maintainers.
   Dependencies: milestone 2.
   Entry criteria: starter changes land locally.
   Exit criteria: consuming-project adoption validates cleanly.

## Adoption and Rollout
Roll out the converged design in TheKnowledge `trunk`, keep compatibility
wrappers for one or more maintenance cycles, and update docs to direct new
POSIX users to `./install.sh`. Consuming projects can then refresh managed
starter files without having to preserve a large local bootstrap override.

## Decision Log
- 2026-03-31T21:28:54-07:00 - Drafted and marked approved by Codex after the
  operator directed TheKnowledge and `codex-wrangler` to adopt the converged
  managed stage-1 and stage-2 design on `trunk`.
