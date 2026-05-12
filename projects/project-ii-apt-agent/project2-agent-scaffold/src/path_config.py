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
EXPLOIT_DONE_PATH = SHARED_DIR / "exploit_done"
COREDUMP_DIR = SHARED_DIR / "coredump"
STATE_PATH = SHARED_DIR / "triage_state.json"
ROUND_LOG_PATH = SHARED_DIR / "round_log.jsonl"
AGENT_LOG_PATH = SHARED_DIR / "project2_agent.log"

