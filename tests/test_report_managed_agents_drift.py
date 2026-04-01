from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.initial_setup import (
    MANAGED_REFRESH_TEMPLATES,
    installable_entries,
    iter_install_files,
    project_slug,
    render_file,
    repo_root,
)

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


def _write_managed_starter_files(project_root: Path, knowledge_root: str) -> None:
    knowledge_repo_root = repo_root()
    templates_root = knowledge_repo_root / "templates"
    project_name_slug = project_slug(project_root)
    for source, relative_path in iter_install_files(
        [
            installable_entries(knowledge_repo_root, templates_root)[name]
            for name in MANAGED_REFRESH_TEMPLATES
        ]
    ):
        destination = project_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(render_file(source, knowledge_root, project_name_slug))


def test_report_managed_agents_drift_passes_when_sections_match(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    knowledge_root = "TheKnowledge"
    slug = project_slug(project)
    header = render_file(TEMPLATES / "AGENTS-header.md", knowledge_root, slug).decode(
        "utf-8"
    )
    footer = render_file(TEMPLATES / "AGENTS-footer.md", knowledge_root, slug).decode(
        "utf-8"
    )
    _write_agents(project, header, footer)
    _write_managed_starter_files(project, knowledge_root)

    result = _run(project, "--knowledge-root", knowledge_root)

    assert result.returncode == 0
    assert "managed header is up to date" in result.stdout
    assert "managed footer is up to date" in result.stdout
    assert "managed file .python-version is up to date" in result.stdout
    assert "managed file bootstrap.sh is up to date" in result.stdout
    assert "managed file tool_execution_constraints.json is up to date" in (
        result.stdout
    )
    assert "managed file tool_validation_profiles.json is up to date" in (result.stdout)


def test_report_managed_agents_drift_reports_header_or_footer_changes(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    knowledge_root = "TheKnowledge"
    slug = project_slug(project)
    header = render_file(TEMPLATES / "AGENTS-header.md", knowledge_root, slug).decode(
        "utf-8"
    )
    footer = render_file(TEMPLATES / "AGENTS-footer.md", knowledge_root, slug).decode(
        "utf-8"
    )
    drifted_footer = footer.replace(
        "Run `git diff` before any `git add`",
        "Review project changes before staging",
    )
    _write_agents(project, header, drifted_footer)
    _write_managed_starter_files(project, knowledge_root)

    result = _run(project, "--knowledge-root", knowledge_root)

    assert result.returncode == 1
    assert "managed footer differs" in result.stdout
    assert "DIFF footer" in result.stdout
    assert (
        "initial-setup.py --project-root . --knowledge-root TheKnowledge "
        "--force --template .python-version --template ECRs --template "
        "bootstrap.sh --template bootstrap-stage2.py --template "
        "python-environments.json --template requirements-dev.txt --template "
        "scripts --template scripts/python_environment_bootstrap.py "
        "--template scripts/tool_validation_profiles.py --template "
        "set-context-bootstrap.sh --template set-context.sh --template "
        "tool_execution_constraints.json --template "
        "tool_validation_profiles.json" in result.stdout
    )


def test_report_managed_agents_drift_reports_managed_file_changes(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    knowledge_root = "TheKnowledge"
    slug = project_slug(project)
    header = render_file(TEMPLATES / "AGENTS-header.md", knowledge_root, slug).decode(
        "utf-8"
    )
    footer = render_file(TEMPLATES / "AGENTS-footer.md", knowledge_root, slug).decode(
        "utf-8"
    )
    _write_agents(project, header, footer)
    _write_managed_starter_files(project, knowledge_root)
    (project / "tool_execution_constraints.json").write_text(
        '{"schema_version": "1.0.0", "products": {}}\n',
        encoding="utf-8",
    )

    result = _run(project, "--knowledge-root", knowledge_root)

    assert result.returncode == 1
    assert "managed file tool_execution_constraints.json differs" in result.stdout
    assert "DIFF file-tool_execution_constraints.json" in result.stdout
