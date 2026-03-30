#!/usr/bin/env python3
"""Run Codex CLI with optional repo-local npm isolation."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

LOCAL_DIR_NAME = ".codex-local"
MANIFEST_NAME = "package.json"
LOCAL_PACKAGE_MARKER = Path("node_modules") / "@openai" / "codex"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def local_dir(root: Path) -> Path:
    return root / LOCAL_DIR_NAME


def local_manifest(root: Path) -> Path:
    return local_dir(root) / MANIFEST_NAME


def local_package_marker(root: Path) -> Path:
    return local_dir(root) / LOCAL_PACKAGE_MARKER


def npm_executable(name: str) -> str:
    if os.name == "nt":
        return f"{name}.cmd"
    return name


def build_install_command(root: Path) -> list[str]:
    return [
        npm_executable("npm"),
        "install",
        "--prefix",
        str(local_dir(root)),
    ]


def build_local_run_command(root: Path, argv: Sequence[str]) -> list[str]:
    return [
        npm_executable("npx"),
        "--prefix",
        str(local_dir(root)),
        "codex",
        *argv,
    ]


def build_fallback_command(argv: Sequence[str]) -> list[str]:
    return [
        npm_executable("npx"),
        "--yes",
        "--package",
        "@openai/codex",
        "codex",
        *argv,
    ]


def has_local_manifest(root: Path) -> bool:
    return local_manifest(root).is_file()


def needs_local_install(root: Path) -> bool:
    return has_local_manifest(root) and not local_package_marker(root).exists()


def choose_commands(
    root: Path, argv: Sequence[str]
) -> tuple[list[str] | None, list[str]]:
    if has_local_manifest(root):
        install = build_install_command(root) if needs_local_install(root) else None
        return install, build_local_run_command(root, argv)
    return None, build_fallback_command(argv)


def run(command: Sequence[str], cwd: Path) -> int:
    return subprocess.run(list(command), cwd=cwd, check=False).returncode


def main(argv: Sequence[str] | None = None) -> int:
    root = repo_root()
    install_command, run_command = choose_commands(root, argv or sys.argv[1:])

    if install_command is not None:
        print(
            "[codex-local] Installing repo-local Codex CLI dependencies from "
            f"{local_manifest(root)}"
        )
        install_result = run(install_command, cwd=root)
        if install_result != 0:
            return install_result

    return run(run_command, cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())
