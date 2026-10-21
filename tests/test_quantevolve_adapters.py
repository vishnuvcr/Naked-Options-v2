import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from tools.quantevolve.strategy_dsl import (
    SpecValidationError,
    build_causal_features,
    evaluate_spec,
    parse_spec_text,
    validate_daily_frame,
)
from tools.quantevolve.options_contract_gate import inspect_options


VALID = """STRATEGY_SPEC = {
    'version': 1, 'track': 'prediction', 'model': 'linear',
    'features': ['ret_1'], 'weights': {'ret_1': 0.25},
    'intercept': 0.0, 'clip': 0.02
}"""


def daily_fixture(n=900):
    rng = np.random.default_rng(44)
    returns = rng.normal(0.0003, 0.01, n)
    close = 22000 * np.exp(np.cumsum(returns))
    open_ = close * (1 + rng.normal(0, .002, n))
    high = np.maximum(open_, close) * 1.004
    low = np.minimum(open_, close) * .996
    dates = pd.bdate_range("2020-01-01", periods=n)
    return pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"), "open": open_, "high": high,
        "low": low, "close": close, "volume": np.arange(n) + 1,
        "source_id": "synthetic_test_fixture",
    })


def test_spec_uses_literal_ast_only():
    spec = parse_spec_text(VALID)
    assert spec["track"] == "prediction"
    unsafe = [
        "import os\nSTRATEGY_SPEC = {'version':1}",
        "STRATEGY_SPEC = get_spec()",
        "STRATEGY_SPEC = {'version': 1}\nprint('bad')",
        "STRATEGY_SPEC = {'version':1,'track':'prediction','model':'linear','features':['__import__'],'weights':{'__import__':1},'intercept':0,'clip':.02}",
    ]
    for source in unsafe:
        with pytest.raises(SpecValidationError):
            parse_spec_text(source)


def test_spec_bounds_and_feature_limits():
    with pytest.raises(SpecValidationError):
        parse_spec_text(VALID.replace("'ret_1': 0.25", "'ret_1': 4.0"))
    too_many = """STRATEGY_SPEC = {
      'version':1,'track':'prediction','model':'linear',
      'features':['ret_1','ret_5','ret_10','ret_20','vol_5','vol_20','vol_60'],
      'weights':{'ret_1':0,'ret_5':0,'ret_10':0,'ret_20':0,'vol_5':0,'vol_20':0,'vol_60':0},
      'intercept':0,'clip':0.02
    }"""
    with pytest.raises(SpecValidationError):
        parse_spec_text(too_many)


def test_feature_rows_are_causal_under_future_mutation():
    original = validate_daily_frame(daily_fixture())
    changed = original.copy()
    changed.loc[700:, ["open", "high", "low", "close"]] *= 1.2
    f1 = build_causal_features(original)
    f2 = build_causal_features(changed)
    pd.testing.assert_frame_equal(f1.iloc[:700], f2.iloc[:700])


def test_holdout_does_not_influence_development_fitness():
    frame = validate_daily_frame(daily_fixture())
    spec = parse_spec_text(VALID)
    dev1 = evaluate_spec(frame, spec, "development")["metrics"]
    altered = frame.copy()
    altered.loc[int(len(frame)*0.8):, ["open", "high", "low", "close"]] *= 1.7
    dev2 = evaluate_spec(validate_daily_frame(altered), spec, "development")["metrics"]
    assert dev1["combined_score"] == pytest.approx(dev2["combined_score"])
    assert dev1["sample_count"] == dev2["sample_count"]


def test_holdout_metrics_have_block_interval_and_no_selection_flag():
    frame = validate_daily_frame(daily_fixture())
    metrics = evaluate_spec(frame, parse_spec_text(VALID), "holdout")["metrics"]
    assert metrics["evaluation_stage"] == "holdout"
    assert metrics["sample_count"] >= 50
    assert metrics["final_holdout_used_for_candidate_selection"] == 0.0
    assert np.isfinite(metrics["mae_improvement_ci95_low"])
    assert np.isfinite(metrics["mae_improvement_ci95_high"])


