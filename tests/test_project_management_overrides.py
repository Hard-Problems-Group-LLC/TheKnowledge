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
    STANDARDS / "docs" / "development-workflow.txt",
    OVERRIDES / "README.txt",
    OVERRIDES / "backlog.txt",
    OVERRIDES / "tasks-in-progress.txt",
    OVERRIDES / "completed-tasks.txt",
    OVERRIDES / "deferred.txt",
    OVERRIDES / "ai-human-requests.txt",
    OVERRIDES / "bugs" / "known-bugs.txt",
    OVERRIDES / "bugs" / "bugs-in-progress.txt",
    OVERRIDES / "bugs" / "closed-bugs.txt",
]


def test_override_record_tree_exists() -> None:
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing override record: {path.relative_to(ROOT)}"


def test_override_guidance_is_wired_into_repository_docs() -> None:
    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
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
    assert "submodule itself" in internal_text
    assert "templates/project-management/" in overrides_text
    assert "scripts/initial-setup.py" in templates_text
    assert "{$KNOWLEDGE_ROOT}/AGENTS.md" in header_text
    assert "TheKnowledge Overrides" in footer_text
    assert "project-management/backlog.txt" in workflow_text
