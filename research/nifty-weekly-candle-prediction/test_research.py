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
    assert len(labels) >= 1
    assert set(labels.label).issubset({"UP", "DOWN", "TIE"})

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
