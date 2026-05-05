from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "run_tool_with_timeout.py"


def _load_script_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_tool_with_timeout", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_resolve_tool_run_replaces_default_scope_with_explicit_paths() -> None:
    module = _load_script_module()
    config = {
        "default_timeout_seconds": 60,
        "tools": {
            "black": {
                "command": [
                    "python",
                    "-m",
                    "black",
                    ".",
                    "--no-cache",
                    "--exclude",
                    "/(\\.venv|project\\.egg-info)/",
                ],
                "timeout_seconds": 120,
                "replace_default_scope_with_args": True,
            }
        },
    }

    command, timeout, retries, cleanup_patterns = module._resolve_tool_run(
        config,
        "black",
        None,
        ["--", "src/app.py", "tests/test_app.py"],
    )

    assert command == [
        "python",
        "-m",
        "black",
        "src/app.py",
        "tests/test_app.py",
        "--no-cache",
        "--exclude",
        "/(\\.venv|project\\.egg-info)/",
    ]
    assert timeout == 120
    assert retries == 0
    assert cleanup_patterns == []


def test_resolve_tool_run_keeps_default_scope_without_explicit_paths() -> None:
    module = _load_script_module()
    config = {
        "default_timeout_seconds": 60,
        "tools": {
            "black": {
                "command": [
                    "python",
                    "-m",
                    "black",
                    ".",
                    "--no-cache",
                    "--exclude",
                    "/(\\.venv|project\\.egg-info)/",
                ],
                "timeout_seconds": 120,
                "replace_default_scope_with_args": True,
            }
        },
    }

    command, timeout, retries, cleanup_patterns = module._resolve_tool_run(
        config,
        "black",
        None,
        [],
    )

    assert command == [
        "python",
        "-m",
        "black",
        ".",
        "--no-cache",
        "--exclude",
        "/(\\.venv|project\\.egg-info)/",
    ]
    assert timeout == 120
    assert retries == 0
    assert cleanup_patterns == []


def test_resolve_tool_run_can_reuse_wrapper_python() -> None:
    module = _load_script_module()
    config = {
        "default_timeout_seconds": 60,
        "tools": {
            "pytest": {
                "command": ["python", "-m", "pytest"],
                "use_wrapper_python": True,
            }
        },
    }

    command, timeout, retries, cleanup_patterns = module._resolve_tool_run(
        config,
        "pytest",
        None,
        [],
    )

    assert command == [sys.executable, "-m", "pytest"]
    assert timeout == 60
    assert retries == 0
    assert cleanup_patterns == []


def test_resolve_tool_run_can_use_runtime_policy(monkeypatch) -> None:
    module = _load_script_module()
    config = {
        "default_timeout_seconds": 60,
        "tools": {
            "pytest": {
                "command": ["python", "-m", "pytest"],
                "runtime_policy": "steady_state_python_tools",
            }
        },
    }

    monkeypatch.setattr(
        module,
        "resolve_runtime_policy_executable",
        lambda cwd, policy_name: "managed-python",
    )

    command, timeout, retries, cleanup_patterns = module._resolve_tool_run(
        config,
        "pytest",
        None,
        [],
    )

    assert command == ["managed-python", "-m", "pytest"]
    assert timeout == 60
    assert retries == 0
    assert cleanup_patterns == []


