# Two-stage POSIX Bootstrap With install.sh, pyenv, and direnv

Title: Engineering Change Request: Two-stage POSIX Bootstrap With
`install.sh`, Python Stage 2, `pyenv`, and Mandatory `direnv`
Author: Codex
Date: 2026-03-31T15:38:05-07:00
Status: Under Review
Reviewers: operator (repository maintainer), AI maintainers
Related Work: Direct operator request on 2026-03-31; consuming-project
cross-distro bootstrap investigation in `codex-wrangler`; README.md section
"Direct Checkout"; standards-and-practices/docs/installation.txt;
standards-and-practices/docs/development-workflow.txt;
standards-and-practices/docs/AI-sandbox-configuration.txt;
standards-and-practices/docs/specifications/
pinned_python_dev_tool_versions.txt;
internal/overrides/proposals/under-review/imported-ecrs/
python-bootstrap-and-context-strategy-ecr.md

## Problem Statement
TheKnowledge currently treats `scripts/install_prerequisites.sh` plus
`scripts/install_prerequisites.py` as the canonical bootstrap path. That flow
has three problems.

First, it assumes distro behavior that does not hold consistently across
modern Rocky and Ubuntu environments. In particular, Ubuntu's externally
managed Python packaging rules make the current documented install paths less
straightforward than the docs imply, while Rocky-oriented assumptions can
hide those failures until a maintainer tries a fresh machine.

Second, the bootstrap responsibilities are split across too many surfaces.
The shell wrapper, Python bootstrap, `scripts/dev_setup.py`, git-hook setup,
and any project-local pyenv or shell-integration expectations are not
described as one coherent system. That leaves maintainers guessing which
parts are prerequisites, which parts are optional, and which interpreter is
supposed to own the repo-local `.venv`.

Third, TheKnowledge does not currently codify the shell-integration piece
that actually makes a repo-local environment ergonomic. If `pyenv` selects
the Python but nothing auto-activates the environment, maintainers still have
to remember additional manual steps on every shell entry.

## Goals
- Provide one canonical developer bootstrap entry point that works cleanly on
  current Rocky and Ubuntu systems.
- Keep stage 1 small, auditable, and limited to host-level prerequisite
  discovery plus the minimum package-manager interaction needed to launch
  stage 2.
- Require stage 2 to stay runnable under Python 3.9-compatible syntax so the
  bootstrap can start from a conservative system interpreter.
- Standardize on user-scoped `pyenv`, a repo-local `.python-version`, and a
  repo-local `.venv`.
- Make `direnv` mandatory for developer installs so the selected Python and
  repo environment become active automatically on directory entry.
- Preserve a separate simpler path for non-development user installs where a
  project only wants the user-facing command.

## Non-Goals
- Replace project-local overrides in consuming projects that intentionally use
  a different bootstrap flow.
- Guarantee a native Windows bootstrap path in the same script family.
- Manage application-specific dependencies beyond the Python/dev-tooling stack
  that TheKnowledge itself requires.
- Require `sudo` or host-level package installation when the operator does
  not want that.
- Force `pyenv-virtualenv` or named global virtualenvs when repo-local `.venv`
  remains sufficient.

## Use Cases
1. A maintainer on Ubuntu clones a TheKnowledge-based project and wants one
   documented command that tells them exactly which host packages are missing
   before creating the working environment.
2. A maintainer on Rocky wants the same bootstrap path without having to
   remember different README instructions.
3. A consuming project inherits TheKnowledge guidance and expects an AI agent
   to choose the same bootstrap path a human would choose.
4. A direct TheKnowledge checkout wants automatic environment activation on
   `cd` instead of manual `source .venv/bin/activate` repetition.

## Constraints and Assumptions
- Stage 1 should stay POSIX-shell-based and as small as possible.
- Stage 2 should be stdlib-only and Python 3.9-compatible.
- Installing Python toolchains with `pyenv` still requires system-level build
  dependencies, which cannot always be solved without the operator's package
  manager.
- `pyenv` belongs in user scope, not in system scope, so it can coexist with
  multiple repositories and does not require root.
- TheKnowledge's existing repo-local `.venv` workflow remains useful and does
  not need to be replaced by `pyenv-virtualenv`.
- If `direnv` becomes mandatory for developer installs, the bootstrap must
  manage both the shell hook and a repo-local `.envrc` policy clearly.
- The new default must continue installing managed hooks and any other setup
  side effects that the current canonical bootstrap already promises.

## Proposed Approach
Replace the current default developer bootstrap story with a two-stage model.

Stage 1 should be a repo-root `install.sh`:
- require any Python 3 interpreter that can run 3.9-compatible code;
- when run with sufficient privileges, install the minimum host packages
  needed to continue, including Python, pip, venv support, git, curl, direnv,
  and the `pyenv` build prerequisites for the current distro;
- when not run with sufficient privileges, perform the same checks but stop
  with exact distro-specific remediation commands instead of guessing; and
- launch the Python stage once a suitable interpreter is available.

Stage 2 should be `scripts/install-stage-2.py`:
- remain stdlib-only and Python 3.9-compatible;
- initialize required submodules before any managed validation or refresh;
- install or update user-scoped `pyenv`;
- install a managed Python 3.12.x interpreter through `pyenv`;
- write the repo-local `.python-version`;
- create or refresh the repo-local `.venv`, preferably by driving
  `scripts/dev_setup.py`;
