# TheKnowledge Tool Runtime Isolation and Bootstrap Reliability

Title: TheKnowledge Tool Runtime Isolation and Bootstrap Reliability
Author: Codex
Date: 2026-04-22T18:28:42-07:00
Status: Under Review
Reviewers: operator, AI maintainers
Related Work: `python-environments.json`; `tool_validation_profiles.json`;
`scripts/dev_setup.py`; `scripts/install-stage-2.py`;
`scripts/git_standard_commit_push.py`;
`standards-and-practices/docs/specifications/`
`tool_validation_profiles_and_python_runtime_selection.txt`;
`standards-and-practices/docs/specifications/`
`python_bootstrap_and_context_strategy.txt`

## Problem Statement
TheKnowledge must be able to run its own validation and Git workflow tooling
reliably when maintained as a direct checkout. At the same time, many
consuming projects include TheKnowledge as a submodule. Any tooling material
checked into TheKnowledge must not make those consuming projects inherit
unwanted Python environments, dirty submodule working trees, unexpected
install side effects, or project-specific runtime names.

The current runtime-selection guidance is directionally correct but not yet
operationally robust. During local maintenance, the standard commit helper
needed a Python 3.12 tool runtime with Black, Ruff, and pytest. The direct
checkout had a stale repo-local `.venv` using Python 3.9 without Black, no
per-user TheKnowledge tool venv, a system Python 3.12 without Black or global
pip, and no configured pyenv `3.12.12` runtime. A consuming-project pyenv
environment happened to satisfy the tool requirements, but using that
environment for TheKnowledge maintenance was wrong because it belonged to an
external project and its runtime name should not appear in TheKnowledge
records or workflows.

There is also a bootstrap deadlock. `scripts/dev_setup.py --python
/path/to/python3.12` currently validates the explicit candidate against the
steady-state tool policy, including required modules such as Black, before it
creates the venv that would install those modules.
`scripts/install-stage-2.py` then calls
`scripts/dev_setup.py --python <runtime_python>` for repo-local venv
creation, so the documented bootstrap path can fail when the base interpreter
is correct but bare.

## Goals
- Give TheKnowledge a reliable, self-owned way to run its validation and Git
  workflow helpers from a compliant Python 3.12 tool runtime.
- Keep that runtime isolated from consuming projects that carry TheKnowledge
  as a submodule.
- Avoid checking generated venvs, local tool caches, or project-specific
  runtime names into TheKnowledge.
- Fix the bootstrap deadlock between base-interpreter selection and
  steady-state tool-module validation.
- Make the fallback order explicit enough that agents do not reach for
  unrelated project environments when a local tool runtime is missing.

## Non-Goals
- Force every consuming project to use TheKnowledge's own tool venv.
- Make TheKnowledge silently install tooling merely because it is present as a
  submodule.
- Replace consuming-project validation profiles with TheKnowledge's internal
  maintenance environment.
- Require global pip installs or system-wide Python package mutation.

## Current Situation
- `python-environments.json` declares a bootstrap Python floor of 3.9 and a
  steady-state runtime selection of Python `3.12.12`.
- `tool_validation_profiles.json` defines `steady_state_python_tools` with
  Python 3.12 minimum and required Black support.
- The resolver prefers `.venv/bin/python`, then `python3.12`, `python`, and
  `python3`, with explicit overrides such as `THEKNOWLEDGE_PYTHON_TOOLS`.
- The direct checkout's `.venv` was stale Python 3.9 and lacked Black.
- The ambient `python` was Python 3.9 and lacked Black, Ruff, and pytest.
- The ambient `python3.12` was Python 3.12 but lacked Black and global pip.
- A probe confirmed that `python3.12 -m venv --clear .venv` can seed pip in a
  repo-local ignored venv, but that alone does not install the pinned tools.
- The existing `scripts/dev_setup.py` path is not usable from a bare Python
  3.12 because the explicit candidate must already provide Black.

## Proposed Approach
Introduce a TheKnowledge-owned tool-runtime bootstrap contract with separate
base-interpreter and tool-environment phases.

1. Add a small managed tool-runtime helper, for example
   `scripts/ensure_theknowledge_tool_runtime.py`.
2. Teach that helper to resolve a base Python 3.12 interpreter without
   requiring Black, then create or refresh a tool venv and install
   TheKnowledge's pinned developer dependencies into that venv.
3. Store the default generated tool venv in a standard ignored checkout-local
   path so it does not dirty parent repositories when TheKnowledge is a
   submodule. The preferred direct-checkout default should be
   `.local/theknowledge-tool-runtime/`, with an XDG user-cache fallback keyed
   by checkout path and dependency fingerprint when the checkout-local path is
   not writable or not appropriate.
4. Keep explicit repo-local `.venv` support for direct development mode, but
   do not make `.venv` the only maintenance-tool path.
5. Make the standard Git helper and quality-gate entry points either re-exec
   through the ensured tool runtime or emit one exact command that does so.
6. Require any explicit override, such as `THEKNOWLEDGE_PYTHON_TOOLS`, to name
   a deliberate TheKnowledge-compatible runtime. Documentation should warn
   agents not to borrow runtime environments from consuming projects merely
   because they satisfy imports.
