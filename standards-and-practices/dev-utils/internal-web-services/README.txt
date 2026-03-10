Internal Web Service Utilities
==============================

This directory contains reusable utility scripts for private web services that
follow the `internal-web-services.txt` technique.

- `reissue_tailscale_caddy_certificate.py`: request or renew a Tailscale-
  managed HTTPS certificate, update a Caddy reverse-proxy config, restart the
  proxy container, and reconfigure `tailscale serve`.
- `check_tailscale_service_stack.py`: inspect the Podman stack, local TLS
  listener, Tailscale state, and the service URLs exposed through the tailnet.

Keep these scripts generic. Do not add product names, company names, personal
names, or machine-specific assumptions.
