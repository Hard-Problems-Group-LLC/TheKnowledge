from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTERNAL = ROOT / "internal"
OVERRIDES = INTERNAL / "overrides"
STANDARDS = ROOT / "standards-and-practices"
TEMPLATES = ROOT / "templates"

EXPECTED_FILES = [
    INTERNAL / "README.md",
    ROOT / ".python-version",
    ROOT / "README.md",
    ROOT / "install.sh",
    ROOT / "bootstrap.sh",
    ROOT / "bootstrap-stage2.py",
    ROOT / "python-environments.json",
    ROOT / "set-context-bootstrap.sh",
    ROOT / "set-context.sh",
    ROOT / "scripts" / "dev_setup.py",
    ROOT / "scripts" / "install-stage-2.py",
    ROOT / "scripts" / "python_environment_bootstrap.py",
    ROOT / "tool_execution_constraints.json",
    ROOT / "tool_validation_profiles.json",
    TEMPLATES / "AGENTS-header.md",
    TEMPLATES / "AGENTS-footer.md",
    TEMPLATES / ".python-version",
    TEMPLATES / "README.md",
    TEMPLATES / "install.sh",
    TEMPLATES / "bootstrap.sh",
    TEMPLATES / "bootstrap-stage2.py",
    TEMPLATES / "python-environments.json",
    TEMPLATES / "requirements-dev.txt",
    TEMPLATES / "set-context-bootstrap.sh",
    TEMPLATES / "set-context.sh",
    TEMPLATES / "ECRs" / "README.md",
    TEMPLATES / "ECRs" / "TheKnowledge" / "README.md",
    TEMPLATES / "scripts" / "dev_setup.py",
    ROOT / "scripts" / "tool_validation_profiles.py",
    TEMPLATES / "project-management" / "git-flow.txt",
    TEMPLATES / "project-management" / "proposals" / "README.txt",
    TEMPLATES / "project-management" / "proposals" / "approved" / "README.txt",
    TEMPLATES / "project-management" / "proposals" / "rejected" / "README.txt",
    TEMPLATES / "project-management" / "proposals" / "deferred" / "README.txt",
    TEMPLATES / "project-management" / "proposals" / "under-review" / "README.txt",
    TEMPLATES / "project-management" / "bugs" / "README.txt",
    TEMPLATES / "project-management" / "bugs" / "open" / "README.txt",
    TEMPLATES / "project-management" / "bugs" / "in-progress" / "README.txt",
    TEMPLATES / "project-management" / "bugs" / "closed" / "README.txt",
    STANDARDS / "docs" / "development-workflow.txt",
    STANDARDS
    / "docs"
    / "specifications"
    / "codex_sandbox_file_safe_static_analysis.txt",
    STANDARDS / "docs" / "specifications" / "tool_execution_constraints_registry.txt",
    STANDARDS / "docs" / "specifications" / "pinned_python_dev_tool_versions.txt",
    STANDARDS / "docs" / "specifications" / "python_bootstrap_and_context_strategy.txt",
    STANDARDS
    / "docs"
    / "specifications"
    / "read_only_upstream_ecr_directory_structure.txt",
    STANDARDS
    / "docs"
    / "specifications"
    / "tool_validation_profiles_and_python_runtime_selection.txt",
    STANDARDS / "docs" / "specifications" / "inline_ai_conversation_timestamps.txt",
    STANDARDS / "docs" / "specifications" / "theknowledge_submodule_workflows.txt",
    STANDARDS
    / "docs"
    / "specifications"
    / "status_subdirectories_for_proposals_and_bugs.txt",
    OVERRIDES / "README.txt",
    OVERRIDES / "backlog.txt",
    OVERRIDES / "tasks-in-progress.txt",
    OVERRIDES / "completed-tasks.txt",
    OVERRIDES / "deferred.txt",
    OVERRIDES / "ai-human-requests.txt",
    OVERRIDES / "proposals" / "README.txt",
    OVERRIDES / "proposals" / "approved" / "README.txt",
    OVERRIDES / "proposals" / "rejected" / "README.txt",
    OVERRIDES / "proposals" / "deferred" / "README.txt",
    OVERRIDES / "proposals" / "under-review" / "README.txt",
    OVERRIDES / "state" / "README.txt",
    OVERRIDES / "state" / "pending-commit-changes.txt",
    OVERRIDES / "bugs" / "README.txt",
    OVERRIDES / "bugs" / "known-bugs.txt",
    OVERRIDES / "bugs" / "bugs-in-progress.txt",
    OVERRIDES / "bugs" / "resolved-bugs.txt",
    OVERRIDES / "bugs" / "open" / "README.txt",
    OVERRIDES / "bugs" / "in-progress" / "README.txt",
    OVERRIDES / "bugs" / "closed" / "README.txt",
]


