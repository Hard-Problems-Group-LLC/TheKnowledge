from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.initial_setup import render_file


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "report_managed_agents_drift.py"
TEMPLATES = ROOT / "templates"


def _run(project_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--project-root", str(project_root), *args],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def _write_agents(project_root: Path, header: str, footer: str) -> None:
    agents = project_root / "AGENTS.md"
    agents.write_text(
        "\n\n".join(
            [
                header.strip(),
                "## Local Rules\n\nKeep this project concise.",
                footer.strip(),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_report_managed_agents_drift_passes_when_sections_match(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    knowledge_root = "TheKnowledge"
    header = render_file(TEMPLATES / "AGENTS-header.md", knowledge_root).decode("utf-8")
    footer = render_file(TEMPLATES / "AGENTS-footer.md", knowledge_root).decode("utf-8")
    _write_agents(project, header, footer)

    result = _run(project, "--knowledge-root", knowledge_root)

    assert result.returncode == 0
    assert "managed header is up to date" in result.stdout
    assert "managed footer is up to date" in result.stdout


def test_report_managed_agents_drift_reports_header_or_footer_changes(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    knowledge_root = "TheKnowledge"
    header = render_file(TEMPLATES / "AGENTS-header.md", knowledge_root).decode("utf-8")
    footer = render_file(TEMPLATES / "AGENTS-footer.md", knowledge_root).decode("utf-8")
    drifted_footer = footer.replace(
        "Run `git diff` before any `git add`",
        "Review project changes before staging",
    )
    _write_agents(project, header, drifted_footer)

    result = _run(project, "--knowledge-root", knowledge_root)

    assert result.returncode == 1
    assert "managed footer differs" in result.stdout
    assert "DIFF footer" in result.stdout
    assert (
        "initial-setup.py --project-root . --knowledge-root "
        "TheKnowledge --force" in result.stdout
    )
