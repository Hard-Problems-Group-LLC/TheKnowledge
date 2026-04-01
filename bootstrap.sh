#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CANDIDATES=()
if [ -n "${PYTHON_BIN:-}" ]; then
  PYTHON_CANDIDATES+=("${PYTHON_BIN}")
fi
PYTHON_CANDIDATES+=(python3.12 python3.11 python3.10 python3.9 python3 python)

log() {
  echo "[bootstrap.sh] $*"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

supports_bootstrap_python() {
  "$1" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 9) else 1)' \
    >/dev/null 2>&1
}

detect_package_manager() {
  for candidate in apt-get dnf yum brew; do
    if command_exists "$candidate"; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

need_sudo() {
  if [ "$(id -u)" -eq 0 ]; then
    return 1
  fi
  command_exists sudo
}

install_python_if_missing() {
  local manager sudo_cmd
  manager=$(detect_package_manager) || return 1
  if need_sudo; then
    sudo_cmd="sudo"
  else
    sudo_cmd=""
  fi

  case "$manager" in
    apt-get)
      log "Installing python3 and venv tooling with apt-get"
      ${sudo_cmd:+$sudo_cmd }$manager update
      ${sudo_cmd:+$sudo_cmd }$manager install -y python3 python3-venv python3-pip
      ;;
    dnf|yum)
      log "Installing python3 and venv tooling with $manager"
      ${sudo_cmd:+$sudo_cmd }$manager -y install python3 python3-pip python3-virtualenv
      ;;
    brew)
      log "Installing python via Homebrew"
      $manager update
      $manager install python
      ;;
    *)
      return 1
      ;;
  esac
}

select_python() {
  local candidate
  for candidate in "${PYTHON_CANDIDATES[@]}"; do
    if command_exists "$candidate" && supports_bootstrap_python "$candidate"; then
      echo "$candidate"
      return 0
    fi
  done
  install_python_if_missing || true
  for candidate in "${PYTHON_CANDIDATES[@]}"; do
    if command_exists "$candidate" && supports_bootstrap_python "$candidate"; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

PYTHON_BIN_PATH=$(select_python) || {
  log "Python 3.9+ is required to start bootstrap."
  exit 1
}

log "Using bootstrap interpreter $PYTHON_BIN_PATH"
"$PYTHON_BIN_PATH" "$SCRIPT_DIR/bootstrap-stage2.py" "$@"
