from __future__ import annotations

import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def _write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def _fake_root_env(tmp_path: Path) -> dict[str, str]:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    _write_executable(fake_bin / "id", "#!/usr/bin/env bash\necho 0\n")
    env = os.environ.copy()
    env["PATH"] = "{}:{}".format(fake_bin, env["PATH"])
    return env


def test_install_stage_2_help_includes_standard_default() -> None:
    script = ROOT / "scripts" / "install-stage-2.py"
    result = subprocess.run(
        ["python3", str(script), "--help"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "user-local non-development install" in result.stdout
    assert "--mode {standard,dev,venv-only}" in result.stdout
    assert "--system" in result.stdout


def test_install_sh_rejects_system_without_root() -> None:
    script = ROOT / "install.sh"
    result = subprocess.run(
        ["bash", str(script), "--system"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "--system requires root privileges" in result.stderr


def test_install_sh_rejects_sudo_without_system(tmp_path: Path) -> None:
    script = ROOT / "install.sh"
    env = _fake_root_env(tmp_path)
    env["SUDO_USER"] = "operator"
    result = subprocess.run(
        ["bash", str(script)],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "sudo is only supported together with --system" in result.stderr


def test_install_sh_root_without_system_requires_confirmation(
    tmp_path: Path,
) -> None:
    script = ROOT / "install.sh"
    result = subprocess.run(
        ["bash", str(script)],
        cwd=ROOT,
        env=_fake_root_env(tmp_path),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "needs interactive confirmation" in result.stderr


def test_install_sh_root_with_system_invokes_stage_2(tmp_path: Path) -> None:
    script = ROOT / "install.sh"
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    output = tmp_path / "python-args.txt"
    _write_executable(fake_bin / "id", "#!/usr/bin/env bash\necho 0\n")
    _write_executable(
        fake_bin / "python3",
        """#!/usr/bin/env bash
if [ "${1-}" = "-" ]; then
  exit 0
fi
printf '%s\n' "$@" > "$INSTALL_SH_TEST_OUTPUT"
""",
    )
    env = os.environ.copy()
    env["PATH"] = "{}:{}".format(fake_bin, env["PATH"])
    env["INSTALL_SH_TEST_OUTPUT"] = str(output)
    result = subprocess.run(
        ["bash", str(script), "--system"],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    forwarded_args = output.read_text(encoding="utf-8").splitlines()
    assert forwarded_args[0].endswith("scripts/install-stage-2.py")
    assert "--system" in forwarded_args
