# Placement-Driven Black Validation and Runtime Profiles

Title: Placement-Driven Black Validation and Runtime Profiles
Author: Codex
Date: 2026-03-27T00:30:54-07:00
Status: Approved
Reviewers: operator (repository maintainer), AI maintainers
Related Work: Direct operator request on 2026-03-27;
internal/overrides/bugs/open/starter-validation-stack-drifts-from-supported-
python-and-black-behavior.txt;
internal/overrides/bugs/open/bootstrap-and-steady-state-python-runtime-
policy-are-not-separated.txt;
internal/overrides/bugs/open/full-scope-black-validation-reformats-
unrelated-tracked-files-on-supported-interpreter.txt;
internal/overrides/bugs/open/codex-sandbox-asyncio-wakeup-fails-for-multi-
file-static-analysis.txt;
internal/overrides/proposals/approved/pin_python_dev_tool_versions.md;
internal/overrides/proposals/approved/serial-file-safe-static-analysis-in-
affected-sandboxes.txt;
standards-and-practices/docs/specifications/pinned_python_dev_tool_versions.
txt;
standards-and-practices/docs/specifications/codex_sandbox_file_safe_static_
analysis.txt

## Problem Statement
TheKnowledge now has several Black-related failures that share one deeper
cause: formatter behavior, file discovery, and Python runtime selection are
not described by a coherent placement-driven policy.

Current behavior makes small maintenance work brittle in four ways:
- the starter and repository bootstrap paths still imply that one Python
  interpreter can cover both installer entry points and the pinned Black
  toolchain;
- the timeout wrapper's serial Black fallback discovers files by walking the
  filesystem rather than starting from Git-tracked files and `.gitignore`;
- the full-scope Black check does not resolve files into meaningful
  validation classes, so one scoped edit can trigger unrelated repository
  formatting churn; and
- sandbox-safe serial execution already exists, but it is not connected to a
  path-aware notion of which files should be formatted together and with
  which target version.

The repository therefore lacks a durable answer to a simple question: when a
new Python-like file appears, what validation should apply based on its
location and extension, without adding a rule for that exact filename?

## Goals
- Make Black file discovery honor Git intent by default.
- Resolve Black target behavior from placement and extension rather than from
  filename-specific rules.
- Separate bootstrap-runtime policy from steady-state developer-tool runtime
  policy.
- Preserve the existing sandbox-safe serial fallback where it is needed.
- Let maintainers add a new file to an established directory and inherit the
  correct validation profile automatically.
- Keep the configuration inspectable, testable, and repository-managed.

## Non-Goals
- Fix the upstream Codex sandbox wakeup defect inside TheKnowledge.
- Guarantee that every possible future tool can use the same profile system
  unchanged.
- Support arbitrary one-off local exceptions without making them visible in
  repository-managed configuration.
- Resolve repository-wide Black baseline drift silently inside unrelated
  changesets.

## Use Cases
1. A maintainer adds a new bootstrap installer script and wants it validated
   as Python-3.9-compatible while the formatter itself still runs from the
   supported steady-state toolchain.
2. A maintainer adds a new ordinary repository Python file under `tests/` or
   `src/` and expects it to inherit the default steady-state Black profile
   automatically.
3. A consuming project runs the managed starter bootstrap and needs a clear
   handoff from bootstrap Python to the steady-state pinned toolchain.
4. A sandboxed AI maintainer runs Black on a changed-file set and needs the
   same placement-based profile resolution while still benefiting from serial
   one-file-at-a-time execution where required.

## Constraints and Assumptions
- The repository still needs a Python-3.9-compatible bootstrap story for
  installer entry points unless the declared floor is raised explicitly.
- The pinned Black toolchain currently needs a newer runtime than Python 3.9.
- The current Codex sandbox may still require serial Black dispatch for
  multi-file formatting in known affected environments.
- The policy must prefer directory structure and extension over explicit
  filename allowlists, because the operator wants naming and placement to be
  the configuration.
- Existing user-facing entry-point paths may need compatibility shims if code
  is reorganized into clearer directories.

## Proposed Approach
Adopt one repository-managed validation-profile registry for Black. A JSON
file such as `tool_validation_profiles.json` should define:
- ordered validation profiles;
- the path prefixes or directory classes each profile owns;
- eligible file extensions for each profile;
- the Black target version for each profile;
- the runtime policy key used to select the interpreter that actually runs
  Black; and
- whether the profile may use serial one-file-at-a-time fallback in a known
  affected sandbox.

The core rule should be: path placement plus extension selects the profile.
No profile should be keyed to one specific tracked filename unless the file is
itself a documented compatibility shim.

Discovery should become Git-first instead of filesystem-first:
- for default full-scope Black runs, start from `git ls-files` for tracked
  candidates with supported extensions;
- for explicit directories, resolve the tracked files under those
  directories;
- for explicit ignored files, skip them by default and require an explicit
  override if the operator truly wants to format them; and
- keep a small hardcoded directory blacklist as defense in depth, not as the
  primary policy source.

Runtime policy should split two concerns cleanly:
- bootstrap compatibility: which files must stay runnable on the bootstrap
  floor, such as Python 3.9; and
- steady-state tool runtime: which interpreter actually runs Black and the
  pinned developer toolchain, such as Python 3.12.

That means a bootstrap-profile file can still be formatted by Black running on
the steady-state runtime, while Black applies `--target-version py39` to the
file because of its placement.

To make placement meaningful, repository structure may need one deliberate
cleanup:
- bootstrap entry-point implementations should live in dedicated bootstrap
  directories, for example `scripts/bootstrap/` and matching starter script
  locations; and
- general repository-maintenance code should live in directories that map to
  the steady-state profile by default.

