from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "run_quality_gate_cached.py"


def _load_script_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_quality_gate_cached", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_cached(
    repo_root: Path,
    *args: str,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    run_env = os.environ.copy()
    run_env.pop("CODEX_SANDBOX_NETWORK_DISABLED", None)
    run_env.pop("CODEX_CI", None)
    run_env.pop("CODEX_MANAGED_BY_NPM", None)
    if env:
        run_env.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(repo_root), *args],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=run_env,
    )


def _git_dir(repo_root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    git_dir = Path(result.stdout.strip())
    if not git_dir.is_absolute():
        git_dir = (repo_root / git_dir).resolve()
    return git_dir


def _make_fake_repo(tmp_path: Path, *, separate_git_dir: bool = False) -> Path:
    repo = tmp_path / "repo"
    init_command = ["git", "init", "--quiet"]
    if separate_git_dir:
        init_command.extend(["--separate-git-dir", str(tmp_path / "repo-git")])
    init_command.append(str(repo))
    subprocess.run(init_command, check=True, capture_output=True, text=True)
    (repo / "src").mkdir(parents=True)
    (repo / "tests").mkdir(parents=True)
    (repo / "scripts").mkdir(parents=True)
    (repo / "standards-and-practices" / "dev-utils").mkdir(parents=True)
    (repo / "resources").mkdir(parents=True)
    (repo / "knacks").mkdir(parents=True)

    (repo / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (repo / "tests" / "test_app.py").write_text(
        "def test_ok():\n    assert 1\n",
        encoding="utf-8",
    )
    (repo / "resources" / "fixture.txt").write_text(
        "fixture\n",
        encoding="utf-8",
    )
    (repo / "pyproject.toml").write_text(
        "[tool.black]\nline-length = 88\n",
        encoding="utf-8",
    )

    stub = repo / "scripts" / "run_tool_with_timeout.py"
    stub.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import pathlib",
                "import subprocess",
                "import sys",
                "git_dir = subprocess.run(",
                "    ['git', 'rev-parse', '--git-dir'],",
                "    check=True,",
                "    capture_output=True,",
                "    text=True,",
                ").stdout.strip()",
                "git_dir_path = pathlib.Path(git_dir)",
                "if not git_dir_path.is_absolute():",
                "    git_dir_path = (pathlib.Path.cwd() / git_dir_path).resolve()",
                "log = git_dir_path / 'quality-gate-calls.log'",
                "log.parent.mkdir(parents=True, exist_ok=True)",
                "with log.open('a', encoding='utf-8') as handle:",
                "    handle.write(' '.join(sys.argv[1:]) + '\\n')",
                "raise SystemExit(0)",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return repo


def _read_call_lines(repo_root: Path) -> list[str]:
    log = _git_dir(repo_root) / "quality-gate-calls.log"
    if not log.exists():
        return []
    return [
        line.strip()
        for line in log.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _read_calls(repo_root: Path) -> list[str]:
    return [line.split(" ", 1)[0] for line in _read_call_lines(repo_root)]


def _write_execution_constraints(repo_root: Path) -> None:
    (repo_root / "tool_execution_constraints.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "products": {
                    "codex": {
                        "sandbox_technologies": {
                            "bubblewrap": {
                                "environments": {
                                    "managed_linux_sandbox": {
                                        "match": {
                                            "env_all_of": {
                                                "CODEX_CI": "1",
                                                "CODEX_MANAGED_BY_NPM": "1",
                                                "CODEX_SANDBOX_NETWORK_DISABLED": "1",
                                            }
                                        },
                                        "tools": {
                                            "black": {
                                                "parallel_safety": {
                                                    "status": "unsafe",
                                                    "applies_when": {
                                                        "invocation_kind": (
                                                            "explicit_paths"
                                                        ),
                                                        "path_count_gte": 2,
                                                    },
                                                    "preferred_workaround": {
                                                        "mode": (
                                                            "serial_explicit_paths"
                                                        )
                                                    },
                                                }
                                            }
                                        },
                                    }
                                }
                            }
                        }
                    }
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def test_quality_gate_cache_skips_when_inputs_unchanged(tmp_path: Path) -> None:
    repo = _make_fake_repo(tmp_path)

    first = _run_cached(repo, "--checks", "black", "entropy_tripwire_verify")
    assert first.returncode == 0
    assert "RUN black: cache miss" in first.stdout
    assert "RUN entropy_tripwire_verify: cache miss" in first.stdout

    second = _run_cached(repo, "--checks", "black", "entropy_tripwire_verify")
    assert second.returncode == 0
    assert "SKIP black: cache hit" in second.stdout
    assert "SKIP entropy_tripwire_verify: cache hit" in second.stdout

    calls = _read_calls(repo)
    assert calls == ["black", "entropy_tripwire_verify"]

    cache = json.loads(
        (_git_dir(repo) / "project-quality-cache.json").read_text(encoding="utf-8")
    )
    assert cache["schema_version"] == "1.0.0"
    assert cache["checks"]["black"]["status"] == "pass"


def test_quality_gate_cache_invalidates_when_inputs_change(tmp_path: Path) -> None:
    repo = _make_fake_repo(tmp_path)

    first = _run_cached(repo, "--checks", "black")
    assert first.returncode == 0

    (repo / "src" / "app.py").write_text("print('changed')\n", encoding="utf-8")
    second = _run_cached(repo, "--checks", "black")
    assert second.returncode == 0
    assert "RUN black: cache miss" in second.stdout

    calls = _read_calls(repo)
    assert calls == ["black", "black"]


def test_quality_gate_cache_excludes_knacks_from_entropy_but_runs_knack_check(
    tmp_path: Path,
) -> None:
    repo = _make_fake_repo(tmp_path)
    (repo / "knacks" / "demo.knack.md").write_text(
        "# Demo\n\nplain prose content\n",
        encoding="utf-8",
    )

    first = _run_cached(repo, "--checks", "entropy_check", "knack_check")
    assert first.returncode == 0
    assert "RUN entropy_check: cache miss" in first.stdout
    assert "RUN knack_check: cache miss" in first.stdout

    second = _run_cached(repo, "--checks", "entropy_check", "knack_check")
    assert second.returncode == 0
    assert "SKIP entropy_check: cache hit" in second.stdout
    assert "SKIP knack_check: cache hit" in second.stdout

    (repo / "knacks" / "demo.knack.md").write_text(
        "# Demo\n\nplain prose content updated\n",
        encoding="utf-8",
    )
    third = _run_cached(repo, "--checks", "entropy_check", "knack_check")
    assert third.returncode == 0
    assert "SKIP entropy_check: cache hit" in third.stdout
    assert "RUN knack_check: cache miss" in third.stdout

    calls = _read_calls(repo)
    assert calls == ["entropy_check", "knack_check", "knack_check"]


def test_default_git_cache_path_uses_real_git_dir_for_separate_git_repo(
    tmp_path: Path,
) -> None:
    repo = _make_fake_repo(tmp_path, separate_git_dir=True)

    result = _run_cached(repo, "--checks", "black")
    assert result.returncode == 0

    git_dir = _git_dir(repo)
    assert (repo / ".git").is_file()
    assert (git_dir / "project-quality-cache.json").is_file()
    assert not (repo / ".git" / "project-quality-cache.json").exists()


def test_resolve_cache_path_maps_dot_git_prefix_through_real_git_dir(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = _load_script_module()
    repo = tmp_path / "repo"
    repo.mkdir()
    git_dir = tmp_path / "actual-git-dir"
    git_dir.mkdir()

    monkeypatch.setattr(module, "resolve_git_dir", lambda _: git_dir)

    resolved = module.resolve_cache_path(
        repo,
        ".git/project-quality-cache.json",
    )

    assert resolved == git_dir / "project-quality-cache.json"


def test_quality_gate_serializes_black_in_affected_codex_sandbox(
    tmp_path: Path,
) -> None:
    repo = _make_fake_repo(tmp_path)
    (repo / "scripts" / "helper.py").write_text("print('helper')\n", encoding="utf-8")
    _write_execution_constraints(repo)

    result = _run_cached(
        repo,
        "--checks",
        "black",
        env={
            "CODEX_CI": "1",
            "CODEX_MANAGED_BY_NPM": "1",
            "CODEX_SANDBOX_NETWORK_DISABLED": "1",
        },
    )

    assert result.returncode == 0
    assert "SERIAL black" in result.stdout
    assert "codex/bubblewrap/managed_linux_sandbox" in result.stdout

    call_lines = _read_call_lines(repo)
    assert all(line.startswith("black -- ") for line in call_lines)
    assert {line.split(" -- ", 1)[1] for line in call_lines} == {
        "scripts/helper.py",
        "scripts/run_tool_with_timeout.py",
        "src/app.py",
        "tests/test_app.py",
    }


def test_quality_gate_does_not_serialize_without_matching_registry(
    tmp_path: Path,
) -> None:
    repo = _make_fake_repo(tmp_path)

    result = _run_cached(
        repo,
        "--checks",
        "black",
        env={
            "CODEX_CI": "1",
            "CODEX_MANAGED_BY_NPM": "1",
            "CODEX_SANDBOX_NETWORK_DISABLED": "1",
        },
    )

    assert result.returncode == 0
    assert "SERIAL black" not in result.stdout
    assert _read_calls(repo) == ["black"]
