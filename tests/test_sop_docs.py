from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOP = ROOT / "standards-and-practices" / "docs" / "sop"

EXPECTED_FILES = [
    SOP / "README.txt",
    SOP / "languages" / "README.txt",
    SOP / "languages" / "_TEMPLATE.txt",
    SOP / "languages" / "python.txt",
    SOP / "languages" / "typescript.txt",
    SOP / "technologies" / "README.txt",
    SOP / "technologies" / "_TEMPLATE.txt",
    SOP / "technologies" / "fastapi.txt",
    SOP / "technologies" / "podman.txt",
    SOP / "technologies" / "tailscale.txt",
    SOP / "technologies" / "caddy.txt",
    SOP / "technologies" / "react.txt",
    SOP / "technologies" / "vite.txt",
    SOP / "technologies" / "sqlalchemy.txt",
    SOP / "technologies" / "alembic.txt",
    SOP / "technologies" / "postgresql.txt",
    SOP / "technologies" / "berkeleydb.txt",
    SOP / "techniques" / "README.txt",
    SOP / "techniques" / "_TEMPLATE.txt",
    SOP / "techniques" / "new-web-service.txt",
    SOP / "techniques" / "internal-web-services.txt",
]

BANNED_TERMS = [
    "HPG",
    "mheck",
    "Hard Problems Group",
    "Hard-Problems-Group",
]


def test_sop_core_documents_exist() -> None:
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing SOP document: {path.relative_to(ROOT)}"


def test_sop_documents_are_generic_for_distribution() -> None:
    for path in sorted(SOP.rglob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for banned in BANNED_TERMS:
            assert banned not in text, (
                f"unexpected project-specific term {banned!r} in "
                f"{path.relative_to(ROOT)}"
            )


def test_new_web_service_sop_covers_default_stack() -> None:
    text = (SOP / "techniques" / "new-web-service.txt").read_text(encoding="utf-8")
    assert "Python 3.12" in text
    assert "rootless Podman" in text
    assert "React" in text
    assert "Vite" in text
    assert "BerkeleyDB" in text
    assert "PostgreSQL" in text
