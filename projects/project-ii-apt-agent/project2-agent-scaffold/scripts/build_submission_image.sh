#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_ROOT/dist"
IMAGE_TAG="${PROJECT2_IMAGE_TAG:-project2-agent-submission:phase2}"
OUT="$DIST_DIR/project2-agent-submission-image-phase2.tar.gz"

cd "$PROJECT_ROOT"
./scripts/run_static_checks.sh >/tmp/project2-static-checks.log
mkdir -p "$DIST_DIR"
docker build -t "$IMAGE_TAG" . >/tmp/project2-submission-image-build.log
# gzip output is smaller and accepted by many upload systems; if the grader
# requires a raw tar, run: gzip -dk <file>.tar.gz
docker save "$IMAGE_TAG" | gzip -c > "$OUT"
python3 - <<PY
from pathlib import Path
out = Path('$OUT')
print(f'submission_image={out}')
print(f'image_tag=$IMAGE_TAG')
print(f'size_bytes={out.stat().st_size}')
PY