- install the editable dev environment into that `.venv`;
- ensure `direnv` is present, install the managed shell-hook block, write the
  repo-local `.envrc`, and run `direnv allow`; and
- install or refresh the managed git hooks and other setup artifacts that the
  current bootstrap contract already covers.

Retain a simpler non-development install helper for projects that only need a
stable user-facing command and not the full editable developer environment.

For migration, TheKnowledge may keep `scripts/install_prerequisites.sh` as a
temporary compatibility shim that delegates to `./install.sh`, but the
documentation and tests should treat `install.sh` as canonical.

## Risks and Mitigations
- Risk: the POSIX-only default leaves Windows expectations ambiguous.
  Mitigation: document WSL2 or a separate Windows path explicitly instead of
  implying unsupported parity.
- Risk: `pyenv` installation can fail when distro build dependencies are
  missing.
  Mitigation: make stage 1 responsible for exact host-package diagnostics and
  for root-assisted installation when the operator chooses that path.
- Risk: mandatory `direnv` changes shell startup files.
  Mitigation: keep the hook block small, managed, idempotent, and clearly
  delimited so operators can audit it.
- Risk: the new flow duplicates behavior already present in
  `scripts/dev_setup.py` or existing hook installers.
  Mitigation: keep stage 2 orchestration-focused and reuse the existing lower-
  level helpers rather than rebuilding their logic inline.
- Risk: existing consumers depend on `scripts/install_prerequisites.sh`.
  Mitigation: keep a compatibility shim for at least one transition period and
  update the docs/tests in the same change.

## Testing and Validation
- Add unit tests for `install.sh --help` behavior and stage-1 option
  pass-through where practical.
- Add unit tests for `scripts/install-stage-2.py` argument parsing, direct-run
  guards, `pyenv` version selection, managed `direnv` block rendering, and
  `.envrc` generation.
- Update documentation tests so the new bootstrap command appears in
  TheKnowledge and managed downstream surfaces.
- Preserve coverage for repo-local `.venv` recreation when the requested
  interpreter changes.
- Run manual smoke checks on at least one Rocky machine and one Ubuntu machine
  before declaring the migration complete.

## Alternatives Considered
1. Keep `scripts/install_prerequisites.sh` and only patch its docs.
   Rejected because the current contract is split and underspecified, not just
   poorly documented.
2. Standardize solely on `python scripts/dev_setup.py`.
   Rejected because it does not solve the host-prerequisite, `pyenv`, or
   shell-integration parts of the problem.
3. Require an exact `python3.9` system package name everywhere.
   Rejected because distro naming and availability vary; the requirement is
   Python 3.9-compatible execution, not a literal `python3.9` binary.
4. Use `pyenv-virtualenv` instead of repo-local `.venv`.
   Rejected because TheKnowledge already relies on repo-local `.venv`, and
   `direnv` can supply the missing activation ergonomics without changing that
   model.
5. Keep `direnv` optional.
   Rejected because the environment-selection story stays incomplete if shell
   entry still requires manual activation.

## Open Questions
1. Should TheKnowledge pin a specific Python 3.12 patch release in stage 2,
   or intentionally take the newest available `3.12.x` patch from `pyenv`?
2. How long should the compatibility shim for
   `scripts/install_prerequisites.sh` remain in place?
3. Should the direct-checkout bootstrap install `direnv` itself when root is
   unavailable but a user-local install is possible, or should that remain a
   manual prerequisite with explicit instructions?

## Milestones
1. Review and approve or revise this ECR.
   Target date: 2026-04-02.
   Owners: operator, AI maintainers.
   Dependencies: review of the current bootstrap docs and helper surfaces.
   Entry criteria: proposal exists under review.
   Exit criteria: operator decision recorded in the proposal.
2. Update the canonical bootstrap specification and docs.
   Target date: 2026-04-04.
   Owners: AI maintainers.
   Dependencies: proposal approval.
   Entry criteria: approved stage-1/stage-2 design.
   Exit criteria: installation, development-workflow, README, and template
   guidance all name the new canonical path.
3. Implement the new bootstrap path.
   Target date: 2026-04-06.
   Owners: AI maintainers.
   Dependencies: updated specification.
   Entry criteria: canonical behavior and compatibility expectations are
   documented.
   Exit criteria: `install.sh`, `scripts/install-stage-2.py`, and any needed
   helper changes land with passing tests.
4. Validate Rocky and Ubuntu behavior.
   Target date: 2026-04-07.
   Owners: AI maintainers.
   Dependencies: implementation complete.
   Entry criteria: bootstrap code and docs are updated.
   Exit criteria: manual smoke checks and the automated validation suite pass.

## Adoption and Rollout
If approved, land the new bootstrap on `trunk`, keep a short-lived
compatibility shim for the old script name if needed, and update all managed
template/docs surfaces together so consuming projects receive one consistent
story.

The rollout should explicitly distinguish:
- direct-checkout developer bootstrap;
- consuming-project managed defaults; and
- non-development user installs.

That separation keeps the developer path coherent without forcing every
downstream project to look identical.

## Decision Log
- 2026-03-31T15:38:05-07:00 - Drafted by Codex after a consuming-project
  maintenance session showed that TheKnowledge's current canonical bootstrap
  guidance is too Rocky-shaped, under-specifies Ubuntu behavior, and does not
  define a coherent default for `pyenv` plus automatic repo-environment
  activation.