def test_override_record_tree_exists() -> None:
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing override record: {path.relative_to(ROOT)}"


def test_override_guidance_is_wired_into_repository_docs() -> None:
    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    repo_text = (ROOT / "README.md").read_text(encoding="utf-8")
    internal_text = (INTERNAL / "README.md").read_text(encoding="utf-8")
    overrides_text = (OVERRIDES / "README.txt").read_text(encoding="utf-8")
    templates_text = (TEMPLATES / "README.md").read_text(encoding="utf-8")
    header_text = (TEMPLATES / "AGENTS-header.md").read_text(encoding="utf-8")
    footer_text = (TEMPLATES / "AGENTS-footer.md").read_text(encoding="utf-8")
    workflow_text = (STANDARDS / "docs" / "development-workflow.txt").read_text(
        encoding="utf-8"
    )
    git_flow_text = (TEMPLATES / "project-management" / "git-flow.txt").read_text(
        encoding="utf-8"
    )
    installation_text = (STANDARDS / "docs" / "installation.txt").read_text(
        encoding="utf-8"
    )
    sandbox_spec_text = (
        STANDARDS
        / "docs"
        / "specifications"
        / "codex_sandbox_file_safe_static_analysis.txt"
    ).read_text(encoding="utf-8")
    pinning_spec_text = (
        STANDARDS / "docs" / "specifications" / "pinned_python_dev_tool_versions.txt"
    ).read_text(encoding="utf-8")
    bootstrap_spec_text = (
        STANDARDS
        / "docs"
        / "specifications"
        / "python_bootstrap_and_context_strategy.txt"
    ).read_text(encoding="utf-8")
    ecr_spec_text = (
        STANDARDS
        / "docs"
        / "specifications"
        / "read_only_upstream_ecr_directory_structure.txt"
    ).read_text(encoding="utf-8")
    profile_spec_text = (
        STANDARDS
        / "docs"
        / "specifications"
        / "tool_validation_profiles_and_python_runtime_selection.txt"
    ).read_text(encoding="utf-8")
    pending_queue_spec_text = (
        STANDARDS / "docs" / "specifications" / "pending_commit_change_queue.txt"
    ).read_text(encoding="utf-8")
    submodule_spec_text = (
        STANDARDS / "docs" / "specifications" / "theknowledge_submodule_workflows.txt"
    ).read_text(encoding="utf-8")
    timing_spec_text = (
        STANDARDS / "docs" / "specifications" / "inline_ai_conversation_timestamps.txt"
    ).read_text(encoding="utf-8")
    constraints_spec_text = (
        STANDARDS
        / "docs"
        / "specifications"
        / "tool_execution_constraints_registry.txt"
    ).read_text(encoding="utf-8")
    assert "standards-and-practices/docs/development-workflow.txt" in agents_text
    assert "templates/project-management/git-flow.txt" in agents_text
    assert "internal/overrides/README.txt" in agents_text
    assert "internal/overrides/state/pending-commit-changes.txt" in agents_text
    assert "internal/overrides/proposals/" in agents_text
    assert "internal/overrides/bugs/" in agents_text
    assert "Load this file before running automated tooling" in agents_text
    assert "Every maintained source file should" in agents_text
    assert "Python 3.12 best practices" in agents_text
    assert "tool_execution_constraints.json" in agents_text
    assert "send_theknowledge_feedback.py prepare" in agents_text
    assert "ECRs/TheKnowledge/" in agents_text
    assert "Before any `git add`, list the files about to be staged" in agents_text
    assert "Never guess a Git author or committer email address" in agents_text
    assert "explicit committer identity for author" in agents_text
    assert "Run `git diff --cached` before any commit" in agents_text
    assert "`TheKnowledge/` submodule" in agents_text
    assert "one file at a time" in agents_text
    assert "`black -W 1`" in agents_text
    assert "inline bracketed ISO 8601 timestamp" in agents_text
    assert "workflow profiling" in agents_text
    assert "default visual review path" in agents_text
    assert "submodule itself" in internal_text
    assert "templates/project-management/" in overrides_text
    assert "proposals/approved/README.txt" in overrides_text
    assert "state/pending-commit-changes.txt" in overrides_text
    assert "bugs/open/README.txt" in overrides_text
    assert "bugs/resolved-bugs.txt" in overrides_text
    assert "scripts/initial-setup.py" in templates_text
    assert "install.sh" in templates_text
    assert "bootstrap.sh" in templates_text
    assert "python-environments.json" in templates_text
    assert "ECRs/TheKnowledge/" in templates_text
    assert "requirements-dev.txt" in templates_text
    assert "scripts/dev_setup.py" in templates_text
    assert "tool_execution_constraints.json" in templates_text
    assert "tool_validation_profiles.json" in templates_text
    assert "default pinned" in templates_text
    assert "Black, Ruff, and pytest" in templates_text
    assert "report_managed_agents_drift.py" in templates_text
    assert "update_theknowledge_submodule.py" in templates_text
    assert "send_theknowledge_feedback.py prepare" in templates_text
    assert "review `git diff`" in templates_text
    assert "review the incoming upstream delta" in templates_text
    assert "timestamped" in templates_text
    assert "workflow profiling" in templates_text
    assert "git diff --cached" in templates_text
    assert "--resume-review-prompts" in templates_text
    assert "approved/" in templates_text
    assert "open/" in templates_text
    assert "pending-commit-changes.txt" in templates_text
    assert "{$KNOWLEDGE_ROOT}/AGENTS.md" in header_text
    assert "must load `{$KNOWLEDGE_ROOT}/AGENTS.md` before running automated" in (
        header_text
    )
    assert "live-state override record map" in header_text
    assert "TheKnowledge Overrides" in footer_text
    assert "Feedback` branch" in footer_text
    assert "`{$KNOWLEDGE_ROOT}/` submodule checkout" in footer_text
    assert "./install.sh" in footer_text
    assert "python-environments.json" in footer_text
    assert "ECRs/TheKnowledge/" in footer_text
    assert "Python 3.12 best practices" in footer_text
    assert "incoming upstream `trunk` delta" in footer_text
    assert "one file at a time" in footer_text
    assert "`black -W 1`" in footer_text
    assert "requirements-dev.txt" in footer_text
    assert "tool_execution_constraints.json" in footer_text
    assert "tool_validation_profiles.json" in footer_text
    assert "send_theknowledge_feedback.py prepare" in footer_text
    assert "update_theknowledge_submodule.py" in footer_text
    assert "Before any `git add`, list the files about to be staged" in footer_text
    assert "inline bracketed ISO 8601 timestamp" in footer_text
    assert "workflow profiling" in footer_text
    assert "git diff --cached" in footer_text
    assert "report_managed_agents_drift.py" in footer_text
    assert "normal internal trees on `trunk`" in footer_text
    assert "top-level `knacks/` directory" in footer_text
    assert "scripts/validate_knacks.py --project-root ." in footer_text
    assert ".git/knack-validation-cache.json" in footer_text
    assert "Never guess a Git author or committer email address" in footer_text
    assert "explicit committer identity for author" in footer_text
    assert "review in Meld" in footer_text
    assert "default visual review path" in footer_text
    assert "--resume-review-prompts" in footer_text
    assert "project-management/proposals/" in footer_text
    assert "project-management/state/pending-commit-changes.txt" in footer_text
    assert "Timestamped Intermediary Updates" in repo_text
    assert "./install.sh" in repo_text
    assert "python-environments.json" in repo_text
    assert "ECRs/TheKnowledge/" in repo_text
    assert "scripts/dev_setup.py" in repo_text
    assert "requirements-dev.txt" in repo_text
    assert "tool_execution_constraints.json" in repo_text
    assert "tool_validation_profiles.json" in repo_text
    assert "update_theknowledge_submodule.py" in repo_text
    assert "send_theknowledge_feedback.py prepare" in repo_text
    assert "workflow profiling" in repo_text
    assert "[2026-03-25T01:05:12-07:00] Running full pytest." in repo_text
    assert "Review-first staging" in repo_text
    assert "git diff --cached" in repo_text
    assert "--assume-reviewed" in repo_text
    assert "https://gnome.pages.gitlab.gnome.org/meld/" in repo_text
    assert "default recommended visual review path" in repo_text
    assert "git log --oneline HEAD..origin/trunk" in repo_text
    assert "active `TheKnowledge/` submodule checkout" in repo_text
    assert "project-management/proposals/" in workflow_text
    assert "workflow profiling" in workflow_text
    assert "[2026-03-25T01:05:12-07:00] Running full pytest." in workflow_text
    assert "project-management/backlog.txt" in workflow_text
    assert "./install.sh" in workflow_text
    assert "tool_execution_constraints.json" in workflow_text
    assert "tool_validation_profiles.json" in workflow_text
    assert "./scripts/install_prerequisites.sh" in workflow_text
    assert "project-management/state/pending-commit-changes.txt" in workflow_text
    assert "review in Meld" in workflow_text
    assert "default visual review path" in workflow_text
    assert "Never infer a Git author or committer email address" in workflow_text
    assert "committer identity for author" in workflow_text
    assert "git diff --cached" in workflow_text
    assert "one file at a time" in workflow_text
    assert "`black -W 1`" in workflow_text
    assert "./install.sh" in git_flow_text
    assert "ECRs/TheKnowledge/" in git_flow_text
    assert "Never infer a Git author or committer email address" in git_flow_text
    assert "committer identity for author" in git_flow_text
    assert "requirements-dev.txt" in git_flow_text
    assert "tool_validation_profiles.json" in git_flow_text
    assert "incoming upstream `trunk` delta" in git_flow_text
    assert "update_theknowledge_submodule.py" in git_flow_text
    assert "TheKnowledge submodule" in installation_text
    assert "install.sh" in installation_text
    assert "python-environments.json" in installation_text
    assert "ECRs/TheKnowledge/" in installation_text
    assert "tool_execution_constraints.json" in installation_text
    assert "--template tool_execution_constraints.json" in installation_text
    assert "tool_validation_profiles.json" in installation_text
    assert "send_theknowledge_feedback.py prepare" in installation_text
    assert "pyproject.toml" in pinning_spec_text
    assert "templates/requirements-dev.txt" in pinning_spec_text
    assert "templates/scripts/dev_setup.py" in pinning_spec_text
    assert "python-environments.json" in pinning_spec_text
    assert "install.sh" in bootstrap_spec_text
    assert "set-context.sh" in bootstrap_spec_text
    assert "ECRs/TheKnowledge/" in ecr_spec_text
    assert "ECRs/README.md" in ecr_spec_text
    assert "tool_validation_profiles.json" in pinning_spec_text
    assert "placement plus extension" in profile_spec_text
    assert "steady-state Python runtime" in profile_spec_text
    assert "Python 3.12 or newer" in profile_spec_text
    assert "must refuse to create a commit" in pending_queue_spec_text
    assert "must never infer email addresses" in pending_queue_spec_text
    assert "review-and-adopt flow" in submodule_spec_text
    assert "active `TheKnowledge/` submodule checkout" in submodule_spec_text
    assert "ECRs/TheKnowledge/" in submodule_spec_text
    assert "update_theknowledge_submodule.py" in submodule_spec_text
    assert "send_theknowledge_feedback.py" in submodule_spec_text
    assert "one file at a time" in sandbox_spec_text
    assert "`black -W 1`" in sandbox_spec_text
    assert "whole-repository validation" in sandbox_spec_text
    assert "tool_execution_constraints.json" in sandbox_spec_text
    assert "hardcoded script rule" in sandbox_spec_text
    assert "tool_execution_constraints.json" in constraints_spec_text
    assert "sandbox_technologies" in constraints_spec_text
    assert "serial_explicit_paths" in constraints_spec_text
    assert "[YYYY-MM-DDThh:mm:ss+hh:mm] Message text." in timing_spec_text
    assert "Final summary messages do not need timestamp prefixes" in timing_spec_text
    assert "workflow profiling" in timing_spec_text
