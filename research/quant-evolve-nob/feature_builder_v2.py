"""Point-in-time intraday feature builder for QE-NOB-2.0.

Only NIFTY underlying OHLCV data are used here. Features are computed within each
IST session and use current/past rows only. Unsupported external/option features are
not synthesized; callers must apply the returned availability gate.
"""
from __future__ import annotations
from typing import Any
import numpy as np
import pandas as pd

NUMERIC_FEATURES = {
    "nifty_return_1", "nifty_return_3", "nifty_return_6",
    "opening_gap_pct", "opening_range_position",
    "ema_fast_slow_sign", "vwap_distance_pct",
}
CATEGORICAL_FEATURES = {"opening_range_break", "time_of_day_bucket"}
FEATURE_NAMES = NUMERIC_FEATURES | CATEGORICAL_FEATURES


def build_features(underlying: pd.DataFrame, minimum_coverage: float = 0.80) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Return timestamp-aligned features and explicit coverage/inclusion metadata."""
    if not 0 < minimum_coverage <= 1:
        raise ValueError("minimum_coverage must be in (0, 1]")
    required = {"timestamp", "open", "high", "low", "close"}
    missing = required - set(underlying.columns)
    if missing:
        raise ValueError(f"underlying missing required columns: {sorted(missing)}")
    data = underlying.copy()
    data["timestamp"] = pd.to_numeric(data["timestamp"], errors="coerce")
    if data["timestamp"].isna().any():
        raise ValueError("underlying timestamp contains non-numeric/null values")
    if data["timestamp"].duplicated().any():
        raise ValueError("underlying timestamps must be unique")
    data["timestamp"] = data["timestamp"].astype("int64")
    for col in ("open", "high", "low", "close"):
        data[col] = pd.to_numeric(data[col], errors="coerce")
    if data[list(required - {"timestamp"})].isna().any().any():
        raise ValueError("underlying OHLC contains null/non-numeric values")
    if (data[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("underlying OHLC must be positive")
    if (data["high"] < data[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError("underlying high violates OHLC constraints")
    if (data["low"] > data[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError("underlying low violates OHLC constraints")

    data = data.sort_values("timestamp").reset_index(drop=True)
    data["datetime_ist"] = pd.to_datetime(data["timestamp"], unit="s", utc=True).dt.tz_convert("Asia/Kolkata")
    data["session_date"] = data["datetime_ist"].dt.strftime("%Y-%m-%d")
    time_str = data["datetime_ist"].dt.strftime("%H:%M")
    data["time_of_day_bucket"] = np.select(
        [time_str < "09:45", time_str < "11:00", time_str < "13:00"],
        ["open", "morning", "midday"], default="afternoon"
    )

    group = data.groupby("session_date", sort=False, group_keys=False)
    for lag in (1, 3, 6):
        data[f"nifty_return_{lag}"] = group["close"].transform(lambda x: x.pct_change(lag))

    # Opening gap is computed from the previous observed session close, never from
    # same-day future values. It is replicated within the session after the open.
    session_rows = data.groupby("session_date", sort=False)
    first_open = session_rows["open"].first()
    last_close = session_rows["close"].last()
    prev_close = last_close.shift(1)
    gap = ((first_open - prev_close) / prev_close).replace([np.inf, -np.inf], np.nan)
    data["opening_gap_pct"] = data["session_date"].map(gap.to_dict())

    # Freeze opening range from the first three 5-minute bars. Signal features are
    # withheld until a fourth bar exists, so a bar cannot be compared to a range
    # that includes itself. Sessions with fewer than four rows stay unavailable.
    data["_bar_no"] = data.groupby("session_date", sort=False).cumcount()
    first3 = data[data["_bar_no"] < 3].groupby("session_date").agg(or_high=("high", "max"), or_low=("low", "min"))
    data["or_high"] = data["session_date"].map(first3["or_high"].to_dict())
    data["or_low"] = data["session_date"].map(first3["or_low"].to_dict())
    denom = data["or_high"] - data["or_low"]
    valid_range = (data["_bar_no"] >= 3) & denom.gt(0)
    data["opening_range_position"] = np.where(
        valid_range, (data["close"] - data["or_low"]) / denom, np.nan
    )
    data["opening_range_break"] = np.select(
        [valid_range & data["close"].gt(data["or_high"]),
         valid_range & data["close"].lt(data["or_low"])],
        ["up", "down"], default="inside"
    )
    data.loc[~valid_range, "opening_range_break"] = np.nan

    # Session-reset EMA crossover sign; EWM only uses prices up to the row.
    fast = group["close"].transform(lambda x: x.ewm(span=8, adjust=False, min_periods=8).mean())
    slow = group["close"].transform(lambda x: x.ewm(span=21, adjust=False, min_periods=21).mean())
    data["ema_fast_slow_sign"] = np.sign(fast - slow).where(fast.notna() & slow.notna())

    # VWAP is enabled only when usable volume exists. No volume is fabricated.
    if "volume" in data.columns:
        data["volume"] = pd.to_numeric(data["volume"], errors="coerce")
        valid_vol = data["volume"].notna() & data["volume"].ge(0)
        typical = (data["high"] + data["low"] + data["close"]) / 3
        pv = (typical * data["volume"].where(valid_vol, 0)).groupby(data["session_date"], sort=False).cumsum()
        cumvol = data["volume"].where(valid_vol, 0).groupby(data["session_date"], sort=False).cumsum()
        vwap = pv.div(cumvol.where(cumvol > 0))
        data["vwap_distance_pct"] = (data["close"] - vwap) / vwap
    else:
        data["vwap_distance_pct"] = np.nan

    # Do not expose implementation columns to the model/search layer.
    output = data[["timestamp"] + sorted(FEATURE_NAMES)].copy()
    metadata = {
        "schema_version": "qe-nob-feature-builder-v2.0",
        "timezone": "Asia/Kolkata",
        "row_count": int(len(output)),
        "session_count": int(data["session_date"].nunique()),
        "minimum_coverage": minimum_coverage,
        "feature_coverage": {},
        "feature_inclusion": {},
        "available_features": [],
        "limitations": [
            "Only point-in-time derived features from the supplied NIFTY OHLCV are considered.",
            "Timestamp epoch-unit and bar-label semantics must be confirmed against source documentation.",
            "Opening range uses first three bars and becomes active only from the fourth row in each session.",
            "VWAP is unavailable if usable volume is absent; no volume/feature values are synthesized.",
            "Global markets, India VIX, option IV/OI, FII/DII, event/news and contract-level features are not created here."
        ]
    }
    for feature in sorted(FEATURE_NAMES):
        series = output[feature]
        coverage = float(series.notna().mean()) if len(series) else 0.0
        if feature in CATEGORICAL_FEATURES:
            unique_values = int(series.dropna().nunique())
            varies = unique_values >= 2
        else:
            unique_values = int(series.dropna().nunique())
            varies = unique_values >= 2
        included = coverage >= minimum_coverage and varies
        metadata["feature_coverage"][feature] = coverage
        metadata["feature_inclusion"][feature] = {
            "included": included, "non_null_count": int(series.notna().sum()),
            "unique_non_null_values": unique_values,
            "reason": "coverage and variation gates passed" if included else
                      ("coverage below minimum" if coverage < minimum_coverage else "feature has fewer than two observed values")
        }
        if included:
            metadata["available_features"].append(feature)
    return output, metadata
