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

## Git Safety
- Before any `git add`, list the files about to be staged and ask the
  operator whether to review them.
- Offer these staging-review choices: `1.` review at least one file in the
  changeset, `2.` proceed without review for this changeset, `3.` proceed and
  suppress review prompts for the rest of the current session until the
  operator asks to resume them.
- If review is requested, prefer changeset review in Meld when
  available as the default visual review path. Otherwise offer
  file-by-file review in the conversation or abort the staging
  step.
- Run `git diff` before any `git add`.
- Run `git diff --cached` before any commit.

## Project Management Orders
- Keep `internal/overrides/backlog.txt` as ordered pending work.
- Keep `internal/overrides/tasks-in-progress.txt` minimal and current.
- Record finished work at the top of
  `internal/overrides/completed-tasks.txt` with ISO 8601 timestamps.
- Track operator actions for AI in `internal/overrides/ai-human-requests.txt`.
- Track proposal records under `internal/overrides/proposals/` using the
  status subdirectories `approved/`, `rejected/`, `deferred/`, and
  `under-review/`.
- Use `internal/overrides/deferred.txt` for explicitly deferred work.
- Queue brief commit-ready summaries in
  `internal/overrides/state/pending-commit-changes.txt`.
- Maintain bug lifecycle summary files under `internal/overrides/bugs/` and
  keep detailed bug records in the status subdirectories `open/`,
  `in-progress/`, and `closed/`.
- Treat `templates/project-management/` as starter material for consuming
  projects, not as TheKnowledge's live state.

## Backlog Iteration
- When told to "iterate the backlog" (or "iterate"), follow exactly one cycle
  from `standards-and-practices/docs/AI-backlog-iteration.txt` unless another
  list is specified.

## Feedback Branch
- The `Feedback` branch is for TheKnowledge-focused bugs, proposals,
  complaints, and general notes discovered while working primarily inside
  some other project that uses TheKnowledge.
- When maintaining TheKnowledge directly as its own checkout, keep using
  the normal `trunk` workflow plus `internal/overrides/`, proposal
  records, and bug tracking. Do not route routine direct-checkout
  maintenance through `Feedback`.
- Periodically inspect `Feedback` while maintaining TheKnowledge itself.
- Backlog evaluation tasks for `Feedback` items on `trunk`. That
  evaluation should produce recommendations.
- If a recommendation is approved, backlog the resulting fix on `trunk` or
  merge the resulting proposal on `trunk`, then remove or update the
  originating `Feedback` entry.
- If an item is not yet resolved, keep it on `Feedback` with additional
  discussion, or drop it from `Feedback` by collaborative human-and-AI
  agreement.

## Knack Validation
- Knack-specific validation should stay lightweight.
- When `.knack.md` files change, run
  `python scripts/run_tool_with_timeout.py knack_check`.
- The validator checks changed knack files for basic Markdown
  well-formedness and high-entropy findings as errors, and reports word-count
  recommendation overruns as warnings.
- The validator uses `.git/knack-validation-cache.json` so unchanged knack
  files can be skipped.
- Projects that use TheKnowledge may keep additional proprietary or
  third-party knacks in the consuming project's top-level `knacks/`
  directory.
- When a project-local knack path collides with a stock TheKnowledge knack
  path, warn and evaluate both files.

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

When `.knack.md` files change, also run
`python scripts/run_tool_with_timeout.py knack_check`.

Use standardized operations where available:
- Commit/push: `python scripts/git_standard_commit_push.py -m "<subject>"`
  The script lists files about to stage, asks for review unless
  `--assume-reviewed` is passed or prompts were disabled earlier in the
  current shell session, runs `git diff` before its own staging steps, runs
  `git diff --cached` before commit, uses
  `internal/overrides/state/pending-commit-changes.txt` as commit body text
  when it is nonblank, and clears the file after a successful local commit.
  Use `--resume-review-prompts` to re-enable prompts for the current shell
  session.
- Pull: `python scripts/git_veteran_pull.py`

## Codex Log Handling
- Do not inspect Codex logs unless explicitly instructed for iteration-log
  analysis.
