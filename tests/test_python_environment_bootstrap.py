from __future__ import annotations

from pathlib import Path

from scripts.python_environment_bootstrap import (
    append_shell_init_snippet,
    build_direnv_hook_block,
    context_requires_virtualenv,
    direnv_download_name,
    load_python_environment_config,
    pyenv_python_executable,
    pyenv_shell_init_snippet,
    selection_name,
    slugify_project_name,
)

ROOT = Path(__file__).resolve().parent.parent


def test_slugify_project_name_normalizes_mixed_case_and_symbols() -> None:
    assert slugify_project_name("Build QM!") == "build-qm"


def test_load_python_environment_config_reads_bootstrap_and_runtime() -> None:
    config = load_python_environment_config(ROOT)

    assert config.bootstrap.required_version == "3.9"
    assert config.runtime.required_version == "3.12"
    assert config.runtime.environment_name == "3.12.12"
    assert not context_requires_virtualenv(config.runtime)
    assert selection_name(config.runtime) == "3.12.12"


def test_pyenv_python_executable_uses_expected_posix_layout(tmp_path: Path) -> None:
    executable = pyenv_python_executable(tmp_path, "demo-runtime")

    assert executable == tmp_path / "versions" / "demo-runtime" / "bin" / "python"


def test_append_shell_init_snippet_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / ".bashrc"
    snippet = pyenv_shell_init_snippet()

    append_shell_init_snippet(target, snippet)
    append_shell_init_snippet(target, snippet)

    content = target.read_text(encoding="utf-8")
    assert content.count("theknowledge pyenv init") == 2


def test_build_direnv_hook_block_contains_direnv_eval() -> None:
    block = build_direnv_hook_block("bash")

    assert "direnv hook bash" in block


def test_direnv_download_name_supports_linux_targets() -> None:
    assert direnv_download_name("linux", "x86_64") == "direnv.linux-amd64"
