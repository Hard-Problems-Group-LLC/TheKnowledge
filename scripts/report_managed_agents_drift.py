#!/usr/bin/env python3
"""Report managed starter drift for submodule users."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path
from typing import Sequence

from initial_setup import (
    AGENTS_FOOTER,
    AGENTS_HEADER,
    AGENTS_PATH,
    GITIGNORE_MARKERS,
    GITIGNORE_PATH,
    GITIGNORE_TEMPLATE,
    MANAGED_REFRESH_TEMPLATES,
    infer_knowledge_root,
    installable_entries,
    iter_install_files,
    project_slug,
    render_file,
    repo_root,
)

HEADER_START = "<!-- THEKNOWLEDGE_MANAGED_HEADER_START -->"
HEADER_END = "<!-- THEKNOWLEDGE_MANAGED_HEADER_END -->"
FOOTER_START = "<!-- THEKNOWLEDGE_MANAGED_FOOTER_START -->"
FOOTER_END = "<!-- THEKNOWLEDGE_MANAGED_FOOTER_END -->"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare a consuming project's managed AGENTS.md sections and "
            "managed starter files with the current TheKnowledge defaults."
        )
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help=(
            "Consuming project root. Defaults to the parent directory of "
            "this repository."
        ),
    )
    parser.add_argument(
        "--knowledge-root",
        default=None,
        help=(
            "Path from the project root back to this TheKnowledge checkout. "
            "Defaults to the inferred relative path when possible."
        ),
    )
    return parser.parse_args(argv)


def extract_managed_block(content: str, start_marker: str, end_marker: str) -> str:
    if start_marker not in content or end_marker not in content:
        return ""
    start = content.index(start_marker)
    end = content.index(end_marker) + len(end_marker)
    block = content[start:end].strip()
    if block:
        return block + "\n"
    return ""


def render_expected_block(
    templates_root: Path,
    template_name: str,
    knowledge_root: str,
    project_name_slug: str,
) -> str:
    return render_file(
        templates_root / template_name,
        knowledge_root,
        project_name_slug,
    ).decode("utf-8")


def extract_delimited_block(content: str, start_marker: str, end_marker: str) -> str:
    if start_marker not in content or end_marker not in content:
        return ""
    start = content.index(start_marker)
    end = content.index(end_marker) + len(end_marker)
    block = content[start:end].strip()
    if block:
        return block + "\n"
    return ""


def print_diff(label: str, current: str, expected: str) -> None:
    diff = list(
        difflib.unified_diff(
            current.splitlines(),
            expected.splitlines(),
            fromfile=f"current-{label}",
            tofile=f"expected-{label}",
            lineterm="",
        )
    )
    if diff:
        print(f"[managed-drift] DIFF {label}:")
        for line in diff:
            print(line)


def decode_text(content: bytes) -> str | None:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return None


def expected_managed_files(
    knowledge_repo_root: Path,
    templates_root: Path,
    knowledge_root: str,
    project_name_slug: str,
) -> list[tuple[Path, Path]]:
    entries = [
        installable_entries(knowledge_repo_root, templates_root)[name]
        for name in MANAGED_REFRESH_TEMPLATES
    ]
    return iter_install_files(entries)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    knowledge_repo_root = repo_root()
    templates_root = knowledge_repo_root / "templates"
    project_root = (
        args.project_root.resolve()
        if args.project_root is not None
        else knowledge_repo_root.parent.resolve()
    )

    try:
        knowledge_root = args.knowledge_root or infer_knowledge_root(
            project_root=project_root,
            knowledge_repo_root=knowledge_repo_root,
        )
        project_name_slug = project_slug(project_root)
    except RuntimeError as error:
        print(f"[managed-drift] FAIL: {error}", file=sys.stderr)
        return 2

    agents_path = project_root / AGENTS_PATH
    if not agents_path.is_file():
        print(
            f"[managed-drift] FAIL: missing {agents_path.relative_to(project_root)}",
            file=sys.stderr,
        )
        return 2

    content = agents_path.read_text(encoding="utf-8")
    current_header = extract_managed_block(content, HEADER_START, HEADER_END)
    current_footer = extract_managed_block(content, FOOTER_START, FOOTER_END)
    expected_header = render_expected_block(
        templates_root,
        AGENTS_HEADER,
        knowledge_root,
        project_name_slug,
    )
    expected_footer = render_expected_block(
        templates_root,
        AGENTS_FOOTER,
        knowledge_root,
        project_name_slug,
    )

    drift_found = False
    print(
        f"[managed-drift] Project root: {project_root}\n"
        f"[managed-drift] Knowledge root: {knowledge_root}"
    )

    for label, current, expected in (
        ("header", current_header, expected_header),
        ("footer", current_footer, expected_footer),
    ):
        if current == expected:
            print(f"[managed-drift] OK: managed {label} is up to date.")
            continue
        drift_found = True
        if not current:
            print(f"[managed-drift] WARN: managed {label} block is missing.")
        else:
            print(f"[managed-drift] WARN: managed {label} differs.")
        print_diff(label, current, expected)

    gitignore_path = project_root / GITIGNORE_PATH
    gitignore_text = (
        gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    )
    start_marker, end_marker = GITIGNORE_MARKERS
    current_gitignore = extract_delimited_block(
        gitignore_text, start_marker, end_marker
    )
    expected_gitignore = render_expected_block(
        templates_root,
        GITIGNORE_TEMPLATE,
        knowledge_root,
        project_name_slug,
    )
    if current_gitignore == expected_gitignore:
        print("[managed-drift] OK: managed file .gitignore is up to date.")
    else:
        drift_found = True
        if not current_gitignore:
            print("[managed-drift] WARN: managed file .gitignore is missing.")
        else:
            print("[managed-drift] WARN: managed file .gitignore differs.")
        print_diff("file-.gitignore", current_gitignore, expected_gitignore)

    for source, relative_path in expected_managed_files(
        knowledge_repo_root,
        templates_root,
        knowledge_root,
        project_name_slug,
    ):
        if relative_path == GITIGNORE_PATH:
            continue
        destination = project_root / relative_path
        expected_bytes = render_file(source, knowledge_root, project_name_slug)
        current_bytes = destination.read_bytes() if destination.is_file() else None
        label = relative_path.as_posix()
        if current_bytes == expected_bytes:
            print(f"[managed-drift] OK: managed file {label} is up to date.")
            continue

        drift_found = True
        if current_bytes is None:
            print(f"[managed-drift] WARN: managed file {label} is missing.")
        else:
            print(f"[managed-drift] WARN: managed file {label} differs.")
        current_text = decode_text(current_bytes or b"")
        expected_text = decode_text(expected_bytes)
        if current_text is not None and expected_text is not None:
            print_diff(f"file-{label}", current_text, expected_text)

    if drift_found:
        refresh_flags = " ".join(
            f"--template {name}" for name in MANAGED_REFRESH_TEMPLATES
        )
        print(
            "[managed-drift] NEXT: review the diffs above, then refresh the "
            "managed sections with:"
        )
        print(
            "[managed-drift] NEXT: python "
            f"{knowledge_root}/scripts/initial-setup.py --project-root . "
            f"--knowledge-root {knowledge_root} --force {refresh_flags}"
        )
        print(
            "[managed-drift] NEXT: run `git diff` before any `git add` so "
            "the staged update is reviewed first."
        )
        return 1

    print(
        "[managed-drift] PASS: managed AGENTS.md sections and starter files "
        "match current templates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