7. Print runtime provenance in diagnostics using generic categories, such as
   `repo-local tool venv`, `git-dir tool venv`, `user-cache tool venv`, or
   `explicit THEKNOWLEDGE_PYTHON_TOOLS`, instead of embedding unrelated
   project names in records.

The fallback order should be explicit and testable:

1. Deliberate `THEKNOWLEDGE_PYTHON_TOOLS` override when set.
2. Existing repo-local `.venv` only when it is Python 3.12+ and has required
   tool modules.
3. TheKnowledge checkout-local or user-cache tool venv when its dependency
   fingerprint matches.
4. Creation or refresh of that tool venv from a base Python 3.12 interpreter.
5. Base interpreter discovery through configured pyenv selection,
   `python3.12`, or a documented installer-managed pyenv fallback.
6. Clear failure with remediation commands when no compliant base interpreter
   can be found.

## Consumer-Project Safety Rules
- The helper must not run automatically when TheKnowledge is imported or
  merely present as a submodule.
- The helper must not write generated tooling into a consuming project's root
  unless the consuming project explicitly invokes its own managed bootstrap.
- Generated TheKnowledge maintenance venvs must be ignored by Git and should
  use a documented local-only placement such as `.local/` rather than ad hoc
  paths.
- Starter files copied into consuming projects may describe the same policy,
  but their generated environments must be owned by the consuming project, not
  by the TheKnowledge submodule.
- Submodule validation should keep using the active project's configured
  tooling unless the operator is explicitly maintaining TheKnowledge itself.

## Testing and Validation
- Add resolver tests that distinguish base-interpreter selection from
  tool-runtime selection.
- Add a regression test showing that a bare Python 3.12 without Black can
  create a compliant tool venv.
- Add tests for direct checkout and submodule paths so generated runtime
  artifacts do not dirty the parent repository.
- Add tests for `git_standard_commit_push.py` or the quality gate wrapper so
  it uses the ensured tool runtime without requiring a hand-written path.
- Add documentation tests or assertions that no TheKnowledge-authored proposal
  or standard mentions unrelated project-specific runtime names.

## Alternatives Considered
1. Keep using the ambient shell Python.
   Rejected because the ambient Python can be Python 3.9 and lack the pinned
   tools required by TheKnowledge validation.
2. Require direct maintainers to run `./install.sh --mode dev` manually.
   Insufficient because the current bootstrap path has a bare-runtime
   deadlock and because submodule worktrees should not be dirtied merely to
   maintain TheKnowledge.
3. Check in a `requirements-dev.txt` at the TheKnowledge root and rely on
   humans to create `.venv` manually.
   Insufficient because it does not solve runtime placement, submodule
   cleanliness, or standard-helper re-execution.
4. Use whatever local pyenv environment already has Black.
   Rejected because it can borrow consuming-project identity and leak
   unrelated project names into TheKnowledge records.

## Risks and Mitigations
- Risk: a checkout-local `.local/` venv could be mistaken for shipped project
  state.
  Mitigation: keep `.local/` ignored by Git, document it as operator-only
  state, and keep starter guidance clear that the directory is local and
  mutable.
- Risk: automatic creation downloads packages in restricted environments.
  Mitigation: separate `ensure`, `check`, and `explain` modes, and require an
  explicit install step before networked package installation.
- Risk: direct-checkout developers expect `.venv`.
  Mitigation: keep `.venv` as an accepted explicit development-mode target,
  but do not require it for safe submodule maintenance.
- Risk: helper complexity hides failures.
  Mitigation: print the chosen base interpreter, generated venv location,
  dependency fingerprint, and exact remediation command on failure.

## Open Questions
1. Should the default generated maintenance venv always live under
   project-root `.local/`, or should XDG user-cache placement remain an
   automatic fallback when that local path is unavailable?
2. Should TheKnowledge add a root `requirements-dev.txt`, or should the helper
   install `.[dev]` directly from `pyproject.toml`?
3. Should `git_standard_commit_push.py` re-exec automatically through the
   ensured runtime, or should operators invoke a separate wrapper command?

## Milestones
1. Approve the runtime-isolation strategy.
   Target date: 2026-04-24.
   Owners: operator, AI maintainers.
   Exit criteria: default storage location and helper behavior are selected.
2. Implement the helper and resolver split.
   Target date: 2026-04-27.
   Owners: AI maintainers.
   Exit criteria: a bare Python 3.12 can create a compliant tool runtime.
3. Integrate the standard Git and quality-gate helpers.
   Target date: 2026-04-28.
   Owners: AI maintainers.
   Exit criteria: `ACP` can run from a direct checkout without handwritten
   project-specific runtime paths.
4. Validate submodule safety.
   Target date: 2026-04-29.
   Owners: AI maintainers.
   Exit criteria: a consuming-project submodule checkout remains clean unless
   TheKnowledge maintenance is explicitly invoked.

## Decision Log
- 2026-04-22T18:28:42-07:00 - Drafted after a direct TheKnowledge
  maintenance session exposed a stale `.venv`, missing per-user
  TheKnowledge tool runtime, bare system Python 3.12, and an accidental
  attempt to use a consuming-project pyenv environment for TheKnowledge
  validation.
