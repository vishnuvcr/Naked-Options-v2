import importlib.util
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT = Path(__file__).with_name("run_research.py")
spec = importlib.util.spec_from_file_location("qe_nob", SCRIPT)
qe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qe)


def test_cache_filename_parser_loads_fresh_option_rows(tmp_path, monkeypatch):
    opt_cache = tmp_path / "options"
    idx_cache = tmp_path / "underlying"
    opt_cache.mkdir()
    idx_cache.mkdir()
    monkeypatch.setattr(qe, "OPT_CACHE", opt_cache)
    monkeypatch.setattr(qe, "IDX_CACHE", idx_cache)

    # Two 5-minute bars on 2025-12-30, timestamped in Asia/Kolkata.
    ts = pd.Timestamp("2025-12-30 09:15", tz="Asia/Kolkata").timestamp()
    timestamps = [int(ts), int(ts + 300)]
    underlying = {
        "timestamp": timestamps, "open": [25000, 25010], "high": [25015, 25025],
        "low": [24995, 25005], "close": [25010, 25020], "volume": [1000, 1100]
    }
    (idx_cache / "nifty_5m_20251230_20251231.json").write_text(json.dumps(underlying))

    side = {
        "timestamp": timestamps, "open": [100, 105], "high": [110, 112],
        "low": [95, 101], "close": [105, 108], "iv": [15, 15],
        "volume": [100, 120], "oi": [1000, 1100], "strike": [25000, 25000],
        "spot": [25010, 25020]
    }
    payload = {"data": {"ce": side, "pe": None}}
    (opt_cache / "week1_20251201_20251231_+0_call.json").write_text(json.dumps(payload))

    u, o = qe.load_frames()
    assert len(u) == 2
    assert len(o) == 2
    assert set(o["side"]) == {"CALL"}
    assert set(o["expiry_flag"]) == {"WEEK1"}
    assert set(o["strike"].astype(int)) == {25000}


def test_rolling_offset_is_part_of_duplicate_identity(tmp_path, monkeypatch):
    opt_cache = tmp_path / "options"
    idx_cache = tmp_path / "underlying"
    opt_cache.mkdir()
    idx_cache.mkdir()
    monkeypatch.setattr(qe, "OPT_CACHE", opt_cache)
    monkeypatch.setattr(qe, "IDX_CACHE", idx_cache)

    ts = int(pd.Timestamp("2025-12-30 09:15", tz="Asia/Kolkata").timestamp())
    underlying = {
        "timestamp": [ts], "open": [25000], "high": [25010],
        "low": [24990], "close": [25005], "volume": [1000]
    }
    (idx_cache / "nifty_5m_20251230_20251231.json").write_text(json.dumps(underlying))

    for offset, price in [(0, 100), (1, 125)]:
        side = {
            "timestamp": [ts], "open": [price], "high": [price + 5],
            "low": [price - 5], "close": [price + 2], "iv": [15],
            "volume": [100], "oi": [1000], "strike": [25000], "spot": [25005]
        }
        payload = {"data": {"ce": side, "pe": None}}
        (opt_cache / f"week1_20251201_20251231_{offset:+d}_call.json").write_text(json.dumps(payload))

    _, options, quality = qe.load_frames(return_quality=True)
    assert len(options) == 2
    assert set(options["offset"]) == {0, 1}
    assert quality["duplicate_groups"] == 0
    assert quality["conflicting_duplicate_groups"] == 0


def test_dated_nifty_lot_size_proxy_uses_expiry_family():
    # NSE circulars: 50 before the Apr-2024 transition, then distinct
    # weekly/monthly transition expiries for 25 -> 75 and 75 -> 65.
    assert qe.lot_size_proxy("2022-06-01", "WEEK1") == 50
    assert qe.lot_size_proxy("2024-04-25", "MONTH1") == 50
    assert qe.lot_size_proxy("2024-04-26", "WEEK1") == 25
    assert qe.lot_size_proxy("2024-12-19", "WEEK1") == 25
    assert qe.lot_size_proxy("2024-12-20", "WEEK1") == 75
    assert qe.lot_size_proxy("2025-01-30", "MONTH1") == 25
    assert qe.lot_size_proxy("2025-01-31", "MONTH1") == 75
    assert qe.lot_size_proxy("2025-12-23", "WEEK1") == 75
    assert qe.lot_size_proxy("2025-12-24", "WEEK1") == 65
    assert qe.lot_size_proxy("2025-12-30", "MONTH1") == 75
    assert qe.lot_size_proxy("2025-12-31", "MONTH1") == 65


