# Engineering Change Request: Cross-Project Change Confirmation

## Summary

TheKnowledge should require AI agents to get explicit confirmation, in the
current session, before making filesystem, service, container, or project-
management changes outside the active project.

## Incident

During an external project session on 2026-04-22, the operator accidentally
sent an external-project UI-change request to the wrong terminal tab. The
request referenced:

```text
external project viewer URL
```

The agent correctly inferred that the target page belonged to
`/path/to/external-project-code`, not the active
an external project workspace. However, after a follow-up clarification that
mentioned `header.content__header`, the agent treated the clarification as
sufficient approval to patch the external project from the external project
session.

That was the wrong operational response. The agent should have stopped and
asked for explicit cross-project authorization before writing to the other
repository, especially because a separate Codex process was already active in
the external project workspace.

## Problem

Interactive operators often have multiple terminal tabs, editor panels, or
Codex sessions open at the same time. A request can be sent to the wrong tab,
or a pasted URL can refer to a service owned by a different repository. In
that situation, inference alone is not safe enough.

Command-level escalation approval is also not sufficient by itself. A user
may approve a narrow filesystem operation without realizing the session has
crossed from one project into another. The confirmation must happen at the
intent level, before the agent edits, restarts, deploys, stages, commits, or
updates project-management records in a different project.

## Proposed Guidance

Add a cross-project boundary rule to TheKnowledge-managed agent guidance:

```text
Before making changes outside the active project, stop and ask for explicit
cross-project confirmation in the current session. The confirmation must name
the active project, the target project or path, and the intended change class.
Do not infer authorization from a URL, adjacent discussion, a prior session,
or a command-escalation approval. Read-only inspection may proceed when it is
necessary to identify the boundary, but mutating work must wait for explicit
operator confirmation.
```

## Requirements

- Define "cross-project change" to include edits, deletes, generated files,
  project-management records, service restarts, container rebuilds, queued
  jobs, commits, pushes, and deployments outside the active project root.
- Require confirmation on a session-by-session basis; prior approval in
  another session does not carry over.
- Require the agent to state the active project and target project before
  asking for confirmation.
- Require the agent to disclose any detected active writer in the target
  project before proceeding.
- Allow bounded read-only inspection when needed to identify the owning
  project, service, or repository.
- Treat accidental wrong-terminal or wrong-tab requests as plausible until
  explicit cross-project confirmation resolves the ambiguity.
- Clarify that sandbox or escalation approval is not a substitute for
  cross-project intent confirmation.

## Suggested Confirmation Pattern

When the target differs from the active project, ask a concrete question such
as:

```text
This session is active in an external project, but the requested page appears to
be served by an external project at /path/to/external-project-code. Do you
want this external-project session to edit external project files and, if
needed, restart the external project viewer service?
```

If another writer is detected, include it:

```text
I also see an active Codex process in the external project workspace. Confirm
whether this session should proceed anyway, hand off to that session, or stop.
```

## Non-Goals

- Prevent cross-project work when the operator explicitly authorizes it.
- Block read-only orientation needed to discover the project boundary.
- Require confirmation for vendored standards reads, documentation references,
  or ordinary dependency inspection that does not mutate another project.
- Replace existing `collision resume` rules. This rule complements them by
  requiring explicit confirmation before crossing project boundaries.

## Acceptance Criteria

- Managed `AGENTS.md` guidance and workflow documents include the rule.
- Agents must interrupt before mutating outside the active project root.
- Standard confirmation language names both active and target projects.
- Active-writer detection is recommended before proceeding with target
  project changes.
- Future consuming projects can adopt the rule without custom local wording.
