#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

: "${PROJECT2_SHARED_DIR:=/shared}"
export PROJECT2_SHARED_DIR
export PROJECT2_ENABLE_PHASE2_PROBE=1
export PYTHONDONTWRITEBYTECODE=1

cd "$PROJECT_ROOT"
python3 -m src.exploit_runner
