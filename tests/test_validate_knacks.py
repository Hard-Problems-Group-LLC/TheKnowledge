from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate_knacks.py"
TIMEOUTS = ROOT / "scripts" / "tool_timeouts.json"
ENTROPY = (
    ROOT / "standards-and-practices" / "dev-utils" / "security" / "entropy-check.py"
)


def _run(project_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--project-root", str(project_root), *args],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def _git_dir(project_root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    )
    git_dir = Path(result.stdout.strip())
    if not git_dir.is_absolute():
        git_dir = (project_root / git_dir).resolve()
    return git_dir


def _make_project(tmp_path: Path, *, separate_git_dir: bool = False) -> Path:
    project = tmp_path / "project"
    init_command = ["git", "init", "--quiet"]
    if separate_git_dir:
        init_command.extend(["--separate-git-dir", str(tmp_path / "project-git")])
    init_command.append(str(project))
    subprocess.run(init_command, check=True, capture_output=True, text=True)
    (project / "knacks").mkdir(parents=True)
    return project


def _make_knowledge_root(tmp_path: Path) -> Path:
    knowledge = tmp_path / "Knowledge"
    target = knowledge / "standards-and-practices" / "dev-utils" / "security"
    target.mkdir(parents=True)
    shutil.copy2(ENTROPY, target / "entropy-check.py")
    (knowledge / "knacks").mkdir(parents=True)
    return knowledge


def test_knack_validator_uses_cache_for_unchanged_files(tmp_path: Path) -> None:
    project = _make_project(tmp_path)
    knack = project / "knacks" / "demo.knack.md"
    knack.write_text(
        "# Demo\n\nPlain prose with stable wording.\n",
        encoding="utf-8",
    )

    first = _run(project, "--knowledge-root", str(ROOT))
    assert first.returncode == 0
    assert "PASS: project:demo.knack.md" in first.stdout

    second = _run(project, "--knowledge-root", str(ROOT))
    assert second.returncode == 0
    assert "SKIP: project:demo.knack.md" in second.stdout

    cache = project / ".git" / "knack-validation-cache.json"
    assert cache.is_file()


def test_knack_validator_uses_real_git_dir_for_separate_git_repo(
    tmp_path: Path,
) -> None:
    project = _make_project(tmp_path, separate_git_dir=True)
    knack = project / "knacks" / "demo.knack.md"
    knack.write_text(
        "# Demo\n\nPlain prose with stable wording.\n",
        encoding="utf-8",
    )

    result = _run(project, "--knowledge-root", str(ROOT))

    assert result.returncode == 0
    git_dir = _git_dir(project)
    assert (project / ".git").is_file()
    assert (git_dir / "knack-validation-cache.json").is_file()
    assert not (project / ".git" / "knack-validation-cache.json").exists()


def test_knack_validator_reports_unclosed_fence_as_error(tmp_path: Path) -> None:
    project = _make_project(tmp_path)
    knack = project / "knacks" / "broken.knack.md"
    knack.write_text(
        "# Broken\n\n```python\nprint('oops')\n",
        encoding="utf-8",
    )

    result = _run(project, "--knowledge-root", str(ROOT))

    assert result.returncode == 1
    assert "unclosed fenced code block" in result.stderr


def test_knack_validator_reports_word_count_as_warning(tmp_path: Path) -> None:
    project = _make_project(tmp_path)
    text = " ".join(["word"] * 1300)
    knack = project / "knacks" / "large.knack.md"
    knack.write_text(f"# Large\n\n{text}\n", encoding="utf-8")

    result = _run(project, "--knowledge-root", str(ROOT))

    assert result.returncode == 0
    assert "WARNING" in result.stdout
    assert "recommended 1250 words" in result.stdout


def test_knack_validator_reports_high_entropy_as_error(tmp_path: Path) -> None:
    project = _make_project(tmp_path)
    knack = project / "knacks" / "secret.knack.md"
    high_entropy_token = "".join(
        [
            "X4b9Rk2Qm8Lp0Vz7",
            "Hn6Tw3Ys5Df1Ja9C",
            "u2Me7Po4Gi8Nr5Kb",
            "1Qx6Zv0",
        ]
    )
    knack.write_text(
        "\n".join(
            [
                "# Secret",
                "",
                "this is ordinary prose content with predictable words and spacing.",
                "documentation text usually has repeated structures and lower entropy.",
                "another normal line that should be part of the clipped baseline set.",
                high_entropy_token,
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = _run(project, "--knowledge-root", str(ROOT))

    assert result.returncode == 1
    assert "high-entropy content detected" in result.stderr


def test_knack_validator_warns_on_stock_name_collision_but_checks_both(
    tmp_path: Path,
) -> None:
    project = _make_project(tmp_path)
    knowledge = _make_knowledge_root(tmp_path)
    project_knack = project / "knacks" / "UI" / "terminal" / "ansi.knack.md"
    project_knack.parent.mkdir(parents=True)
    project_knack.write_text("# Project ANSI\n\nPlain text.\n", encoding="utf-8")

    stock_knack = knowledge / "knacks" / "UI" / "terminal" / "ansi.knack.md"
    stock_knack.parent.mkdir(parents=True)
    stock_knack.write_text("# Stock ANSI\n\nPlain text.\n", encoding="utf-8")

    result = _run(project, "--knowledge-root", str(knowledge))

    assert result.returncode == 0
    assert "path collision" in result.stdout
    assert "project:UI/terminal/ansi.knack.md" in result.stdout
    assert "knowledge:UI/terminal/ansi.knack.md" in result.stdout


def test_timeout_wrapper_config_includes_knack_check() -> None:
    config = TIMEOUTS.read_text(encoding="utf-8")
    assert '"knack_check"' in config
    assert '"scripts/validate_knacks.py"' in config
