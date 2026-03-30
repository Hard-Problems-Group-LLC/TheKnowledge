"""Install starter templates from TheKnowledge into a consuming project."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable, Sequence

PLACEHOLDERS = ("{{THEKNOWLEDGE_ROOT}}", "{$KNOWLEDGE_ROOT}")
AGENTS_PATH = Path("AGENTS.md")
AGENTS_HEADER = "AGENTS-header.md"
AGENTS_FOOTER = "AGENTS-footer.md"
MANAGED_ROOT_FILES = (
    Path("tool_execution_constraints.json"),
    Path("tool_validation_profiles.json"),
    Path("scripts/tool_validation_profiles.py"),
)
MANAGED_REFRESH_TEMPLATES = (
    "requirements-dev.txt",
    "scripts",
    "scripts/tool_validation_profiles.py",
    "tool_execution_constraints.json",
    "tool_validation_profiles.json",
)
MANAGED_MARKERS = (
    "<!-- THEKNOWLEDGE_MANAGED_HEADER_START -->",
    "<!-- THEKNOWLEDGE_MANAGED_HEADER_END -->",
    "<!-- THEKNOWLEDGE_MANAGED_FOOTER_START -->",
    "<!-- THEKNOWLEDGE_MANAGED_FOOTER_END -->",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def infer_knowledge_root(project_root: Path, knowledge_repo_root: Path) -> str:
    try:
        relative = knowledge_repo_root.relative_to(project_root)
    except ValueError as error:
        raise RuntimeError(
            "--knowledge-root is required when --project-root does not contain "
            "this repository."
        ) from error

    return relative.as_posix() or "."


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install template files from TheKnowledge into a consuming project."
        )
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help=(
            "Target project root. Defaults to the parent directory of this "
            "repository."
        ),
    )
    parser.add_argument(
        "--knowledge-root",
        default=None,
        help=(
            "Path from the target project root back to this repository. "
            "Defaults to the relative path when it can be inferred."
        ),
    )
    parser.add_argument(
        "--template",
        action="append",
        dest="templates",
        default=None,
        help=(
            "Top-level entry under templates/ to install. Repeat to install "
            "multiple entries. Defaults to all installable entries."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in the target project.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned writes without changing the target project.",
    )
    return parser.parse_args(argv)


def installable_entries(
    knowledge_repo_root: Path,
    templates_root: Path,
) -> dict[str, tuple[Path, Path]]:
    entries = {
        path.name: (path, path.relative_to(templates_root))
        for path in sorted(templates_root.iterdir())
        if path.name not in {"README.md", AGENTS_HEADER, AGENTS_FOOTER}
    }
    for relative_path in MANAGED_ROOT_FILES:
        entries[relative_path.as_posix()] = (
            knowledge_repo_root / relative_path,
            relative_path,
        )
    return entries


def selected_templates(
    knowledge_repo_root: Path, templates_root: Path, requested: Iterable[str] | None
) -> list[tuple[Path, Path]]:
    available = installable_entries(knowledge_repo_root, templates_root)
    if requested is None:
        return list(available.values())

    selected: list[tuple[Path, Path]] = []
    for name in requested:
        path = available.get(name)
        if path is None:
            known = ", ".join(sorted(available))
            raise RuntimeError(f"Unknown template '{name}'. Available: {known}")
        selected.append(path)
    return selected


def iter_install_files(sources: Iterable[tuple[Path, Path]]) -> list[tuple[Path, Path]]:
    planned: list[tuple[Path, Path]] = []
    for source, destination_root in sources:
        if source.is_file():
            planned.append((source, destination_root))
            continue

        for file_path in sorted(source.rglob("*")):
            if file_path.is_file():
                planned.append(
                    (file_path, destination_root / file_path.relative_to(source))
                )
    return planned


def render_file(source: Path, knowledge_root: str) -> bytes:
    content = source.read_bytes()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return content
    for placeholder in PLACEHOLDERS:
        text = text.replace(placeholder, knowledge_root)
    return text.encode("utf-8")


def strip_managed_agents_sections(content: str) -> str:
    updated = content
    header_start, header_end, footer_start, footer_end = MANAGED_MARKERS

    while header_start in updated and header_end in updated:
        start = updated.index(header_start)
        end = updated.index(header_end) + len(header_end)
        updated = updated[:start] + updated[end:]

    while footer_start in updated and footer_end in updated:
        start = updated.index(footer_start)
        end = updated.index(footer_end) + len(footer_end)
        updated = updated[:start] + updated[end:]

    return updated.strip()


def install_agents_file(
    templates_root: Path,
    project_root: Path,
    knowledge_root: str,
    dry_run: bool,
) -> Path:
    header = render_file(templates_root / AGENTS_HEADER, knowledge_root).decode("utf-8")
    footer = render_file(templates_root / AGENTS_FOOTER, knowledge_root).decode("utf-8")
    destination = project_root / AGENTS_PATH

    existing = ""
    if destination.exists():
        existing = destination.read_text(encoding="utf-8")

    body = strip_managed_agents_sections(existing)
    sections = [header.strip()]
    if body:
        sections.append(body)
    sections.append(footer.strip())
    content = "\n\n".join(sections) + "\n"

    if dry_run:
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return destination


def install_templates(
    knowledge_repo_root: Path,
    templates_root: Path,
    project_root: Path,
    knowledge_root: str,
    requested: Iterable[str] | None,
    force: bool,
    dry_run: bool,
) -> list[Path]:
    sources = selected_templates(knowledge_repo_root, templates_root, requested)
    files = iter_install_files(sources)
    destinations = [project_root / relative_path for _, relative_path in files]

    conflicts = [
        path
        for path in destinations
        if path.exists() and path != project_root / AGENTS_PATH
    ]
    if conflicts and not force:
        joined = ", ".join(
            path.relative_to(project_root).as_posix() for path in conflicts
        )
        raise RuntimeError(
            "Refusing to overwrite existing files without --force: " + joined
        )

    if dry_run:
        return [project_root / AGENTS_PATH] + destinations

    project_root.mkdir(parents=True, exist_ok=True)
    written = [install_agents_file(templates_root, project_root, knowledge_root, False)]
    for source, relative_path in files:
        destination = project_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(render_file(source, knowledge_root))
        os.chmod(destination, source.stat().st_mode & 0o777)
        written.append(destination)
    return written


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
        destinations = install_templates(
            knowledge_repo_root=knowledge_repo_root,
            templates_root=templates_root,
            project_root=project_root,
            knowledge_root=knowledge_root,
            requested=args.templates,
            force=args.force,
            dry_run=args.dry_run,
        )
    except RuntimeError as error:
        print(f"[initial-setup] FAIL: {error}", file=sys.stderr)
        return 1

    action = "would install" if args.dry_run else "installed"
    print(
        f"[initial-setup] PASS: {action} {len(destinations)} files into "
        f"{project_root}"
    )
    for destination in destinations:
        print(f"[initial-setup] -> {destination.relative_to(project_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
