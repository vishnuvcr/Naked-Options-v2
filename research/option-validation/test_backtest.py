import importlib.util
from pathlib import Path
import math
import pandas as pd

SCRIPT = Path(__file__).with_name("backtest.py")
spec = importlib.util.spec_from_file_location("option_backtest", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_paytm_order_fee_and_cost_formula_are_positive():
    trade = {
        "entry_prices": [100.0, 110.0],
        "exit_prices": [120.0, 100.0],
        "trade_date": "2026-10-13",
        "lot_size": 75,
        "structure": "straddle",
    }
    out = mod.calculate_trade(trade, slippage_bps=0, brokerage_per_order=10)
    assert out["gross_pnl_points"] == 10.0
    assert out["brokerage_rupees"] == 40.0
    assert out["stt_rate"] == 0.0015
    assert out["net_pnl_rupees"] < out["gross_pnl_rupees"]
    assert out["entry_debit_rupees"] > 0
    assert 0 < out["total_cost_rupees"]


def test_slippage_never_improves_long_option_pnl():
    trade = {
        "entry_prices": [100.0, 90.0],
        "exit_prices": [120.0, 100.0],
        "trade_date": "2025-10-13",
        "lot_size": 25,
        "structure": "straddle",
    }
    no_slip = mod.calculate_trade(trade, slippage_bps=0, brokerage_per_order=10)
    high_slip = mod.calculate_trade(trade, slippage_bps=100, brokerage_per_order=10)
    assert high_slip["net_pnl_rupees"] < no_slip["net_pnl_rupees"]


def test_pre_april_2026_stt_rate():
    trade = {
        "entry_prices": [10.0, 10.0],
        "exit_prices": [11.0, 9.0],
        "trade_date": "2026-03-31",
        "lot_size": 50,
        "structure": "straddle",
    }
    out = mod.calculate_trade(trade, slippage_bps=0, brokerage_per_order=10)
    assert out["stt_rate"] == 0.001


def test_quote_matching_does_not_use_another_strike():
    rows = pd.DataFrame([
        {"date": "2026-10-13", "time": "09:20", "option_type": "CALL",
         "strike": 25000.0, "open": 100.0, "close": 105.0, "spot": 25010.0},
        {"date": "2026-10-13", "time": "15:25", "option_type": "CALL",
         "strike": 25050.0, "open": 80.0, "close": 90.0, "spot": 25040.0},
    ])
    assert mod.match_exit_price(rows, "2026-10-13", "CALL", 25000.0) is None


def test_block_bootstrap_deterministic_and_finite():
    series = [0.01, -0.02, 0.03, -0.01, 0.00, 0.02, -0.015, 0.004] * 8
    a = mod.block_bootstrap_mean(series, block_len=5, n_boot=200, seed=12)
    b = mod.block_bootstrap_mean(series, block_len=5, n_boot=200, seed=12)
    assert a == b
    assert all(math.isfinite(v) for v in a)
    assert a[0] <= a[1]


def test_holm_preserves_order_and_bounds():
    p = [0.01, 0.04, 0.03, float("nan")]
    adjusted = mod.holm_adjust(p)
    assert len(adjusted) == 4
    assert adjusted[0] >= p[0]
    assert all(0 <= x <= 1 for x in adjusted[:3])
    assert math.isnan(adjusted[3])


def test_nifty_lot_size_proxy_includes_december_2025_revision():
    assert mod.lot_size_proxy("2024-04-25") == 50
    assert mod.lot_size_proxy("2024-04-26") == 25
    assert mod.lot_size_proxy("2024-11-20") == 75
    assert mod.lot_size_proxy("2025-12-30") == 75
    assert mod.lot_size_proxy("2025-12-31") == 65
    assert mod.lot_size_proxy("2026-10-13") == 65


def test_safe_response_detail_redacts_access_token_and_jwt():
    class FakeResponse:
        text = ""
        def json(self):
            return {
                "debug": "access-token=secret-token eyJabcdefghijklmno.abcdefghijk.abcdefghijk"
            }
    detail = mod.safe_response_detail(FakeResponse(), secret="secret-token")
    assert "BAD_REQUEST" in detail
    assert "bad schema" in detail
    assert "secret-token" not in detail
    assert "eyJabcdefghijklmno" not in detail


def test_exit_price_lookup_uses_exact_date_time_type_and_strike():
    lookup = {
        ("2026-10-13", "15:25", "CALL", 25000.0): 105.0,
        ("2026-10-13", "15:25", "CALL", 25050.0): 90.0,
    }
    assert mod.match_exit_price(lookup, "2026-10-13", "CALL", 25000.0) == 105.0
    assert mod.match_exit_price(lookup, "2026-10-13", "CALL", 25025.0) is None
    assert mod.match_exit_price(lookup, "2026-10-14", "CALL", 25000.0) is None


def test_primary_daily_pnl_uses_zero_for_non_alert_days():
    rows = [
        {
            "net_return_on_debit": -0.10, "net_pnl_rupees": -100.0, "did_trade": True,
            "entry_debit_points": 200.0, "total_cost_rupees": 20.0,
        },
        {
            "net_return_on_debit": 0.0, "net_pnl_rupees": 0.0, "did_trade": False,
            "entry_debit_points": 0.0, "total_cost_rupees": 0.0,
        },
    ]
    metrics = mod.metrics_from_daily(rows, block_len=1)
    assert metrics["mean_net_pnl_rupees_daily"] == -50.0
    assert metrics["mean_net_pnl_rupees_per_trade"] == -100.0
    assert metrics["total_net_pnl_rupees"] == -100.0


def test_fixed_strike_trade_candidate_uses_indexed_exit_rows():
    day = "2026-10-13"
    rows = [
        {"date": day, "time": "09:20", "option_type": "CALL", "strike": 25000.0, "open": 100.0, "close": 100.0, "spot": 25010.0},
        {"date": day, "time": "09:20", "option_type": "PUT", "strike": 25000.0, "open": 105.0, "close": 105.0, "spot": 25010.0},
        {"date": day, "time": "09:20", "option_type": "CALL", "strike": 25050.0, "open": 80.0, "close": 80.0, "spot": 25010.0},
        {"date": day, "time": "09:20", "option_type": "PUT", "strike": 24950.0, "open": 80.0, "close": 80.0, "spot": 25010.0},
        {"date": day, "time": "15:25", "option_type": "CALL", "strike": 25000.0, "open": 118.0, "close": 120.0, "spot": 25020.0},
        {"date": day, "time": "15:25", "option_type": "PUT", "strike": 25000.0, "open": 82.0, "close": 80.0, "spot": 25020.0},
        {"date": day, "time": "15:25", "option_type": "CALL", "strike": 25050.0, "open": 94.0, "close": 95.0, "spot": 25020.0},
        {"date": day, "time": "15:25", "option_type": "PUT", "strike": 24950.0, "open": 48.0, "close": 50.0, "spot": 25020.0},
    ]
    frame = pd.DataFrame(rows)
    exit_lookup = {
        (day, "15:25", row["option_type"], row["strike"]): row["close"]
        for row in rows if row["time"] == "15:25"
    }
    quote_days = {day: frame}
    straddle, reason = mod.build_trade_candidate(frame, day, "straddle", quote_days, exit_lookup)
    assert reason == "PASS"
    assert straddle["entry_prices"] == [100.0, 105.0]
    assert straddle["exit_prices"] == [120.0, 80.0]
    strangle, reason = mod.build_trade_candidate(frame, day, "strangle", quote_days, exit_lookup)
    assert reason == "PASS"
    assert strangle["entry_prices"] == [80.0, 80.0]
    assert strangle["exit_prices"] == [95.0, 50.0]
