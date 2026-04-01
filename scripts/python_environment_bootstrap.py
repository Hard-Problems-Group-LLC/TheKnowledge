#!/usr/bin/env python3
"""Shared helpers for pyenv-based bootstrap and context selection.

This module keeps the bootstrap-stage-two scripts and the starter-installed
context helpers aligned on one JSON config format. It handles config loading,
pyenv environment planning, `.python-version` updates, and optional shell-init
snippet management without baking those details into multiple entry points.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

CONFIG_FILE_NAME = "python-environments.json"
SHELL_INIT_BEGIN = "# >>> theknowledge pyenv init >>>"
SHELL_INIT_END = "# <<< theknowledge pyenv init <<<"


@dataclass(frozen=True)
class PythonContextConfig:
    """Describe one named Python context from `python-environments.json`."""

    required_version: str
    base_version: str
    environment_name: str


@dataclass(frozen=True)
class PythonEnvironmentConfig:
    """Hold the bootstrap and runtime Python context definitions."""

    bootstrap: PythonContextConfig
    runtime: PythonContextConfig


def slugify_project_name(name: str) -> str:
    """Convert a project directory name into a stable lowercase slug."""

    lowered = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered)
    return slug.strip("-") or "project"


def _load_context(data: dict[str, object], key: str) -> PythonContextConfig:
    """Load one context record from parsed JSON data."""

    entry = data.get(key)
    if not isinstance(entry, dict):
        raise ValueError(f"python-environments config must define '{key}'")

    required = entry.get("required_version")
    base = entry.get("base_version")
    env_name = entry.get("environment_name")
    if not isinstance(required, str):
        raise ValueError(f"python-environments.{key}.required_version must be a string")
    if not isinstance(base, str):
        raise ValueError(f"python-environments.{key}.base_version must be a string")
    if not isinstance(env_name, str):
        raise ValueError(f"python-environments.{key}.environment_name must be a string")
    return PythonContextConfig(
        required_version=required,
        base_version=base,
        environment_name=env_name,
    )


def load_python_environment_config(
    repo_root: Path, config_name: str = CONFIG_FILE_NAME
) -> PythonEnvironmentConfig:
    """Load and validate the pyenv bootstrap/runtime configuration."""

    config_path = repo_root / config_name
    with config_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("python-environments config must be a JSON object")
    return PythonEnvironmentConfig(
        bootstrap=_load_context(data, "bootstrap"),
        runtime=_load_context(data, "runtime"),
    )


def version_tuple(version_text: str) -> tuple[int, ...]:
    """Parse a dotted Python version string into a comparable tuple."""

    return tuple(int(part) for part in version_text.split("."))


def ensure_minimum_python(
    version_info: Sequence[int], minimum_version: str, *, label: str
) -> None:
    """Fail when the active interpreter is below the configured minimum."""

    current = tuple(version_info[: len(version_tuple(minimum_version))])
    minimum = version_tuple(minimum_version)
    if current < minimum:
        current_text = ".".join(str(part) for part in current)
        raise RuntimeError(
            f"{label} requires Python {minimum_version}+ but is running on "
            f"{current_text}."
        )


def ensure_pyenv_available() -> None:
    """Verify that `pyenv` and the `virtualenv` plugin are available."""

    version_result = subprocess.run(
        ["pyenv", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    if version_result.returncode != 0:
        raise RuntimeError(
            "pyenv is required for this bootstrap flow. Install pyenv and "
            "retry, or use a project-local bootstrap override instead."
        )

    virtualenv_result = subprocess.run(
        ["pyenv", "virtualenv", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    if virtualenv_result.returncode != 0:
        raise RuntimeError(
            "pyenv-virtualenv is required for this bootstrap flow. Install "
            "the plugin and retry."
        )


def pyenv_root() -> Path:
    """Resolve the active pyenv root directory."""

    configured = os.environ.get("PYENV_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()

    result = subprocess.run(
        ["pyenv", "root"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("Unable to resolve `pyenv root`.")
    return Path((result.stdout or "").strip()).expanduser().resolve()


def pyenv_python_executable(pyenv_root_path: Path, environment_name: str) -> Path:
    """Return the expected Python executable path for one pyenv environment."""

    executable = "python.exe" if os.name == "nt" else "python"
    bin_dir = "Scripts" if os.name == "nt" else "bin"
    return pyenv_root_path / "versions" / environment_name / bin_dir / executable


def ensure_pyenv_environment(
    context: PythonContextConfig,
    *,
    runner: Callable[[Sequence[str]], None],
) -> None:
    """Ensure that one configured pyenv base version and virtualenv exist."""

    runner(["pyenv", "install", "-s", context.base_version])
    runner(
        [
            "pyenv",
            "virtualenv",
            "--force",
            context.base_version,
            context.environment_name,
        ]
    )


def write_python_version_file(repo_root: Path, environment_name: str) -> None:
    """Write `.python-version` so pyenv defaults to the runtime context."""

    (repo_root / ".python-version").write_text(
        environment_name + "\n",
        encoding="utf-8",
    )


def shell_init_snippet() -> str:
    """Return the idempotent shell-init block for pyenv integration."""

    return "\n".join(
        [
            SHELL_INIT_BEGIN,
            'export PYENV_ROOT="${PYENV_ROOT:-$HOME/.pyenv}"',
            'case ":$PATH:" in',
            '  *":$PYENV_ROOT/bin:"*) ;;',
            '  *) export PATH="$PYENV_ROOT/bin:$PATH" ;;',
            "esac",
            'eval "$(pyenv init -)"',
            'eval "$(pyenv virtualenv-init -)"',
            SHELL_INIT_END,
            "",
        ]
    )


def default_shell_init_files(home: Path | None = None) -> list[Path]:
    """Return the common shell startup files that may need pyenv init."""

    root = home or Path.home()
    return [root / ".bashrc", root / ".zshrc", root / ".profile"]


def append_shell_init_snippet(path: Path, snippet: str) -> None:
    """Append the pyenv init snippet to one shell startup file once."""

    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if SHELL_INIT_BEGIN in existing and SHELL_INIT_END in existing:
        return

    prefix = existing.rstrip()
    if prefix:
        prefix += "\n\n"
    path.write_text(prefix + snippet, encoding="utf-8")
