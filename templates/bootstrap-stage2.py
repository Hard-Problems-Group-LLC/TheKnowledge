#!/usr/bin/env python3
"""Provision pyenv bootstrap/runtime contexts for a consuming project."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from scripts.python_environment_bootstrap import (
    append_shell_init_snippet,
    default_shell_init_files,
    ensure_minimum_python,
    ensure_pyenv_available,
    ensure_pyenv_environment,
    load_python_environment_config,
    pyenv_python_executable,
    pyenv_root,
    shell_init_snippet,
    write_python_version_file,
)

REPO_ROOT = Path(__file__).resolve().parent
INSTALLER = REPO_ROOT / "scripts" / "dev_setup.py"


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse bootstrap-stage-two arguments and installer passthrough args."""

    parser = argparse.ArgumentParser(
        description=(
            "Create or refresh the configured pyenv bootstrap/runtime "
            "contexts, then hand off to the starter dev-setup path."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned steps without mutating pyenv or repository files.",
    )
    parser.add_argument(
        "--update-shell-init",
        action="store_true",
        help="Append pyenv init snippets to common shell startup files.",
    )
    parsed, passthrough = parser.parse_known_args(argv)
    parsed.installer_args = passthrough[1:] if passthrough[:1] == ["--"] else passthrough
    return parsed


def run(command: Sequence[str], *, dry_run: bool) -> None:
    """Run one external command with a bootstrap-stage-two prefix."""

    printable = " ".join(str(part) for part in command)
    print(f"[bootstrap-stage2] -> {printable}")
    if dry_run:
        return
    subprocess.run([str(part) for part in command], check=True, cwd=REPO_ROOT)


def write_runtime_python_version(environment_name: str, *, dry_run: bool) -> None:
    """Update `.python-version` to the configured runtime environment."""

    target = REPO_ROOT / ".python-version"
    print(f"[bootstrap-stage2] -> write {target.name} = {environment_name}")
    if dry_run:
        return
    write_python_version_file(REPO_ROOT, environment_name)


def update_shell_init_files(*, dry_run: bool) -> None:
    """Append pyenv init snippets to common shell startup files."""

    snippet = shell_init_snippet()
    for target in default_shell_init_files():
        print(f"[bootstrap-stage2] -> ensure pyenv init in {target}")
        if not dry_run:
            append_shell_init_snippet(target, snippet)


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the pyenv bootstrap flow for a consuming project."""

    args = parse_args(argv or sys.argv[1:])
    try:
        config = load_python_environment_config(REPO_ROOT)
        ensure_minimum_python(
            sys.version_info[:3],
            config.bootstrap.required_version,
            label="bootstrap-stage2.py",
        )
        ensure_pyenv_available()
        root = pyenv_root()
        ensure_pyenv_environment(
            config.bootstrap,
            runner=lambda command: run(command, dry_run=args.dry_run),
        )
        ensure_pyenv_environment(
            config.runtime,
            runner=lambda command: run(command, dry_run=args.dry_run),
        )
        runtime_python = pyenv_python_executable(root, config.runtime.environment_name)
        write_runtime_python_version(
            config.runtime.environment_name,
            dry_run=args.dry_run,
        )
        if args.update_shell_init:
            update_shell_init_files(dry_run=args.dry_run)
        if not args.dry_run and not runtime_python.is_file():
            raise RuntimeError(
                f"Expected runtime interpreter is missing: {runtime_python}"
            )
        run(
            [
                str(runtime_python),
                str(INSTALLER),
                "--python",
                str(runtime_python),
                *args.installer_args,
            ],
            dry_run=args.dry_run,
        )
    except (RuntimeError, subprocess.CalledProcessError, ValueError) as error:
        print(f"[bootstrap-stage2] FAIL: {error}", file=sys.stderr)
        return 1

    print("[bootstrap-stage2] PASS: pyenv bootstrap and starter handoff complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
