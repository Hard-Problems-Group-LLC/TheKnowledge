from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.initial_setup import infer_knowledge_root


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "initial-setup.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_infer_knowledge_root_returns_relative_submodule_path() -> None:
    project_root = Path("/tmp/project")
    knowledge_root = Path("/tmp/project/TheKnowledge")
    assert infer_knowledge_root(project_root, knowledge_root) == "TheKnowledge"


def test_initial_setup_installs_project_management_templates(tmp_path: Path) -> None:
    project_root = tmp_path / "TestProject"
    project_root.mkdir()

    result = _run(
        "--project-root",
        str(project_root),
        "--knowledge-root",
        "TheKnowledge",
    )

    assert result.returncode == 0
    agents = project_root / "AGENTS.md"
    proposals_readme = project_root / "project-management" / "proposals" / "README.txt"
    approved_proposals = (
        project_root / "project-management" / "proposals" / "approved" / "README.txt"
    )
    rejected_proposals = (
        project_root / "project-management" / "proposals" / "rejected" / "README.txt"
    )
    deferred_proposals = (
        project_root / "project-management" / "proposals" / "deferred" / "README.txt"
    )
    under_review_proposals = (
        project_root
        / "project-management"
        / "proposals"
        / "under-review"
        / "README.txt"
    )
    git_flow = project_root / "project-management" / "git-flow.txt"
    pending_queue = (
        project_root / "project-management" / "state" / "pending-commit-changes.txt"
    )
    bugs_readme = project_root / "project-management" / "bugs" / "README.txt"
    open_bugs = project_root / "project-management" / "bugs" / "open" / "README.txt"
    in_progress_bugs = (
        project_root / "project-management" / "bugs" / "in-progress" / "README.txt"
    )
    closed_bugs_dir = (
        project_root / "project-management" / "bugs" / "closed" / "README.txt"
    )
    resolved_bugs = project_root / "project-management" / "bugs" / "resolved-bugs.txt"
    closed_bugs = project_root / "project-management" / "bugs" / "closed-bugs.txt"

    assert agents.is_file()
    assert proposals_readme.is_file()
    assert approved_proposals.is_file()
    assert rejected_proposals.is_file()
    assert deferred_proposals.is_file()
    assert under_review_proposals.is_file()
    assert git_flow.is_file()
    assert pending_queue.is_file()
    assert bugs_readme.is_file()
    assert open_bugs.is_file()
    assert in_progress_bugs.is_file()
    assert closed_bugs_dir.is_file()
    assert resolved_bugs.is_file()
    assert not closed_bugs.exists()
    assert "The Hard Problems Group's specifications and guidance" in (
        agents.read_text(encoding="utf-8")
    )
    assert "TheKnowledge/AGENTS.md" in agents.read_text(encoding="utf-8")
    assert "project-management/state/pending-commit-changes.txt" in agents.read_text(
        encoding="utf-8"
    )
    assert "TheKnowledge `Feedback` branch" in agents.read_text(encoding="utf-8")
    assert "normal internal trees on `trunk`" in agents.read_text(encoding="utf-8")
    assert "top-level `knacks/` directory" in agents.read_text(encoding="utf-8")
    assert "scripts/validate_knacks.py --project-root ." in agents.read_text(
        encoding="utf-8"
    )
    assert "report_managed_agents_drift.py" in agents.read_text(encoding="utf-8")
    assert "Run `git diff` before any `git add`" in agents.read_text(encoding="utf-8")
    assert "TheKnowledge/standards-and-practices/docs/format-for-proposals.txt" in (
        proposals_readme.read_text(encoding="utf-8")
    )
    assert "approved/" in proposals_readme.read_text(encoding="utf-8")
    assert "python TheKnowledge/scripts/run_tool_with_timeout.py black" in (
        git_flow.read_text(encoding="utf-8")
    )
    assert pending_queue.read_text(encoding="utf-8").strip() == ""
    assert "open/" in bugs_readme.read_text(encoding="utf-8")
    resolved_text = resolved_bugs.read_text(encoding="utf-8")
    assert "Root cause:" in resolved_text
    assert "Resolution:" in resolved_text