def test_costs_are_positive_and_adverse_slippage_reduces_pnl():
    legs = [{"entry": 100.0, "exit": 120.0}]
    no_slip = qe.cost_and_pnl(legs, "2026-10-20", 0, 10)
    adverse = qe.cost_and_pnl(legs, "2026-10-20", 100, 10)
    assert no_slip["total_cost_rupees"] > 0
    assert no_slip["net_pnl_rupees"] < no_slip["gross_pnl_rupees"]
    assert adverse["net_pnl_rupees"] < no_slip["net_pnl_rupees"]
    assert adverse["stt_rate"] == 0.0015


def test_costs_use_date_effective_stt_rates():
    assert qe.cost_and_pnl([{"entry":10,"exit":11}], "2024-09-30", 0, 10)["stt_rate"] == 0.000625
    assert qe.cost_and_pnl([{"entry":10,"exit":11}], "2024-10-01", 0, 10)["stt_rate"] == 0.001
    assert qe.cost_and_pnl([{"entry":10,"exit":11}], "2026-04-01", 0, 10)["stt_rate"] == 0.0015


def test_request_chunks_are_contiguous_and_bounded():
    spans = list(qe.chunks(date(2026,1,1), date(2026,4,20), 30))
    assert spans[0][0] == date(2026,1,1)
    assert spans[-1][1] == date(2026,4,20)
    assert all((end-start).days <= 30 for start,end in spans)
    assert all(spans[i][1] == spans[i+1][0] for i in range(len(spans)-1))


def test_candidate_catalogue_is_bounded_and_repeatable():
    first = qe.candidates_for(["WEEK"])
    second = qe.candidates_for(["WEEK"])
    assert first == second
    assert 0 < len(first) <= 600
    keys = [json.dumps(x, sort_keys=True) for x in first]
    assert len(keys) == len(set(keys))


def test_holm_adjustment_monotone_in_sorted_p_values():
    adjusted = np.asarray(qe.adjust_holm([0.001, 0.02, 0.01, 0.5]))
    assert np.all((adjusted >= 0) & (adjusted <= 1))
    order = np.argsort([0.001, 0.02, 0.01, 0.5])
    sorted_adjusted = adjusted[order]
    assert np.all(np.diff(sorted_adjusted) >= -1e-12)

def test_exchange_fee_schedule_is_date_effective():
    assert qe.exchange_rate("2022-06-01") == 0.000535
    assert qe.exchange_rate("2023-07-01") == 0.000505
    assert qe.exchange_rate("2024-07-01") == 0.000500
    assert qe.exchange_rate("2025-01-01") == 0.0003553

def test_genome_key_is_deterministic_and_order_independent():
    a = {"family":"orb", "hold":3, "expiry":"WEEK1", "buffer":0.1}
    b = {"buffer":0.1, "expiry":"WEEK1", "hold":3, "family":"orb"}
    assert qe.genome_key(a) == qe.genome_key(b)


def test_random_genome_outputs_only_supported_grammar():
    rng = np.random.default_rng(20261022)
    allowed = {"orb","trend","gap_cont","gap_fade","pullback","orb_straddle","orb_strangle"}
    for _ in range(100):
        c = qe.random_genome(rng, ["WEEK1","MONTH1"])
        assert c["family"] in allowed
        assert c["expiry"] in {"WEEK1","MONTH1"}
        assert c["hold"] in {1,3,6,12,24}
        if "fast" in c:
            assert c["fast"] < c["slow"]


def test_repricing_cost_stress_is_monotone_on_flat_premium():
    raw_buy = 100 * 65
    raw_sell = 100 * 65
    zero = qe.reprice_premium_turnovers(raw_buy, raw_sell, "2026-10-20", 0, 10, 1)
    stress = qe.reprice_premium_turnovers(raw_buy, raw_sell, "2026-10-20", 100, 20, 1)
    assert zero["net_pnl_rupees"] < 0
    assert stress["net_pnl_rupees"] < zero["net_pnl_rupees"]


