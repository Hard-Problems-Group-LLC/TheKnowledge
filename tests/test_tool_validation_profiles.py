from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "tool_validation_profiles.py"


def _load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("tool_validation_profiles", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _init_repo(repo: Path) -> None:
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo,
        check=True,
    )


def test_resolve_black_profile_uses_placement_and_extension() -> None:
    module = _load_module()

    starter = module.resolve_black_profile(ROOT, "templates/scripts/dev_setup.py")
    repository = module.resolve_black_profile(ROOT, "scripts/run_tool_with_timeout.py")
    notebook = module.resolve_black_profile(ROOT, "notes/demo.ipynb")

    assert starter["name"] == "starter_python"
    assert starter["target_version"] == "py39"
    assert repository["name"] == "repository_python"
    assert repository["target_version"] == "py39"
    assert notebook["name"] == "python_notebooks"
    assert notebook["target_version"] == "py310"


def test_discover_black_paths_defaults_to_git_tracked_files(tmp_path: Path) -> None:
    module = _load_module()
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    (repo / "src").mkdir()
    (repo / "src" / "tracked.py").write_text("print('tracked')\n", encoding="utf-8")
    (repo / "src" / "untracked.py").write_text(
        "print('untracked')\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "src/tracked.py"], cwd=repo, check=True)

    discovered = module.discover_black_paths(repo)

    assert discovered == ["src/tracked.py"]


def test_discover_black_paths_skips_gitignored_files_by_default(
    tmp_path: Path,
) -> None:
    module = _load_module()
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    (repo / "ignored.py").write_text("print('ignored')\n", encoding="utf-8")
    (repo / ".gitignore").write_text("ignored.py\n", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore"], cwd=repo, check=True)

    default_paths = module.discover_black_paths(repo, ["ignored.py"])
    included_paths = module.discover_black_paths(
        repo,
        ["ignored.py"],
        include_ignored=True,
    )

    assert default_paths == []
    assert included_paths == ["ignored.py"]


def test_discover_black_paths_accepts_explicit_untracked_file(tmp_path: Path) -> None:
    module = _load_module()
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    (repo / "scratch.py").write_text("print('scratch')\n", encoding="utf-8")

    discovered = module.discover_black_paths(repo, ["scratch.py"])

    assert discovered == ["scratch.py"]


def test_resolve_runtime_policy_prefers_environment_override(monkeypatch) -> None:
    module = _load_module()
    candidates = {
        "bad-python": ((3, 9, 0), True),
        "good-python": ((3, 12, 0), True),
    }

    def fake_probe(executable: str, required_modules: list[str]):
        return candidates.get(executable)

    monkeypatch.setattr(module, "_probe_python_candidate", fake_probe)
    monkeypatch.setenv("THEKNOWLEDGE_PYTHON_TOOLS", "good-python")

    resolved = module.resolve_runtime_policy_executable(
        ROOT,
        "steady_state_python_tools",
        required_modules=[],
    )

    assert resolved == "good-python"


def test_resolve_runtime_policy_rejects_too_old_override(monkeypatch) -> None:
    module = _load_module()

    def fake_probe(executable: str, required_modules: list[str]):
        return (3, 9, 0), True

    monkeypatch.setattr(module, "_probe_python_candidate", fake_probe)

    with pytest.raises(RuntimeError):
        module.resolve_runtime_policy_executable(
            ROOT,
            "steady_state_python_tools",
            explicit_candidate="python3.9",
            required_modules=[],
        )


def test_resolve_runtime_policy_skips_missing_windows_candidate(
    monkeypatch,
) -> None:
    module = _load_module()
    preferred = [
        ".venv/Scripts/python.exe",
        "good-python",
    ]

    def fake_runtime_policies(repo_root: Path):
        return {
            "steady_state_python_tools": {
                "minimum_version": "3.12",
                "required_modules": [],
                "environment_variables": [],
                "preferred_executables": preferred,
            }
        }

    def fake_probe(executable: str, required_modules: list[str]):
        if executable.endswith("Scripts/python.exe"):
            return None
        if executable == "good-python":
            return (3, 12, 0), True
        return None

    monkeypatch.setattr(module, "_runtime_policies", fake_runtime_policies)
    monkeypatch.setattr(module, "_probe_python_candidate", fake_probe)

    resolved = module.resolve_runtime_policy_executable(
        ROOT,
        "steady_state_python_tools",
        required_modules=[],
    )

    assert resolved == "good-python"
