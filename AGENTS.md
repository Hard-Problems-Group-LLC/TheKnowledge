# Engineering Guidance

This repository stores reusable standards, SOPs, and operational tooling for
software projects.

Start every engagement by reading
`standards-and-practices/docs/development-workflow.txt` for workflow
sequencing and status tracking. Then read
`templates/project-management/git-flow.txt` for branch and merge operations.
When working inside TheKnowledge itself, interpret `{{THEKNOWLEDGE_ROOT}}` in
that template as the repository root. Finally, check
`.git/codex-local-notes.txt` for local-only operator notes when present. When
`internal/README.md` exists, read it next. When `internal/overrides/README.txt`
exists, use the override record locations it defines for this repository's
live state.

## Style and Documentation
- Write clear, direct prose aligned with Chicago Manual of Style guidance.
- Prefer explicit, self-documenting code and scripts.
- Maintain Python 3.9+ compatibility unless explicitly waived.
- Wrap documentation and standards text files to 78 columns.

## Contribution Rules
- Write or update specifications before implementation when behavior changes.
- Keep standards and process docs concise, actionable, and testable.
- Preserve append-only history in project-management records.

## Project Management Orders
- Keep `internal/overrides/backlog.txt` as ordered pending work.
- Keep `internal/overrides/tasks-in-progress.txt` minimal and current.
- Record finished work at the top of
  `internal/overrides/completed-tasks.txt` with ISO 8601 timestamps.
- Track operator actions for AI in `internal/overrides/ai-human-requests.txt`.
- Use `internal/overrides/deferred.txt` for explicitly deferred work.
- Queue brief commit-ready summaries in
  `internal/overrides/state/pending-commit-changes.txt`.
- Maintain bug lifecycle files under `internal/overrides/bugs/`.
- Treat `templates/project-management/` as starter material for consuming
  projects, not as TheKnowledge's live state.

## Backlog Iteration
- When told to "iterate the backlog" (or "iterate"), follow exactly one cycle
  from `standards-and-practices/docs/AI-backlog-iteration.txt` unless another
  list is specified.

## Testing Expectations
- Use pessimistic, defense-in-depth tests.
- Cover edge cases, failure modes, and regressions.
- Keep reusable fixtures deterministic.
- Prefer reusable scripted smoke checks over one-off shell snippets.

## Cross-platform Validation Expectations
- Keep Linux-side Windows wrapper validation aligned with
  `standards-and-practices/docs/testing/windows/` and its specification.
- Keep Windows-side Linux validation aligned with
  `standards-and-practices/docs/testing/wsl2/` and its specification.
- Treat native CI on target OS as the final compatibility gate.

## Required Local Checks
1. `python scripts/run_tool_with_timeout.py black`
2. `python scripts/run_tool_with_timeout.py ruff`
3. `python scripts/run_tool_with_timeout.py compileall`
4. `python scripts/run_tool_with_timeout.py entropy_check`
5. `python scripts/run_tool_with_timeout.py entropy_tripwire_verify`
6. `python scripts/run_tool_with_timeout.py pytest`

Use standardized operations where available:
- Commit/push: `python scripts/git_standard_commit_push.py -m "<subject>"`
  The script uses
  `internal/overrides/state/pending-commit-changes.txt` as commit body text
  when it is nonblank, then clears the file after a successful local commit.
- Pull: `python scripts/git_veteran_pull.py`

## Codex Log Handling
- Do not inspect Codex logs unless explicitly instructed for iteration-log
  analysis.
