from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.git_standard_commit_push import (
    build_commit_command,
    pending_commit_changes_path,
    pending_commit_changes_text,
)


ROOT = Path(__file__).resolve().parent.parent
COMMIT_PUSH = ROOT / "scripts" / "git_standard_commit_push.py"
VETERAN_PULL = ROOT / "scripts" / "git_veteran_pull.py"


def _run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_git_standard_commit_push_rejects_missing_message() -> None:
    result = _run(COMMIT_PUSH)
    assert result.returncode == 2


def test_git_veteran_pull_rejects_branch_without_remote() -> None:
    result = _run(VETERAN_PULL, "--branch", "trunk")
    assert result.returncode == 1
    assert "--branch requires --remote." in result.stderr


def test_git_standard_commit_push_dry_run_succeeds() -> None:
    result = _run(COMMIT_PUSH, "--dry-run", "-m", "test message")
    assert result.returncode == 0


def test_pending_commit_changes_path_prefers_internal_override(
    tmp_path: Path,
) -> None:
    internal = tmp_path / "internal" / "overrides" / "state"
    project_state = tmp_path / "project-management" / "state"
    internal.mkdir(parents=True)
    project_state.mkdir(parents=True)
    internal_queue = internal / "pending-commit-changes.txt"
    project_queue = project_state / "pending-commit-changes.txt"
    internal_queue.write_text("- internal\n", encoding="utf-8")
    project_queue.write_text("- project\n", encoding="utf-8")

    assert pending_commit_changes_path(tmp_path) == internal_queue


def test_pending_commit_changes_path_falls_back_to_project_management(
    tmp_path: Path,
) -> None:
    project_state = tmp_path / "project-management" / "state"
    project_state.mkdir(parents=True)
    project_queue = project_state / "pending-commit-changes.txt"
    project_queue.write_text("- project\n", encoding="utf-8")

    assert pending_commit_changes_path(tmp_path) == project_queue


def test_pending_commit_changes_text_strips_blank_lines(tmp_path: Path) -> None:
    pending_queue = tmp_path / "pending-commit-changes.txt"
    pending_queue.write_text("\n- first item\n- second item\n\n", encoding="utf-8")

    assert pending_commit_changes_text(pending_queue) == "- first item\n- second item"


def test_build_commit_command_uses_pending_queue_as_body() -> None:
    command = build_commit_command(
        "subject line",
        "- first item\n- second item",
        allow_empty=False,
    )

    assert command == [
        "git",
        "commit",
        "-m",
        "subject line",
        "-m",
        "- first item\n- second item",
    ]
