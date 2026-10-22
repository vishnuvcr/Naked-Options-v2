import importlib.util
from datetime import date
from pathlib import Path

import pandas as pd

SCRIPT = Path(__file__).with_name("acquire_public_underlying.py")
SPEC = importlib.util.spec_from_file_location("public_underlying_fallback", SCRIPT)
FALLBACK = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(FALLBACK)


def minute_frame(start="2025-12-30 09:15", count=5):
    times = pd.date_range(start, periods=count, freq="min", tz="Asia/Kolkata")
    return pd.DataFrame({
        "timestamp": [int(t.timestamp()) for t in times],
        "datetime_ist": times,
        "session_date": [t.strftime("%Y-%m-%d") for t in times],
        "open": [100.0 + i for i in range(count)],
        "high": [102.0 + i for i in range(count)],
        "low": [99.0 + i for i in range(count)],
        "close": [101.0 + i for i in range(count)],
    })


def test_resample_aggregates_only_complete_five_minute_bar():
    bars = FALLBACK.resample_one_minute_to_five(minute_frame())
    assert len(bars) == 1
    row = bars.iloc[0]
    assert row["timestamp"] == int(pd.Timestamp("2025-12-30 09:15", tz="Asia/Kolkata").timestamp())
    assert row["open"] == 100.0
    assert row["high"] == 106.0
    assert row["low"] == 99.0
    assert row["close"] == 105.0


def test_resample_drops_incomplete_bins_instead_of_filling_them():
    bars = FALLBACK.resample_one_minute_to_five(minute_frame(count=4))
    assert bars.empty


def test_resample_drops_a_bin_with_a_missing_minute():
    frame = minute_frame(count=5).drop(index=2).reset_index(drop=True)
    bars = FALLBACK.resample_one_minute_to_five(frame)
    assert bars.empty


def test_study_window_is_explicit_and_bounded():
    assert FALLBACK.START_DATE == date(2021, 10, 23)
    assert FALLBACK.END_DATE_EXCLUSIVE == date(2025, 12, 31)
    assert FALLBACK.SOURCE_COMMIT == "a8d738ff6b248c4636464cbd9d82e7bcb7f902a8"