If stable public paths must stay where they are today, keep thin wrappers at
the old paths and classify those wrappers by directory placement or by a
small documented compatibility-shim profile.

Black execution should then work in three stages:
1. discover tracked candidate files;
2. assign each file to a profile from its path and extension; and
3. run Black separately per profile, using the profile's target version and
   runtime policy, plus serial fallback when the current environment matches a
   known affected sandbox constraint.

This should also become the basis for future formatter and linter policy, but
the first implementation scope should stay Black-focused.

## Risks and Mitigations
- Risk: introducing a new JSON profile registry adds configuration
  complexity.
  Mitigation: keep one registry with ordered profiles and a tested schema,
  not multiple overlapping files.
- Risk: directory reorganization can break scripts or documentation.
  Mitigation: keep backward-compatible shims at established entry points
  until the migration is complete.
- Risk: a default fallback profile may hide misclassified files.
  Mitigation: require tests that prove every tracked Python-like file resolves
  to a profile intentionally, and flag unmatched paths explicitly.
- Risk: Git-tracked discovery may skip a new untracked file during local
  formatting.
  Mitigation: allow explicit path arguments to format new files while still
  honoring ignored-path defaults unless the operator overrides them.
- Risk: the sandbox workaround and profile system may diverge.
  Mitigation: make the serial-dispatch decision part of the same profile and
  constraint-resolution path, not a separate ad hoc branch.

## Testing and Validation
Validation should cover both policy logic and workflow behavior:
- unit tests for profile resolution from path plus extension;
- tests that full-scope discovery uses tracked files and skips Git-ignored
  files by default;
- tests that explicit ignored files remain skipped unless an override is
  present;
- tests that bootstrap-profile files resolve to the bootstrap target version
  while ordinary files resolve to the steady-state profile;
- tests that the runtime resolver chooses the documented steady-state
  interpreter when available;
- regression tests that the sandbox serial fallback still runs one file at a
  time when the known affected constraint matches; and
- one deliberate repository-wide normalization pass after approval so Black's
  baseline matches the selected profile policy.

Per Joel Spolsky's shipping guidance, do not treat this work as complete
until the automated tests cover discovery, profile resolution, and runtime
selection, and one approved normalization changeset lands cleanly.

## Alternatives Considered
1. Rely on `.gitignore` alone.
   Rejected because `.gitignore` can exclude local state, but it does not
   express Python target versions, runtime selection, or profile grouping.
2. Keep the current hardcoded blacklist and extend it.
   Rejected because it scales poorly and still leaves tracked-file profile
   resolution undefined.
3. Add explicit filename rules for every exceptional script.
   Rejected because the operator explicitly wants naming and placement to be
   the configuration.
4. Use one universal Black target version for the whole repository.
   Rejected because it does not fit a repository that may need Python-3.9-
   compatible bootstrap entry points and a newer steady-state developer-tool
   runtime.
5. Solve the issue only by repinning Black.
   Rejected because repinning may reduce immediate pain, but it does not
   solve file discovery, placement-driven classification, or the
   bootstrap-versus-steady-state runtime split.

## Open Questions
None at approval time. The approved implementation keeps the first registry
Black-focused, uses placement-plus-extension profile selection, keeps the
existing entry-point paths, and adopts an ordered steady-state runtime policy
with a Python 3.10 minimum and Python 3.12 preference.

## Milestones
1. Approve or revise this proposal.
   Target date: 2026-03-28.
   Owners: operator, AI maintainers.
   Dependencies: review of the linked bug set.
   Entry criteria: proposal exists under review.
   Exit criteria: decision recorded and implementation direction agreed.
2. Draft the specification and profile schema.
   Target date: 2026-03-29.
   Owners: AI maintainers.
   Dependencies: proposal approval.
   Entry criteria: approved proposal.
   Exit criteria: a specification names the registry, discovery rules, and
   runtime policies.
3. Implement discovery and profile resolution.
   Target date: 2026-03-30.
   Owners: AI maintainers.
   Dependencies: approved specification.
   Entry criteria: schema and profile rules are defined.
   Exit criteria: the wrapper resolves files by profile and honors Git-aware
   discovery.
4. Normalize the repository baseline and update docs.
   Target date: 2026-03-31.
   Owners: AI maintainers and operator.
   Dependencies: implementation complete.
   Entry criteria: new logic and tests pass.
   Exit criteria: one deliberate formatter normalization changeset lands and
   documentation explains the bootstrap-versus-steady-state runtime split.

## Adoption and Rollout
Roll this out in phases.

First, approve the model and publish the profile registry plus the
bootstrap-versus-steady-state runtime policy in a specification.

Second, teach the Black wrapper to discover tracked files, resolve profiles by
placement, and use the profile runtime and target settings. Keep the existing
sandbox serial fallback, but make it operate on resolved profile groups.

Third, reorganize bootstrap implementations into placement-significant
directories where needed, leaving compatibility wrappers at old entry points
until documentation and consumers are ready.

Finally, run one intentional repository-wide normalization pass on the chosen
steady-state runtime so future scoped changes can clear Black without
unrelated churn.

## Decision Log
- 2026-03-27T00:30:54-07:00 - Proposal drafted by Codex in response to an
  operator request to resolve the known Black-related bugs with a placement-
  driven validation strategy.
- 2026-03-27T09:26:42-07:00 - Approved by the operator for execution.
- 2026-03-27T12:38:45-07:00 - Implemented on `trunk` with a new
  `tool_validation_profiles.json` registry, Git-first Black discovery,
  managed steady-state runtime selection for Black and starter setup, updated
  downstream installation and drift-refresh paths, regression coverage for
  the new helper behavior, and one deliberate repository-wide Black
  normalization pass on the supported toolchain.
