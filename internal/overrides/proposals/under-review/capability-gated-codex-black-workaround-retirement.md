# Capability-Gated Codex Black Workaround Retirement

| Field | Value |
| --- | --- |
| Title | Capability-Gated Codex Black Workaround Retirement |
| Author | Codex |
| Date | 2026-04-22T11:54:55-07:00 |
| Status | Under Review |
| Reviewers | Matt Heck, repository maintainer/operator |

Related work:
- `internal/overrides/bugs/open/codex-sandbox-asyncio-wakeup-fails-for-`
  `multi-file-static-analysis.txt`
- `internal/overrides/proposals/approved/serial-file-safe-static-analysis-`
  `in-affected-sandboxes.md`
- `standards-and-practices/docs/specifications/codex_sandbox_file_safe_`
  `static_analysis.txt`
- `tool_execution_constraints.json`

## Problem Statement
TheKnowledge serializes Black one file at a time in matched Codex sandboxes
because direct multi-file Black previously hung. The operator asked whether
new Codex CLI and sandbox/container changes make that process hack removable.

The current evidence says no. The exact symptom changed, but the direct
multi-file path remains unsafe in the current sandbox. Direct single-file
Black succeeds. Direct multi-file Black now fails quickly with a
`multiprocessing.managers.SyncManager` `PermissionError` instead of hanging.
`black -W 1` still fails the same way. The existing serial wrapper path
passes. A minimal `loop.call_soon_threadsafe()` probe still fails to wake the
event loop before timeout, and Ruff's ordinary multi-file check still passes.

The current guidance is therefore directionally right, but its evidence and
retirement criteria are too narrow. The issue is no longer only "Black hangs";
it is "the current Codex sandbox still cannot safely run Black's multi-file
concurrency path."

## Goals
- Keep the Black serial fallback until direct multi-file Black is proven safe
  in the active Codex sandbox.
- Replace hang-specific retirement thinking with capability probes.
- Distinguish Black-specific sandbox constraints from tools such as Ruff that
  continue to run normally.
- Preserve final validation quality without forcing one-file execution in
  unaffected shells or CI.
- Give future maintainers a repeatable way to decide whether the workaround
  can be removed.

## Non-Goals
- Removing the current Black serial workaround immediately.
- Serializing Ruff or other tools without evidence.
- Fixing the upstream Codex sandbox from inside TheKnowledge.
- Changing Black versions as part of this proposal.
- Editing guidance before the operator approves the retirement gate.

## Use Cases
1. A maintainer in a Codex sandbox wants to run required checks and avoid a
   broken direct multi-file Black path.
2. A future Codex release fixes both the asyncio wakeup and multiprocessing
   manager socket behavior, and TheKnowledge needs a safe way to remove the
   serial fallback.
3. A consuming project inherits TheKnowledge tooling and wants validation
   behavior determined by measured sandbox capability instead of stale
   environment-variable heuristics.

## Constraints and Assumptions
- The current Codex session sets `CODEX_CI=1`,
  `CODEX_MANAGED_BY_NPM=1`, and `CODEX_SANDBOX_NETWORK_DISABLED=1`.
- Local Codex CLI version is `0.123.0-alpha.8`.
- The managed Python tool runtime used for experiments was
  `/home/mheck/.pyenv/versions/autotomato-runtime-3.12/bin/python`.
- Black version was `26.3.1`; Ruff version was `0.15.7`.
- The default `python` in this shell is 3.9 and does not provide Black or
  Ruff, so the probe must use the managed steady-state tool runtime.

## Proposed Approach
On approval, add a reusable Codex sandbox capability probe and update the
workaround-retirement process to depend on probe results rather than on one
specific historical symptom.

The probe should test, without editing repository files:
- direct single-file Black with `--check --diff`;
- direct multi-file Black with `--check --diff`;
- direct multi-file Black with `-W 1 --check --diff`;
- the repository Black wrapper serial path with `--check --diff`;
- a minimal `loop.call_soon_threadsafe()` wakeup case;
- a minimal `multiprocessing.Manager()` startup case; and
- ordinary Ruff multi-file checking.

