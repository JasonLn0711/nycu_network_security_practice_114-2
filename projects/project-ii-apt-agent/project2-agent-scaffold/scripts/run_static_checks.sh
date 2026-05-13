#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"
export PYTHONDONTWRITEBYTECODE=1

test -f exploit
test -f triage
test -f .dockerignore
test -x exploit
test -x triage
test -f docs/SPEC.md
test -f docs/SDD.md
test -f docs/STUDENT_CHECKLIST.md
test -f docs/SAFETY_BOUNDARY.md
test -f docs/COMPLETION_AUDIT.md
test -x scripts/run_phase2_probe_against_shared.sh
test -x scripts/build_submission_package.sh
test -x scripts/build_submission_image.sh
test -f docs/SUBMISSION_GUIDE.md
test -f docs/REQUIREMENTS_TRACEABILITY.md

python3 - <<'PY'
import importlib

modules = [
    "src.path_config",
    "src.logger",
    "src.safety_guard",
    "src.state_manager",
    "src.environment_checker",
    "src.blogic_metadata",
    "src.phase2_payload",
    "src.config_planner",
    "src.exploit_runner",
    "src.coredump_scanner",
    "src.coredump_analyzer",
    "src.triage_runner",
    "src.mock_grader",
    "src.readiness_report",
]
for name in modules:
    importlib.import_module(name)
print("static checks passed")
PY
