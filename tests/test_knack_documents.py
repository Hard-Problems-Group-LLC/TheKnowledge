from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STANDARDS = ROOT / "standards-and-practices" / "docs" / "specifications"

EXPECTED_FILES = [
    STANDARDS / "knack_documents.txt",
    ROOT / "knacks" / "README.md",
    ROOT / "knacks" / "authoring-guide.md",
    ROOT / "knacks" / "auditing" / "README.md",
    ROOT / "knacks" / "auditing" / "Software-Bill-of-Materials.knack.md",
    ROOT / "knacks" / "performance" / "README.md",
    ROOT / "knacks" / "performance" / "profiling" / "README.md",
    ROOT
    / "knacks"
    / "performance"
    / "profiling"
    / "WebPageLoadAndRenderProfiling.knack.md",
    ROOT / "knacks" / "debugging" / "README.md",
    ROOT / "knacks" / "debugging" / "HighLevelDebugging.knack.md",
    ROOT / "knacks" / "licenses" / "README.md",
    ROOT / "knacks" / "licenses" / "mit-license.knack.md",
    ROOT / "knacks" / "licenses" / "apache-license-2.0.knack.md",
    ROOT / "knacks" / "licenses" / "gpl-lgpl-v2-v3.knack.md",
    ROOT / "knacks" / "licenses" / "source-available-business-licenses.knack.md",
    ROOT / "knacks" / "sandboxing" / "README.md",
    ROOT / "knacks" / "sandboxing" / "bubblewrap.knack.md",
    ROOT / "knacks" / "UI" / "README.md",
    ROOT / "knacks" / "UI" / "terminal" / "README.md",
    ROOT / "knacks" / "UI" / "terminal" / "curses.api.C.knack.md",
    ROOT / "knacks" / "UI" / "terminal" / "curses.api.Python.knack.md",
    ROOT / "knacks" / "UI" / "terminal" / "ncurses.api.C.knack.md",
    ROOT / "knacks" / "UI" / "terminal" / "ncurses.api.CPP.knack.md",
]


def test_knack_scaffold_exists() -> None:
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing knack scaffold: {path.relative_to(ROOT)}"


