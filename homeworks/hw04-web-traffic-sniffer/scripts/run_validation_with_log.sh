#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
timestamp="$(date +%Y%m%d-%H%M%S)"
log_dir="$repo_dir/logs"
log_file="$log_dir/validation-$timestamp.log"

mkdir -p "$log_dir"

{
  echo "# HW4 validation log"
  echo "timestamp=$timestamp"
  echo "repo_dir=$repo_dir"
  echo

  echo "## Environment"
  node --version
  python3 --version
  echo

  echo "## JavaScript syntax"
  node --check "$repo_dir/solution/Extension/background.js"
  echo

  echo "## Extension logic tests"
  node "$repo_dir/scripts/test_extension_logic.js"
  echo

  echo "## Manifest JSON"
  python3 -m json.tool "$repo_dir/solution/Extension/manifest.json" >/tmp/hw4-manifest-validation.json
  echo "manifest-json-ok"
  echo

  echo "## Final package validation"
  python3 "$repo_dir/scripts/validate_submission.py" \
    --student-id 513559004 \
    --package-dir "$repo_dir/submission/final/HW6_513559004" \
    --zip "$repo_dir/submission/final/HW6_513559004.zip"
  echo

  echo "## ZIP listing"
  unzip -l "$repo_dir/submission/final/HW6_513559004.zip"
  echo

  echo "## PDF metadata"
  pdfinfo "$repo_dir/report/513559004_report.pdf" || true
  echo

  echo "## Ignore checks"
  git -C "$repo_dir" check-ignore -v \
    evidence/raw-local/edge-profile \
    evidence/raw-local/runtime-smoke-summary.json \
    evidence/raw-local/sanitized-evidence-records.json \
    submission/dry-run/HW6_513559004.zip \
    submission/final/HW6_513559004.zip
} | tee "$log_file"

echo "Validation log written to $log_file"
