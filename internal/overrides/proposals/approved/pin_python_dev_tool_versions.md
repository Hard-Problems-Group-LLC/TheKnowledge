# Pin Default Python Tool Versions Across TheKnowledge and Starter Projects

Title: Pin Default Python Tool Versions Across TheKnowledge and Starter
Projects
Author: Codex
Date: 2026-03-25T14:34:52-07:00
Status: Approved
Reviewers: operator (repository maintainer), AI maintainers
Related Work: Direct operator request on 2026-03-25;
standards-and-practices/docs/specifications/
pinned_python_dev_tool_versions.txt;
pyproject.toml; templates/requirements-dev.txt; templates/scripts/dev_setup.py

## Problem Statement
TheKnowledge currently leaves its default Python quality-gate tools loosely
versioned with `>=` constraints. That means Black, Ruff, and pytest behavior
can drift across machines and over time even when contributors are following
the documented workflow. The drift is not theoretical: in this session, the
same official Black command produced broad repo churn because the repository
had older formatting already committed and the active environment resolved a
newer Black release.

The mismatch is worse for consuming projects. TheKnowledge's
`scripts/initial-setup.py` currently installs project-management records and
managed `AGENTS.md` content, but it does not install a starter Python
toolchain manifest or setup script. As a result, downstream projects can
inherit TheKnowledge's workflow commands without inheriting the exact tool
versions those commands were written and tested against.

## Goals
- Make TheKnowledge's default Python formatter, linter, and test toolchain
  reproducible across machines.
- Ensure new and lightly customized consuming projects inherit the same pinned
  defaults through the managed setup path.
- Keep the downstream bootstrap lightweight and easy to override locally.
- Add tests that catch version drift between TheKnowledge itself and the
  managed starter files.
- Document how maintainers and consuming projects refresh the pinned tools.

## Non-Goals
- Pin every application dependency a consuming project may need.
- Prevent mature projects from using stricter or more specialized local
  environment management.
- Solve every source of formatter churn in existing repositories with this
  proposal alone.
- Replace the existing quality-gate commands or timeout-wrapper workflow.

## Use Cases
1. A maintainer clones TheKnowledge on a new machine and expects `black`,
   `ruff`, and `pytest` behavior to match the rest of the team.
2. A consuming project runs `python TheKnowledge/scripts/initial-setup.py`
   and wants an immediate starter path for the same pinned Python quality-gate
   tools.
3. An upgrade to TheKnowledge changes default tool versions, and consuming
   projects need a visible managed file change that tells them what drifted.
4. A project with custom bootstrap needs to keep its override, while still
   understanding what TheKnowledge considers the default pinned stack.

## Constraints and Assumptions
- TheKnowledge must stay usable both as its own repository and as a submodule
  consumed by other repositories.
- Consuming projects often have local override files, so the managed starter
  must remain replaceable rather than mandatory.
- The default bootstrap path should stay simple: a requirements file plus a
  small setup script are easier to inspect than hidden installer logic.
- The pinned versions should be concrete and test-enforced so drift fails fast
  in review.
- Documentation and templates must stay aligned because many users learn the
  workflow from generated files rather than from TheKnowledge's root README.

## Proposed Approach
Pin TheKnowledge's own dev-tool versions exactly in `pyproject.toml` so
`scripts/install_prerequisites.py` installs a stable default stack when it
pulls the editable dev extras.

Mirror that same pinned stack into managed starter files for consuming
projects:
- add `templates/requirements-dev.txt` with the exact pinned versions; and
- add `templates/scripts/dev_setup.py` that creates or refreshes a `.venv`,
  upgrades packaging tooling, and installs the pinned requirements file.

Because `scripts/initial-setup.py` already installs all non-README template
entries by default, new consuming projects will receive those starter files
automatically. Existing projects can keep local overrides or adopt the managed
versions on the next forced template refresh.

Document the bootstrap flow in the repository README, the installation guide,
the downstream template README, the managed downstream `AGENTS` footer, and
the downstream git-flow template. Add tests that verify:
- the pins in `pyproject.toml` remain exact;
- the managed `requirements-dev.txt` stays synchronized with those pins; and
- initial setup installs the starter files into consuming projects.

