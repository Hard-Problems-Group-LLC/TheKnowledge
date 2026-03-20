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
- Use `python {$KNOWLEDGE_ROOT}/scripts/git_standard_commit_push.py -m
  "<subject>"` so queued commit summaries become commit body text and the
  queue file is cleared after a successful local commit.
<!-- THEKNOWLEDGE_MANAGED_FOOTER_END -->