The current `tool_execution_constraints.json` entry should remain active
until all Black direct-multi-file probes pass in the active sandbox within a
bounded timeout and without `PermissionError`, timeout, or hang symptoms.
When that happens, TheKnowledge can narrow or remove the serial fallback with
evidence instead of guesswork.

## Evidence From Current Experiment
| Probe | Result |
| --- | --- |
| Direct single-file Black with `--check --diff --fast` | exited `0` |
| Direct multi-file Black with `--check --diff --fast` | exited `1`; `SyncManager` `PermissionError` |
| Direct multi-file Black with `-W 1 --check --diff --fast` | failed with the same `PermissionError` |
| Repository wrapper serial Black path | serialized three files and exited `0` |
| Minimal `loop.call_soon_threadsafe()` worker-thread wakeup | timed out before the future completed |
| Minimal `multiprocessing.Manager()` startup | failed with `PermissionError`, then `EOFError` |
| Direct Ruff multi-file checking | exited `0` |

## Risks and Mitigations
- Risk: keeping the serial fallback costs time after Codex fixes the issue.
  Mitigation: provide a bounded probe that can justify removal quickly.
- Risk: removing the fallback based on startup improvements alone reopens
  formatter failures.
  Mitigation: require direct Black multi-file probes to pass before removal.
- Risk: environment-variable matching stays too broad or too narrow.
  Mitigation: move toward measured capability data while preserving the
  current heuristic until the probe exists.
- Risk: test probes accidentally edit files.
  Mitigation: require `--check --diff` for formatter probes and use temporary
  scratch inputs where new files are needed.

## Testing and Validation
Validation should include the capability probe in the current Codex sandbox,
outside the Codex sandbox when practical, and in at least one consuming
project that uses TheKnowledge's managed tooling. A passing removal gate must
show:
- direct multi-file Black exits successfully;
- `black -W 1` no longer fails on the multi-file path;
- the asyncio wakeup probe completes promptly;
- the multiprocessing manager probe starts and shuts down cleanly;
- Ruff remains unaffected; and
- the standard wrapper path still behaves correctly.

## Alternatives Considered
1. Remove the serial fallback because the old hang did not reproduce.
   Rejected because direct multi-file Black still fails.
2. Keep the fallback forever.
   Rejected because Codex sandbox behavior can improve, and stale workarounds
   should be retired when evidence supports removal.
3. Rely on `black -W 1`.
   Rejected because it still fails on the current direct multi-file path.
4. Serialize every formatter and linter.
   Rejected because Ruff passed normally and broad serialization would add
   unnecessary friction without evidence.

## Open Questions
- Should the probe result be written to a git-ignored cache file so agents can
  avoid re-running the full capability suite during one session?
- Should `tool_execution_constraints.json` eventually support capability
  probe names in addition to environment-variable matches?
- Should the current open bug be renamed from an asyncio wakeup failure to a
  broader Codex sandbox multi-file Black concurrency failure?

## Milestones
1. Approval.
   Entry: the operator accepts capability-gated retirement.
   Exit: the current serial workaround remains active pending probe support.
2. Probe implementation.
   Entry: probe location and output format are chosen.
   Exit: the probe produces human and JSON summaries without editing files.
3. Constraint integration.
   Entry: probe behavior is stable in TheKnowledge.
   Exit: `tool_execution_constraints.json` can be reviewed against measured
   capability data rather than only static environment variables.
4. Workaround retirement.
   Entry: a future Codex baseline passes every removal-gate probe.
   Exit: the serial fallback and related guidance are narrowed or removed,
   and the bug record is closed or reclassified.

## Adoption and Rollout
Do not change current validation behavior until the proposal is approved and
the probe exists. After approval, implement the probe in TheKnowledge first,
then decide whether to propagate it to starter material for consuming
projects. Remove the serial fallback only after current-environment evidence
shows the direct multi-file Black path is safe.

## Decision Log
- 2026-04-22T11:54:55-07:00 - Drafted from non-destructive local
  experiments after a Codex CLI update and `codex-wrangler`
  `--set-reasonable-permissions` changed the sandbox baseline.
