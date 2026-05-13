#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

: "${PROJECT2_SHARED_DIR:=$PROJECT_ROOT/mock_shared}"
: "${PROJECT2_READINESS_ROUNDS:=2}"
export PROJECT2_SHARED_DIR
export PYTHONDONTWRITEBYTECODE=1

cd "$PROJECT_ROOT"

# Keep this report reproducible: start from a clean mock shared directory unless
# the caller explicitly asks to inspect an existing shared volume.
if [ "${PROJECT2_READINESS_PRESERVE_SHARED:-0}" != "1" ]; then
  ./scripts/clean_shared.sh >/dev/null 2>&1 || true
fi

./scripts/run_mock_grader.sh --rounds "$PROJECT2_READINESS_ROUNDS" >/tmp/project2-readiness-mock.log
python3 -m src.readiness_report --run-static --output "$PROJECT2_SHARED_DIR/readiness_report.json"
echo "mock_log=/tmp/project2-readiness-mock.log"
