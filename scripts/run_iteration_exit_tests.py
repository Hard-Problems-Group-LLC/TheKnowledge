#!/usr/bin/env python3
"""Run a configurable pytest subset for backlog-iteration exit checks."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run iteration-exit tests with optional junit output and extra "
            "pytest arguments."
        )
    )
    parser.add_argument(
        "--junitxml",
        type=Path,
        default=None,
        help="Optional junit XML output path.",
    )
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Extra arguments forwarded to pytest.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    command: list[str] = [sys.executable, "-m", "pytest"]
    if args.junitxml is not None:
        command.extend(["--junitxml", str(args.junitxml)])
    command.extend(args.pytest_args)
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
