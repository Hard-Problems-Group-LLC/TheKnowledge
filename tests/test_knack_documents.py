from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STANDARDS = ROOT / "standards-and-practices" / "docs" / "specifications"

EXPECTED_FILES = [
    STANDARDS / "knack_documents.txt",
    ROOT / "knacks" / "README.md",
    ROOT / "knacks" / "authoring-guide.md",
    ROOT / "knacks" / "UI" / "README.md",
    ROOT / "knacks" / "UI" / "terminal" / "README.md",
]


def test_knack_scaffold_exists() -> None:
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing knack scaffold: {path.relative_to(ROOT)}"


def test_knack_docs_are_wired_into_repository_docs() -> None:
    repo_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    knack_readme = (ROOT / "knacks" / "README.md").read_text(encoding="utf-8")
    guide_text = (ROOT / "knacks" / "authoring-guide.md").read_text(encoding="utf-8")
    terminal_readme = (ROOT / "knacks" / "UI" / "terminal" / "README.md").read_text(
        encoding="utf-8"
    )
    spec_text = (STANDARDS / "knack_documents.txt").read_text(encoding="utf-8")

    assert "`knacks/`" in repo_readme
    assert "proprietary or third-party knacks" in repo_readme
    assert "authoring-guide.md" in knack_readme
    assert ".overview.knack.md" in knack_readme
    assert ".api.knack.md" in knack_readme
    assert ".knack/" in knack_readme
    assert "project-local knack path collides" in knack_readme
    assert "skills" in knack_readme
    assert "1,250" in guide_text
    assert "2,500" in guide_text
    assert "5,000" in guide_text
    assert "per-file ceiling" in guide_text
    assert "top-level `knacks/` directory" in guide_text
    assert "validate_knacks.py" in guide_text
    assert ".git/knack-validation-cache.json" in guide_text
    assert "dedicated unit tests" in guide_text
    assert "high-entropy findings as errors" in guide_text
    assert "word-count recommendation overruns as warnings" in guide_text
    assert "bug tracking" in guide_text
    assert "serious or high-priority" in guide_text
    assert "terminal" in terminal_readme.lower()
    assert "`knacks/`" in spec_text
    assert ".knack.md" in spec_text
    assert "1,250" in spec_text
    assert "2,500" in spec_text
    assert "5,000" in spec_text
    assert ".overview.knack.md" in spec_text
    assert ".api.knack.md" in spec_text
    assert "`knacks/authoring-guide.md`" in spec_text
    assert ".git/knack-validation-cache.json" in spec_text
    assert "project-local knack path collides" in spec_text
    assert "dedicated unit tests" in spec_text
    assert "malformed Markdown documents as" in spec_text
    assert "word-count recommendation overruns as" in spec_text
    assert "knacks/UI/terminal/" in spec_text
