from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = (
    ROOT / "standards-and-practices" / "dev-utils" / "security" / "entropy-check.py"
)


def _run_entropy_check(
    target: Path, *extra_args: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *extra_args, str(target)],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def _init_repo(repo_root: Path, *ignored_patterns: str) -> None:
    subprocess.run(
        ["git", "init", "--quiet", str(repo_root)],
        check=True,
        capture_output=True,
        text=True,
    )
    if ignored_patterns:
        (repo_root / ".gitignore").write_text(
            "".join(f"{pattern}\n" for pattern in ignored_patterns),
            encoding="utf-8",
        )


def test_entropy_check_flags_high_entropy_spike(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    low_lines = [
        "this is ordinary prose content with predictable words and spacing.",
        "documentation text usually has repeated structures and lower entropy.",
        "another normal line that should be part of the clipped baseline set.",
    ]
    high_line = "X4b9Rk2Qm8Lp0Vz7Hn6Tw3Ys5Df1Ja9Cu2Me7Po4Gi8Nr5Kb1Qx6Zv0"
    sample.write_text("\n".join(low_lines + [high_line]) + "\n", encoding="utf-8")

    result = _run_entropy_check(sample)

    assert result.returncode == 1
    assert "flagged 1 files" in result.stdout
    assert "reported 1 high-entropy lines" in result.stdout
    assert "L4" in result.stdout


def test_entropy_check_returns_zero_when_no_spikes(tmp_path: Path) -> None:
    sample = tmp_path / "normal.txt"
    lines = [
        "plain documentation line with repeated terms and clear prose.",
        "another plain line that should not trigger secret-like detection.",
        "more prose to make the baseline stable across the small fixture.",
        "final plain line with no random-looking token material present.",
    ]
    sample.write_text("\n".join(lines) + "\n", encoding="utf-8")

    result = _run_entropy_check(sample)

    assert result.returncode == 0
    assert "flagged 0 files" in result.stdout
    assert "reported 0 high-entropy lines" in result.stdout


def test_entropy_check_json_output_has_schema_version_first(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    token = "".join(
        [
            "X4b9Rk2Q",
            "m8Lp0Vz7",
            "Hn6Tw3Ys",
            "5Df1Ja9C",
            "u2Me7Po4",
            "Gi8Nr5Kb",
            "1Qx6Zv0",
        ]
    )
    sample.write_text(
        "\n".join(
            [
                "plain baseline text with repeated words and predictable structure.",
                "another plain baseline line to stabilize relative entropy.",
                token,
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = _run_entropy_check(sample, "--json-output")

    assert result.returncode == 1
    stripped = result.stdout.lstrip()
    assert stripped.startswith('{\n  "schema_version": ')

    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "1.0.0"
    assert payload["summary"]["flagged_files"] == 1
    assert payload["summary"]["reported_high_entropy_lines"] >= 1


def test_entropy_check_skips_gitignored_paths_by_default(tmp_path: Path) -> None:
    _init_repo(tmp_path, "local-state/")
    sample = tmp_path / "local-state" / "target.txt"
    sample.parent.mkdir(parents=True)
    sample.write_text(
        "\n".join(
            [
                "plain baseline text with repeated words and predictable structure.",
                "another plain baseline line to stabilize relative entropy.",
                "X4b9Rk2Qm8Lp0Vz7Hn6Tw3Ys5Df1Ja9Cu2Me7Po4Gi8Nr5Kb1Qx6Zv0",
                "",
            ]
        ),
        encoding="utf-8",
    )
    symlink_path = tmp_path / "local-state" / "secret.txt"
    try:
        symlink_path.symlink_to("target.txt")
    except OSError:
        pytest.skip("symlinks are unavailable in this test environment")

    result = _run_entropy_check(tmp_path, "--json-output")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["summary"]["scanned_files"] == 1
    assert payload["summary"]["flagged_files"] == 0


def test_entropy_check_supports_even_gitignored(tmp_path: Path) -> None:
    _init_repo(tmp_path, "local-state/")
    sample = tmp_path / "local-state" / "secret.txt"
    sample.parent.mkdir(parents=True)
    sample.write_text(
        "\n".join(
            [
                "plain baseline text with repeated words and predictable structure.",
                "another plain baseline line to stabilize relative entropy.",
                "X4b9Rk2Qm8Lp0Vz7Hn6Tw3Ys5Df1Ja9Cu2Me7Po4Gi8Nr5Kb1Qx6Zv0",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = _run_entropy_check(tmp_path, "--json-output", "--even-gitignored")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["summary"]["scanned_files"] == 2
    assert payload["summary"]["flagged_files"] == 1
    assert payload["results"][0]["path"].endswith("local-state/secret.txt")