def test_oos_gate_requires_baseline_and_two_period_consistency():
    source = SCRIPT.read_text()
    assert "oos_baseline_holm_p" in source
    assert "oos_part1_mean_daily_net_rupees" in source
    assert "oos_part2_mean_daily_net_rupees" in source
    assert "execution_data_gate_reason" in source


def test_v2_acquisition_offsets_and_timeout_budget_are_bounded():
    assert qe.OPTION_OFFSETS == (-1, 0, 1)
    assert qe.OPTION_REQUEST_TIMEOUT_SECONDS == 40
    assert qe.OPTION_REQUEST_ATTEMPTS == 4
    assert qe.MAX_CONSECUTIVE_OPTION_FAILURES == 10


def test_option_acquisition_stops_after_consecutive_failures_and_preserves_cache(tmp_path, monkeypatch):
    opt_cache = tmp_path / "options"
    opt_cache.mkdir()
    monkeypatch.setattr(qe, "OPT_CACHE", opt_cache)
    monkeypatch.setattr(qe.time, "sleep", lambda _: None)
    monkeypatch.setattr(qe, "chunks", lambda start, end, days: iter([(start, min(start + qe.timedelta(days=30), end)), (min(start + qe.timedelta(days=30), end), min(start + qe.timedelta(days=60), end))]))
    calls = {"n": 0}

    def failing_api(*args, **kwargs):
        calls["n"] += 1
        raise RuntimeError("simulated temporary source failure")

    monkeypatch.setattr(qe, "api_post", failing_api)
    result = qe.retrieve_options("not-a-real-token", [{"flag": "WEEK", "code": 1}])
    assert result["status"] == "BLOCKED_NO_OPTION_DATA"
    assert result["consecutive_failures"] == qe.MAX_CONSECUTIVE_OPTION_FAILURES
    assert calls["n"] == qe.MAX_CONSECUTIVE_OPTION_FAILURES * qe.OPTION_REQUEST_ATTEMPTS
    assert not list(opt_cache.glob("*.json"))


def test_acquisition_ready_requires_complete_option_and_underlying():
    assert qe.acquisition_ready({"status": "PASS"}, {"status": "PASS"})
    assert not qe.acquisition_ready({"status": "PARTIAL"}, {"status": "PASS"})
    assert not qe.acquisition_ready({"status": "PARTIAL_NO_PROGRESS"}, {"status": "PASS"})
    assert not qe.acquisition_ready({"status": "PASS"}, {"status": "PARTIAL"})
    assert not qe.acquisition_ready({"status": "PASS"}, {"status": "BLOCKED_NO_UNDERLYING"})


def test_empty_option_payloads_do_not_pass_source_coverage_gate(tmp_path, monkeypatch):
    opt_cache = tmp_path / "options"
    opt_cache.mkdir()
    monkeypatch.setattr(qe, "OPT_CACHE", opt_cache)
    monkeypatch.setattr(qe.time, "sleep", lambda _: None)
    monkeypatch.setattr(qe, "chunks", lambda start, end, days: iter([(start, min(start + qe.timedelta(days=30), end))]))

    empty_side = {key: [] for key in ("timestamp", "open", "high", "low", "close", "strike", "spot")}
    def empty_api(*args, **kwargs):
        return {"data": {"ce": dict(empty_side), "pe": dict(empty_side)}}

    monkeypatch.setattr(qe, "api_post", empty_api)
    result = qe.retrieve_options("not-a-real-token", [{"flag": "WEEK", "code": 1}])
    assert result["status"] == "PARTIAL"
    assert result["requests_recorded"] == result["requests_expected"] == 6
    assert result["nonempty_response_count"] == 0
    assert result["data_response_fraction"] == 0.0
    assert not list(opt_cache.glob("*.json"))


