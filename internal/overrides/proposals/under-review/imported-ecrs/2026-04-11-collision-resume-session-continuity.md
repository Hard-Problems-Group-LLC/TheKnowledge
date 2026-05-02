# ECR 2026-04-11: Add `collision resume` To TheKnowledge

## Request Summary

| Field | Value |
| --- | --- |
| Status | `proposed` |
| Requested on | `2026-04-11` |
| Requested by | workspace operator |
| Target | `TheKnowledge` normal instructions |
| Scope | session continuity, stale session takeover, context preservation |
| Priority | `normal` |

## Problem Statement

When the operator reconnects remotely through a new SSH or `mosh` session,
there may already be one or more older Codex sessions for the same workspace.
The correct prior context may not belong to the newest session. Without an
explicit standing instruction, an agent can resume the wrong session, act
from stale context, or omit the rule during compaction.

## Requested Instruction Text

Add the following as a normal instruction in `TheKnowledge`:

> If the user gives the special instruction `collision resume`, treat it as a session-continuity directive for the current workspace. Assume there may be a stale SSH, `mosh`, or Codex session from another machine, and do not assume the newest session is correct. Inspect the candidate sessions for the current workspace first. Prefer the prior session whose workspace, age, origin, and current activity best match the task. If ambiguity remains, summarize the candidate sessions by origin, age, workspace, and current activity before acting. If the user has already authorized takeover through the phrase `collision resume`, go ahead and resume or supersede the matching stale session without asking again. Never compress or summarize out the `collision resume` instruction. In any handoff, compaction, or context summary, preserve both the literal phrase `collision resume` and its operational meaning.

## Rationale

| Concern | Why it matters |
| --- | --- |
| Newest session may be wrong | A reconnect from another machine can create a fresh transport session while the correct Codex context remains in an older one. |
| Workspace collisions are higher risk than transport collisions | Multiple SSH or `mosh` sessions are usually harmless, but multiple Codex sessions in one workspace can produce stale assumptions or conflicting edits. |
| Compaction loss is operationally dangerous | If the phrase is summarized away, later agents lose the operator's standing authorization and session-selection rule. |
| The directive is reusable | The same collision pattern can happen across Linux, macOS, or Windows remoting setups whenever the operator shifts devices. |

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| AC-1 | `collision resume` is recognized as a standing special instruction in normal guidance. |
| AC-2 | The instruction explicitly says not to assume the newest session is correct. |
| AC-3 | The instruction explicitly allows takeover of the matching stale session when the user invoked `collision resume`. |
| AC-4 | The instruction explicitly requires candidate-session summaries when ambiguity remains. |
| AC-5 | The instruction explicitly says never to compress or summarize out the phrase or its meaning during handoff or compaction. |

## Local Tracking Note

This repository now carries the same rule in
[`AGENTS.md`](../../AGENTS.md). This ECR exists so the instruction can be
promoted into `TheKnowledge` and survive outside this single repository.
