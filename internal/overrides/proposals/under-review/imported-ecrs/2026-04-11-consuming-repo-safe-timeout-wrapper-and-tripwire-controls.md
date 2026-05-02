# ECR 2026-04-11: Consuming-Repo-Safe Timeout Wrapper and Tripwire Controls

## Request Summary

| Field | Value |
| --- | --- |
| Status | `proposed` |
| Requested on | `2026-04-11` |
| Requested by | workspace operator |
| Target | `TheKnowledge` quality-gate tooling |
| Scope | vendored timeout-wrapper path resolution, entropy-tripwire usability in consuming repositories |
| Priority | `high` |

## Problem Statement

an external project vendors `TheKnowledge/` and runs the timeout wrapper from
the consuming-project root. Two issues surfaced in that mode.

First, `TheKnowledge/scripts/run_tool_with_timeout.py` launched configured
tool scripts like
`standards-and-practices/dev-utils/security/verify_entropy_tripwire.py`
relative to the consuming-project root, not relative to the owning
`TheKnowledge/` checkout. That made `entropy_tripwire_verify` fail
immediately in consuming repositories unless they mirrored TheKnowledge's
directory layout at the top level.

Second, after that local launch-path bug was repaired, the
`verify_entropy_tripwire.py` full-repository check still remained a poor fit
for a generated-artifact-heavy consuming repository. It ran silently for long
enough to hit its own `120s` timeout, which makes it operationally
indistinguishable from a hang.

## Requested Direction

Improve TheKnowledge so its quality-gate tooling behaves correctly and
legibly when used from a consuming repository that vendors TheKnowledge.

### 1. Wrapper-owned script paths must resolve relative to the wrapper tree

When `tool_timeouts.json` names a relative helper script path, for example:

- `scripts/validate_knacks.py`
- `scripts/windows/verify-windows-shims-linux.sh`
- `standards-and-practices/dev-utils/security/verify_entropy_tripwire.py`

the timeout wrapper should resolve that path relative to the owning
TheKnowledge checkout when the path does not exist relative to the current
working directory.

This lets one config file work both:

- inside TheKnowledge itself; and
- inside consuming repositories that invoke the vendored wrapper from their
  own repository root.

### 2. Entropy tripwire verification needs a consuming-repo control surface

The current full-repository tripwire model does not scale well to large
generated-artifact trees. TheKnowledge should offer at least one explicit
mechanism so consuming repositories can keep the tripwire honest without
pretending a broken or impractical full-repo run is a required gate.

Acceptable directions include:

- repo-local path scopes;
- repo-local exclude controls;
- an explicit consuming-project opt-out path documented in managed guidance;
- or a documented alternate verification mode that keeps the tripwire useful
  on large generated trees.

### 3. Long-running tripwire phases should report progress

Even when the verifier is still doing correct work, it currently emits no
useful signal until an entire scan phase finishes. Add phase-level progress
or milestone output so operators can distinguish "working slowly" from
"wedged or dead."

## Why This Matters

| Concern | Why it matters |
| --- | --- |
| Broken vendored path handling | Consuming projects cannot reliably run TheKnowledge's own helper scripts from the repository root. |
| False sense of mandatory validation | Managed instructions say tripwire verification is required, but some consuming repositories cannot run it practically as-is. |
| Silent long-running scans | Operators lose confidence in the gate because no output appears until timeout or completion. |
| Generated-artifact-heavy repos are common | Large report trees, vendored content, and generated HTML/PDF artifacts are normal in some consumers. |

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| AC-1 | `run_tool_with_timeout.py` resolves configured relative helper-script paths against the owning TheKnowledge checkout when they are absent from the current working directory. |
| AC-2 | TheKnowledge tests cover both Python-script and shell-script relative helper paths in a consuming-repository-style invocation context. |
| AC-3 | TheKnowledge documents or implements an explicit consuming-repository control path for `entropy_tripwire_verify` when a full-repository run is not practical. |
| AC-4 | Tripwire verification emits phase-level progress or equivalent milestones during long-running scans. |
| AC-5 | Managed guidance stops implying that every consuming repository can or should run an unscoped full-repository tripwire check unchanged. |

## Local Tracking Note

An external project now carries a local fix for the timeout-wrapper path
resolution issue in its vendored `TheKnowledge/scripts/run_tool_with_timeout.py`.
It also documents a local disable for normal entropy-tripwire use because the
full-repository verifier times out on this repository. This ECR exists so the
upstream TheKnowledge tree can absorb the portable fix and define a better
consuming-repository story for tripwire verification.