def test_knack_docs_are_wired_into_repository_docs() -> None:
    repo_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    knack_readme = (ROOT / "knacks" / "README.md").read_text(encoding="utf-8")
    guide_text = (ROOT / "knacks" / "authoring-guide.md").read_text(encoding="utf-8")
    auditing_readme = (ROOT / "knacks" / "auditing" / "README.md").read_text(
        encoding="utf-8"
    )
    performance_readme = (ROOT / "knacks" / "performance" / "README.md").read_text(
        encoding="utf-8"
    )
    profiling_readme = (
        ROOT / "knacks" / "performance" / "profiling" / "README.md"
    ).read_text(encoding="utf-8")
    profiling_knack = (
        ROOT
        / "knacks"
        / "performance"
        / "profiling"
        / "WebPageLoadAndRenderProfiling.knack.md"
    ).read_text(encoding="utf-8")
    debugging_readme = (ROOT / "knacks" / "debugging" / "README.md").read_text(
        encoding="utf-8"
    )
    debugging_knack = (
        ROOT / "knacks" / "debugging" / "HighLevelDebugging.knack.md"
    ).read_text(encoding="utf-8")
    licenses_readme = (ROOT / "knacks" / "licenses" / "README.md").read_text(
        encoding="utf-8"
    )
    sbom_knack = (
        ROOT / "knacks" / "auditing" / "Software-Bill-of-Materials.knack.md"
    ).read_text(encoding="utf-8")
    sandboxing_readme = (ROOT / "knacks" / "sandboxing" / "README.md").read_text(
        encoding="utf-8"
    )
    terminal_readme = (ROOT / "knacks" / "UI" / "terminal" / "README.md").read_text(
        encoding="utf-8"
    )
    spec_text = (STANDARDS / "knack_documents.txt").read_text(encoding="utf-8")

    assert "`knacks/`" in repo_readme
    assert "proprietary or third-party knacks" in repo_readme
    assert "authoring-guide.md" in knack_readme
    assert ".overview.knack.md" in knack_readme
    assert ".api.knack.md" in knack_readme
    assert ".api.C.knack.md" in knack_readme
    assert ".api.Python.knack.md" in knack_readme
    assert ".api.rendering.CPP.knack.md" in knack_readme
    assert ".knack/" in knack_readme
    assert "project-local knack path collides" in knack_readme
    assert "skills" in knack_readme
    assert "debugging/" in knack_readme
    assert "licenses/" in knack_readme
    assert "auditing/" in knack_readme
    assert "performance/" in knack_readme
    assert "HighLevelDebugging.knack.md" in debugging_readme
    assert "AI-assisted debugging" in debugging_readme
    assert "high-level debugging" in debugging_knack.lower()
    assert "anti-patterns" in debugging_knack.lower()
    assert "1,250" in guide_text
    assert "2,500" in guide_text
    assert "5,000" in guide_text
    assert "per-file ceiling" in guide_text
    assert "top-level `knacks/` directory" in guide_text
    assert "validate_knacks.py" in guide_text
    assert ".git/knack-validation-cache.json" in guide_text
    assert ".cache/knack-validation-cache.json" in guide_text
    assert "dedicated unit tests" in guide_text
    assert "high-entropy findings as errors" in guide_text
    assert "word-count recommendation overruns as warnings" in guide_text
    assert "bug tracking" in guide_text
    assert "serious or high-priority" in guide_text
    assert ".api.C.knack.md" in guide_text
    assert ".api.Python.knack.md" in guide_text
    assert ".api.rendering.CPP.knack.md" in guide_text
    assert "software bill" in auditing_readme.lower()
    assert "materials generation and auditing" in auditing_readme.lower()
    assert "measurement and profiling" in performance_readme.lower()
    assert "webpageloadandrenderprofiling.knack.md" in profiling_readme.lower()
    assert "playwright" in profiling_knack.lower()
    assert "quiet window" in profiling_knack.lower()
    assert "data-load-state" in profiling_knack.lower()
    assert "top twenty" in licenses_readme.lower()
    assert "software-bill-of-materials.knack.md" in licenses_readme.lower()
    assert "top twenty set of software licenses" in licenses_readme.lower()
    assert "CycloneDX" in sbom_knack
    assert "SPDX" in sbom_knack
    assert "vulnerability audit" in sbom_knack.lower()
    assert "bubblewrap" in sandboxing_readme.lower()
    assert "sandbox" in sandboxing_readme.lower()
    assert "terminal" in terminal_readme.lower()
    assert "curses.api.C.knack.md" in terminal_readme
    assert "curses.api.Python.knack.md" in terminal_readme
    assert "ncurses.api.C.knack.md" in terminal_readme
    assert "ncurses.api.CPP.knack.md" in terminal_readme
    assert "`knacks/`" in spec_text
    assert ".knack.md" in spec_text
    assert "1,250" in spec_text
    assert "2,500" in spec_text
    assert "5,000" in spec_text
    assert ".overview.knack.md" in spec_text
    assert ".api.knack.md" in spec_text
    assert ".api.C.knack.md" in spec_text
    assert ".api.Python.knack.md" in spec_text
    assert ".api.rendering.CPP.knack.md" in spec_text
    assert "`knacks/authoring-guide.md`" in spec_text
    assert ".git/knack-validation-cache.json" in spec_text
    assert ".cache/knack-validation-cache.json" in spec_text
    assert "project-local knack path collides" in spec_text
    assert "dedicated unit tests" in spec_text
    assert "malformed Markdown documents as" in spec_text
    assert "word-count recommendation overruns as" in spec_text
    assert "knacks/UI/terminal/" in spec_text
    assert "knacks/performance/profiling/" in spec_text
