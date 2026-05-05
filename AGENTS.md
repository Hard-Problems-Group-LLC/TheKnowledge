# Engineering Guidance

This repository stores reusable standards, SOPs, and operational tooling for
software projects.

Start every engagement by reading
`standards-and-practices/docs/development-workflow.txt` for workflow
sequencing and status tracking. Then read
`templates/project-management/git-flow.txt` for branch and merge operations.
When working inside TheKnowledge itself, interpret `{{THEKNOWLEDGE_ROOT}}` in
that template as the repository root. Finally, check
`.git/codex-local-notes.txt`, `.local/ai-local-notes.md`, and
`.local/ai-local-notes.txt` for local-only operator notes when present. When
`internal/README.md` exists, read it next. When
`internal/overrides/README.txt` exists, use the override record locations it
defines for this repository's live state.

## Style and Documentation
- Write clear, direct prose aligned with Chicago Manual of Style guidance.
- Prefer Markdown (`.md`) for maintained prose documents, internal records,
  starter documents, and generated consumer-project guidance unless a file is
  machine-consumed, intentionally extensionless, or temporarily kept in a
  legacy format during an explicit migration.
- Treat documentation as delivery work. Every maintained source file should
  carry top-of-file context, every type and callable should be documented,
  and non-trivial control flow should carry local rationale where structure
  alone would be ambiguous.
- Bootstrap, setup, prerequisite, and environment-selection code should
  follow Python 3.9 best practices unless a higher floor is documented.
- Normal runtime, automation, test, and developer-tooling code should follow
  Python 3.12 best practices unless a component is intentionally constrained.
- Wrap documentation and standards Markdown/text files to 78 columns. Tables
  and other Markdown structures that cannot tolerate that width should stay
  at 118 columns when practical, or use the narrowest readable open-ended
  width when the structure requires it.

## Contribution Rules
- Write or update specifications before implementation when behavior changes.
- Keep standards and process docs concise, actionable, and testable.
- Preserve append-only history in project-management records.

## Critical Context
- Load this file before running automated tooling that edits, validates,
  stages, or tests repository files.
- Keep the live-state override record map and any repository-specific
  non-destructive safety boundaries in active context rather than
  summarizing them away.

## Local-Only Policy Inputs
- Project-root `.local/` is the standard home for checkout-local operator
  state and untracked policy inputs.
- Load `.local/ai-local-notes.md` or `.local/ai-local-notes.txt` before broad
  automation, validation, staging, or cleanup when either file exists.
- Treat `.git/codex-local-notes.txt`, `.local/ai-local-notes.md`,
  `.local/ai-local-notes.txt`, and `.theknowledge-restricted-names.local` as
  local-only policy inputs: obey them when present, never add them to Git,
  and do not copy their contents into tracked docs unless the operator
  explicitly directs that.
- Keep local wrappers and mutable maintenance tooling under `.local/`, for
  example `.local/bin/` and `.local/theknowledge-tool-runtime/`, rather than
  under `.git/`.
- Keep the managed `.gitignore` baseline in place so `.local/`,
  `.theknowledge-restricted-names.local`, and known local Codex artifacts are
  ignored even before those paths exist.

## Restricted External-Project Names
- TheKnowledge must not name external client projects that include
  TheKnowledge. In maintained TheKnowledge content, write `an external
  project` instead of a client-project name unless an operator explicitly
  approves a narrow exception.
- Keep the restricted-name source list local and untracked. Use
  `.theknowledge-restricted-names.local` in this checkout, or an equivalent
  out-of-tree local list, and never add that list to Git.
- Do not flag the restricted-name list itself. Validation or review scans
  must skip the configured local list path and any other explicitly local
  policy-input path.
- Treat path-component hits as hard stops. If a restricted name appears as a
  directory or filename component, stop, report the offending path class, and
  ask the operator how to resolve it before renaming, deleting, redacting, or
  moving anything.
- For non-path prose or code references, replace the restricted name with
  `an external project` or another operator-approved generic phrase.
- Imported ECR holding directories must use project-neutral names such as
  `imported-ecrs/`, not source-project names. Keep imported ECR basenames
  unchanged as source-facing identifiers, and track accepted or implemented
  files in `internal/overrides/proposals/accepted-ecrs-list.md`.
- If an imported ECR filename collides with an existing imported ECR
  filename, stop and ask the operator how to disambiguate before overwriting,
  renaming, merging, or dropping either file.

## Workflow Profiling
- For substantive development work, prefix intermediary status
  updates with an inline bracketed ISO 8601 timestamp including the
  timezone offset, for example
  `[2026-03-25T01:05:12-07:00] Running full pytest.`
- Use timestamped updates when work begins, before and after
  commands or waits likely to take more than a few seconds, and at
  major phase boundaries.
- Include elapsed durations when they are easy to compute.
- Keep final answers readable; this rule applies to intermediary
  development updates for workflow profiling, not to every sentence
  of casual chat.

## Git Safety
- Before any `git add`, list the files about to be staged and ask the
  operator whether to review them.
- Offer these staging-review choices: `1.` review at least one file in the
  changeset, `2.` proceed without review for this changeset, `3.` proceed and
  suppress review prompts for the rest of the current session until the
  operator asks to resume them.
