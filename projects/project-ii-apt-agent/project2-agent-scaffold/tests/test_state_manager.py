import importlib
import json


def _reload_path(monkeypatch, tmp_path):
    monkeypatch.setenv("PROJECT2_SHARED_DIR", str(tmp_path))
    import src.path_config as path_config
    import src.state_manager as state_manager

    importlib.reload(path_config)
    importlib.reload(state_manager)
    return path_config, state_manager


def test_default_state_valid():
    from src.state_manager import default_state

    state = default_state()
    assert state["schema_version"] == "1.0"
    assert state["project"] == "project2"
    assert state["phase"] == "II"
    assert state["next_action"]["strategy_id"] == "baseline-observation"
    assert state["next_action"]["parameters"]["candidate_length"] == 16
    assert state["search_state"]["strategy_family"] == "safe-placeholder-feedback-loop"
    assert state["safety"]["lab_only"] is True
    assert state["safety"]["external_network"] is False


def test_save_load_state(monkeypatch, tmp_path):
    path_config, state_manager = _reload_path(monkeypatch, tmp_path)
    tmp_path.mkdir(exist_ok=True)
    state = state_manager.default_state()
    state["round"] = 4

    state_manager.save_state(state)
    loaded = state_manager.load_state()

    assert path_config.STATE_PATH.exists()
    assert loaded["round"] == 4
    json.loads(path_config.STATE_PATH.read_text(encoding="utf-8"))
