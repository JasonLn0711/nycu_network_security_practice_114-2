from pathlib import Path

from src import path_config


def test_path_constants_exist():
    assert path_config.SHARED_DIR.name
    assert path_config.CONFIG_PATH.name == "config.data"
    assert path_config.BLOGIC_COPY_PATH.name == "blogic.copy"
    assert path_config.EXPLOIT_DONE_PATH.name == "exploit_done"
    assert path_config.COREDUMP_DIR.name == "coredump"
    assert path_config.STATE_PATH.name == "triage_state.json"
    assert path_config.ROUND_LOG_PATH.name == "round_log.jsonl"


def test_wrappers_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "exploit").is_file()
    assert (root / "triage").is_file()