- If review is requested, prefer changeset review in Meld when
  available as the default visual review path.
- Launch `meld .` from the repository or submodule root so Meld opens its
  version-control view for the full working tree.
- If Meld version-control view is unavailable or unsuitable, compare a
  temporary clean snapshot directory against the working tree in Meld's
  folder-comparison mode.
- Otherwise offer file-by-file review in the conversation or abort the
  staging step.
- Never guess a Git author or committer email address from commit history,
  hostnames, remote URLs, network overlays, or similar context.
- Require an explicit commit identity before creating a commit. Prefer
  configured `git` properties such as `user.name` and `user.email`; explicit
  `GIT_COMMITTER_*` and optional separate `GIT_AUTHOR_*` overrides are
  acceptable when set deliberately.
- When a separate author identity is not explicitly configured, reuse the
  explicit committer identity for author instead of inventing a second
  address.
- Run `git diff` before any `git add`.
- Run `git diff --cached` before any commit.

## Project Management Orders
- Keep `internal/overrides/backlog.txt` as ordered pending work.
- Keep `internal/overrides/tasks-in-progress.txt` minimal and current.
- Record finished work at the top of
  `internal/overrides/completed-tasks.txt` with ISO 8601 timestamps.
- Track operator actions for AI in `internal/overrides/ai-human-requests.txt`.
- Track proposal records as Markdown files under
  `internal/overrides/proposals/` using the
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
- When that feedback is discovered from a consuming project, use the active
  `TheKnowledge/` submodule in that project. Prefer
  `python TheKnowledge/scripts/send_theknowledge_feedback.py prepare` and
  `finish` so the helper captures and restores the submodule state for you.
  Use `--push` only when the configured remote push URL is writable for the
  current operator.
- When that consuming-project checkout is effectively read-only for upstream
  maintenance, draft the request first under `ECRs/TheKnowledge/open/` in
  the consuming project so the handoff stays reviewable before it reaches a
  writable TheKnowledge checkout. Move the record to
  `ECRs/TheKnowledge/in-progress/` when active upstream handling begins, and
  move it to `ECRs/TheKnowledge/closed/` when a TheKnowledge proposal,
  implementation, rejection, or deferral record resolves it. Closed records
  should note which TheKnowledge record or commit settled the request.
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
- The validator uses `.git/knack-validation-cache.json` when a writable
  Git-backed cache path is available and falls back to
  `.cache/knack-validation-cache.json` otherwise so unchanged knack files can
  be skipped safely in non-Git contexts.
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
- Follow `tool_execution_constraints.json` when it marks a
  tool-and-environment combination unsafe to parallelize.
- In a matched Codex sandbox, run Black only through
  `python scripts/run_tool_with_timeout.py black`; the harness will fall back
  to exactly one file at a time when Black would otherwise hit the known
  multi-file hang. Do not assume `black -W 1` is sufficient.
- If another file-safe formatter or linter hangs in a Codex sandbox on a
  multi-file run, retry the explicit file list one file at a time, and rerun
  the full required checks outside the affected sandbox or in CI before
  clearing the work.

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
  `git diff --cached` before commit, rejects commits whose author/committer
  identity is not explicitly configured, uses
  `internal/overrides/state/pending-commit-changes.txt` as commit body text
  when it is nonblank, and clears the file after a successful local commit.
  Use `--resume-review-prompts` to re-enable prompts for the current shell
  session.
- Pull: `python scripts/git_veteran_pull.py`

## Local Tool Runtime
- When maintaining TheKnowledge directly and no compliant steady-state Python
  tools runtime is available yet, run
  `python scripts/ensure_theknowledge_tool_runtime.py` to create or refresh
  `.local/theknowledge-tool-runtime/`.
- `scripts/run_tool_with_timeout.py` and
  `scripts/run_quality_gate_cached.py` will ensure that checkout-local runtime
  automatically in a direct TheKnowledge checkout when no deliberate
  `THEKNOWLEDGE_PYTHON_TOOLS` override is already set.
- Do not borrow another project's Python environment merely because it
  happens to satisfy the required imports. Fix the local TheKnowledge runtime
  instead.

Shortcut:
- `ACP` means "add, commit, push" through the repository's VCS workflow. It
  is an order to stage, commit, and push meaningful blocks of work with
  appropriate commit messages; it is not an instruction to collapse unrelated
  changes into one monolithic commit.

## Codex Log Handling
- Do not inspect Codex logs unless explicitly instructed for iteration-log
  analysis.

## Local Codex CLI
- Treat `.codex-local/` as repository-local operator tooling for repo-scoped
  Codex CLI installs when it exists.
- Treat `.codex-home/`, `README-LOCAL-Start-Codex.md`, and
  `bin/codex-local` as operator-local generated artifacts when they exist.
- Do not classify `.codex-local/package.json` as a tracked project dependency
  manifest for TheKnowledge itself.
- Prefer `python scripts/codex_local.py` when repo-local Codex CLI invocation
  is needed without remembering `npx --prefix` details. Do not rely on
  generated helper launchers being present.
