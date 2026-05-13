import importlib
import json


def _reload_modules(monkeypatch, tmp_path):
    monkeypatch.setenv("PROJECT2_SHARED_DIR", str(tmp_path))
    import src.path_config as path_config
    import src.readiness_report as readiness_report

    importlib.reload(path_config)
    importlib.reload(readiness_report)
    return path_config, readiness_report


def test_readiness_report_summarizes_protocol_state(monkeypatch, tmp_path):
    path_config, readiness_report = _reload_modules(monkeypatch, tmp_path)
    path_config.SHARED_DIR.mkdir(parents=True, exist_ok=True)
    path_config.COREDUMP_DIR.mkdir(parents=True, exist_ok=True)
    path_config.CONFIG_PATH.write_text("MOCK_CONFIG\n", encoding="utf-8")
    path_config.BLOGIC_FALLBACK_PATH.write_text("MOCK_BLOGIC\n", encoding="utf-8")
    path_config.STATE_PATH.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "project": "project2",
                "phase": "II",
                "round": 1,
                "last_exploit": {"strategy_id": "baseline-observation"},
                "last_triage": {"analysis_status": "no-evidence"},
                "next_action": {"strategy_id": "length-sweep-placeholder"},
                "safety": {"external_network": False, "lab_only": True},
            }
        ),
        encoding="utf-8",
    )
    path_config.ROUND_LOG_PATH.write_text('{"event":"x"}\n', encoding="utf-8")

    report = readiness_report.build_report(run_static=False)

    assert report["protocol_checks"]["state_json_parseable"] is True
    assert report["protocol_checks"]["round_log_events"] == 1
    assert report["protocol_checks"]["blogic_path"].endswith("blogic")
    assert report["latest_state_summary"]["phase"] == "II"
    assert report["blogic_metadata"]["file_kind"] == "non-elf"
    assert "exploit" in report["wrappers"]
