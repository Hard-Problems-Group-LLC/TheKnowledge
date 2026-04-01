#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "[install_prerequisites.sh] Delegating to ${ROOT_DIR}/bootstrap.sh"
exec "${ROOT_DIR}/bootstrap.sh" "$@"
