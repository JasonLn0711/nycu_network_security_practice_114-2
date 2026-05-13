"""Central path configuration for the Project II scaffold.

The real course grader mounts the shared volume at /shared. For classroom
demonstrations and tests, set PROJECT2_SHARED_DIR to a local directory such as
./mock_shared.
"""

from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SHARED_DIR = Path(os.environ.get("PROJECT2_SHARED_DIR", "/shared")).expanduser()
if not SHARED_DIR.is_absolute():
    SHARED_DIR = (Path.cwd() / SHARED_DIR).resolve()
else:
    SHARED_DIR = SHARED_DIR.resolve()

CONFIG_PATH = SHARED_DIR / "config.data"
BLOGIC_COPY_PATH = SHARED_DIR / "blogic.copy"
# The brief names /shared/blogic.copy, while the provided lab/docker.sh also
# places the observable binary at /shared/blogic. Support both to keep the EC
# protocol robust across instructor harness variants.
BLOGIC_FALLBACK_PATH = SHARED_DIR / "blogic"
BLOGIC_CANDIDATE_PATHS = (BLOGIC_COPY_PATH, BLOGIC_FALLBACK_PATH)
EXPLOIT_DONE_PATH = SHARED_DIR / "exploit_done"
COREDUMP_DIR = SHARED_DIR / "coredump"
STATE_PATH = SHARED_DIR / "triage_state.json"
ROUND_LOG_PATH = SHARED_DIR / "round_log.jsonl"
AGENT_LOG_PATH = SHARED_DIR / "project2_agent.log"



def resolve_blogic_path():
    """Return the first available shared blogic artifact path.

    Prefer /shared/blogic.copy from the project brief, but accept /shared/blogic
    from the supplied lab script. If neither exists, return the preferred path
    so callers can produce a stable error message.
    """

    for candidate in BLOGIC_CANDIDATE_PATHS:
        if candidate.exists():
            return candidate
    return BLOGIC_COPY_PATH
