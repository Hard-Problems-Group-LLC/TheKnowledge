# Templates

The files and directories under `templates/` are starting points for projects
that consume TheKnowledge, usually as a Git submodule.

Copy them into the consuming project root instead of editing them in place
inside the submodule. Use `scripts/initial-setup.py` to install them.

The `project-management/` starter tree includes proposal status directories
(`approved/`, `rejected/`, `deferred/`, and `under-review/`) plus bug status
directories (`open/`, `in-progress/`, and `closed/`). Keep the consuming
project's live records in the installed copy, not inside this submodule.
Proposal records and proposal directory README files are Markdown (`.md`) by
default.

The starter set also includes `install.sh`, `bootstrap.sh`,
`scripts/install-stage-2.py`, `bootstrap-stage2.py`,
`python-environments.json`, `.python-version`, `set-context.sh`,
`set-context-bootstrap.sh`, `requirements-dev.txt`,
`scripts/dev_setup.py`, `scripts/python_environment_bootstrap.py`,
`scripts/tool_validation_profiles.py`, `tool_execution_constraints.json`,
`tool_validation_profiles.json`, a managed `.gitignore` block, and
`ECRs/TheKnowledge/` lifecycle scaffolding.
Together they install TheKnowledge's default pinned Black, Ruff, and pytest
toolchain plus a default user-local standard install, an explicit repo-local
development mode with pinned pyenv runtime selection plus `.venv`, managed
registries for known environment-specific tool execution constraints and
placement-driven Black/runtime policy, development-mode `direnv`
integration, and the standard local directory for read-only upstream
TheKnowledge requests. The managed `.gitignore` block proactively ignores
`.local/`, `.theknowledge-restricted-names.local`, `.codex-local/`,
`.codex-home/`, `.codex`, `bin/codex-local`, and
`README-LOCAL-Start-Codex.md`. `bootstrap.sh` and `bootstrap-stage2.py`
remain compatibility wrappers around the canonical `install.sh` and
`scripts/install-stage-2.py` entry points. Consuming projects may also
provide `scripts/install_project.py` when they need custom development,
user-local standard, or system-standard install semantics beyond the managed
default behavior.

When templates contain `{{THEKNOWLEDGE_ROOT}}` or `{$KNOWLEDGE_ROOT}`, the
setup script replaces that placeholder with the submodule path relative to
the consuming project root.

The installer also manages `AGENTS.md` in the consuming project root. It uses
`AGENTS-header.md` and `AGENTS-footer.md` to create or wrap the project file
so local project instructions can live between the managed sections. Before it
rewrites `AGENTS.md`, it removes any existing managed header or footer blocks
so rerunning the installer does not duplicate them.

Project-local operator notes that AI agents must consider but must never
commit or push should live under `.local/`, typically
`.local/ai-local-notes.md` or `.local/ai-local-notes.txt`.

Managed agent guidance also carries session and project-boundary safeguards.
The literal phrase `collision resume` tells agents to inspect candidate
sessions for the current workspace rather than assuming the newest session is
right. Before mutating outside the active project root, agents must ask for
explicit cross-project confirmation in the current session and name the
active project, target project, and intended change class.

After updating the submodule, first review the incoming upstream delta in the
TheKnowledge checkout, then run `scripts/report_managed_agents_drift.py` to
compare the consuming project's managed `AGENTS.md` sections plus managed
starter files with the updated templates. The helper prints unified diffs that
both human and AI developers can review before rerunning
`scripts/initial-setup.py --force --template .python-version --template ECRs`
`--template .gitignore --template install.sh --template bootstrap.sh --template`
`bootstrap-stage2.py --template python-environments.json --template`
`requirements-dev.txt --template scripts --template`
`scripts/install-stage-2.py --template scripts/python_environment_bootstrap.py`
`--template scripts/tool_validation_profiles.py --template`
`set-context-bootstrap.sh --template set-context.sh --template`
`tool_execution_constraints.json --template tool_validation_profiles.json`,
review `git diff`, and stage the resulting submodule-pointer update plus only
the intended project-file changes.

For the normal review-and-adopt path, prefer
`python {$KNOWLEDGE_ROOT}/scripts/update_theknowledge_submodule.py`
` --project-root . --knowledge-root {$KNOWLEDGE_ROOT}`. That helper fetches
and summarizes the upstream delta, adopts the reviewed `trunk` commit, runs
managed drift detection, refreshes the managed starter files when needed, and
leaves a reviewable parent-repo diff without auto-committing.

If that rerun updates `install.sh`, `bootstrap.sh`,
`scripts/install-stage-2.py`, `bootstrap-stage2.py`,
`python-environments.json`, `.python-version`, `set-context.sh`,
`set-context-bootstrap.sh`, `requirements-dev.txt`, `scripts/dev_setup.py`,
`scripts/python_environment_bootstrap.py`,
`scripts/tool_validation_profiles.py`, or `tool_validation_profiles.json`,
refresh the starter toolchain with `./install.sh` unless the consuming
project intentionally overrides those files. If it updates
`tool_execution_constraints.json` or `tool_validation_profiles.json`, review
the policy change alongside the submodule update so shared helpers stay
aligned with the current managed constraints.

When the active `TheKnowledge/` checkout is read-only in the consuming
project and an upstream request needs a local holding area first, use
`ECRs/TheKnowledge/open/`. Move the request to
`ECRs/TheKnowledge/in-progress/` during active upstream handling and to
`ECRs/TheKnowledge/closed/` once the upstream disposition is recorded in a
writable TheKnowledge checkout or through the TheKnowledge `Feedback` branch
flow.

When an upstream writable TheKnowledge checkout resolves a carried ECR, the
consuming project can compare the ECR filename against that checkout's
`internal/overrides/proposals/accepted-ecrs-list.md`.

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

Projects with durable user-facing, operator-facing, or release-facing history
should maintain `CHANGELOG.md` separately. Copy or summarize notable
pending-queue entries there before the standardized commit helper clears the
queue.

The standardized commit helper also defaults to a review-first staging path.
It lists files about to be staged, asks whether to review them, and
prefers launching Meld when available as the default visual review
path. It can also pause for file-by-file review and runs
`git diff --cached` before commit. Use `--assume-reviewed` only
after an explicit review decision made outside the helper, and use
`--resume-review-prompts` to re-enable prompts for the current shell session.
If an operator says `ACP`, treat that as "add, commit, push" through the same
VCS workflow. Stage, commit, and push meaningful blocks with appropriate
comments rather than creating one monolithic commit.

Managed downstream `AGENTS.md` files also inherit timestamped
intermediary-update guidance for workflow profiling. Use inline
bracketed ISO 8601 prefixes such as
`[2026-03-25T01:05:12-07:00] Running full pytest.` when work begins,
before and after long-running commands or waits, and at major phase
boundaries.

Managed downstream testing guidance favors real local implementations when
they are deterministic, cheap, and safe. Prefer deterministic fixtures and
fakes before dynamic mocks, reserve mocks for hard or unsafe boundaries, and
pair important mocked behavior with real integration, contract, smoke,
browser, or scripted coverage.
