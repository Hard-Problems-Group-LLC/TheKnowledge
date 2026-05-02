# Engineering Change Request: Steady-State Validation Guidance

## Summary

TheKnowledge should make consuming-project validation guidance explicitly
runtime-resolved. Starter instructions, managed AGENTS text, and project-flow
templates should not present ambient `python ...` commands as stable required
checks when a consuming project has a declared steady-state runtime.

This ECR is narrower than the companion tool-environment interrupt ECR. The
interrupt ECR defines what to do after a surprise is observed. This ECR asks
TheKnowledge to prevent that surprise by improving the initial guidance that
agents read before they run checks.

## Incident

During an external project maintenance on 2026-04-22, the agent followed the
local inherited required-check pattern and ran:

```text
python TheKnowledge/scripts/run_tool_with_timeout.py ruff ...
```

That command used the ambient shell `python`, which resolved to a Python 3.9
pyenv shim. the external project's steady-state runtime is the repository
virtualenv Python 3.12. The result was a validation-wrapper failure that
should have been avoided before execution.

TheKnowledge already distinguishes bootstrap Python from steady-state runtime
Python in several places. The problem is that its initial examples and starter
required-check guidance still make it easy for an agent to bypass that
distinction by invoking validation helpers with ambient `python`.

## Current Guidance Gap

TheKnowledge guidance currently says, in effect, to run required checks
such as:

```text
python scripts/run_tool_with_timeout.py ruff
python TheKnowledge/scripts/run_tool_with_timeout.py ruff
```

Those examples are unsafe as general consuming-project guidance because:

- `python` may be a pyenv, system, distro, sandbox, or container interpreter;
- bootstrap Python may intentionally be lower than the steady-state tooling
  floor;
- the validation wrapper may use its launching interpreter for some tools;
- a consuming project may require `.venv/bin/python`, `uv run`, `poetry run`,
  a project-local helper, or another declared runtime entry point; and
- agents may treat a successful fallback as enough instead of noticing that
  the documented path did not actually pass.

## Requested Change

TheKnowledge should update starter guidance so agents must resolve and use the
consuming project's declared steady-state validation runtime before running
checks.

Suggested guidance text:

```text
Before running validation in a consuming project, resolve the project's
steady-state validation runtime from its local runtime/tool profile or local
SOP. Do not invoke validation wrappers through ambient `python`, `python3`,
PATH shims, or other shell-selected executables unless the consuming project
explicitly declares that as the intended validation runtime. If no stable
runtime entry point is documented, stop and establish one before treating
validation results as authoritative.
```

## Template Changes Requested

Update the following TheKnowledge surfaces:

- `standards-and-practices/docs/development-workflow.txt`
  - Add a pre-validation step requiring runtime resolution.
  - Clarify that bootstrap Python compatibility is not validation-runtime
    compatibility.
- `templates/project-management/git-flow.txt`
  - Replace ambient `python {{THEKNOWLEDGE_ROOT}}/scripts/...` examples with a
    placeholder for the consuming project's validation entry point.
  - Instruct consuming projects to define that entry point in their local SOP.
- Managed AGENTS footer guidance
  - Require agents to verify runtime selection before automated validation.
  - Warn that wrong-runtime discovery is an interrupt, not a normal failure.
- Starter or managed-file drift checks
  - Detect stale required-check examples that still use ambiguous bare
    `python` where a managed steady-state runtime is expected.

## Requirements

- Keep bootstrap tooling able to run on the documented bootstrap Python floor.
- Keep steady-state validation tied to the declared steady-state runtime.
- Make consuming projects define a stable validation entry point, such as a
  project-local helper, `.venv/bin/python`, `uv run`, or another explicit
  command family.
- Ensure agents can tell the difference between bootstrap commands and normal
  validation commands.
- Treat missing or ambiguous validation-runtime guidance as a setup defect to
  resolve before clearing development work.
- Update examples and tests so new consuming projects do not inherit ambient
  `python` validation commands by default.

## Non-Goals

- Mandate `.venv` for every consuming project.
- Remove support for lower-version bootstrap Python where bootstrap scripts
  are intentionally compatible.
- Replace the separate immediate-interrupt rule for surprises discovered at
  runtime.
- Redesign TheKnowledge's timeout wrapper in this ECR.

## Recommended Validation

- Build a consuming-project fixture with a bootstrap Python lower than its
  steady-state runtime and confirm generated guidance does not tell agents to
  run validation with ambient `python`.
- Add tests or documentation checks that fail if managed required-check
  examples use bare `python` without also naming a consuming-project runtime
  resolver.
- Confirm the generated starter SOP asks the consuming project to declare its
  validation entry point.
- Confirm the companion interrupt guidance covers what happens when the
  observed runtime still differs from the declared one.

## Relationship To Existing ECRs

This ECR complements:

- `2026-04-22-tool-environment-surprise-interrupt-standard.md`, which defines
  the required stop-and-resolve behavior after a wrong runtime or authority
  boundary is observed.
- the imported standardized commit-helper contract-drift ECR from
  2026-04-16, which covers inconsistent helper entrypoint assumptions in the
  commit and quality-gate stack.

The shared theme is that TheKnowledge should provide one stable consuming-
project entrypoint contract instead of relying on ambient shell state.

## External-Project Adoption Note

An external project adopted the local version on 2026-04-22 by adding a
project-local validation helper, updating
`project-management/git-flow.txt`, adding
`standards-and-practices/docs/specifications/`
`tool_environment_interrupt_contract.txt`, and updating `AGENTS.md`. The
local helper resolves the project `.venv` Python 3.12 runtime before
validation and uses explicit local command scopes where the generic wrapper
defaults would be misleading.
