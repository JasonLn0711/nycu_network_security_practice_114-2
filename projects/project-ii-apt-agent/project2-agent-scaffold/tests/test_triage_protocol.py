import importlib
import json
import time


def _reload_modules(monkeypatch, tmp_path):
    monkeypatch.setenv("PROJECT2_SHARED_DIR", str(tmp_path))
    import src.path_config as path_config
    import src.logger as logger
    import src.state_manager as state_manager
    import src.environment_checker as environment_checker
    import src.safety_guard as safety_guard
    import src.coredump_scanner as coredump_scanner
    import src.triage_runner as triage_runner

    for module in [
        path_config,
        logger,
        state_manager,
        environment_checker,
        safety_guard,
        coredump_scanner,
        triage_runner,
    ]:
        importlib.reload(module)
    return path_config, triage_runner


def test_triage_no_coredump(monkeypatch, tmp_path):
    path_config, triage_runner = _reload_modules(monkeypatch, tmp_path)
    path_config.SHARED_DIR.mkdir(parents=True, exist_ok=True)
    path_config.COREDUMP_DIR.mkdir(parents=True, exist_ok=True)

    result = triage_runner.main()

    assert result == 0
    state = json.loads(path_config.STATE_PATH.read_text(encoding="utf-8"))
    assert state["last_triage"]["coredump_found"] is False
    assert state["last_triage"]["analysis_status"] == "no-evidence"
    assert state["next_action"]["strategy_id"] == "length-sweep-placeholder"
    assert path_config.ROUND_LOG_PATH.exists()


def test_triage_with_coredump(monkeypatch, tmp_path):
    path_config, triage_runner = _reload_modules(monkeypatch, tmp_path)
    path_config.SHARED_DIR.mkdir(parents=True, exist_ok=True)
    path_config.COREDUMP_DIR.mkdir(parents=True, exist_ok=True)
    older = path_config.COREDUMP_DIR / "core.old.txt"
    newer = path_config.COREDUMP_DIR / "core.new.txt"
    older.write_text("OLDER MOCK CORE\n", encoding="utf-8")
    time.sleep(0.01)
    newer.write_text("NEWER MOCK CORE\n", encoding="utf-8")

    result = triage_runner.main()

    assert result == 0
    state = json.loads(path_config.STATE_PATH.read_text(encoding="utf-8"))
    assert state["last_triage"]["coredump_found"] is True
    assert state["last_triage"]["selected_coredump"].endswith("core.new.txt")
    assert state["next_action"]["strategy_id"] in {
        "boundary-search-placeholder",
        "stability-check-placeholder",
    }

