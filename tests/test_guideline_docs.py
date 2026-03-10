from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GUIDELINES = ROOT / "guidelines"
SPECS = ROOT / "standards-and-practices" / "docs" / "specifications"


def test_guideline_spec_and_ui_limit_doc_exist() -> None:
    assert (SPECS / "guideline_documents.txt").is_file()
    assert (GUIDELINES / "ui-complexity-limits.txt").is_file()
    assert (GUIDELINES / "ui-antipatterns.txt").is_file()
    assert (GUIDELINES / "development-antipatterns.txt").is_file()


def test_ui_complexity_limit_doc_has_required_sections() -> None:
    text = (GUIDELINES / "ui-complexity-limits.txt").read_text(encoding="utf-8")
    assert "Guideline" in text
    assert "Repository recommendation" in text
    assert "Brief theoretical note" in text
    assert "References" in text
    assert "7 to 9 items" in text
    assert "Miller" in text
    assert "Cowan" in text
    assert "Rate-distortion theory" in text


def test_ui_antipatterns_doc_has_required_sections() -> None:
    text = (GUIDELINES / "ui-antipatterns.txt").read_text(encoding="utf-8")
    assert "Scope" in text
    assert "Avoid" in text
    assert "Repository recommendation" in text
    assert "References" in text
    assert "ui-complexity-limits.txt" in text
    assert "dialog" in text.lower()
    assert "keyboard focus" in text.lower()


def test_development_antipatterns_doc_has_required_sections() -> None:
    text = (GUIDELINES / "development-antipatterns.txt").read_text(encoding="utf-8")
    assert "Scope" in text
    assert "Avoid" in text
    assert "Repository recommendation" in text
    assert "References" in text
    assert "specification" in text.lower()
    assert "manual" in text.lower()
    assert "recovery" in text.lower()
