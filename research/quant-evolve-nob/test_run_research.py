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

    # Two 5-minute bars on 2026-10-21, timestamped in Asia/Kolkata.
    ts = pd.Timestamp("2026-10-21 09:15", tz="Asia/Kolkata").timestamp()
    timestamps = [int(ts), int(ts + 300)]
    underlying = {
        "timestamp": timestamps, "open": [25000, 25010], "high": [25015, 25025],
        "low": [24995, 25005], "close": [25010, 25020], "volume": [1000, 1100]
    }
    (idx_cache / "nifty_5m_20261021_20261022.json").write_text(json.dumps(underlying))

    side = {
        "timestamp": timestamps, "open": [100, 105], "high": [110, 112],
        "low": [95, 101], "close": [105, 108], "iv": [15, 15],
        "volume": [100, 120], "oi": [1000, 1100], "strike": [25000, 25000],
        "spot": [25010, 25020]
    }
    payload = {"data": {"ce": side, "pe": None}}
    (opt_cache / "week1_20261021_20261022_+0_call.json").write_text(json.dumps(payload))

    u, o = qe.load_frames()
    assert len(u) == 2
    assert len(o) == 2
    assert set(o["side"]) == {"CALL"}
    assert set(o["expiry_flag"]) == {"WEEK1"}
    assert set(o["strike"].astype(int)) == {25000}


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
