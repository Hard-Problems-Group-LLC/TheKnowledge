from __future__ import annotations

from pathlib import Path
from unittest import mock

from scripts import codex_local


def test_choose_commands_falls_back_when_local_manifest_is_absent(
    tmp_path: Path,
) -> None:
    install, run = codex_local.choose_commands(tmp_path, ["--help"])

    assert install is None
    assert run == [
        "npx",
        "--yes",
        "--package",
        "@openai/codex",
        "codex",
        "--help",
    ]


def test_choose_commands_uses_local_prefix_when_manifest_exists(tmp_path: Path) -> None:
    local_dir = tmp_path / ".codex-local"
    local_dir.mkdir()
    (local_dir / "package.json").write_text("{}", encoding="utf-8")

    install, run = codex_local.choose_commands(tmp_path, ["status"])

    assert install == ["npm", "install", "--prefix", str(local_dir)]
    assert run == ["npx", "--prefix", str(local_dir), "codex", "status"]


def test_choose_commands_skips_install_when_local_codex_is_present(
    tmp_path: Path,
) -> None:
    local_dir = tmp_path / ".codex-local"
    package_dir = local_dir / "node_modules" / "@openai" / "codex"
    package_dir.mkdir(parents=True)
    (local_dir / "package.json").write_text("{}", encoding="utf-8")

    install, run = codex_local.choose_commands(tmp_path, [])

    assert install is None
    assert run == ["npx", "--prefix", str(local_dir), "codex"]


def test_npm_executable_uses_cmd_suffix_on_windows() -> None:
    with mock.patch.object(codex_local.os, "name", "nt"):
        assert codex_local.npm_executable("npm") == "npm.cmd"
        assert codex_local.npm_executable("npx") == "npx.cmd"
