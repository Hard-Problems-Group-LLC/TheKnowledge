from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = (
    ROOT
    / "standards-and-practices"
    / "dev-utils"
    / "security"
    / "verify_entropy_tripwire.py"
)


def _token() -> str:
    return "".join(
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


def _run_tripwire(
    repo_root: Path, *extra_args: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(repo_root), *extra_args],
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


def _sentinel_fixture() -> str:
    return "\n".join(
        [
            "# baseline: repeated words repeated words repeated words repeated words",
            'normal_a = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"',
            'normal_b = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"',
            f'high_line = "{_token()}"',
            "",
        ]
    )


def test_tripwire_verifier_passes_for_clean_repo_with_sentinel(tmp_path: Path) -> None:
    tripwire = tmp_path / "tests" / "test_entropy_check.py"
    tripwire.parent.mkdir(parents=True)
    tripwire.write_text(_sentinel_fixture(), encoding="utf-8")
    (tmp_path / "README.txt").write_text(
        "normal text line one\nnormal text line two\n", encoding="utf-8"
    )

    result = _run_tripwire(tmp_path)

    assert result.returncode == 0
    assert "PASS: tripwire verification complete." in result.stdout


def test_tripwire_verifier_fails_when_non_sentinel_finding_exists(
    tmp_path: Path,
) -> None:
    tripwire = tmp_path / "tests" / "test_entropy_check.py"
    tripwire.parent.mkdir(parents=True)
    tripwire.write_text(_sentinel_fixture(), encoding="utf-8")
    (tmp_path / "secretish.txt").write_text(
        "\n".join(
            [
                "ordinary prose for baseline stabilization",
                "another ordinary prose line for baseline",
                _token(),
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = _run_tripwire(tmp_path)

    assert result.returncode == 1
    assert "Entropy harness reported non-sentinel findings." in result.stderr


def test_tripwire_verifier_ignores_gitignored_findings_by_default(
    tmp_path: Path,
) -> None:
    _init_repo(tmp_path, "local-state/")
    tripwire = tmp_path / "tests" / "test_entropy_check.py"
    tripwire.parent.mkdir(parents=True)
    tripwire.write_text(_sentinel_fixture(), encoding="utf-8")

    ignored_file = tmp_path / "local-state" / "secret.txt"
    ignored_file.parent.mkdir(parents=True)
    ignored_file.write_text(
        "\n".join(
            [
                "ordinary prose for baseline stabilization",
                "another ordinary prose line for baseline",
                _token(),
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = _run_tripwire(tmp_path)

    assert result.returncode == 0
    assert "PASS: tripwire verification complete." in result.stdout


def test_tripwire_verifier_supports_even_gitignored(tmp_path: Path) -> None:
    _init_repo(tmp_path, "local-state/")
    tripwire = tmp_path / "tests" / "test_entropy_check.py"
    tripwire.parent.mkdir(parents=True)
    tripwire.write_text(_sentinel_fixture(), encoding="utf-8")

    ignored_file = tmp_path / "local-state" / "secret.txt"
    ignored_file.parent.mkdir(parents=True)
    ignored_file.write_text(
        "\n".join(
            [
                "ordinary prose for baseline stabilization",
                "another ordinary prose line for baseline",
                _token(),
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = _run_tripwire(tmp_path, "--even-gitignored")

    assert result.returncode == 1
    assert "Entropy harness reported non-sentinel findings." in result.stderr
