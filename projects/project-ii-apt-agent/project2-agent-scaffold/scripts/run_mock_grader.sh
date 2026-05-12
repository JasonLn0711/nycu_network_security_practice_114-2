#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

: "${PROJECT2_SHARED_DIR:=$PROJECT_ROOT/mock_shared}"
export PROJECT2_SHARED_DIR
export PYTHONDONTWRITEBYTECODE=1

cd "$PROJECT_ROOT"
mkdir -p "$PROJECT2_SHARED_DIR"
exec python3 -m src.mock_grader "$@"