## Risks and Mitigations
- Risk: Adding managed starter files creates overwrite conflicts in consuming
  projects that already own `requirements-dev.txt` or `scripts/dev_setup.py`.
  Mitigation: keep `initial-setup.py`'s existing no-overwrite default so those
  projects must opt into replacement with `--force`.
- Risk: The pinned versions can grow stale.
  Mitigation: make updates explicit through proposal/spec review, committed
  file diffs, and sync tests that force maintainers to touch all required
  surfaces together.
- Risk: A generic starter script may not match every project's preferred
  environment manager.
  Mitigation: document it as the default managed path, not as a prohibition on
  project-local bootstrap scripts.
- Risk: Duplicate version lists in `pyproject.toml` and
  `templates/requirements-dev.txt` could drift.
  Mitigation: add automated tests that compare them directly.

## Testing and Validation
Validate the implementation with repository tests and a starter-install smoke
check. At minimum:
- add tests that parse `pyproject.toml` and require exact `==` pins for the
  managed developer tools;
- verify that `templates/requirements-dev.txt` matches those pins exactly;
- verify that `scripts/initial-setup.py` installs the starter toolchain files
  into a temporary consuming project tree; and
- review the updated README/template guidance to ensure the bootstrap path is
  explained consistently for both TheKnowledge and consuming projects.

Per Joel Spolsky's shipping guidance, do not treat the proposal as fully
executed until the automated checks prove the pins are synchronized and the
starter-install path is visible in the managed documentation.

## Alternatives Considered
1. Keep broad `>=` constraints and accept drift.
   Rejected because it leaves validation behavior and formatting output
   unstable across time and machines.
2. Pin TheKnowledge itself but leave consuming projects to choose tools.
   Rejected because TheKnowledge would still export workflow commands without
   exporting the versions those commands assume.
3. Generate pins only inside a setup script and not in a visible manifest.
   Rejected because a standalone `requirements-dev.txt` is easier to inspect,
   diff, and override in consuming projects.
4. Force all consuming projects to adopt the managed bootstrap files.
   Rejected because many repositories already have tighter local policies and
   should be able to keep them.

## Open Questions
None at approval time. The operator explicitly requested immediate execution,
so this proposal records the adopted default: exact pins in TheKnowledge,
mirrored starter pins for consuming projects, and setup-script-driven
bootstrap for teams that use the managed default path.

## Milestones
1. Approve the proposal and draft the specification.
   Target date: 2026-03-25.
   Owners: operator, AI maintainers.
   Dependencies: operator decision.
   Entry criteria: proposal exists for review.
   Exit criteria: status is Approved and the specification is written.
2. Implement the pinned-tool surfaces.
   Target date: 2026-03-25.
   Owners: AI maintainers.
   Dependencies: approved specification.
   Entry criteria: specification names the required files and behaviors.
   Exit criteria: `pyproject.toml`, templates, docs, and tests are updated.
3. Validate and roll out.
   Target date: 2026-03-25.
   Owners: AI maintainers.
   Dependencies: implementation complete.
   Entry criteria: code and docs are updated.
   Exit criteria: automated validation passes and the `Feedback` branch is
   ready to push.

## Adoption and Rollout
Roll out in two layers.

First, TheKnowledge itself adopts exact pins in `pyproject.toml`, so direct
repository maintenance gets stable default tool versions immediately through
`scripts/install_prerequisites.py`.

Second, consuming projects inherit starter `requirements-dev.txt` and
`scripts/dev_setup.py` files through `scripts/initial-setup.py`. New projects
can use those files directly. Existing projects can compare them during
submodule upgrades and either adopt them or keep their local overrides.

When the default pins change in the future, maintainers should update the
proposal/spec references as needed, adjust the pinned files together, rerun
validation, and call out the starter-toolchain change clearly in upgrade
notes.

## Decision Log
- 2026-03-25T14:34:52-07:00 - Proposal drafted by Codex in response to an
  operator request to pin static-analysis and related Python developer tools.
- 2026-03-25T14:34:52-07:00 - Approved by the operator for immediate
  implementation on the `Feedback` branch.
