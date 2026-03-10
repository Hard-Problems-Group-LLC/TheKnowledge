#!/usr/bin/env python3
"""Renew Tailscale HTTPS certificates for a Caddy-backed internal service."""

from __future__ import annotations

import argparse
import grp
import json
import os
import pwd
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Request or renew a Tailscale-managed HTTPS certificate, rewrite "
            "a Caddy config, restart the proxy container, and verify the "
            "local TLS endpoint."
        )
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("/opt/internal-web-service"),
        help="Base directory for service data, certificates, and proxy config.",
    )
    parser.add_argument(
        "--proxy-config",
        type=Path,
        default=None,
        help="Path to the Caddyfile to rewrite. Defaults to <base-dir>/caddy/Caddyfile.",
    )
    parser.add_argument(
        "--cert-dir",
        type=Path,
        default=None,
        help="Directory that stores certificate files. Defaults to <base-dir>/certs.",
    )
    parser.add_argument(
        "--service-upstream",
        default="http://127.0.0.1:80",
        help="Upstream application URL for the Caddy reverse proxy.",
    )
    parser.add_argument(
        "--proxy-container",
        default="proxy",
        help="Proxy container name to restart after config changes.",
    )
    parser.add_argument(
        "--service-user",
        default="internal-web",
        help="Service user that owns the rootless Podman stack.",
    )
    parser.add_argument(
        "--service-group",
        default="internal-web",
        help="Service group that owns the certificate and config files.",
    )
    parser.add_argument(
        "--listen-port",
        type=int,
        default=8443,
        help="Local TLS port exposed by the reverse proxy.",
    )
    parser.add_argument(
        "--serve-port",
        type=int,
        default=443,
        help="Tailnet HTTPS port exposed through tailscale serve.",
    )
    parser.add_argument(
        "--tailscale-fqdn",
        default=None,
        help="Override the detected Tailscale DNS name.",
    )
    parser.add_argument(
        "--skip-serve",
        action="store_true",
        help="Do not reconfigure tailscale serve after certificate renewal.",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Do not run the post-renewal TLS verification checks.",
    )
    return parser.parse_args(argv)


