# Retire Obsolete Codex Bubblewrap Startup Fallbacks

| Field | Value |
| --- | --- |
| Title | Retire Obsolete Codex Bubblewrap Startup Fallbacks |
| Author | Codex |
| Date | 2026-04-22T11:54:55-07:00 |
| Status | Under Review |
| Reviewers | Matt Heck, repository maintainer/operator |

Related work:
- `internal/overrides/bugs/open/bubblewrap-argv0-sandbox-incompatibility.txt`
- `internal/specifications/repo_local_codex_cli_isolation.txt`
- `standards-and-practices/docs/AI-sandbox-configuration.txt`

## Problem Statement
TheKnowledge currently carries an open bug record for a Codex sandbox startup
failure caused by an old system `bubblewrap` binary that does not support
`--argv0`. That failure previously forced escalated command fallbacks even
for ordinary read-only shell commands and made normal patching fragile.

The current local Codex baseline is materially better. `codex-wrangler`
metadata now reports `reasonable_permissions_enabled: true`, the local Codex
CLI is `0.123.0-alpha.8`, and ordinary non-escalated commands run in the
sandbox. The active `PATH` resolves `bwrap` to a user-local `0.11.1` binary
that supports `--argv0`.

The old host risk is not gone entirely. `/usr/bin/bwrap` remains version
`0.6.3`, still lacks `--argv0`, and still fails when invoked directly with
that option. Any future Codex launch path that bypasses the user-local
`bwrap` can regress to the old startup failure.

## Goals
- Retire guidance or workflow assumptions that treat sandbox startup failure
  as the normal current Codex path on this host.
- Keep the retirement capability-gated, not version-gated only.
- Preserve the open bug record until the operator accepts the new closure
  criteria or decides that alpha-channel behavior is sufficient.
- Keep repository content free of host-specific bubblewrap shims.
- Make future startup regressions quick to diagnose without escalating first.

## Non-Goals
- Removing the Black multi-file sandbox workaround.
- Changing `codex-wrangler` itself.
- Requiring every consuming project to use a repo-local Codex install.
- Replacing the system `/usr/bin/bwrap` package from inside TheKnowledge.

## Use Cases
1. An AI maintainer starts a direct TheKnowledge maintenance session after a
   Codex CLI upgrade and needs to know whether ordinary sandboxed commands
   can run without escalation.
2. A consuming project inherits TheKnowledge guidance and wants to avoid
   carrying obsolete warnings about a startup failure that no longer occurs
   in its current Codex baseline.
3. A future Codex release changes its sandbox launcher again, and the
   maintainer needs a small reproducible probe that identifies whether the
   old `--argv0` failure has returned.

## Constraints and Assumptions
- The current evidence was gathered on 2026-04-22 in the TheKnowledge
  checkout under `codex-cli 0.123.0-alpha.8`.
- `codex-wrangler` reported `reasonable_permissions_enabled: true`.
- The active shell resolved `bwrap` to `/home/mheck/.local/bin/bwrap`,
  version `0.11.1`.
- `/usr/bin/bwrap` remained version `0.6.3` and still lacked `--argv0`.
- Closure criteria should account for the operator's prior preference to
  keep the old bug open until the fix is no longer alpha-only.

## Proposed Approach
On approval, replace the old "startup is broken, use escalation" posture with
a capability-gated startup probe and bug-lifecycle update.

The probe should verify:
- ordinary non-escalated shell execution succeeds;
- active `bwrap` resolution and version;
- whether the active `bwrap --help` advertises `--argv0`;
- whether `/usr/bin/bwrap` still lacks required capabilities; and
- the local Codex CLI version and `codex-wrangler` managed-permissions state
  when those metadata files exist.

If the probe passes, TheKnowledge can close or reclassify the old bubblewrap
startup bug as "host hazard retained for diagnostics, not active workflow
blocker." If the probe fails, guidance should continue to recommend guarded
fallbacks without pretending the current session is healthy.

The implementation should prefer a reusable diagnostic script with a
machine-readable output mode rather than ad hoc shell snippets.

## Evidence From Current Experiment
| Probe | Result |
| --- | --- |
| `./bin/codex-local --version` | `codex-cli 0.123.0-alpha.8` |
| `.codex-local/.codex-wrangler.json` | `reasonable_permissions_enabled: true` |
| `which bwrap` | `/home/mheck/.local/bin/bwrap` |
| `bwrap --version` | `bubblewrap 0.11.1` |
| `bwrap --help` | listed `--argv0` |
| `/usr/bin/bwrap --version` | `bubblewrap 0.6.3` |
| `/usr/bin/bwrap --argv0 test true` | failed with `bwrap: Unknown option --argv0` |
| Ordinary non-escalated repository commands | completed successfully |

## Risks and Mitigations
- Risk: closing the old bug too aggressively hides a still-present host
  package hazard.
  Mitigation: record the system-binary hazard separately in the bug closure
  note and require the capability probe to pass before simplifying guidance.
- Risk: alpha-channel Codex behavior differs from stable behavior.
  Mitigation: make channel and version part of the recorded probe output.
- Risk: future maintainers mistake the user-local `bwrap` path for a system
  repair.
  Mitigation: report both active-path and `/usr/bin/bwrap` capability data.

## Testing and Validation
Validate the accepted change by running the startup probe in:
- the direct TheKnowledge checkout;
- at least one consuming project with a repo-local Codex install; and
- a shell where the user-local `bwrap` path is intentionally absent, if
  practical, to confirm the probe catches the old failure.

The validation must not edit repository files. It should print a concise
human summary and optionally emit JSON for issue records or CI logs.

## Alternatives Considered
1. Close the old bug immediately.
   Rejected because `/usr/bin/bwrap` still lacks `--argv0`, and the operator
   previously wanted non-alpha/mainline closure evidence.
2. Keep all old guidance unchanged indefinitely.
   Rejected because it would preserve unnecessary escalation bias where the
   current sandbox startup path is healthy.
3. Replace `/usr/bin/bwrap` as part of repository maintenance.
   Rejected because that is host administration, not TheKnowledge content.

## Open Questions
- Should alpha-channel Codex plus passing local probes be sufficient to close
  the old bug, or should closure still wait for stable/mainline Codex?
- Should the probe live under `scripts/` for direct repository maintenance or
  under `standards-and-practices/dev-utils/` for managed propagation?
- Should consuming-project starter material include this probe by default or
  only document how to copy it when Codex sandbox startup fails?

## Milestones
1. Approval.
   Entry: this proposal is accepted by the operator.
   Exit: closure criteria are chosen for the old bubblewrap bug.
2. Probe implementation.
   Entry: scope and location are decided.
   Exit: the probe reports startup capability data without editing files.
3. Guidance cleanup.
   Entry: the probe passes in target environments.
   Exit: obsolete escalation-first wording is removed or narrowed, and the
   old bug record is closed or reclassified.

## Adoption and Rollout
Apply the cleanup first in TheKnowledge's direct-checkout records, then
refresh starter guidance only if the operator approves propagation to
consuming projects. Keep the old bug reference available for historical
diagnostics even after active workflow guidance is simplified.

## Decision Log
- 2026-04-22T11:54:55-07:00 - Drafted from non-destructive local
  experiments after the operator enabled `codex-wrangler`
  `--set-reasonable-permissions`.
