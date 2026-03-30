#!/usr/bin/env python3
"""Manage a two-phase Feedback-branch workflow from a consuming project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from theknowledge_submodule_common import (
    current_branch,
    current_commit,
    describe_remote,
    ensure_clean_tree,
    ensure_ok,
    git_dir,
    local_branch_exists,
    remote_branch_exists,
    resolve_context,
    run,
)

PREFIX = "theknowledge-feedback"
SESSION_FILE = "theknowledge-feedback-session.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare, finish, or abort a Feedback-branch workflow from an "
            "active TheKnowledge submodule checkout."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser(
        "prepare",
        help="Capture the current state and switch the submodule to Feedback.",
    )
    prepare.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help=(
            "Consuming project root. Defaults to the parent directory of this "
            "TheKnowledge checkout."
        ),
    )
    prepare.add_argument(
        "--knowledge-root",
        default=None,
        help=(
            "Path from the consuming project root to this TheKnowledge "
            "checkout. Defaults to the inferred relative path."
        ),
    )
    prepare.add_argument(
        "--remote",
        default="origin",
        help="Remote used to synchronize Feedback refs (default: origin).",
    )
    prepare.add_argument(
        "--feedback-branch",
        default="Feedback",
        help="Feedback branch name (default: Feedback).",
    )

    finish = subparsers.add_parser(
        "finish",
        help=(
            "Optionally commit and push Feedback changes, then restore the "
            "previous submodule state."
        ),
    )
    finish.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help=(
            "Consuming project root. Defaults to the parent directory of this "
            "TheKnowledge checkout."
        ),
    )
    finish.add_argument(
        "--knowledge-root",
        default=None,
        help=(
            "Path from the consuming project root to this TheKnowledge "
            "checkout. Defaults to the inferred relative path."
        ),
    )
    finish.add_argument(
        "--message",
        default=None,
        help=(
            "Commit message to use when the Feedback worktree still has local "
            "changes that need committing."
        ),
    )
    finish.add_argument(
        "--push",
        action="store_true",
        help="Attempt to push the Feedback branch after committing locally.",
    )

    abort = subparsers.add_parser(
        "abort",
        help="Restore the prior submodule state without publishing feedback.",
    )
    abort.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help=(
            "Consuming project root. Defaults to the parent directory of this "
            "TheKnowledge checkout."
        ),
    )
    abort.add_argument(
        "--knowledge-root",
        default=None,
        help=(
            "Path from the consuming project root to this TheKnowledge "
            "checkout. Defaults to the inferred relative path."
        ),
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def session_path(knowledge_repo_root: Path) -> Path:
    return git_dir(knowledge_repo_root, prefix=PREFIX) / SESSION_FILE


def save_session(path: Path, data: dict[str, str]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_session(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise RuntimeError(
            "No active Feedback helper session is recorded. Run `prepare` first."
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Feedback session file is invalid JSON: {error}") from error
    if not isinstance(data, dict):
        raise RuntimeError("Feedback session file must contain a JSON object.")
    return {str(key): str(value) for key, value in data.items()}


def switch_to_feedback_branch(
    knowledge_repo_root: Path,
    *,
    remote: str,
    feedback_branch: str,
) -> None:
    remote_ref_exists = remote_branch_exists(
        knowledge_repo_root,
        remote=remote,
        branch=feedback_branch,
        prefix=PREFIX,
    )
    local_ref_exists = local_branch_exists(
        knowledge_repo_root,
        feedback_branch,
        prefix=PREFIX,
    )

    if local_ref_exists:
        switch_result = run(
            ["git", "switch", feedback_branch],
            cwd=knowledge_repo_root,
            prefix=PREFIX,
        )
        ensure_ok(
            switch_result,
            context=f"switch to local {feedback_branch}",
            prefix=PREFIX,
        )
        if remote_ref_exists:
            ff_result = run(
                ["git", "merge", "--ff-only", f"{remote}/{feedback_branch}"],
                cwd=knowledge_repo_root,
                prefix=PREFIX,
            )
            ensure_ok(
                ff_result,
                context=f"fast-forward {feedback_branch} from {remote}/{feedback_branch}",
                prefix=PREFIX,
            )
        return

    if remote_ref_exists:
        create_result = run(
            [
                "git",
                "switch",
                "--create",
                feedback_branch,
                "--track",
                f"{remote}/{feedback_branch}",
            ],
            cwd=knowledge_repo_root,
            prefix=PREFIX,
        )
        ensure_ok(
            create_result,
            context=f"create tracked {feedback_branch}",
            prefix=PREFIX,
        )
        return

    create_result = run(
        ["git", "switch", "--create", feedback_branch],
        cwd=knowledge_repo_root,
        prefix=PREFIX,
    )
    ensure_ok(
        create_result,
        context=f"create local {feedback_branch}",
        prefix=PREFIX,
    )
    print(
        f"[{PREFIX}] Remote branch {remote}/{feedback_branch} does not exist yet; "
        f"created a local {feedback_branch} branch."
    )


def restore_previous_state(
    knowledge_repo_root: Path,
    *,
    original_branch: str | None,
    original_commit: str,
) -> None:
    if original_branch:
        result = run(
            ["git", "switch", original_branch],
            cwd=knowledge_repo_root,
            prefix=PREFIX,
        )
        ensure_ok(
            result,
            context=f"restore branch {original_branch}",
            prefix=PREFIX,
        )
        return

    result = run(
        ["git", "checkout", "--detach", original_commit],
        cwd=knowledge_repo_root,
        prefix=PREFIX,
    )
    ensure_ok(
        result,
        context=f"restore detached commit {original_commit}",
        prefix=PREFIX,
    )


def prepare(argv: argparse.Namespace) -> int:
    try:
        context = resolve_context(
            project_root_arg=argv.project_root,
            knowledge_root_arg=argv.knowledge_root,
            prefix=PREFIX,
        )
        ensure_clean_tree(
            context.knowledge_repo_root,
            allow_dirty=False,
            label="TheKnowledge submodule",
            prefix=PREFIX,
        )
        state_path = session_path(context.knowledge_repo_root)
        if state_path.exists():
            raise RuntimeError(
                f"A Feedback helper session is already active at {state_path}."
            )
        original_branch = current_branch(context.knowledge_repo_root, prefix=PREFIX)
        if original_branch == argv.feedback_branch:
            raise RuntimeError(
                "The active TheKnowledge checkout is already on Feedback. "
                "Finish or abort that work manually before starting a new session."
            )
        original_commit = current_commit(context.knowledge_repo_root, prefix=PREFIX)
        describe_remote(
            context.knowledge_repo_root,
            remote=argv.remote,
            prefix=PREFIX,
        )
        fetch_result = run(
            ["git", "fetch", "--prune", argv.remote],
            cwd=context.knowledge_repo_root,
            prefix=PREFIX,
        )
        ensure_ok(fetch_result, context=f"fetch {argv.remote}", prefix=PREFIX)
        switch_to_feedback_branch(
            context.knowledge_repo_root,
            remote=argv.remote,
            feedback_branch=argv.feedback_branch,
        )
        save_session(
            state_path,
            {
                "feedback_branch": argv.feedback_branch,
                "knowledge_root": context.knowledge_root,
                "original_branch": original_branch or "",
                "original_commit": original_commit,
                "project_root": str(context.project_root),
                "remote": argv.remote,
            },
        )
    except RuntimeError as error:
        print(f"[{PREFIX}] FAIL: {error}", file=sys.stderr)
        return 1

    print(
        f"[{PREFIX}] PASS: switched {context.knowledge_root} to {argv.feedback_branch}."
    )
    print(
        f"[{PREFIX}] NEXT: record the Feedback item, review it, and run "
        f"`finish` with `--message` to commit locally."
    )
    print(
        f"[{PREFIX}] NEXT: add `--push` to `finish` only when you want this "
        "helper to attempt a push with the configured remote push URL."
    )
    return 0


def finish(argv: argparse.Namespace) -> int:
    push_error = None
    feedback_commit = None
    try:
        context = resolve_context(
            project_root_arg=argv.project_root,
            knowledge_root_arg=argv.knowledge_root,
            prefix=PREFIX,
        )
        state = load_session(session_path(context.knowledge_repo_root))
        feedback_branch = state["feedback_branch"]
        if (
            current_branch(context.knowledge_repo_root, prefix=PREFIX)
            != feedback_branch
        ):
            raise RuntimeError(
                f"The active TheKnowledge checkout is not on {feedback_branch}."
            )
        dirty = bool(
            run(
                ["git", "status", "--porcelain"],
                cwd=context.knowledge_repo_root,
                prefix=PREFIX,
            ).stdout.strip()
        )
        if dirty:
            if not argv.message:
                raise RuntimeError(
                    "Feedback changes are still uncommitted. Pass --message "
                    "to let the helper create the local commit."
                )
            add_result = run(
                ["git", "add", "-A"],
                cwd=context.knowledge_repo_root,
                prefix=PREFIX,
            )
            ensure_ok(add_result, context="stage Feedback changes", prefix=PREFIX)
            commit_result = run(
                ["git", "commit", "-m", argv.message],
                cwd=context.knowledge_repo_root,
                prefix=PREFIX,
            )
            ensure_ok(commit_result, context="commit Feedback changes", prefix=PREFIX)
        feedback_commit = current_commit(context.knowledge_repo_root, prefix=PREFIX)
        if feedback_commit == state["original_commit"]:
            raise RuntimeError(
                "No Feedback commit was recorded. Use `abort` to restore the "
                "previous state without publishing."
            )
        if argv.push:
            push_result = run(
                ["git", "push", state["remote"], feedback_branch],
                cwd=context.knowledge_repo_root,
                prefix=PREFIX,
            )
            if push_result.returncode == 0:
                sync_result = run(
                    ["git", "fetch", "--prune", state["remote"], feedback_branch],
                    cwd=context.knowledge_repo_root,
                    prefix=PREFIX,
                )
                ensure_ok(
                    sync_result,
                    context=f"sync {state['remote']}/{feedback_branch}",
                    prefix=PREFIX,
                )
            else:
                push_error = (push_result.stderr or push_result.stdout or "").strip()
        restore_previous_state(
            context.knowledge_repo_root,
            original_branch=state["original_branch"] or None,
            original_commit=state["original_commit"],
        )
        session_path(context.knowledge_repo_root).unlink(missing_ok=True)
    except RuntimeError as error:
        print(f"[{PREFIX}] FAIL: {error}", file=sys.stderr)
        return 1

    if push_error:
        print(
            f"[{PREFIX}] FAIL: push was not completed, but the local Feedback "
            f"commit {feedback_commit} was preserved and the previous "
            "submodule state was restored.",
            file=sys.stderr,
        )
        print(f"[{PREFIX}] Push error: {push_error}", file=sys.stderr)
        return 1

    if argv.push:
        print(
            f"[{PREFIX}] PASS: pushed Feedback commit {feedback_commit} and "
            "restored the previous submodule state."
        )
        return 0

    print(
        f"[{PREFIX}] PASS: recorded local Feedback commit {feedback_commit} "
        "and restored the previous submodule state without pushing."
    )
    return 0


def abort(argv: argparse.Namespace) -> int:
    try:
        context = resolve_context(
            project_root_arg=argv.project_root,
            knowledge_root_arg=argv.knowledge_root,
            prefix=PREFIX,
        )
        ensure_clean_tree(
            context.knowledge_repo_root,
            allow_dirty=False,
            label="TheKnowledge submodule",
            prefix=PREFIX,
        )
        state = load_session(session_path(context.knowledge_repo_root))
        restore_previous_state(
            context.knowledge_repo_root,
            original_branch=state["original_branch"] or None,
            original_commit=state["original_commit"],
        )
        session_path(context.knowledge_repo_root).unlink(missing_ok=True)
    except RuntimeError as error:
        print(f"[{PREFIX}] FAIL: {error}", file=sys.stderr)
        return 1

    print(f"[{PREFIX}] PASS: restored the previous submodule state.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "prepare":
        return prepare(args)
    if args.command == "finish":
        return finish(args)
    if args.command == "abort":
        return abort(args)
    raise AssertionError(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
