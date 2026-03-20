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

The `project-management/state/` template directory includes
`pending-commit-changes.txt`, which is the short-lived queue for brief commit
summary lines. The standardized commit helper consumes that file as commit
body text and clears it after a successful local commit.