def test_initial_setup_refuses_to_overwrite_without_force(tmp_path: Path) -> None:
    project_root = tmp_path / "TestProject"
    target = project_root / "project-management"
    target.mkdir(parents=True)
    backlog = target / "backlog.txt"
    backlog.write_text("existing\n", encoding="utf-8")

    result = _run(
        "--project-root",
        str(project_root),
        "--knowledge-root",
        "TheKnowledge",
    )

    assert result.returncode == 1
    assert backlog.read_text(encoding="utf-8") == "existing\n"


def test_initial_setup_dry_run_leaves_tree_unchanged(tmp_path: Path) -> None:
    project_root = tmp_path / "TestProject"
    project_root.mkdir()

    result = _run(
        "--project-root",
        str(project_root),
        "--knowledge-root",
        "TheKnowledge",
        "--dry-run",
    )

    assert result.returncode == 0
    assert not (project_root / "AGENTS.md").exists()
    assert not (project_root / "project-management").exists()


def test_initial_setup_wraps_existing_agents_file(tmp_path: Path) -> None:
    project_root = tmp_path / "TestProject"
    project_root.mkdir()
    agents = project_root / "AGENTS.md"
    agents.write_text(
        "## Local Rules\n\nKeep this project concise.\n", encoding="utf-8"
    )

    result = _run(
        "--project-root",
        str(project_root),
        "--knowledge-root",
        "TheKnowledge",
    )

    assert result.returncode == 0
    content = agents.read_text(encoding="utf-8")
    assert "THEKNOWLEDGE_MANAGED_HEADER_START" in content
    assert "THEKNOWLEDGE_MANAGED_FOOTER_START" in content
    assert "## Local Rules" in content
    assert content.index("THEKNOWLEDGE_MANAGED_HEADER_END") < content.index(
        "## Local Rules"
    )
    assert content.index("## Local Rules") < content.index(
        "THEKNOWLEDGE_MANAGED_FOOTER_START"
    )


def test_initial_setup_does_not_duplicate_managed_agents_sections(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "TestProject"
    project_root.mkdir()

    first = _run(
        "--project-root",
        str(project_root),
        "--knowledge-root",
        "TheKnowledge",
    )
    second = _run(
        "--project-root",
        str(project_root),
        "--knowledge-root",
        "TheKnowledge",
        "--force",
    )

    assert first.returncode == 0
    assert second.returncode == 0

    content = (project_root / "AGENTS.md").read_text(encoding="utf-8")
    assert content.count("THEKNOWLEDGE_MANAGED_HEADER_START") == 1
    assert content.count("THEKNOWLEDGE_MANAGED_HEADER_END") == 1
    assert content.count("THEKNOWLEDGE_MANAGED_FOOTER_START") == 1
    assert content.count("THEKNOWLEDGE_MANAGED_FOOTER_END") == 1


def test_initial_setup_normalizes_preexisting_duplicate_managed_sections(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "TestProject"
    project_root.mkdir()
    agents = project_root / "AGENTS.md"
    header = (ROOT / "templates" / "AGENTS-header.md").read_text(encoding="utf-8")
    footer = (ROOT / "templates" / "AGENTS-footer.md").read_text(encoding="utf-8")
    agents.write_text(
        "\n\n".join(
            [
                header.strip(),
                header.strip(),
                "## Local Rules\n\nKeep this project concise.",
                footer.strip(),
                footer.strip(),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = _run(
        "--project-root",
        str(project_root),
        "--knowledge-root",
        "TheKnowledge",
        "--force",
    )

    assert result.returncode == 0

    content = agents.read_text(encoding="utf-8")
    assert content.count("THEKNOWLEDGE_MANAGED_HEADER_START") == 1
    assert content.count("THEKNOWLEDGE_MANAGED_HEADER_END") == 1
    assert content.count("THEKNOWLEDGE_MANAGED_FOOTER_START") == 1
    assert content.count("THEKNOWLEDGE_MANAGED_FOOTER_END") == 1
    assert content.count("## Local Rules") == 1
