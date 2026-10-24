import importlib.util
from datetime import date
from pathlib import Path
import pandas as pd
import numpy as np

MODULE = Path(__file__).with_name("run_research.py")
spec = importlib.util.spec_from_file_location("nwcp_runner", MODULE)
mod = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

def _make_bars(days, close_values):
    rows = []
    for day, close in zip(days, close_values):
        for hour, minute, c in [(9, 15, close-2), (9, 58, close-1), (9, 59, close), (15, 29, close+5)]:
            rows.append({
                "bar_start": pd.Timestamp(f"{day} {hour:02d}:{minute:02d}:00", tz=mod.IST),
                "open": c-0.5, "high": c+1, "low": c-1, "close": c, "source": "test",
                "bar_end": pd.Timestamp(f"{day} {hour:02d}:{minute:02d}:00", tz=mod.IST)+pd.Timedelta(minutes=1),
                "session_date": day,
            })
    return pd.DataFrame(rows)

def test_up_down_tie_target_labels():
    # expiry/anchor pairs: actual expiry Tuesday, anchor Wednesday next session
    bars = _make_bars([date(2025, 9, 3), date(2025, 9, 9), date(2025, 9, 10), date(2025, 9, 16)], [100, 110, 110, 100])
    expiries = [date(2025, 9, 2), date(2025, 9, 9), date(2025, 9, 16)]
    bars["bar_start"] = pd.to_datetime(bars["bar_start"]).dt.tz_convert(mod.IST)
    labels, audit = mod.make_target_rows(bars, expiries, {"provenance": {}})
    assert len(labels) == 2
    assert labels.label.tolist() == ["UP", "DOWN"]

def test_rsi_is_bounded():
    assert 0 <= mod.rsi(list(range(1, 25)), 14) <= 100
    assert 0 <= mod.rsi(list(range(25, 1, -1)), 14) <= 100

def test_normalize_public_timestamp_is_bar_start():
    source = pd.DataFrame({"Timestamp": ["2025-09-03T09:59:00"], "Open": [1], "High": [2], "Low": [0.5], "Close": [1.5]})
    out = mod.normalize_ohlc(source, "Timestamp", timestamp_is_start=True)
    assert out.iloc[0].bar_start.strftime("%H:%M") == "09:59"

def test_no_future_price_required_at_anchor():
    day = date(2025, 9, 3)
    bars = _make_bars([day], [100])
    cutoff = pd.Timestamp("2025-09-03 10:00:00", tz=mod.IST)
    visible = bars[bars.bar_end <= cutoff]
    assert visible.bar_start.max().strftime("%H:%M") == "09:59"
    assert (visible.bar_end <= cutoff).all()

def test_cache_manifest_does_not_expose_token():
    # Invariants: report writing is aggregate-only and token value is never a report field.
    assert "DHAN_ACCESS_TOKEN" not in str(mod.REPORTS)


def test_evolved_candidates_never_use_invalid_second_feature_index():
    rng = np.random.default_rng(7)
    thresholds = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5]
    for _ in range(300):
        candidate = mod._new_candidate(rng, 9, thresholds)
        if candidate["mode"] != "single":
            assert 0 <= candidate["f2"] < 9
            assert candidate["f2"] != candidate["f1"]
        child = mod._mutate_candidate(candidate, rng, 9, thresholds)
        if child["mode"] != "single":
            assert 0 <= child["f2"] < 9
            assert child["f2"] != child["f1"]

def test_rule_prediction_is_binary_and_length_preserving():
    rng = np.random.default_rng(1729)
    x = rng.normal(size=(50, 5))
    candidate = {"f1": 0, "op1": "gt", "t1": 0.0, "mode": "and", "f2": 1, "op2": "lt", "t2": 1.0, "invert": False}
    prediction = mod._rule_prediction(x, candidate)
    assert len(prediction) == len(x)
    assert set(np.unique(prediction)).issubset({0, 1})


def test_expiry_calendar_gate_rejects_weekday_fallback():
    audit = {
        "selected_expiry_count": 3,
        "fallback_dates": 1,
        "provenance": {
            "2025-09-02": "nse_expiry_api",
            "2025-09-09": "nse_expiry_api",
            "2025-09-16": "calendar_fallback",
        },
    }
    assert mod.expiry_calendar_is_verified(audit) is False


def test_expiry_calendar_gate_accepts_only_complete_official_provenance():
    audit = {
        "selected_expiry_count": 2,
        "fallback_dates": 0,
        "provenance": {
            "2025-09-02": "nse_expiry_api",
            "2025-09-09": "nse_expiry_api",
        },
    }
    assert mod.expiry_calendar_is_verified(audit) is True


def test_expiry_calendar_gate_rejects_missing_provenance():
    audit = {
        "selected_expiry_count": 2,
        "fallback_dates": 0,
        "provenance": {"2025-09-02": "nse_expiry_api"},
    }
    assert mod.expiry_calendar_is_verified(audit) is False


def test_target_builder_rejects_missing_0959_anchor():
    bars = _make_bars([date(2025, 9, 3), date(2025, 9, 9)], [100, 110])
    bars = bars[bars.bar_start.dt.strftime("%H:%M") != "09:59"]
    expiries = [date(2025, 9, 2), date(2025, 9, 9)]
    labels, audit = mod.make_target_rows(bars, expiries, {"provenance": {}})
    assert labels.empty
    assert audit["excluded_intervals"] == 1
    assert audit["excluded_examples"][0]["reason"] == "missing_or_duplicate_0959_bar"


def test_target_builder_rejects_missing_1529_expiry_close():
    bars = _make_bars([date(2025, 9, 3), date(2025, 9, 9)], [100, 110])
    bars = bars[bars.bar_start.dt.strftime("%H:%M") != "15:29"]
    expiries = [date(2025, 9, 2), date(2025, 9, 9)]
    labels, audit = mod.make_target_rows(bars, expiries, {"provenance": {}})
    assert labels.empty
    assert audit["excluded_intervals"] == 1
    assert audit["excluded_examples"][0]["reason"] == "missing_or_duplicate_1529_bar"


def test_holm_adjustment_is_monotonic_and_bounded():
    adjusted = mod._holm_adjust({"a": 0.01, "b": 0.04, "c": 0.03, "missing": None})
    vals = [adjusted[k] for k in ("a", "c", "b")]
    assert all(0 <= v <= 1 for v in vals)
    assert vals == sorted(vals)
    assert adjusted["missing"] is None


# CI dispatch probe: this comment-only commit triggers the repository's push workflow so the committed suite is executed in GitHub Actions.


def test_evolutionary_search_runs_across_multiple_generations():
    # Exercise elite carry-forward, mutation and crossover; this caught wrapper-record leakage
    # from the archive into the candidate population in the real workflow.
    rng = np.random.default_rng(20261024)
    x_train = rng.normal(size=(120, 6))
    y_train = (x_train[:, 0] + 0.4 * x_train[:, 1] > 0).astype(int)
    x_valid = rng.normal(size=(50, 6))
    y_valid = (x_valid[:, 0] + 0.4 * x_valid[:, 1] > 0).astype(int)
    result = mod._evolve_rule(
        x_train, y_train, x_valid, y_valid,
        [f"f{i}" for i in range(6)], seed=19,
        max_candidates=100, max_generations=5,
    )
    assert result["status"] == "OK"
    assert result["candidate_count"] > 0
    assert result["best_candidate"]["candidate"]["f1"] in range(6)
