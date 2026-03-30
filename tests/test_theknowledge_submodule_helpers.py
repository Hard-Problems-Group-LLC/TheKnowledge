from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run(
    command: list[str],
    *,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _git(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return _run(["git", *args], cwd=cwd)


def _git_ok(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    result = _git(*args, cwd=cwd)
    if result.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} failed in {cwd}:\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def _configure_identity(repo: Path) -> None:
    _git_ok("config", "user.name", "Test User", cwd=repo)
    _git_ok("config", "user.email", "test@example.com", cwd=repo)


def _copy_workspace(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(
            ".codex-home",
            ".codex-local",
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".ruff_cache",
            ".venv",
            "README-LOCAL-Start-Codex.md",
        ),
    )


def _make_knowledge_remote(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "knowledge-source"
    _copy_workspace(ROOT, source)
    _git_ok("init", "--initial-branch=trunk", cwd=source)
    _configure_identity(source)
    _git_ok("add", "-A", cwd=source)
    _git_ok("commit", "-m", "Initial import", cwd=source)
    _git_ok("switch", "-c", "Feedback", cwd=source)
    _git_ok("commit", "--allow-empty", "-m", "Initialize Feedback", cwd=source)
    _git_ok("switch", "trunk", cwd=source)

    remote = tmp_path / "knowledge-remote.git"
    _git_ok("clone", "--bare", str(source), str(remote), cwd=tmp_path)
    _git_ok("remote", "add", "origin", str(remote), cwd=source)
    _git_ok("push", "--all", "origin", cwd=source)
    return source, remote


def _make_consuming_project(tmp_path: Path) -> tuple[Path, Path, Path]:
    source, remote = _make_knowledge_remote(tmp_path)
    project = tmp_path / "project"
    project.mkdir()
    _git_ok("init", "--initial-branch=trunk", cwd=project)
    _configure_identity(project)
    (project / "README.md").write_text("# Project\n", encoding="utf-8")
    _git_ok("add", "README.md", cwd=project)
    _git_ok("commit", "-m", "Initial project", cwd=project)
    submodule_add = _run(
        [
            "git",
            "-c",
            "protocol.file.allow=always",
            "submodule",
            "add",
            str(remote),
            "TheKnowledge",
        ],
        cwd=project,
    )
    assert submodule_add.returncode == 0, submodule_add.stderr
    _git_ok("commit", "-am", "Add TheKnowledge submodule", cwd=project)
    knowledge_repo = project / "TheKnowledge"
    _configure_identity(knowledge_repo)

    setup = _run(
        [
            sys.executable,
            str(knowledge_repo / "scripts" / "initial-setup.py"),
            "--project-root",
            str(project),
            "--knowledge-root",
            "TheKnowledge",
        ],
        cwd=knowledge_repo,
    )
    assert setup.returncode == 0, setup.stderr
    _git_ok("add", "-A", cwd=project)
    _git_ok("commit", "-m", "Install TheKnowledge managed files", cwd=project)
    return project, source, remote


def _git_stdout(*args: str, cwd: Path) -> str:
    return _git_ok(*args, cwd=cwd).stdout.strip()


def _session_path(knowledge_repo: Path) -> Path:
    git_dir = _git_stdout("rev-parse", "--git-dir", cwd=knowledge_repo)
    git_path = Path(git_dir)
    if not git_path.is_absolute():
        git_path = (knowledge_repo / git_path).resolve()
    return git_path / "theknowledge-feedback-session.json"


def test_update_theknowledge_submodule_adopts_upstream_and_refreshes_managed_files(
    tmp_path: Path,
) -> None:
    project, source, _remote = _make_consuming_project(tmp_path)
    knowledge_repo = project / "TheKnowledge"
    assert knowledge_repo.joinpath(".git").is_file()

    template = source / "templates" / "AGENTS-footer.md"
    marker = "Update helper marker for downstream refresh."
    template.write_text(
        template.read_text(encoding="utf-8") + f"\n- {marker}\n",
        encoding="utf-8",
    )
    _git_ok("add", "templates/AGENTS-footer.md", cwd=source)
    _git_ok("commit", "-m", "Update managed footer", cwd=source)
    _git_ok("push", "origin", "trunk", cwd=source)
    updated_commit = _git_stdout("rev-parse", "HEAD", cwd=source)

    helper = _run(
        [
            sys.executable,
            str(knowledge_repo / "scripts" / "update_theknowledge_submodule.py"),
            "--project-root",
            str(project),
            "--knowledge-root",
            "TheKnowledge",
        ],
        cwd=knowledge_repo,
    )

    assert helper.returncode == 0, helper.stderr
    assert "Incoming commits on origin/trunk" in helper.stdout
    assert "Managed drift detected" in helper.stdout
    assert marker in (project / "AGENTS.md").read_text(encoding="utf-8")
    assert _git_stdout("rev-parse", "HEAD", cwd=knowledge_repo) == updated_commit

    status = _git_stdout("status", "--short", cwd=project)
    assert "M AGENTS.md" in status
    assert "M TheKnowledge" in status


def test_send_theknowledge_feedback_prepare_and_finish_without_push(
    tmp_path: Path,
) -> None:
    project, _source, _remote = _make_consuming_project(tmp_path)
    knowledge_repo = project / "TheKnowledge"
    original_branch = _git_stdout("branch", "--show-current", cwd=knowledge_repo)

    prepare = _run(
        [
            sys.executable,
            str(knowledge_repo / "scripts" / "send_theknowledge_feedback.py"),
            "prepare",
            "--project-root",
            str(project),
            "--knowledge-root",
            "TheKnowledge",
        ],
        cwd=knowledge_repo,
    )

    assert prepare.returncode == 0, prepare.stderr
    assert _git_stdout("branch", "--show-current", cwd=knowledge_repo) == "Feedback"
    assert _session_path(knowledge_repo).is_file()

    note = knowledge_repo / "feedback-note.txt"
    note.write_text("feedback\n", encoding="utf-8")

    finish = _run(
        [
            sys.executable,
            str(knowledge_repo / "scripts" / "send_theknowledge_feedback.py"),
            "finish",
            "--project-root",
            str(project),
            "--knowledge-root",
            "TheKnowledge",
            "--message",
            "Record Feedback",
        ],
        cwd=knowledge_repo,
    )

    assert finish.returncode == 0, finish.stderr
    assert "without pushing" in finish.stdout
    assert (
        _git_stdout("branch", "--show-current", cwd=knowledge_repo) == original_branch
    )
    assert not _session_path(knowledge_repo).exists()
    assert _git_stdout("rev-parse", "Feedback", cwd=knowledge_repo) != _git_stdout(
        "rev-parse", "origin/Feedback", cwd=knowledge_repo
    )
    assert _git_stdout("status", "--short", cwd=project) == ""


def test_send_theknowledge_feedback_restores_state_when_push_fails(
    tmp_path: Path,
) -> None:
    project, _source, _remote = _make_consuming_project(tmp_path)
    knowledge_repo = project / "TheKnowledge"
    original_branch = _git_stdout("branch", "--show-current", cwd=knowledge_repo)

    _git_ok(
        "remote",
        "set-url",
        "--push",
        "origin",
        str(tmp_path / "missing-remote.git"),
        cwd=knowledge_repo,
    )

    prepare = _run(
        [
            sys.executable,
            str(knowledge_repo / "scripts" / "send_theknowledge_feedback.py"),
            "prepare",
            "--project-root",
            str(project),
            "--knowledge-root",
            "TheKnowledge",
        ],
        cwd=knowledge_repo,
    )
    assert prepare.returncode == 0, prepare.stderr

    (knowledge_repo / "feedback-note.txt").write_text("feedback\n", encoding="utf-8")

    finish = _run(
        [
            sys.executable,
            str(knowledge_repo / "scripts" / "send_theknowledge_feedback.py"),
            "finish",
            "--project-root",
            str(project),
            "--knowledge-root",
            "TheKnowledge",
            "--message",
            "Record Feedback",
            "--push",
        ],
        cwd=knowledge_repo,
    )

    assert finish.returncode == 1
    assert "push was not completed" in finish.stderr
    assert (
        _git_stdout("branch", "--show-current", cwd=knowledge_repo) == original_branch
    )
    assert not _session_path(knowledge_repo).exists()
    assert _git_stdout("rev-parse", "Feedback", cwd=knowledge_repo) != _git_stdout(
        "rev-parse", "origin/Feedback", cwd=knowledge_repo
    )
    assert _git_stdout("status", "--short", cwd=project) == ""


def test_send_theknowledge_feedback_abort_restores_state(
    tmp_path: Path,
) -> None:
    project, _source, _remote = _make_consuming_project(tmp_path)
    knowledge_repo = project / "TheKnowledge"
    original_branch = _git_stdout("branch", "--show-current", cwd=knowledge_repo)

    prepare = _run(
        [
            sys.executable,
            str(knowledge_repo / "scripts" / "send_theknowledge_feedback.py"),
            "prepare",
            "--project-root",
            str(project),
            "--knowledge-root",
            "TheKnowledge",
        ],
        cwd=knowledge_repo,
    )
    assert prepare.returncode == 0, prepare.stderr

    abort = _run(
        [
            sys.executable,
            str(knowledge_repo / "scripts" / "send_theknowledge_feedback.py"),
            "abort",
            "--project-root",
            str(project),
            "--knowledge-root",
            "TheKnowledge",
        ],
        cwd=knowledge_repo,
    )

    assert abort.returncode == 0, abort.stderr
    assert (
        _git_stdout("branch", "--show-current", cwd=knowledge_repo) == original_branch
    )
    assert not _session_path(knowledge_repo).exists()
