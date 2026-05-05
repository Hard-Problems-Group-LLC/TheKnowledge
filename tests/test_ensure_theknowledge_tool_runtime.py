from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "ensure_theknowledge_tool_runtime.py"


def _load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "ensure_theknowledge_tool_runtime",
        SCRIPT,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_resolve_ready_runtime_prefers_explicit_environment_override(
    monkeypatch,
) -> None:
    module = _load_module()
    monkeypatch.setenv("THEKNOWLEDGE_PYTHON_TOOLS", "managed-python")
    monkeypatch.setattr(
        module,
        "resolve_runtime_policy_executable",
        lambda repo_root, policy_name, **kwargs: kwargs["explicit_candidate"],
    )

    resolved = module.resolve_ready_runtime(module.LOCAL_RUNTIME_DIR)

    assert resolved == "managed-python"


def test_ensure_runtime_builds_local_runtime_when_missing(
    monkeypatch,
    tmp_path: Path,
) -> None:
    module = _load_module()
    runtime_python = tmp_path / "runtime" / "bin" / "python"
    calls: list[tuple[str, object]] = []
    resolution = iter([None, str(runtime_python)])

    monkeypatch.setattr(
        module,
        "resolve_ready_runtime",
        lambda runtime_dir: next(resolution),
    )
    monkeypatch.setattr(module, "select_base_python", lambda override: "python3.12")
    monkeypatch.setattr(
        module,
        "ensure_virtualenv",
        lambda base_python, runtime_dir: runtime_python,
    )
    monkeypatch.setattr(
        module,
        "install_tooling",
        lambda python_path: calls.append(("install", python_path)),
    )
    monkeypatch.setattr(
        module,
        "write_local_wrapper",
        lambda python_path: calls.append(("wrapper", python_path)),
    )

    resolved = module.ensure_runtime(tmp_path / "runtime", None)

    assert resolved == str(runtime_python)
    assert calls == [("install", runtime_python), ("wrapper", runtime_python)]
