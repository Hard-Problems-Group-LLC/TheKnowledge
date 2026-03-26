# Templates

The files and directories under `templates/` are starting points for projects
that consume TheKnowledge, usually as a Git submodule.

Copy them into the consuming project root instead of editing them in place
inside the submodule. Use `scripts/initial-setup.py` to install them.

The `project-management/` starter tree includes proposal status directories
(`approved/`, `rejected/`, `deferred/`, and `under-review/`) plus bug status
directories (`open/`, `in-progress/`, and `closed/`). Keep the consuming
project's live records in the installed copy, not inside this submodule.

The starter set also includes `requirements-dev.txt`,
`scripts/dev_setup.py`, and `tool_execution_constraints.json`. Together they
install TheKnowledge's default pinned Black, Ruff, and pytest toolchain plus
a managed registry for known environment-specific tool execution constraints
for consuming projects that have not yet defined a tighter local bootstrap
policy.

When templates contain `{{THEKNOWLEDGE_ROOT}}` or `{$KNOWLEDGE_ROOT}`, the
setup script replaces that placeholder with the submodule path relative to
the consuming project root.

The installer also manages `AGENTS.md` in the consuming project root. It uses
`AGENTS-header.md` and `AGENTS-footer.md` to create or wrap the project file
so local project instructions can live between the managed sections. Before it
rewrites `AGENTS.md`, it removes any existing managed header or footer blocks
so rerunning the installer does not duplicate them.

After updating the submodule, first review the incoming upstream delta in the
TheKnowledge checkout, then run `scripts/report_managed_agents_drift.py` to
compare the consuming project's managed `AGENTS.md` sections plus managed
starter files with the updated templates. The helper prints unified diffs that
both human and AI developers can review before rerunning
`scripts/initial-setup.py --force --template requirements-dev.txt --template`
`scripts --template tool_execution_constraints.json`, review `git diff`, and
stage the resulting submodule-pointer update plus only the intended
project-file changes.

For the normal review-and-adopt path, prefer
`python {$KNOWLEDGE_ROOT}/scripts/update_theknowledge_submodule.py`
` --project-root . --knowledge-root {$KNOWLEDGE_ROOT}`. That helper fetches
and summarizes the upstream delta, adopts the reviewed `trunk` commit, runs
managed drift detection, refreshes the managed starter files when needed, and
leaves a reviewable parent-repo diff without auto-committing.

If that rerun updates `requirements-dev.txt` or `scripts/dev_setup.py`,
refresh the starter toolchain with `python scripts/dev_setup.py` unless the
consuming project intentionally overrides those files. If it updates
`tool_execution_constraints.json`, review the policy change alongside the
submodule update so shared helpers stay aligned with the current managed
constraints.

When contributors need to file TheKnowledge feedback from a consuming project,
prefer the helper flow:
- `python {$KNOWLEDGE_ROOT}/scripts/send_theknowledge_feedback.py prepare`
  ` --project-root . --knowledge-root {$KNOWLEDGE_ROOT}`
- record the Feedback item in the active submodule checkout
- `python {$KNOWLEDGE_ROOT}/scripts/send_theknowledge_feedback.py finish`
  ` --project-root . --knowledge-root {$KNOWLEDGE_ROOT} --message`
  ` "Record TheKnowledge feedback"`
- add `--push` only when the configured remote push URL is writable for the
  current operator
- use `abort` to restore the prior submodule state without finishing

The `project-management/state/` template directory includes
`pending-commit-changes.txt`, which is the short-lived queue for brief commit
summary lines. The standardized commit helper consumes that file as commit
body text and clears it after a successful local commit.

The standardized commit helper also defaults to a review-first staging path.
It lists files about to be staged, asks whether to review them, and
prefers launching Meld when available as the default visual review
path. It can also pause for file-by-file review and runs
`git diff --cached` before commit. Use `--assume-reviewed` only
after an explicit review decision made outside the helper, and use
`--resume-review-prompts` to re-enable prompts for the current shell session.

Managed downstream `AGENTS.md` files also inherit timestamped
intermediary-update guidance for workflow profiling. Use inline
bracketed ISO 8601 prefixes such as
`[2026-03-25T01:05:12-07:00] Running full pytest.` when work begins,
before and after long-running commands or waits, and at major phase
boundaries.
