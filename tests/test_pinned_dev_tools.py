from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
TEMPLATE_REQUIREMENTS = ROOT / "templates" / "requirements-dev.txt"
TEMPLATE_DEV_SETUP = ROOT / "templates" / "scripts" / "dev_setup.py"

EXPECTED_DEV_TOOLS = [
    "black==26.3.1",
    "ruff==0.15.7",
    "pytest==9.0.2",
    "pytest-timeout==2.4.0",
]


def _requirements_lines(path: Path) -> list[str]:
    lines = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def test_pyproject_dev_dependencies_are_exact_pins() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    dev_dependencies = data["project"]["optional-dependencies"]["dev"]

    assert dev_dependencies == EXPECTED_DEV_TOOLS
    assert all("==" in dependency for dependency in dev_dependencies)


def test_template_requirements_match_pyproject_dev_dependencies() -> None:
    assert _requirements_lines(TEMPLATE_REQUIREMENTS) == EXPECTED_DEV_TOOLS


def test_starter_dev_setup_uses_managed_requirements_file() -> None:
    content = TEMPLATE_DEV_SETUP.read_text(encoding="utf-8")

    assert "requirements-dev.txt" in content
    assert "pip" in content
    assert "install" in content
