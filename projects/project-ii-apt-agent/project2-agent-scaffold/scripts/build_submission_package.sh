#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PROJECT_NAME="project2-agent-scaffold"
DIST_DIR="$PROJECT_ROOT/dist"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$DIST_DIR/${PROJECT_NAME}-${STAMP}.zip"

cd "$PROJECT_ROOT"
./scripts/run_static_checks.sh >/tmp/project2-static-checks.log
mkdir -p "$DIST_DIR"

python3 - <<PY
from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path('$PROJECT_ROOT').resolve()
out = Path('$OUT').resolve()
project_name = '$PROJECT_NAME'
excluded_dirs = {'.git', '__pycache__', '.pytest_cache', 'mock_shared', 'dist'}
excluded_suffixes = {'.pyc', '.pyo', '.core'}
excluded_names = {'.DS_Store'}
required = {
    f'{project_name}/Dockerfile',
    f'{project_name}/exploit',
    f'{project_name}/triage',
    f'{project_name}/src/exploit_runner.py',
    f'{project_name}/src/triage_runner.py',
    f'{project_name}/docs/REQUIREMENTS_TRACEABILITY.md',
    f'{project_name}/docs/SUBMISSION_GUIDE.md',
    f'{project_name}/docs/PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md',
    f'{project_name}/docs/PHASE2_EXPERIMENT_LOG.md',
    f'{project_name}/docs/PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md',
    f'{project_name}/docs/PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md',
    f'{project_name}/docs/PHASE2_BACKWARD_PIVOT_FEASIBILITY_2026-05-15.md',
    f'{project_name}/docs/PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md',
    f'{project_name}/docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md',
    f'{project_name}/docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md',
    f'{project_name}/docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md',
    f'{project_name}/docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md',
    f'{project_name}/docs/SUBMISSION_SPEC.md',
    f'{project_name}/docs/SUBMISSION_SDD.md',
    f'{project_name}/docs/PARTIAL_SUBMISSION_BRIEF.md',
    f'{project_name}/docs/TA_CLARIFICATION_DRAFT.md',
}

with ZipFile(out, 'w', ZIP_DEFLATED) as archive:
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in excluded_dirs for part in rel.parts):
            continue
        if path.name in excluded_names or path.suffix in excluded_suffixes:
            continue
        arcname = Path(project_name) / rel
        if path.is_dir():
            continue
        archive.write(path, arcname.as_posix())

with ZipFile(out, 'r') as archive:
    names = set(archive.namelist())
    missing = sorted(required - names)
    forbidden = [
        name for name in names
        if '/mock_shared/' in name or '/dist/' in name or '__pycache__/' in name
    ]
    if missing:
        raise SystemExit('missing required package entries: ' + ', '.join(missing))
    if forbidden:
        raise SystemExit('forbidden generated entries in package: ' + ', '.join(sorted(forbidden)[:10]))

print(f'submission_package={out}')
print(f'size_bytes={out.stat().st_size}')
print(f'top_level={project_name}/')
PY
