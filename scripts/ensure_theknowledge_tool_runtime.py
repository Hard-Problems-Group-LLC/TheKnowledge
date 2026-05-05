#!/usr/bin/env python3
"""Ensure the direct-checkout TheKnowledge tool runtime exists locally."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
from typing import Optional, Sequence

try:
    from tool_validation_profiles import resolve_runtime_policy_executable
except ImportError:  # pragma: no cover - import path varies by entry point.
    from scripts.tool_validation_profiles import resolve_runtime_policy_executable


REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_RUNTIME_DIR = REPO_ROOT / ".local" / "theknowledge-tool-runtime"
LOCAL_BIN_DIR = REPO_ROOT / ".local" / "bin"
LOCAL_WRAPPER = LOCAL_BIN_DIR / "theknowledge-python-tools"
TOOL_RUNTIME_POLICY = "steady_state_python_tools"
TOOL_RUNTIME_MODULES = ["black", "ruff", "pytest"]
OVERRIDE_ENV_VARS = ("THEKNOWLEDGE_PYTHON_TOOLS", "THEKNOWLEDGE_BLACK_PYTHON")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse command-line arguments for the local tool-runtime helper."""

    parser = argparse.ArgumentParser(
        description=(
            "Ensure a direct-checkout TheKnowledge Python tool runtime exists "
            "under .local/ and print the selected interpreter path."
        )
    )
    parser.add_argument(
        "--print-python",
        action="store_true",
        help="Print the selected tool-runtime interpreter path.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit nonzero instead of creating a runtime when none is ready.",
    )
    parser.add_argument(
        "--python",
        default=None,
        help=(
            "Override the base Python 3.12+ interpreter used to create the "
            "local tool runtime when one must be refreshed."
        ),
    )
    parser.add_argument(
        "--runtime-dir",
        type=Path,
        default=LOCAL_RUNTIME_DIR,
        help="Checkout-local tool-runtime directory path.",
    )
    return parser.parse_args(argv)


def runtime_python_path(runtime_dir: Path) -> Path:
    """Return the interpreter path inside one runtime virtual environment."""

    bin_dir = "Scripts" if os.name == "nt" else "bin"
    executable = "python.exe" if os.name == "nt" else "python"
    return runtime_dir / bin_dir / executable


def run(command: Sequence[object]) -> None:
    """Run one helper command in the repository root."""

    printable = " ".join(str(part) for part in command)
    print(f"[ensure-tool-runtime] -> {printable}", file=sys.stderr)
    subprocess.run([str(part) for part in command], cwd=REPO_ROOT, check=True)


def python_version(executable: object) -> str:
    """Return the interpreter version string reported by one Python binary."""

    completed = subprocess.run(
        [str(executable), "--version"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    version_text = (completed.stdout or completed.stderr).strip()
    prefix = "Python "
    if not version_text.startswith(prefix):
        raise RuntimeError(
            f"Unexpected version output from {executable}: {version_text}"
        )
    return version_text[len(prefix) :]


def resolve_ready_runtime(runtime_dir: Path) -> str | None:
    """Return a deliberate ready runtime, if one already exists."""

    for env_name in OVERRIDE_ENV_VARS:
        explicit = os.environ.get(env_name)
        if not explicit:
            continue
        return resolve_runtime_policy_executable(
            REPO_ROOT,
            TOOL_RUNTIME_POLICY,
            explicit_candidate=explicit,
            required_modules=TOOL_RUNTIME_MODULES,
        )

    candidates = [
        REPO_ROOT / ".venv" / "bin" / "python",
        REPO_ROOT / ".venv" / "Scripts" / "python.exe",
        runtime_python_path(runtime_dir),
    ]
    for candidate in candidates:
        if not candidate.exists():
            continue
        try:
            return resolve_runtime_policy_executable(
                REPO_ROOT,
                TOOL_RUNTIME_POLICY,
                explicit_candidate=str(candidate),
                required_modules=TOOL_RUNTIME_MODULES,
            )
        except RuntimeError:
            continue
    return None


def select_base_python(python_override: Optional[str]) -> str:
    """Resolve the base Python 3.12+ interpreter for runtime creation."""

    return resolve_runtime_policy_executable(
        REPO_ROOT,
        TOOL_RUNTIME_POLICY,
        explicit_candidate=python_override,
        required_modules=[],
    )


def ensure_virtualenv(base_python: str, runtime_dir: Path) -> Path:
    """Create or refresh the local tool-runtime virtual environment."""

    runtime_python = runtime_python_path(runtime_dir)
    if runtime_python.exists():
        if python_version(runtime_python) != python_version(base_python):
            run([base_python, "-m", "venv", "--clear", runtime_dir])
        return runtime_python

    runtime_dir.parent.mkdir(parents=True, exist_ok=True)
    run([base_python, "-m", "venv", runtime_dir])
    return runtime_python


def install_tooling(runtime_python: Path) -> None:
    """Install the pinned direct-checkout developer tooling."""

    run(
        [
            runtime_python,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "setuptools",
            "wheel",
        ]
    )
    run([runtime_python, "-m", "pip", "install", "-e", ".[dev]"])


def write_local_wrapper(runtime_python: Path) -> None:
    """Write one checkout-local helper wrapper under `.local/bin/`."""

    wrapper_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        f'exec "{runtime_python}" "$@"',
        "",
    ]
    LOCAL_BIN_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_WRAPPER.write_text("\n".join(wrapper_lines), encoding="utf-8")
    LOCAL_WRAPPER.chmod(0o755)


def ensure_runtime(runtime_dir: Path, python_override: Optional[str]) -> str:
    """Return a ready local tool-runtime interpreter, creating it if needed."""

    ready = resolve_ready_runtime(runtime_dir)
    if ready is not None:
        return ready

    base_python = select_base_python(python_override)
    runtime_python = ensure_virtualenv(base_python, runtime_dir)
    install_tooling(runtime_python)
    write_local_wrapper(runtime_python)
    ready = resolve_ready_runtime(runtime_dir)
    if ready is None:
        raise RuntimeError(
            "Local tool runtime was created, but the required modules are "
            "still unavailable."
        )
    return ready


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Ensure or inspect the direct-checkout tool runtime."""

    args = parse_args(argv or sys.argv[1:])
    try:
        ready = resolve_ready_runtime(args.runtime_dir)
        if ready is None and args.check:
            raise RuntimeError(
                "No ready direct-checkout tool runtime is available. Run "
                "`python scripts/ensure_theknowledge_tool_runtime.py` first."
            )
        if ready is None:
            ready = ensure_runtime(args.runtime_dir, args.python)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"[ensure-tool-runtime] FAIL: {error}", file=sys.stderr)
        return 1

    if args.print_python or not args.check:
        print(ready)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
