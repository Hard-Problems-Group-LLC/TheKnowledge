from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOP = ROOT / "standards-and-practices" / "docs" / "sop"
TOOLS = ROOT / "standards-and-practices" / "dev-utils" / "internal-web-services"

BANNED_TERMS = [
    "Lighthouse",
    "BuildQM",
    "HPG",
    "mheck",
    "kanboard",
    "Tesseraxe",
    "Hard Problems Group",
    "Hard-Problems-Group",
]


def test_internal_web_service_docs_and_tools_exist() -> None:
    expected = [
        SOP / "techniques" / "internal-web-services.txt",
        SOP / "technologies" / "tailscale.txt",
        SOP / "technologies" / "caddy.txt",
        TOOLS / "README.txt",
        TOOLS / "reissue_tailscale_caddy_certificate.py",
        TOOLS / "check_tailscale_service_stack.py",
    ]
    for path in expected:
        assert path.is_file(), f"missing internal web service asset: {path}"


def test_internal_web_service_assets_are_sanitized() -> None:
    for path in sorted((SOP / "techniques").glob("internal-web-services.txt")):
        text = path.read_text(encoding="utf-8")
        for banned in BANNED_TERMS:
            assert banned not in text, f"unexpected {banned!r} in {path}"

    for path in sorted((SOP / "technologies").glob("*.txt")):
        if path.name not in {"tailscale.txt", "caddy.txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for banned in BANNED_TERMS:
            assert banned not in text, f"unexpected {banned!r} in {path}"

    for path in sorted(TOOLS.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for banned in BANNED_TERMS:
            assert banned not in text, f"unexpected {banned!r} in {path}"


def test_internal_web_service_assets_reference_expected_commands() -> None:
    technique_text = (SOP / "techniques" / "internal-web-services.txt").read_text(
        encoding="utf-8"
    )
    reissue_text = (TOOLS / "reissue_tailscale_caddy_certificate.py").read_text(
        encoding="utf-8"
    )
    check_text = (TOOLS / "check_tailscale_service_stack.py").read_text(
        encoding="utf-8"
    )

    assert "new-web-service.txt" in technique_text
    assert "tailscale serve" in technique_text
    assert "reissue_tailscale_caddy_certificate.py" in technique_text
    assert "check_tailscale_service_stack.py" in technique_text

    assert '"tailscale",' in reissue_text
    assert '"cert"' in reissue_text
    assert '"serve"' in reissue_text
    assert "reverse_proxy" in reissue_text
    assert "openssl" in reissue_text
    assert "podman" in reissue_text

    assert '"tailscale", "status", "--json"' in check_text
    assert '"tailscale", "netcheck", "--json"' in check_text
    assert "openssl" in check_text
    assert "podman" in check_text
