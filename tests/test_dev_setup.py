"""Regression coverage for the managed `scripts/dev_setup.py` entrypoints."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATHS = (
    ROOT / "scripts" / "dev_setup.py",
    ROOT / "templates" / "scripts" / "dev_setup.py",
)


def load_module(script_path: Path):
    """Import one dev-setup script directly from its filesystem path."""

    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("script_path", SCRIPT_PATHS)
def test_ensure_virtualenv_keeps_matching_existing_environment(
    script_path: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Leave an existing virtual environment untouched when versions match."""

    module = load_module(script_path)
    venv_python = tmp_path / "venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("", encoding="utf-8")
    commands = []

    monkeypatch.setattr(module, "python_version", lambda executable: "3.12.11")
    monkeypatch.setattr(module, "run", lambda command: commands.append(list(command)))

    result = module.ensure_virtualenv("python3.12", tmp_path / "venv")

    assert result == venv_python
    assert commands == []


@pytest.mark.parametrize("script_path", SCRIPT_PATHS)
def test_ensure_virtualenv_rebuilds_when_python_version_differs(
    script_path: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rebuild the managed virtual environment when the interpreter changes."""

    module = load_module(script_path)
    venv_python = tmp_path / "venv" / "bin" / "python"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("", encoding="utf-8")
    commands = []

    def fake_python_version(executable) -> str:
        if str(executable).endswith("python3.12"):
            return "3.12.11"
        return "3.13.7"

    monkeypatch.setattr(module, "python_version", fake_python_version)
    monkeypatch.setattr(module, "run", lambda command: commands.append(list(command)))

    result = module.ensure_virtualenv("python3.12", tmp_path / "venv")

    assert result == venv_python
    assert commands == [["python3.12", "-m", "venv", "--clear", tmp_path / "venv"]]
