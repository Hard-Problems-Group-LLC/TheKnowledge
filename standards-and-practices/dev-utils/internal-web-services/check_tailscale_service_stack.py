#!/usr/bin/env python3
"""Report Podman, Tailscale, TLS, and URL health for an internal service."""

from __future__ import annotations

import argparse
import json
import os
import pwd
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect a Tailscale-backed internal web service stack, including "
            "Podman state, local TLS listener, and tailnet URLs."
        )
    )
    parser.add_argument(
        "--service-user",
        default="internal-web",
        help="Service user that owns the rootless Podman stack.",
    )
    parser.add_argument(
        "--pod-name",
        default=None,
        help="Optional Podman pod name to inspect.",
    )
    parser.add_argument(
        "--container",
        action="append",
        dest="containers",
        default=None,
        help="Container name to inspect. Repeat for multiple containers.",
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
    return parser.parse_args(argv)


def run(
    command: Sequence[str],
    *,
    as_user: str | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    full_command = list(command)
    current_user = pwd.getpwuid(os.geteuid()).pw_name
    cwd = None
    if as_user and as_user != current_user:
        if os.geteuid() != 0:
            raise RuntimeError(f"must run as root to execute as user {as_user!r}")
        cwd = Path("/tmp")
        full_command = ["runuser", "-u", as_user, "--", *full_command]
    return subprocess.run(
        full_command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


def detect_tailscale_status() -> tuple[str, dict[str, object]]:
    result = run(["tailscale", "status", "--json"], check=False)
    if result.returncode != 0:
        raise RuntimeError("tailscale status --json failed")
    payload = json.loads(result.stdout)
    fqdn = payload.get("Self", {}).get("DNSName", "").rstrip(".\n")
    if not fqdn:
        raise RuntimeError("tailscale status did not report a DNS name")
    return fqdn, payload


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


def check_certificate(fqdn: str, listen_port: int) -> tuple[bool, str]:
    result = subprocess.run(
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
    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    if "CONNECTED" not in combined or "BEGIN CERTIFICATE" not in result.stdout:
        return False, "certificate probe failed"

    subject = parse_x509(result.stdout, "-subject")
    issuer = parse_x509(result.stdout, "-issuer")
    if fqdn not in subject:
        return False, f"subject mismatch: {subject or 'unknown'}"
    if "Tailscale" not in issuer and "Let's Encrypt" not in issuer:
        return False, f"unexpected issuer: {issuer or 'unknown'}"
    return True, issuer


def curl_status(url: str) -> str:
    result = subprocess.run(
        [
            "curl",
            "-k",
            "-o",
            "/dev/null",
            "-s",
            "-w",
            "%{http_code}",
            "--max-time",
            "5",
            url,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() or "ERROR"


def print_check(label: str, value: str) -> None:
    print(f"[service-check] {label}: {value}")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        fqdn, status_payload = detect_tailscale_status()
        if args.tailscale_fqdn:
            fqdn = args.tailscale_fqdn
    except RuntimeError as error:
        print(f"[service-check] FAIL: {error}", file=sys.stderr)
        return 1

    print_check("tailscale-fqdn", fqdn)
    print_check("tailscale-backend", str(status_payload.get("BackendState", "unknown")))

    peers = status_payload.get("Peer", {})
    direct_paths = sum(1 for peer in peers.values() if peer.get("CurAddr"))
    print_check("tailscale-direct-paths", f"{direct_paths}/{len(peers)}")

    netcheck = run(["tailscale", "netcheck", "--json"], check=False)
    if netcheck.returncode == 0:
        try:
            payload = json.loads(netcheck.stdout)
        except json.JSONDecodeError:
            print_check("tailscale-netcheck", "invalid-json")
        else:
            print_check("tailscale-udp", "ok" if payload.get("UDP") else "blocked")
            mapping_varies = payload.get("MappingVariesByDestIP")
            print_check(
                "tailscale-nat-mapping",
                "varies" if mapping_varies else "consistent",
            )

    if args.pod_name:
        pod = run(
            ["podman", "pod", "inspect", args.pod_name, "--format", "{{.State}}"],
            as_user=args.service_user,
            check=False,
        )
        print_check("podman-pod", pod.stdout.strip() or "missing")

    for container in args.containers or []:
        state = run(
            ["podman", "inspect", container, "--format", "{{.State.Status}}"],
            as_user=args.service_user,
            check=False,
        )
        print_check(f"container-{container}", state.stdout.strip() or "missing")

    listener = subprocess.run(
        ["ss", "-tulpn"],
        capture_output=True,
        text=True,
        check=False,
    )
    port_marker = f":{args.listen_port}"
    print_check(
        "listener",
        "present" if port_marker in listener.stdout else f"missing:{args.listen_port}",
    )

    cert_ok, cert_message = check_certificate(fqdn, args.listen_port)
    print_check("certificate", "ok" if cert_ok else f"fail:{cert_message}")

    direct_url = f"https://{fqdn}:{args.listen_port}"
    served_url = (
        f"https://{fqdn}"
        if args.serve_port == 443
        else f"https://{fqdn}:{args.serve_port}"
    )
    print_check("direct-url", f"{direct_url} -> {curl_status(direct_url)}")
    print_check("served-url", f"{served_url} -> {curl_status(served_url)}")

    if not cert_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
