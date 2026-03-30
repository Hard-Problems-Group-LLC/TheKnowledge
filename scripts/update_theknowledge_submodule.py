#!/usr/bin/env python3
"""Update an active TheKnowledge submodule inside a consuming project."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from initial_setup import MANAGED_REFRESH_TEMPLATES
from theknowledge_submodule_common import (
    current_commit,
    describe_remote,
    ensure_clean_tree,
    ensure_ok,
    resolve_context,
    run,
)

PREFIX = "theknowledge-update"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch, review, adopt, and refresh managed downstream files for "
            "an active TheKnowledge submodule inside a consuming project."
        )
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help=(
            "Consuming project root. Defaults to the parent directory of this "
            "TheKnowledge checkout."
        ),
    )
    parser.add_argument(
        "--knowledge-root",
        default=None,
        help=(
            "Path from the consuming project root to this TheKnowledge "
            "checkout. Defaults to the inferred relative path."
        ),
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Submodule remote to fetch from and adopt from (default: origin).",
    )
    parser.add_argument(
        "--branch",
        default="trunk",
        help="Submodule branch to adopt (default: trunk).",
    )
    parser.add_argument(
        "--allow-dirty-project",
        action="store_true",
        help="Allow the helper to run when the parent project worktree is dirty.",
    )
    parser.add_argument(
        "--allow-dirty-submodule",
        action="store_true",
        help="Allow the helper to run when the submodule worktree is dirty.",
    )
    return parser.parse_args(argv)


def summarize_incoming_changes(
    knowledge_repo_root: Path,
    *,
    remote_ref: str,
) -> int:
    log_result = run(
        ["git", "log", "--oneline", f"HEAD..{remote_ref}"],
        cwd=knowledge_repo_root,
        prefix=PREFIX,
    )
    ensure_ok(log_result, context="summarize incoming commits", prefix=PREFIX)
    diff_result = run(
        ["git", "diff", "--stat", f"HEAD..{remote_ref}"],
        cwd=knowledge_repo_root,
        prefix=PREFIX,
    )
    ensure_ok(diff_result, context="summarize incoming diffstat", prefix=PREFIX)
    commits = [line for line in (log_result.stdout or "").splitlines() if line.strip()]
    if commits:
        print(f"[{PREFIX}] Incoming commits on {remote_ref}:")
        for line in commits:
            print(f"[{PREFIX}]   {line}")
    else:
        print(f"[{PREFIX}] No incoming commits on {remote_ref}.")
    diffstat = (diff_result.stdout or "").strip()
    if diffstat:
        print(f"[{PREFIX}] Incoming diffstat for {remote_ref}:")
        for line in diffstat.splitlines():
            print(f"[{PREFIX}]   {line}")
    return len(commits)


def adopt_remote_commit(
    knowledge_repo_root: Path,
    *,
    remote_ref: str,
) -> str:
    target_commit = current_commit(knowledge_repo_root, prefix=PREFIX, ref=remote_ref)
    current_head = current_commit(knowledge_repo_root, prefix=PREFIX)
    if current_head == target_commit:
        print(
            f"[{PREFIX}] The submodule already points at {remote_ref} ({target_commit})."
        )
        return target_commit

    result = run(
        ["git", "checkout", "--detach", target_commit],
        cwd=knowledge_repo_root,
        prefix=PREFIX,
    )
    ensure_ok(result, context=f"adopt {remote_ref}", prefix=PREFIX)
    print(f"[{PREFIX}] Adopted {remote_ref} at {target_commit}.")
    return target_commit


def refresh_managed_files(project_root: Path, *, knowledge_root: str) -> None:
    drift_result = run(
        [
            sys.executable,
            "scripts/report_managed_agents_drift.py",
            "--project-root",
            str(project_root),
            "--knowledge-root",
            knowledge_root,
        ],
        cwd=project_root / knowledge_root,
        prefix=PREFIX,
    )
    if drift_result.stdout:
        print((drift_result.stdout or "").rstrip())
    if drift_result.stderr:
        print((drift_result.stderr or "").rstrip(), file=sys.stderr)

    if drift_result.returncode == 0:
        print(f"[{PREFIX}] Managed downstream files are already current.")
        return
    if drift_result.returncode != 1:
        ensure_ok(drift_result, context="check managed downstream drift", prefix=PREFIX)

    print(f"[{PREFIX}] Managed drift detected; refreshing managed files.")
    refresh_command = [
        sys.executable,
        "scripts/initial-setup.py",
        "--project-root",
        str(project_root),
        "--knowledge-root",
        knowledge_root,
        "--force",
    ]
    for template_name in MANAGED_REFRESH_TEMPLATES:
        refresh_command.extend(["--template", template_name])
    refresh_result = run(
        refresh_command,
        cwd=project_root / knowledge_root,
        prefix=PREFIX,
    )
    ensure_ok(refresh_result, context="refresh managed downstream files", prefix=PREFIX)
    if refresh_result.stdout:
        print((refresh_result.stdout or "").rstrip())


def print_parent_summary(project_root: Path) -> None:
    status_result = run(
        ["git", "status", "--short"],
        cwd=project_root,
        prefix=PREFIX,
    )
    ensure_ok(status_result, context="summarize parent status", prefix=PREFIX)
    status = (status_result.stdout or "").strip()
    if status:
        print(f"[{PREFIX}] Parent project reviewable changes:")
        for line in status.splitlines():
            print(f"[{PREFIX}]   {line}")
    else:
        print(f"[{PREFIX}] Parent project remains clean after the update helper.")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        context = resolve_context(
            project_root_arg=args.project_root,
            knowledge_root_arg=args.knowledge_root,
            prefix=PREFIX,
        )
        ensure_clean_tree(
            context.project_repo_root,
            allow_dirty=args.allow_dirty_project,
            label="parent project repository",
            prefix=PREFIX,
        )
        ensure_clean_tree(
            context.knowledge_repo_root,
            allow_dirty=args.allow_dirty_submodule,
            label="TheKnowledge submodule",
            prefix=PREFIX,
        )
        describe_remote(
            context.knowledge_repo_root,
            remote=args.remote,
            prefix=PREFIX,
        )
        fetch_result = run(
            ["git", "fetch", "--prune", args.remote],
            cwd=context.knowledge_repo_root,
            prefix=PREFIX,
        )
        ensure_ok(fetch_result, context=f"fetch {args.remote}", prefix=PREFIX)
        remote_ref = f"{args.remote}/{args.branch}"
        summarize_incoming_changes(context.knowledge_repo_root, remote_ref=remote_ref)
        adopt_remote_commit(context.knowledge_repo_root, remote_ref=remote_ref)
        refresh_managed_files(
            context.project_root,
            knowledge_root=context.knowledge_root,
        )
        print_parent_summary(context.project_root)
    except RuntimeError as error:
        print(f"[{PREFIX}] FAIL: {error}", file=sys.stderr)
        return 1

    print(
        f"[{PREFIX}] PASS: updated {context.knowledge_root} and left the "
        "parent repo ready for review."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