def test_option_request_progress_counts_each_pair_once(tmp_path, monkeypatch):
    opt_cache = tmp_path / "options"
    opt_cache.mkdir()
    monkeypatch.setattr(qe, "ROOT", tmp_path)
    monkeypatch.setattr(qe, "OPT_CACHE", opt_cache)
    monkeypatch.setattr(qe.time, "sleep", lambda _: None)
    monkeypatch.setattr(qe, "chunks", lambda start, end, days: iter([(qe.date(2026, 1, 1), qe.date(2026, 1, 31))]))

    side = {
        "timestamp": [1767258900], "open": [100], "high": [105],
        "low": [95], "close": [102], "strike": [25000], "spot": [25005]
    }
    payload = {"data": {"ce": dict(side), "pe": dict(side)}}
    cached = opt_cache / "week1_20260101_20260131_+0_call.json"
    cached.write_text(json.dumps(payload))
    calls = {"n": 0}

    def valid_api(*args, **kwargs):
        calls["n"] += 1
        return payload

    monkeypatch.setattr(qe, "api_post", valid_api)
    result = qe.retrieve_options("not-a-real-token", [{"flag": "WEEK", "code": 1}])
    assert result["status"] == "PASS"
    assert result["requests_processed"] == result["requests_expected"] == 6
    assert result["requests_recorded"] == 6
    assert result["cached_files_reused"] == 1
    assert result["downloaded_files"] == 5
    assert calls["n"] == 5


def test_active_expiry_families_are_weekly_code_one_only():
    source_families = [
        {"flag": "WEEK", "code": 1},
        {"flag": "WEEK", "code": 2},
        {"flag": "MONTH", "code": 1},
        {"flag": "week", "code": 1},
    ]
    assert qe.active_expiry_families(source_families) == [
        {"flag": "WEEK", "code": 1},
        {"flag": "week", "code": 1},
    ]
    assert qe.active_expiry_families([{"flag": "MONTH", "code": 1}]) == []


def test_weekly_option_cache_window_requires_all_six_files_per_chunk(tmp_path, monkeypatch):
    opt_cache = tmp_path / "options"
    opt_cache.mkdir()
    monkeypatch.setattr(qe, "ROOT", tmp_path)
    monkeypatch.setattr(qe, "OPT_CACHE", opt_cache)
    start, end = date(2025, 12, 1), date(2025, 12, 31)
    side = {"timestamp": [int(pd.Timestamp("2025-12-30 09:15", tz="Asia/Kolkata").timestamp())],
            "open": [100], "high": [105], "low": [95], "close": [102], "strike": [25000], "spot": [25005]}
    payload = {"data": {"ce": dict(side), "pe": dict(side)}}
    for offset in qe.OPTION_OFFSETS:
        for option_side in ("CALL", "PUT"):
            name = f"week1_{start:%Y%m%d}_{end:%Y%m%d}_{offset:+d}_{option_side.lower()}.json"
            (opt_cache / name).write_text(json.dumps(payload))
    audit = qe.audit_weekly_option_window(start, end)
    assert audit["status"] == "PASS"
    assert audit["expected_file_count"] == audit["valid_nonempty_file_count"] == 6
    (opt_cache / "week1_20251201_20251231_+1_put.json").unlink()
    audit = qe.audit_weekly_option_window(start, end)
    assert audit["status"] == "DATA_LIMITED"
    assert audit["missing_file_count"] == 1


def test_qe_nob_v3_hypothesis_plan_has_six_families_and_fresh_data_gate():
    plan = Path(__file__).with_name("STRATEGY_HYPOTHESIS_LAB_V3.md").read_text()
    for heading in (
        "### H1 — Failed opening-range breakout and reclaim",
        "### H2 — Trend pullback and reclaim",
        "### H3 — Volatility compression then expansion",
        "### H4 — Opening-gap fade conditioned on regime",
        "### H5 — Time-of-day conditional signal",
        "### H6 — Option premium breakeven filter",
    ):
        assert heading in plan
    assert "Do not substitute the old OOS period." in plan
    assert "0/25/50/100/200 bps" in plan
    assert "execution-data gates" in plan


def test_qe_nob_v3_plan_keeps_empirical_testing_blocked_until_data_gate():
    plan = Path(__file__).with_name("STRATEGY_HYPOTHESIS_LAB_V3.md").read_text()
    status = Path(__file__).with_name("PHASE_STATUS_V3.md").read_text()
    assert "Empirical testing: NOT STARTED" in plan
    assert "Fresh data feasibility | BLOCKED / NOT RUN" in status
    assert "These are hypotheses, not recommendations or claims of profitability." in plan
