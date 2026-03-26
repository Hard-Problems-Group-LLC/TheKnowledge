from __future__ import annotations

import importlib.util
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
