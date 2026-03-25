from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INTERNAL = ROOT / "internal"
OVERRIDES = INTERNAL / "overrides"
STANDARDS = ROOT / "standards-and-practices"
TEMPLATES = ROOT / "templates"

EXPECTED_FILES = [
    INTERNAL / "README.md",
    ROOT / "README.md",
    TEMPLATES / "AGENTS-header.md",
    TEMPLATES / "AGENTS-footer.md",
    TEMPLATES / "README.md",
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
    assert "standards-and-practices/docs/development-workflow.txt" in agents_text
    assert "templates/project-management/git-flow.txt" in agents_text
    assert "internal/overrides/README.txt" in agents_text
    assert "internal/overrides/state/pending-commit-changes.txt" in agents_text
    assert "internal/overrides/proposals/" in agents_text
    assert "internal/overrides/bugs/" in agents_text
    assert "Before any `git add`, list the files about to be staged" in agents_text
    assert "Run `git diff --cached` before any commit" in agents_text
    assert "default visual review path" in agents_text
    assert "submodule itself" in internal_text
    assert "templates/project-management/" in overrides_text
    assert "proposals/approved/README.txt" in overrides_text
    assert "state/pending-commit-changes.txt" in overrides_text
    assert "bugs/open/README.txt" in overrides_text
    assert "bugs/resolved-bugs.txt" in overrides_text
    assert "scripts/initial-setup.py" in templates_text
    assert "report_managed_agents_drift.py" in templates_text
    assert "review `git diff`" in templates_text
    assert "git diff --cached" in templates_text
    assert "--resume-review-prompts" in templates_text
    assert "approved/" in templates_text
    assert "open/" in templates_text
    assert "pending-commit-changes.txt" in templates_text
    assert "{$KNOWLEDGE_ROOT}/AGENTS.md" in header_text
    assert "TheKnowledge Overrides" in footer_text
    assert "Feedback` branch" in footer_text
    assert "Before any `git add`, list the files about to be staged" in footer_text
    assert "git diff --cached" in footer_text
    assert "report_managed_agents_drift.py" in footer_text
    assert "normal internal trees on `trunk`" in footer_text
    assert "top-level `knacks/` directory" in footer_text
    assert "scripts/validate_knacks.py --project-root ." in footer_text
    assert ".git/knack-validation-cache.json" in footer_text
    assert "review in Meld" in footer_text
    assert "default visual review path" in footer_text
    assert "--resume-review-prompts" in footer_text
    assert "project-management/proposals/" in footer_text
    assert "project-management/state/pending-commit-changes.txt" in footer_text
    assert "Review-first staging" in repo_text
    assert "git diff --cached" in repo_text
    assert "--assume-reviewed" in repo_text
    assert "https://gnome.pages.gitlab.gnome.org/meld/" in repo_text
    assert "default recommended visual review path" in repo_text
    assert "project-management/proposals/" in workflow_text
    assert "project-management/backlog.txt" in workflow_text
    assert "project-management/state/pending-commit-changes.txt" in workflow_text
    assert "review in Meld" in workflow_text
    assert "default visual review path" in workflow_text
    assert "git diff --cached" in workflow_text
