#!/usr/bin/env python3
"""Validate knack documents with per-file hash caching."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


SCHEMA_VERSION = "1.0.0"
OVERVIEW_TARGET = 1250
REFERENCE_TARGET = 2500
ABSOLUTE_MAXIMUM = 5000
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")


@dataclass(frozen=True)
class KnackFile:
    source_kind: str
    knack_root: Path
    path: Path

    @property
    def logical_name(self) -> str:
        return self.path.relative_to(self.knack_root).as_posix()

    @property
    def cache_key(self) -> str:
        return f"{self.source_kind}:{self.logical_name}"

    @property
    def display_name(self) -> str:
        return f"{self.source_kind}:{self.logical_name}"


@dataclass
class ValidationSummary:
    warnings: List[str]
    errors: List[str]
    word_count: int

    @property
    def status(self) -> str:
        if self.errors:
            return "fail"
        if self.warnings:
            return "warn"
        return "pass"


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate changed knack files for basic Markdown structure, "
            "high-entropy findings, and word-count guidance."
        )
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root that may contain a top-level knacks/ directory.",
    )
    parser.add_argument(
        "--knowledge-root",
        default=None,
        help=(
            "TheKnowledge root that may contain stock knacks/. Defaults to the "
            "repository root that contains this script. Relative values are "
            "resolved from --project-root."
        ),
    )
    parser.add_argument(
        "--cache-file",
        default=".git/knack-validation-cache.json",
        help="Cache file path relative to --project-root.",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore cached file hashes and revalidate all discovered knacks.",
    )
    parser.add_argument(
        "--show-cache",
        action="store_true",
        help="Print the current cache JSON and exit.",
    )
    return parser.parse_args(argv)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve_knowledge_root(project_root: Path, value: str | None) -> Path:
    if value is None:
        return Path(__file__).resolve().parent.parent
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    return candidate.resolve()


def load_cache(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "files": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"schema_version": SCHEMA_VERSION, "files": {}}
    if not isinstance(data, dict):
        return {"schema_version": SCHEMA_VERSION, "files": {}}
    if data.get("schema_version") != SCHEMA_VERSION:
        return {"schema_version": SCHEMA_VERSION, "files": {}}
    files = data.get("files")
    if not isinstance(files, dict):
        data["files"] = {}
    return data


def save_cache(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = {
        "schema_version": SCHEMA_VERSION,
        "files": data.get("files", {}),
    }
    path.write_text(
        json.dumps(ordered, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def sha256_digest(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def collect_knack_files(project_root: Path, knowledge_root: Path) -> List[KnackFile]:
    files: List[KnackFile] = []
    roots: List[tuple[str, Path]] = [("project", project_root / "knacks")]
    if knowledge_root != project_root:
        roots.append(("knowledge", knowledge_root / "knacks"))

    for source_kind, knack_root in roots:
        if not knack_root.exists():
            continue
        for path in sorted(knack_root.rglob("*.knack.md")):
            if path.is_file():
                files.append(
                    KnackFile(
                        source_kind=source_kind,
                        knack_root=knack_root,
                        path=path.resolve(),
                    )
                )
    return files


def detect_collisions(files: Iterable[KnackFile]) -> Dict[str, List[KnackFile]]:
    collisions: Dict[str, List[KnackFile]] = {}
    by_name: Dict[str, List[KnackFile]] = {}
    for knack in files:
        by_name.setdefault(knack.logical_name, []).append(knack)
    for logical_name, entries in by_name.items():
        source_kinds = {entry.source_kind for entry in entries}
        if len(source_kinds) > 1:
            collisions[logical_name] = entries
    return collisions


def load_entropy_module(knowledge_root: Path):
    checker = (
        knowledge_root
        / "standards-and-practices"
        / "dev-utils"
        / "security"
        / "entropy-check.py"
    )
    if not checker.is_file():
        raise FileNotFoundError(f"Missing entropy checker: {checker}")
    spec = importlib.util.spec_from_file_location("knack_entropy_check", checker)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load entropy checker module from {checker}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def validate_markdown(text: str) -> List[str]:
    errors: List[str] = []
    if not text.strip():
        errors.append("document is empty")
        return errors

    fence_char: str | None = None
    fence_length = 0
    fence_line = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        if fence_char is None:
            match = FENCE_RE.match(line)
            if match:
                token = match.group(1)
                fence_char = token[0]
                fence_length = len(token)
                fence_line = line_number
            continue

        closing_pattern = rf"^[ \t]*{re.escape(fence_char)}{{{fence_length},}}[ \t]*$"
        if re.match(closing_pattern, line):
            fence_char = None
            fence_length = 0
            fence_line = 0

    if fence_char is not None:
        errors.append(f"unclosed fenced code block opened on line {fence_line}")
    return errors


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def recommended_word_limit(knack: KnackFile) -> tuple[int, str]:
    name = knack.path.name
    relative_parts = knack.path.relative_to(knack.knack_root).parts[:-1]
    if name.endswith(".overview.knack.md"):
        return OVERVIEW_TARGET, "overview"
    if name.endswith(".api.knack.md"):
        return REFERENCE_TARGET, "api"
    if any(part.endswith(".knack") for part in relative_parts):
        return REFERENCE_TARGET, "fileset"
    return OVERVIEW_TARGET, "single-file"


def validate_knack(knack: KnackFile, entropy_module) -> ValidationSummary:
    text = knack.path.read_text(encoding="utf-8")
    warnings: List[str] = []
    errors = validate_markdown(text)
    word_count = count_words(text)
    limit, label = recommended_word_limit(knack)
    if word_count > limit:
        warnings.append(
            f"word count {word_count} exceeds the recommended {limit} words "
            f"for {label} knack files"
        )
    if word_count > ABSOLUTE_MAXIMUM:
        warnings.append(
            f"word count {word_count} exceeds the recommended absolute "
            f"maximum of {ABSOLUTE_MAXIMUM} words per file"
        )

    scan_result = entropy_module.scan_file(
        path=knack.path,
        top_percent=1.0,
        spike_percent=20.0,
        min_line_length=None,
        max_findings_per_file=20,
        min_token_length=20,
    )
    if scan_result is not None and scan_result.findings:
        line_numbers = ", ".join(str(item.line_number) for item in scan_result.findings)
        errors.append(f"high-entropy content detected on lines {line_numbers}")

    return ValidationSummary(
        warnings=warnings,
        errors=errors,
        word_count=word_count,
    )


def prune_cache(files_cache: Dict[str, object], active_keys: set[str]) -> None:
    stale = [key for key in files_cache if key not in active_keys]
    for key in stale:
        files_cache.pop(key, None)


def emit_warning(message: str) -> None:
    print(f"[knack-check] WARNING: {message}")


def emit_error(message: str) -> None:
    print(f"[knack-check] ERROR: {message}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    project_root = Path(args.project_root).resolve()
    knowledge_root = resolve_knowledge_root(project_root, args.knowledge_root)
    cache_path = (project_root / args.cache_file).resolve()

    if not project_root.exists():
        emit_error(f"missing project root: {project_root}")
        return 2
    if not knowledge_root.exists():
        emit_error(f"missing knowledge root: {knowledge_root}")
        return 2

    cache = load_cache(cache_path)
    files_cache = cache.setdefault("files", {})
    if not isinstance(files_cache, dict):
        files_cache = {}
        cache["files"] = files_cache

    if args.show_cache:
        print(json.dumps(cache, indent=2, sort_keys=False))
        return 0

    try:
        entropy_module = load_entropy_module(knowledge_root)
    except (FileNotFoundError, RuntimeError) as exc:
        emit_error(str(exc))
        return 2

    knack_files = collect_knack_files(project_root, knowledge_root)
    active_keys = {knack.cache_key for knack in knack_files}
    prune_cache(files_cache, active_keys)

    if not knack_files:
        save_cache(cache_path, cache)
        print("[knack-check] PASS: no .knack.md files found.")
        return 0

    collisions = detect_collisions(knack_files)
    for logical_name, entries in sorted(collisions.items()):
        locations = ", ".join(entry.display_name for entry in entries)
        emit_warning(
            f"path collision for {logical_name}; evaluating both files: {locations}"
        )

    validated = 0
    skipped = 0
    warnings_seen = 0
    errors_seen = 0

    for knack in knack_files:
        digest = sha256_digest(knack.path)
        cache_entry = files_cache.get(knack.cache_key)
        if (
            not args.no_cache
            and isinstance(cache_entry, dict)
            and cache_entry.get("sha256") == digest
            and cache_entry.get("status") in {"pass", "warn"}
        ):
            skipped += 1
            cached_warnings = cache_entry.get("warnings", [])
            warning_count = len(cached_warnings)
            if warning_count:
                emit_warning(
                    f"cache hit for {knack.display_name}; skipping unchanged file "
                    f"with {warning_count} cached warning(s)"
                )
                warnings_seen += warning_count
            else:
                print(f"[knack-check] SKIP: {knack.display_name}")
            continue

        summary = validate_knack(knack, entropy_module)
        validated += 1
        warnings_seen += len(summary.warnings)
        errors_seen += len(summary.errors)

        if summary.errors:
            emit_error(f"validation failed for {knack.display_name}")
            for message in summary.errors:
                emit_error(f"  {message}")
        elif summary.warnings:
            emit_warning(f"validated {knack.display_name} with warnings")
            for message in summary.warnings:
                emit_warning(f"  {message}")
        else:
            print(f"[knack-check] PASS: {knack.display_name}")

        files_cache[knack.cache_key] = {
            "status": summary.status,
            "sha256": digest,
            "warnings": summary.warnings,
            "errors": summary.errors,
            "word_count": summary.word_count,
            "updated_at": now_iso(),
        }

    save_cache(cache_path, cache)

    print(
        "[knack-check] SUMMARY: "
        f"validated={validated} skipped={skipped} "
        f"warnings={warnings_seen} errors={errors_seen}"
    )
    if errors_seen:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
