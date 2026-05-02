# Engineering Change Request: Tool Environment Surprise Interrupt Standard

## Summary

TheKnowledge should define tool-environment surprises as immediate interrupt
conditions. Agents should not continue a validation, formatting, deployment,
or diagnostic sequence after discovering that a command ran under an
unexpected interpreter, container, service account, sandbox, tool version, or
other authority boundary.

## Incident

During an external project maintenance on 2026-04-22, an agent ran the vendored
TheKnowledge timeout wrapper as:

```text
python TheKnowledge/scripts/run_tool_with_timeout.py ruff ...
```

In the active shell, bare `python` resolved to a Python 3.9 pyenv shim. The
project's steady-state runtime is the repository `.venv` Python 3.12. The Ruff
wrapper path then attempted to run Ruff through the wrong interpreter and
failed with a missing-module error. The agent continued by running Ruff
directly through `.venv` and only noted the wrapper failure at the end. That
was the wrong operational response: the environment surprise should have
stopped the sequence immediately.

Follow-up inspection found a related scope surprise: the generic Ruff wrapper
kept its default `.` scope when explicit files were appended, and the generic
compileall wrapper retained a default `src` path that did not exist in the
consuming project. Those cases are also interrupt-class because the observed
tool behavior does not match the operator's intended validation scope.

## Problem

A successful fallback result can mask a broken standard workflow. If agents
continue after an unexpected runtime or authority boundary is discovered, the
project can accumulate validation records that are technically passing but do
not prove that the documented workflow works.

This is especially risky when:

- bootstrap Python and steady-state Python have different version floors;
- the same helper behaves differently depending on `sys.executable`;
- rootless Podman state differs between a user shell and a systemd user
  service;
- container and host execution surfaces have different tool availability; or
- sandbox and host-side validation are intentionally separated.

## Proposed Guidance

Add a standard interruption rule to TheKnowledge-managed workflow guidance:

```text
Getting surprised by the environment or running the wrong tool is an
immediate interrupt condition. If a command runs under an unexpected
interpreter, sandbox, container, service account, rootless-Podman context, or
tool version, stop the current tool sequence, report the mismatch, and resolve
or record it before using the result as validation evidence. Do not silently
substitute a different command and continue as if the documented workflow had
passed.
```

## Requirements

- Distinguish ordinary tool failures from environment surprises.
- Require agents to stop and report when the observed runtime or authority
  boundary differs from the expected one.
- Require a corrected rerun before clearing work.
- Require reusable workflow defects to be captured as a bug, ECR, or
  project-management note.
- Encourage consuming projects to provide narrow validation helpers when bare
  interpreter commands are ambiguous.
- Review TheKnowledge's starter Required Checks examples so consuming
  projects do not inherit ambiguous `python ...` commands where a managed
  steady-state runtime is required.

## Non-Goals

- Treat every lint, test, or type-check failure as an interrupt.
- Forbid documented fallback commands after the surprise has been surfaced and
  resolved.
- Remove support for bootstrap Python where bootstrap tooling intentionally
  supports a lower Python version.

## External-Project Adoption Note

An external project adopted this locally on 2026-04-22 through
`standards-and-practices/docs/specifications/tool_environment_interrupt_contract.txt`,
`project-management/git-flow.txt`, `AGENTS.md`, and the new
project-local validation helper. The helper launches TheKnowledge's
validation path through the managed virtualenv Python, fails loudly when the
expected runtime or required module is missing, and uses explicit local
direct commands where a generic wrapper default scope would be misleading.
