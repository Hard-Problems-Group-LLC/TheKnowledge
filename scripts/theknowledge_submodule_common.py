"""Shared helper logic for TheKnowledge submodule maintenance scripts."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from initial_setup import infer_knowledge_root, repo_root as knowledge_repo_root


@dataclass(frozen=True)
class SubmoduleContext:
    """Resolved consuming-project context for an active TheKnowledge checkout."""

    project_root: Path
    project_repo_root: Path
    knowledge_root: str
    knowledge_repo_root: Path


def run(
    command: Sequence[str],
    *,
    cwd: Path,
    prefix: str,
) -> subprocess.CompletedProcess[str]:
    """Run a subprocess while echoing the command for operator visibility."""

    print(f"[{prefix}] -> {' '.join(command)}")
    return subprocess.run(
        list(command),
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def ensure_ok(
    result: subprocess.CompletedProcess[str],
    *,
    context: str,
    prefix: str,
) -> None:
    """Raise a readable error when a subprocess fails."""

    if result.returncode == 0:
        return
    details = (result.stderr or result.stdout or "").strip()
    raise RuntimeError(f"{context} failed (exit {result.returncode}): {details}")


def git_output(
    command: Sequence[str],
    *,
    cwd: Path,
    context: str,
    prefix: str,
) -> str:
    """Run a Git command and return stripped stdout."""

    result = run(command, cwd=cwd, prefix=prefix)
    ensure_ok(result, context=context, prefix=prefix)
    return (result.stdout or "").strip()


def git_repo_root(path: Path, *, prefix: str) -> Path:
    """Resolve the Git toplevel for the given path."""

    return Path(
        git_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
            context="resolve repository root",
            prefix=prefix,
        )
    ).resolve()


def git_dir(path: Path, *, prefix: str) -> Path:
    """Resolve the real Git dir even when `.git` is a file."""

    git_dir_text = git_output(
        ["git", "rev-parse", "--git-dir"],
        cwd=path,
        context="resolve git dir",
        prefix=prefix,
    )
    resolved = Path(git_dir_text)
    if not resolved.is_absolute():
        resolved = (path / resolved).resolve()
    return resolved


def status_porcelain(path: Path, *, prefix: str) -> str:
    """Return porcelain status output for a repository."""

    return git_output(
        ["git", "status", "--porcelain"],
        cwd=path,
        context="inspect working tree",
        prefix=prefix,
    )


def ensure_clean_tree(
    path: Path,
    *,
    allow_dirty: bool,
    label: str,
    prefix: str,
) -> None:
    """Reject dirty repositories unless explicitly overridden."""

    if allow_dirty:
        return
    status = status_porcelain(path, prefix=prefix)
    if status:
        raise RuntimeError(
            f"{label} is dirty. Review or clean the tree first, or rerun with "
            f"the matching allow-dirty flag.\n{status}"
        )


def current_branch(path: Path, *, prefix: str) -> str | None:
    """Return the current branch name, or None for detached HEAD."""

    result = run(
        ["git", "symbolic-ref", "--quiet", "--short", "HEAD"],
        cwd=path,
        prefix=prefix,
    )
    if result.returncode == 0:
        return (result.stdout or "").strip() or None
    if result.returncode == 1:
        return None
    ensure_ok(result, context="resolve current branch", prefix=prefix)
    return None


def current_commit(path: Path, *, prefix: str, ref: str = "HEAD") -> str:
    """Return the commit SHA for the given ref."""

    return git_output(
        ["git", "rev-parse", ref],
        cwd=path,
        context=f"resolve commit for {ref}",
        prefix=prefix,
    )


def local_branch_exists(path: Path, branch: str, *, prefix: str) -> bool:
    """Return True when the named local branch exists."""

    result = run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=path,
        prefix=prefix,
    )
    if result.returncode in {0, 1}:
        return result.returncode == 0
    ensure_ok(result, context=f"check local branch {branch}", prefix=prefix)
    return False


def remote_branch_exists(
    path: Path,
    *,
    remote: str,
    branch: str,
    prefix: str,
) -> bool:
    """Return True when the named remote-tracking branch exists."""

    result = run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/remotes/{remote}/{branch}"],
        cwd=path,
        prefix=prefix,
    )
    if result.returncode in {0, 1}:
        return result.returncode == 0
    ensure_ok(
        result,
        context=f"check remote-tracking branch {remote}/{branch}",
        prefix=prefix,
    )
    return False


def remote_url(path: Path, *, remote: str, push: bool, prefix: str) -> str:
    """Return the configured fetch or push URL for a remote."""

    command = ["git", "remote", "get-url"]
    if push:
        command.append("--push")
    command.append(remote)
    return git_output(
        command,
        cwd=path,
        context=f"resolve {'push' if push else 'fetch'} URL for {remote}",
        prefix=prefix,
    )


def describe_remote(path: Path, *, remote: str, prefix: str) -> tuple[str, str]:
    """Print and return the fetch and push URLs for a remote."""

    fetch_url = remote_url(path, remote=remote, push=False, prefix=prefix)
    push_url = remote_url(path, remote=remote, push=True, prefix=prefix)
    print(f"[{prefix}] Remote {remote} fetch URL: {fetch_url}")
    print(f"[{prefix}] Remote {remote} push URL: {push_url}")
    return fetch_url, push_url


def resolve_context(
    *,
    project_root_arg: Path | None,
    knowledge_root_arg: str | None,
    prefix: str,
) -> SubmoduleContext:
    """Resolve the consuming-project root plus active TheKnowledge path."""

    repo_root = knowledge_repo_root().resolve()
    project_path = (
        project_root_arg.resolve()
        if project_root_arg is not None
        else repo_root.parent.resolve()
    )
    project_repo = git_repo_root(project_path, prefix=prefix)
    knowledge_root = knowledge_root_arg or infer_knowledge_root(project_repo, repo_root)
    configured_repo_root = (project_repo / knowledge_root).resolve()
    if configured_repo_root != repo_root:
        raise RuntimeError(
            "Resolved TheKnowledge path does not match this checkout. "
            f"Expected {configured_repo_root}, but this script lives in {repo_root}."
        )
    return SubmoduleContext(
        project_root=project_repo,
        project_repo_root=project_repo,
        knowledge_root=knowledge_root,
        knowledge_repo_root=repo_root,
    )