def run(
    command: Sequence[str],
    *,
    as_user: str | None = None,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    effective_cwd = cwd
    full_command = list(command)
    current_user = pwd.getpwuid(os.geteuid()).pw_name
    if as_user and as_user != current_user:
        if os.geteuid() != 0:
            raise RuntimeError(f"must run as root to execute as user {as_user!r}")
        effective_cwd = cwd or Path("/tmp")
        full_command = ["runuser", "-u", as_user, "--", *full_command]

    result = subprocess.run(
        full_command,
        cwd=effective_cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        details = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(
            f"command failed ({' '.join(full_command)}): {details or 'no output'}"
        )
    return result


def require_dependencies() -> None:
    missing = []
    for name in ("tailscale", "podman", "openssl", "curl"):
        if shutil.which(name) is None:
            missing.append(name)
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"missing required commands: {joined}")


def detect_tailscale_fqdn() -> str:
    result = run(["tailscale", "status", "--json"])
    payload = json.loads(result.stdout)
    fqdn = payload.get("Self", {}).get("DNSName", "").rstrip(".\n")
    if not fqdn:
        raise RuntimeError("tailscale status did not report a DNS name")
    return fqdn


def resolve_identity(user: str, group: str) -> tuple[int, int]:
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
    except KeyError as error:
        raise RuntimeError(
            f"service user/group {user!r}:{group!r} does not exist"
        ) from error
    return uid, gid


def write_caddyfile(config_path: Path, fqdn: str, upstream: str, port: int) -> None:
    content = (
        "{\n"
        "    auto_https disable_redirects\n"
        "}\n"
        f":{port} {{\n"
        f"    reverse_proxy {upstream}\n"
        f"    tls /etc/caddy/certs/{fqdn}.crt /etc/caddy/certs/{fqdn}.key\n"
        "}\n"
    )
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(content, encoding="utf-8")


def request_tailscale_cert(cert_dir: Path, fqdn: str) -> None:
    cert_dir.mkdir(parents=True, exist_ok=True)
    run(
        [
            "tailscale",
            "cert",
            "--cert-file",
            f"{fqdn}.crt",
            "--key-file",
            f"{fqdn}.key",
            fqdn,
        ],
        cwd=cert_dir,
    )


def fix_permissions(paths: Sequence[Path], uid: int, gid: int) -> None:
    for path in paths:
        if os.geteuid() == 0:
            os.chown(path, uid, gid)
        else:
            stat = path.stat()
            if stat.st_uid != uid or stat.st_gid != gid:
                raise RuntimeError(
                    "run as root to correct ownership for generated files"
                )
        os.chmod(path, 0o640 if path.suffix == ".key" else 0o644)


def restart_proxy_container(container: str, service_user: str) -> None:
    result = run(
        ["podman", "restart", container],
        as_user=service_user,
        check=False,
    )
    if result.returncode == 0:
        return
    start = run(["podman", "start", container], as_user=service_user, check=False)
    if start.returncode != 0:
        details = (start.stderr or start.stdout or "").strip()
        raise RuntimeError(
            f"could not restart or start proxy container {container!r}: "
            f"{details or 'no output'}"
        )


def configure_tailscale_serve(listen_port: int, serve_port: int) -> None:
    run(
        [
            "tailscale",
            "serve",
            "--bg",
            "--yes",
            f"--https={serve_port}",
            f"https+insecure://127.0.0.1:{listen_port}",
        ]
    )


def parse_x509(pem_text: str, flag: str) -> str:
    result = subprocess.run(
        ["openssl", "x509", "-noout", flag],
        input=pem_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def verify_local_tls(fqdn: str, listen_port: int) -> None:
    time.sleep(3)
    probe = subprocess.run(
        [
            "openssl",
            "s_client",
            "-connect",
            f"localhost:{listen_port}",
            "-servername",
            fqdn,
        ],
        input="",
        text=True,
        capture_output=True,
        check=False,
    )
    combined = "\n".join(part for part in (probe.stdout, probe.stderr) if part)
    if "CONNECTED" not in combined or "BEGIN CERTIFICATE" not in probe.stdout:
        raise RuntimeError("openssl could not retrieve a certificate from the proxy")

    subject = parse_x509(probe.stdout, "-subject")
    issuer = parse_x509(probe.stdout, "-issuer")
    if fqdn not in subject:
        raise RuntimeError(f"served certificate subject does not match {fqdn!r}")
    if "Tailscale" not in issuer and "Let's Encrypt" not in issuer:
        raise RuntimeError(
            "served certificate issuer is not Tailscale-managed Let's Encrypt"
        )

    response = subprocess.run(
        [
            "curl",
            "-k",
            "-o",
            "/dev/null",
            "-s",
            "-w",
            "%{http_code}",
            f"https://localhost:{listen_port}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if response.stdout.strip() not in {"200", "301", "302"}:
        raise RuntimeError(
            "local HTTPS endpoint did not return an expected success status"
        )


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    require_dependencies()

    proxy_config = args.proxy_config or args.base_dir / "caddy" / "Caddyfile"
    cert_dir = args.cert_dir or args.base_dir / "certs"
    fqdn = args.tailscale_fqdn or detect_tailscale_fqdn()
    uid, gid = resolve_identity(args.service_user, args.service_group)

    try:
        request_tailscale_cert(cert_dir, fqdn)
        cert_path = cert_dir / f"{fqdn}.crt"
        key_path = cert_dir / f"{fqdn}.key"
        fix_permissions([cert_path, key_path], uid, gid)
        write_caddyfile(
            proxy_config,
            fqdn,
            args.service_upstream,
            args.listen_port,
        )
        fix_permissions([proxy_config], uid, gid)
        restart_proxy_container(args.proxy_container, args.service_user)
        if not args.skip_serve:
            configure_tailscale_serve(args.listen_port, args.serve_port)
        if not args.skip_verify:
            verify_local_tls(fqdn, args.listen_port)
    except RuntimeError as error:
        print(f"[tailscale-caddy-cert] FAIL: {error}", file=sys.stderr)
        return 1

    print("[tailscale-caddy-cert] PASS")
    print(f"[tailscale-caddy-cert] fqdn={fqdn}")
    print(f"[tailscale-caddy-cert] direct=https://{fqdn}:{args.listen_port}")
    if not args.skip_serve:
        if args.serve_port == 443:
            print(f"[tailscale-caddy-cert] served=https://{fqdn}")
        else:
            print(f"[tailscale-caddy-cert] served=https://{fqdn}:{args.serve_port}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
