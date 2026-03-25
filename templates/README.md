# Templates

The files and directories under `templates/` are starting points for projects
that consume TheKnowledge, usually as a Git submodule.

Copy them into the consuming project root instead of editing them in place
inside the submodule. Use `scripts/initial-setup.py` to install them.

The `project-management/` starter tree includes proposal status directories
(`approved/`, `rejected/`, `deferred/`, and `under-review/`) plus bug status
directories (`open/`, `in-progress/`, and `closed/`). Keep the consuming
project's live records in the installed copy, not inside this submodule.

When templates contain `{{THEKNOWLEDGE_ROOT}}` or `{$KNOWLEDGE_ROOT}`, the
setup script replaces that placeholder with the submodule path relative to
the consuming project root.

The installer also manages `AGENTS.md` in the consuming project root. It uses
`AGENTS-header.md` and `AGENTS-footer.md` to create or wrap the project file
so local project instructions can live between the managed sections. Before it
rewrites `AGENTS.md`, it removes any existing managed header or footer blocks
so rerunning the installer does not duplicate them.

After updating the submodule, run `scripts/report_managed_agents_drift.py`
from the TheKnowledge checkout to compare the consuming project's managed
`AGENTS.md` header and footer with the updated templates. The helper prints
unified diffs that both human and AI developers can review before rerunning
`scripts/initial-setup.py --force`, review `git diff`, and stage only the
intended updates.

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
