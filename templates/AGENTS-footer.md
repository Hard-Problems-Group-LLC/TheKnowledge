<!-- THEKNOWLEDGE_MANAGED_FOOTER_START -->
---

<!-- TheKnowledge-managed footer: place overrides here when the consuming
project needs behavior different from TheKnowledge's own repository setup. -->

## TheKnowledge Overrides
- Use `project-management/backlog.txt` as ordered pending work.
- Keep `project-management/tasks-in-progress.txt` minimal and current.
- Record finished work at the top of
  `project-management/completed-tasks.txt` with ISO 8601 timestamps.
- Track operator actions for AI in `project-management/ai-human-requests.txt`.
- Track proposal records under `project-management/proposals/` using
  `approved/`, `rejected/`, `deferred/`, and `under-review/`.
- Use `project-management/deferred.txt` for explicitly deferred work.
- Queue brief commit-ready summaries in
  `project-management/state/pending-commit-changes.txt`.
- Maintain bug lifecycle summary files under `project-management/bugs/` and
  detailed bug records under `open/`, `in-progress/`, and `closed/`.
- Use `{$KNOWLEDGE_ROOT}/standards-and-practices/docs/`
  `AI-backlog-iteration.txt` when told to iterate the backlog.
- Use the consuming project's own `project-management/git-flow.txt` for branch
  and merge operations.
- Prefer patch-style edits when possible so intended changes stay easy
  to review. Use full-file rewrites only for new files, clearly corrupted
  files, or true total overhauls.
- Run `git diff` before any `git add`. The standardized commit helper does
  this automatically before its own staging steps.
- Use `python {$KNOWLEDGE_ROOT}/scripts/git_standard_commit_push.py -m
  "<subject>"` so queued commit summaries become commit body text and the
  queue file is cleared after a successful local commit.
- When working primarily in the consuming project and discovering bugs,
  proposals, complaints, or general notes about TheKnowledge itself,
  record them on the TheKnowledge `Feedback` branch.
- The `Feedback` branch is only for cross-project feedback flowing back
  into TheKnowledge. Direct maintenance of TheKnowledge itself should keep
  using its normal internal trees on `trunk`.
- Projects may keep proprietary or third-party knacks in the consuming
  project's top-level `knacks/` directory, separate from the stock knacks
  under `{$KNOWLEDGE_ROOT}/knacks/`.
- Validate changed knack files with
  `python {$KNOWLEDGE_ROOT}/scripts/validate_knacks.py --project-root .`.
- Knack validation should stay lightweight: malformed Markdown and
  high-entropy findings are errors, word-count overruns are warnings, the
  validator uses `.git/knack-validation-cache.json`, and path collisions with
  stock knacks should warn while still evaluating both files.
- After updating the TheKnowledge submodule, run
  `python {$KNOWLEDGE_ROOT}/scripts/report_managed_agents_drift.py`
  `--project-root . --knowledge-root {$KNOWLEDGE_ROOT}` to compare managed
  `AGENTS.md` header and footer content with the updated templates.
- If that helper reports drift, rerun
  `python {$KNOWLEDGE_ROOT}/scripts/initial-setup.py --project-root .`
  `--knowledge-root {$KNOWLEDGE_ROOT} --force`, review the resulting
  `git diff`, and then stage only the intended updates.
<!-- THEKNOWLEDGE_MANAGED_FOOTER_END -->
