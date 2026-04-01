from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
TEMPLATE_REQUIREMENTS = ROOT / "templates" / "requirements-dev.txt"
TEMPLATE_DEV_SETUP = ROOT / "templates" / "scripts" / "dev_setup.py"
RUNTIME_PROFILES = ROOT / "tool_validation_profiles.json"
VALIDATION_HELPER = ROOT / "scripts" / "tool_validation_profiles.py"
PYTHON_ENVIRONMENTS = ROOT / "python-environments.json"
PYTHON_VERSION = ROOT / ".python-version"

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


def _pyproject_dev_dependencies(path: Path) -> list[str]:
    in_optional_dependencies = False
    in_dev_list = False
    dependencies: list[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("[") and line.endswith("]"):
            in_optional_dependencies = line == "[project.optional-dependencies]"
            if in_dev_list and not in_optional_dependencies:
                break
            continue

        if not in_optional_dependencies:
            continue

        if not in_dev_list:
            if line == "dev = [":
                in_dev_list = True
            continue

        if line == "]":
            return dependencies

        dependencies.append(line.rstrip(",").strip('"'))

    raise AssertionError("could not parse [project.optional-dependencies].dev")


def test_pyproject_dev_dependencies_are_exact_pins() -> None:
    dev_dependencies = _pyproject_dev_dependencies(PYPROJECT)

    assert dev_dependencies == EXPECTED_DEV_TOOLS
    assert all("==" in dependency for dependency in dev_dependencies)


def test_template_requirements_match_pyproject_dev_dependencies() -> None:
    assert _requirements_lines(TEMPLATE_REQUIREMENTS) == EXPECTED_DEV_TOOLS


def test_starter_dev_setup_uses_managed_requirements_file() -> None:
    content = TEMPLATE_DEV_SETUP.read_text(encoding="utf-8")

    assert "requirements-dev.txt" in content
    assert "pip" in content
    assert "install" in content
    assert "resolve_runtime_policy_executable" in content


def test_runtime_profiles_define_steady_state_tool_runtime() -> None:
    content = RUNTIME_PROFILES.read_text(encoding="utf-8")

    assert '"steady_state_python_tools"' in content
    assert '"minimum_version": "3.12"' in content
    assert '"target_version": "py39"' in content
    assert VALIDATION_HELPER.is_file()


def test_python_environment_files_define_bootstrap_and_runtime_contexts() -> None:
    config_text = PYTHON_ENVIRONMENTS.read_text(encoding="utf-8")
    runtime_text = PYTHON_VERSION.read_text(encoding="utf-8")

    assert '"required_version": "3.9"' in config_text
    assert '"required_version": "3.12"' in config_text
    assert '"environment_name": "3.12.12"' in config_text
    assert runtime_text.strip() == "3.12.12"
