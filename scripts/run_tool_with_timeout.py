"""Run standard quality tools with timeout enforcement."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

try:
    from tool_execution_constraints import (
        load_execution_constraints,
        serial_execution_constraint_label,
    )
except ImportError:  # pragma: no cover - import path varies by entry point.
    from scripts.tool_execution_constraints import (
        load_execution_constraints,
        serial_execution_constraint_label,
    )


CONFIG_FILE = Path(__file__).resolve().with_name("tool_timeouts.json")
EXECUTION_CONSTRAINTS_FILE = "tool_execution_constraints.json"
BLACK_FILE_SUFFIXES = {".ipynb", ".py", ".pyi"}
BLACK_EXCLUDED_DIRS = {
    ".codex-home",
    ".codex-local",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "project.egg-info",
}
BLACK_LONG_OPTIONS_WITH_VALUE = {
    "--code",
    "--config",
    "--exclude",
    "--extend-exclude",
    "--force-exclude",
    "--ipynb",
    "--line-length",
    "--line-ranges",
    "--python-cell-magics",
    "--required-version",
    "--stdin-filename",
    "--target-version",
    "--workers",
}
BLACK_SHORT_OPTIONS_WITH_VALUE = {
    "-c",
    "-l",
    "-t",
    "-W",
}


def _load_config() -> Dict[str, object]:
    with CONFIG_FILE.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("timeout configuration must be a JSON object")
    return data


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a configured tool command with a timeout bailout."
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=None,
        help="Override timeout in seconds for this invocation.",
    )
    parser.add_argument(
        "tool", help="Configured tool key in scripts/tool_timeouts.json"
    )
    parsed, tool_args = parser.parse_known_args(argv)
    parsed.tool_args = tool_args
    return parsed


def _resolve_tool_run(
    config: Dict[str, object],
    tool: str,
    override_timeout: int | None,
    tool_args: List[str],
) -> Tuple[List[str], int, int, List[str]]:
    tools = config.get("tools")
    if not isinstance(tools, dict):
        raise ValueError("configuration must include a 'tools' object")

    entry = tools.get(tool)
    if not isinstance(entry, dict):
        available = ", ".join(sorted(tools))
        raise KeyError(f"unknown tool '{tool}'. Available tools: {available}")

    command = entry.get("command")
    if not isinstance(command, list) or not all(
        isinstance(part, str) for part in command
    ):
        raise ValueError(f"tool '{tool}' must define command as a list of strings")

    replace_default_scope_with_args = entry.get(
        "replace_default_scope_with_args", False
    )
    if not isinstance(replace_default_scope_with_args, bool):
        raise ValueError("replace_default_scope_with_args must be a boolean")

    timeout = override_timeout
    if timeout is None:
        configured_timeout = entry.get("timeout_seconds")
        if isinstance(configured_timeout, int) and configured_timeout > 0:
            timeout = configured_timeout
        else:
            default_timeout = config.get("default_timeout_seconds")
            if not isinstance(default_timeout, int) or default_timeout <= 0:
                raise ValueError("default_timeout_seconds must be a positive integer")
            timeout = default_timeout

    if timeout <= 0:
        raise ValueError("timeout must be a positive integer")

    retries = entry.get("timeout_retries", 0)
    if not isinstance(retries, int) or retries < 0:
        raise ValueError("timeout_retries must be a non-negative integer")

    cleanup_patterns = entry.get("cleanup_patterns", [])
    if not isinstance(cleanup_patterns, list) or not all(
        isinstance(pattern, str) for pattern in cleanup_patterns
    ):
        raise ValueError("cleanup_patterns must be a list of strings")

    args = list(tool_args)
    if args and args[0] == "--":
        args = args[1:]

    resolved_command = list(command)
    if args and replace_default_scope_with_args:
        placeholder_indexes = [
            index for index, part in enumerate(resolved_command) if part == "."
        ]
        if len(placeholder_indexes) != 1:
            raise ValueError(
                f"tool '{tool}' must contain exactly one '.' scope placeholder "
                "when replace_default_scope_with_args is enabled"
            )
        placeholder_index = placeholder_indexes[0]
        resolved_command = (
            resolved_command[:placeholder_index]
            + args
            + resolved_command[placeholder_index + 1 :]
        )
        args = []

    return resolved_command + args, timeout, retries, cleanup_patterns


def _cleanup_processes(patterns: List[str]) -> None:
    if not patterns:
        return
    if os.name != "posix":
        return

    for pattern in patterns:
        try:
            subprocess.run(["pkill", "-f", pattern], check=False)
            print(f"[timeout-wrapper] cleanup attempted for pattern: {pattern}")
        except FileNotFoundError:
            print("[timeout-wrapper] cleanup skipped; pkill not available.")
            return


def _normalize_tool_args(tool_args: Sequence[str]) -> List[str]:
    normalized = list(tool_args)
    if normalized and normalized[0] == "--":
        normalized = normalized[1:]
    return normalized


def _black_option_and_path_args(
    tool_args: Sequence[str],
) -> tuple[List[str], List[str]]:
    option_args: List[str] = []
    path_args: List[str] = []
    expecting_value = False

    for arg in _normalize_tool_args(tool_args):
        if expecting_value:
            option_args.append(arg)
            expecting_value = False
            continue

        if arg == "--":
            continue

        if arg.startswith("--") and arg != "--":
            option_args.append(arg)
            if "=" not in arg and arg in BLACK_LONG_OPTIONS_WITH_VALUE:
                expecting_value = True
            continue

        if arg.startswith("-") and arg != "-":
            option_args.append(arg)
            short_flag = arg[:2]
            if len(arg) == 2 and short_flag in BLACK_SHORT_OPTIONS_WITH_VALUE:
                expecting_value = True
            continue

        path_args.append(arg)

    return option_args, path_args


def _supports_black_serial_mode(option_args: Sequence[str]) -> bool:
    for option in option_args:
        if option in {"-c", "--code"}:
            return False
        if option.startswith("--code="):
            return False
    return True


def _serial_black_path_string(path: Path, cwd: Path) -> str:
    try:
        return path.relative_to(cwd).as_posix()
    except ValueError:
        return path.as_posix()


def _discover_black_files_for_token(cwd: Path, token: str) -> List[str] | None:
    if token == "-":
        return None

    candidate = Path(token)
    if not candidate.is_absolute():
        candidate = (cwd / candidate).resolve()

    if not candidate.exists():
        return None

    if candidate.is_file():
        return [_serial_black_path_string(candidate, cwd)]

    if not candidate.is_dir():
        return None

    discovered: List[str] = []
    for current_root, dirnames, filenames in os.walk(candidate):
        current_path = Path(current_root)
        dirnames[:] = [
            dirname for dirname in dirnames if dirname not in BLACK_EXCLUDED_DIRS
        ]
        for filename in filenames:
            file_path = current_path / filename
            if file_path.suffix.lower() not in BLACK_FILE_SUFFIXES:
                continue
            discovered.append(_serial_black_path_string(file_path, cwd))
    return sorted(discovered)


def _serial_black_targets(
    cwd: Path,
    tool_args: Sequence[str],
) -> tuple[List[str], List[str], str] | None:
    option_args, path_args = _black_option_and_path_args(tool_args)
    if not _supports_black_serial_mode(option_args):
        return None

    invocation_kind = "explicit_paths" if path_args else "default_scope"
    tokens = path_args or ["."]
    discovered_paths: List[str] = []

    for token in tokens:
        expanded = _discover_black_files_for_token(cwd, token)
        if expanded is None:
            return None
        discovered_paths.extend(expanded)

    deduped = sorted(set(discovered_paths))
    if len(deduped) < 2:
        return None

    return option_args, deduped, invocation_kind


def _nested_timeout_command(
    tool: str,
    override_timeout: int | None,
    tool_args: Sequence[str],
) -> List[str]:
    command = [sys.executable, str(Path(__file__).resolve())]
    if override_timeout is not None:
        command.extend(["--timeout-seconds", str(override_timeout)])
    command.append(tool)
    command.extend(["--", *tool_args])
    return command


def _maybe_run_serial_black(
    override_timeout: int | None,
    tool_args: Sequence[str],
) -> int | None:
    cwd = Path.cwd()
    constraints_path = cwd / EXECUTION_CONSTRAINTS_FILE
    try:
        execution_constraints = load_execution_constraints(constraints_path)
    except ValueError as error:
        print(f"[timeout-wrapper] {error}", file=sys.stderr)
        return 2

    serial_targets = _serial_black_targets(cwd, tool_args)
    if serial_targets is None:
        return None

    option_args, path_args, invocation_kind = serial_targets
    constraint_label = serial_execution_constraint_label(
        execution_constraints,
        "black",
        len(path_args),
        invocation_kind,
    )
    if constraint_label is None:
        return None

    print(
        f"[timeout-wrapper] SERIAL black: matched {constraint_label}; "
        f"running {len(path_args)} files one at a time through the timeout "
        "harness."
    )
    for index, path_arg in enumerate(path_args, start=1):
        print(f"[timeout-wrapper] SERIAL black: {index}/{len(path_args)} {path_arg}")
        child_command = _nested_timeout_command(
            "black",
            override_timeout,
            [*option_args, path_arg],
        )
        result = subprocess.run(child_command, check=False)
        if result.returncode != 0:
            print(
                f"[timeout-wrapper] SERIAL black: {path_arg} exited "
                f"{result.returncode}.",
                file=sys.stderr,
            )
            return result.returncode
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    if args.tool == "black":
        serial_result = _maybe_run_serial_black(
            args.timeout_seconds,
            args.tool_args,
        )
        if serial_result is not None:
            return serial_result

    config = _load_config()
    command, timeout, retries, cleanup_patterns = _resolve_tool_run(
        config=config,
        tool=args.tool,
        override_timeout=args.timeout_seconds,
        tool_args=args.tool_args,
    )

    pretty = " ".join(shlex.quote(part) for part in command)
    print(f"[timeout-wrapper] running: {pretty}")
    print(f"[timeout-wrapper] timeout: {timeout}s")

    attempts = retries + 1
    for attempt in range(1, attempts + 1):
        try:
            result = subprocess.run(command, check=False, timeout=timeout)
            return result.returncode
        except subprocess.TimeoutExpired:
            print(
                f"[timeout-wrapper] timeout exceeded after {timeout}s "
                f"(attempt {attempt}/{attempts}).",
                file=sys.stderr,
            )
            if attempt >= attempts:
                print(
                    "[timeout-wrapper] no retries remain. Review scope or raise "
                    "--timeout-seconds for justified runs.",
                    file=sys.stderr,
                )
                return 124
            print("[timeout-wrapper] attempting cleanup before retry.")
            _cleanup_processes(cleanup_patterns)

    return 124


if __name__ == "__main__":
    raise SystemExit(main())