def _write_execution_constraints(repo_root: Path) -> None:
    (repo_root / "tool_execution_constraints.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "products": {
                    "codex": {
                        "sandbox_technologies": {
                            "bubblewrap": {
                                "environments": {
                                    "managed_linux_sandbox": {
                                        "match": {
                                            "env_all_of": {
                                                "CODEX_CI": "1",
                                                "CODEX_MANAGED_BY_NPM": "1",
                                                "CODEX_SANDBOX_NETWORK_DISABLED": "1",
                                            }
                                        },
                                        "tools": {
                                            "black": {
                                                "parallel_safety": {
                                                    "status": "unsafe",
                                                    "applies_when": {
                                                        "invocation_kind": "any",
                                                        "path_count_gte": 2,
                                                    },
                                                    "preferred_workaround": {
                                                        "mode": (
                                                            "serial_explicit_paths"
                                                        )
                                                    },
                                                }
                                            }
                                        },
                                    }
                                }
                            }
                        }
                    }
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def test_main_serializes_black_through_timeout_wrapper_in_matching_sandbox(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = _load_script_module()
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "tests").mkdir(parents=True)
    (repo / ".venv").mkdir(parents=True)
    (repo / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (repo / "tests" / "test_app.py").write_text(
        "def test_ok():\n    assert 1\n",
        encoding="utf-8",
    )
    (repo / ".venv" / "ignored.py").write_text("print('skip')\n", encoding="utf-8")
    _write_execution_constraints(repo)

    monkeypatch.chdir(repo)
    monkeypatch.setenv("CODEX_CI", "1")
    monkeypatch.setenv("CODEX_MANAGED_BY_NPM", "1")
    monkeypatch.setenv("CODEX_SANDBOX_NETWORK_DISABLED", "1")
    monkeypatch.setattr(
        module,
        "discover_black_paths",
        lambda cwd, tokens=None, include_ignored=False: [
            "src/app.py",
            "tests/test_app.py",
        ],
    )
    monkeypatch.setattr(
        module,
        "group_black_paths_by_profile",
        lambda cwd, relative_paths: [
            (
                {
                    "name": "repository_python",
                    "allow_serial_fallback": True,
                },
                list(relative_paths),
            )
        ],
    )

    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    result = module.main(["black"])

    assert result == 0
    assert commands == [
        [
            sys.executable,
            str(SCRIPT),
            "black",
            "--",
            "src/app.py",
        ],
        [
            sys.executable,
            str(SCRIPT),
            "black",
            "--",
            "tests/test_app.py",
        ],
    ]


def test_main_preserves_explicit_black_flags_when_serializing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = _load_script_module()
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "tests").mkdir(parents=True)
    (repo / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (repo / "tests" / "test_app.py").write_text(
        "def test_ok():\n    assert 1\n",
        encoding="utf-8",
    )
    _write_execution_constraints(repo)

    monkeypatch.chdir(repo)
    monkeypatch.setenv("CODEX_CI", "1")
    monkeypatch.setenv("CODEX_MANAGED_BY_NPM", "1")
    monkeypatch.setenv("CODEX_SANDBOX_NETWORK_DISABLED", "1")
    monkeypatch.setattr(
        module,
        "discover_black_paths",
        lambda cwd, tokens=None, include_ignored=False: [
            "src/app.py",
            "tests/test_app.py",
        ],
    )
    monkeypatch.setattr(
        module,
        "group_black_paths_by_profile",
        lambda cwd, relative_paths: [
            (
                {
                    "name": "repository_python",
                    "allow_serial_fallback": True,
                },
                list(relative_paths),
            )
        ],
    )

    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    result = module.main(
        [
            "black",
            "--",
            "--check",
            "src/app.py",
            "tests/test_app.py",
        ]
    )

    assert result == 0
    assert commands == [
        [
            sys.executable,
            str(SCRIPT),
            "black",
            "--",
            "--check",
            "src/app.py",
        ],
        [
            sys.executable,
            str(SCRIPT),
            "black",
            "--",
            "--check",
            "tests/test_app.py",
        ],
    ]


def test_main_runs_black_directly_without_matching_constraint(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = _load_script_module()
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "tests").mkdir(parents=True)
    (repo / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (repo / "tests" / "test_app.py").write_text(
        "def test_ok():\n    assert 1\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(repo)
    monkeypatch.setattr(
        module,
        "discover_black_paths",
        lambda cwd, tokens=None, include_ignored=False: [
            "src/app.py",
            "tests/test_app.py",
        ],
    )
    monkeypatch.setattr(
        module,
        "group_black_paths_by_profile",
        lambda cwd, relative_paths: [
            (
                {
                    "name": "repository_python",
                    "allow_serial_fallback": True,
                    "runtime_policy": "steady_state_python_tools",
                    "target_version": "py39",
                },
                list(relative_paths),
            )
        ],
    )
    monkeypatch.setattr(
        module,
        "resolve_runtime_policy_executable",
        lambda cwd, policy_name: "python3.12",
    )

    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    result = module.main(["black"])

    assert result == 0
    assert commands == [
        [
            "python3.12",
            "-m",
            "black",
            "--no-cache",
            "--target-version",
            "py39",
            "src/app.py",
            "tests/test_app.py",
        ]
    ]