def test_options_gate_blocks_missing_source_and_disallows_pnl():
    report = inspect_options(
        Path("file_missing_nifty_options.csv"),
        Path("file_missing_manifest.json"),
        Path("file_missing_underlying.csv"),
    )
    assert report["status"] == "BLOCKED_NO_VERIFIED_CONTRACT_DATA"
    assert report["pnl_permitted"] is False


def test_options_gate_accepts_test_fixture_only_when_all_gates_are_explicit(tmp_path):
    dates = pd.bdate_range("2025-01-01", periods=50)
    rows = []
    for i, stamp in enumerate(dates):
        for option_type in ("CE", "PE"):
            rows.append({
                "timestamp": stamp.strftime("%Y-%m-%d") + "T10:00:00+05:30",
                "expiry": (stamp + pd.Timedelta(days=20)).strftime("%Y-%m-%d"),
                "strike": 23000, "option_type": option_type, "open": 100+i,
                "high": 103+i, "low": 98+i, "close": 101+i, "volume": 1000, "lot_size": 25,
            })
    input_path = tmp_path / "options.csv"
    pd.DataFrame(rows).to_csv(input_path, index=False)
    underlying_path = tmp_path / "underlying.csv"
    pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "close": 23000}).to_csv(underlying_path, index=False)
    digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    manifest_path = tmp_path / "source_manifest.json"
    manifest_path.write_text(json.dumps({
        "status": "PASS", "source_sha256": digest, "official_expiry_reconciled": True,
        "lot_size_history_verified": True, "license_review_status": "PASS_NONCOMMERCIAL",
        "timestamp_timezone": "Asia/Kolkata", "executable_price_policy": "OHLC_ADVERSE_PROXY",
        "source_license": "CC-BY-NC-4.0",
    }))
    report = inspect_options(input_path, manifest_path, underlying_path)
    assert report["status"] == "PASS"
    assert report["pnl_permitted"] is True
    assert report["eligible_date_coverage"] == pytest.approx(1.0)


def test_zero_forecast_has_undefined_direction_accuracy_not_fake_accuracy():
    zero_spec_text = VALID.replace("'ret_1': 0.25", "'ret_1': 0.0")
    frame = validate_daily_frame(daily_fixture())
    metrics = evaluate_spec(frame, parse_spec_text(zero_spec_text), "holdout")["metrics"]
    assert metrics["directional_accuracy"] is None
    assert metrics["directional_accuracy_defined"] is False
    assert metrics["directional_prediction_count"] == 0.0
    assert metrics["directional_prediction_coverage"] == 0.0


def test_gemini_telemetry_records_counters_only_and_runner_requires_success():
    provider = Path("tools/quantevolve/modern_gemini_provider.py").read_text()
    runner = Path("tools/quantevolve/run_prediction.py").read_text()
    assert "requests_attempted" in provider
    assert "requests_succeeded" in provider
    assert "requests_failed" in provider
    assert "QE_LLM_AUDIT_PATH" in provider
    assert '_record_llm_event("success"' in provider
    assert '_record_llm_event("failure"' in provider
    assert "str(exc)" not in provider
    audit_helper = provider[provider.index("def _record_llm_event"):provider.index("class GeminiLLM")]
    assert '"prompt":' not in audit_helper
    assert '"response":' not in audit_helper
    assert '"api_key":' not in audit_helper
    assert "EVOLUTION_NO_SUCCESSFUL_LLM_RESPONSES" in runner
    assert "QE_LLM_AUDIT_PATH" in runner


def test_gemini_telemetry_json_persists_cumulative_counters(tmp_path, monkeypatch):
    import ast
    import os
    import threading
    from typing import Optional

    provider_path = Path("tools/quantevolve/modern_gemini_provider.py")
    tree = ast.parse(provider_path.read_text(encoding="utf-8"))
    function = next(node for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == "_record_llm_event")
    namespace = {
        "os": os, "json": json, "threading": threading, "Path": Path,
        "Optional": Optional, "_AUDIT_LOCK": threading.Lock(),
    }
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(provider_path), "exec"), namespace)

    audit_path = tmp_path / "audit.json"
    monkeypatch.setenv("QE_LLM_AUDIT_PATH", str(audit_path))
    namespace["_record_llm_event"]("attempt", "test-model")
    namespace["_record_llm_event"]("success", "test-model")
    namespace["_record_llm_event"]("failure", "test-model", "TimeoutError")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    assert audit["requests_attempted"] == 1
    assert audit["requests_succeeded"] == 1
    assert audit["requests_failed"] == 1
    assert audit["failure_types"] == {"TimeoutError": 1}


