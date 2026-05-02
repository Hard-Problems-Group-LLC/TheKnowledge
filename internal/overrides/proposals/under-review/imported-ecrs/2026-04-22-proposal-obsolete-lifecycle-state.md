# Engineering Change Request: Narrow Obsolete Proposal Lifecycle State

## Summary

TheKnowledge should define a narrow, sparingly used proposal lifecycle state
for approved or historical proposal records that no longer make sense as
active work because later decisions, implementations, or architecture changes
superseded their assumptions.

The state should preserve traceability without polluting active queues. A
reasonable directory name is `obsolete/`, but the important policy is not the
name; it is that agents should use this state rarely and only when a proposal
is neither merely deferred nor rejected on its original merits.

## Incident

During an external project proposal lifecycle audit on 2026-04-22, several
proposal records under `project-management/proposals/approved/` were found to
be complete or incomplete in ordinary ways. One approved proposal was different:
`workspace-report-management-and-cap-hit-status.md` had been partially absorbed
by a newer orthogonal lifecycle-and-incident overlay design.

The proposal's original `cap_hit` terminal-status model no longer matched the
current system. Keeping it in `approved/` made the active queue misleading, but
marking it simply `rejected/` would falsely imply that the original objective
had been denied or was wrong. Marking it `deferred/` would imply it might be
implemented later as written, which was also inaccurate.

an external project therefore created `project-management/proposals/obsolete/`
for this narrow case and retained the record there for traceability.

## Current Problem

The standard proposal lifecycle directories cover common states:

- `under-review/` for proposals not yet accepted;
- `approved/` for accepted work that should still be executable;
- `complete/` for delivered work;
- `deferred/` for valid work intentionally postponed; and
- `rejected/` for work that should not proceed.

They do not clearly cover a proposal that was reasonable when written, was not
rejected, and was not exactly completed, but has become structurally obsolete
because later implementation made its assumptions stale.

Without a defined state, agents tend to leave these records in `approved/`.
That weakens project-management signal because `approved/` stops meaning
"approved and still pending."

## Proposed Guidance

Add a narrow obsolete or superseded lifecycle state to TheKnowledge proposal
management guidance.

Suggested policy text:

```text
Use `obsolete/` sparingly for proposal records whose assumptions no longer
match the current system because later decisions or implementation superseded
them. Do not use `obsolete/` for merely postponed work, disliked work, or work
that remains valid but unfinished. Prefer `deferred/` for valid postponed work,
`rejected/` for work that should not proceed, and `complete/` for delivered
work. When moving a proposal to `obsolete/`, retain a short note explaining
what superseded it and which current record or implementation now owns the
intent.
```

The directory name could also be `superseded/`. If TheKnowledge prefers
operator-facing precision over brevity, `superseded/` may be better. If it
prefers a broad archival category for stale assumptions, `obsolete/` is
adequate. In either case, the standard should warn that the state is rare.

## Requirements

- Preserve historical proposal records for traceability.
- Keep `approved/` limited to executable, still-pending approved work.
- Distinguish obsolete or superseded records from deferred and rejected work.
- Require a short supersession rationale when moving a record into this state.
- Require agents to use the state sparingly.
- Update proposal index generation guidance so unknown or new lifecycle
  directories remain visible in generated proposal catalogs.
- If rendered proposal companions exist, move or regenerate them together with
  their source records so stale HTML companions are not left behind.

## Non-Goals

- Create a dumping ground for uncomfortable, vague, or low-priority work.
- Replace `deferred/` for valid work that should happen later.
- Replace `rejected/` for proposals that should not proceed.
- Require every project to add an obsolete directory before it has a real use
  case.

## Recommended Validation

- Add a starter project-management fixture with one obsolete or superseded
  proposal and confirm proposal index generation includes it.
- Add guidance that moving proposal lifecycle records should move source and
  rendered companions together.
- Confirm `approved/` counts exclude obsolete records.
- Confirm generated indexes label the directory clearly as `Obsolete` or
  `Superseded`.

## External-Project Adoption Note

An external project adopted this locally on 2026-04-22 after a critical review
of approved proposals. The state was used for one proposal whose specific
`cap_hit` terminal-status design had been superseded by the newer orthogonal
workspace lifecycle and incident overlay model. Six divergent stale rendered
HTML companions were also preserved under an obsolete holding subtree rather
than deleted, because they were not byte-identical to the complete-directory
copies.