def test_options_source_audit_sample_selection_is_bounded_and_deterministic():
    import ast
    from datetime import date
    import inspect

    source_path = Path("tools/quantevolve/options_source_audit.py")
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    wanted = {"expiry_from_path", "select_sample_files"}
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
    namespace = {"date": date, "Path": Path}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(source_path), "exec"), namespace)
    paths = [
        "options/NIFTY/2021-05-27.parquet",
        "options/NIFTY/2023-12-28.parquet",
        "options/NIFTY/2024-01-04.parquet",
        "options/NIFTY/2025-06-26.parquet",
        "options/NIFTY/2026-08-04.parquet",
    ]
    selected = namespace["select_sample_files"](paths, limit=99)
    assert len(selected) == 3
    assert selected[0] == paths[0]
    assert selected[-1] == paths[-1]
    assert namespace["select_sample_files"](paths, limit=3) == selected
    source = source_path.read_text(encoding="utf-8")
    assert "import pandas as pd" in source
    assert '"pnl_permitted": False' in source
    assert 'official_expiry_reconciled": False' in source
    assert 'lot_size_history_verified": False' in source


def test_official_nifty_sample_lot_mapping_is_expiry_specific_and_cited():
    import ast

    source_path = Path("tools/quantevolve/options_source_audit.py")
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    node = next(
        item for item in tree.body
        if isinstance(item, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "OFFICIAL_SAMPLE_MAP" for target in item.targets)
    )
    mapping = ast.literal_eval(node.value)
    assert mapping["2021-05-27"]["lot_size"] == 75
    assert mapping["2024-01-04"]["lot_size"] == 50
    assert mapping["2026-08-04"]["lot_size"] == 65
    assert mapping["2021-05-27"]["expected_expiry_weekday"] == "Thursday"
    assert mapping["2024-01-04"]["expected_expiry_weekday"] == "Thursday"
    assert mapping["2026-08-04"]["expected_expiry_weekday"] == "Tuesday"
    for cohort in mapping.values():
        assert cohort["circulars"]
        assert all(url.startswith("https://nsearchives.nseindia.com/content/circulars/") for url in cohort["circulars"])


def test_dhan_options_probe_sanitizes_rows_and_never_opens_pnl_gate():
    import ast
    from datetime import datetime
    from zoneinfo import ZoneInfo

    source_path = Path("tools/quantevolve/dhan_options_api_audit.py")
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "inspect_response")
    namespace = {
        "datetime": datetime,
        "ZoneInfo": ZoneInfo,
        "API_URL": "https://api.dhan.co/v2/charts/rollingoption",
        "NIFTY_SECURITY_ID": 13,
    }
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(source_path), "exec"), namespace)

    sample_payload = {"data": {"ce": {
        "timestamp": [1785753000, 1785753060],
        "open": [100.0, 101.0], "high": [102.0, 103.0], "low": [99.0, 100.0],
        "close": [101.0, 102.0], "volume": [50, 60], "iv": [12.0, 13.0],
        "strike": [25000, 25000], "oi": [300, 310], "spot": [24980, 24990],
    }, "pe": None}}
    report = namespace["inspect_response"](sample_payload, 200)
    assert report["status"] == "PASS_SAMPLE_DATA_RETRIEVED_IDENTITY_GATE_STILL_BLOCKED"
    assert report["rows"] == 2
    assert report["explicit_expiry_metadata_present"] is False
    assert report["pnl_permitted"] is False
    assert "close" not in report
    assert "data" not in report
    assert '"access-token": token' in source
    assert "DHAN_ACCESS_TOKEN" in source
    assert "response.text" not in source
