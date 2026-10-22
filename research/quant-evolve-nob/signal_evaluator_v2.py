"""Leakage-aware signal evaluator for QE-NOB-2.0 strategy ASTs.

Input is a timestamp-sorted feature DataFrame with one row per completed bar.
This module creates signal timestamps only; it does not simulate option fills or P&L.
The caller must shift execution to the next available bar and provide a verified feature set.
"""
from __future__ import annotations
from typing import Any
import math
import pandas as pd

from strategy_grammar_v2 import Predicate, Strategy, validate_strategy

NUMERIC_FEATURES = {
    "nifty_return_1", "nifty_return_3", "nifty_return_6", "opening_gap_pct",
    "opening_range_position", "ema_fast_slow_sign", "vwap_distance_pct",
    "realized_vol_percentile", "india_vix_percentile", "option_iv_percentile",
    "iv_minus_realized", "option_volume_change", "option_oi_change",
    "implied_move_edge", "global_lead_return",
}
CATEGORICAL_FEATURES = {"opening_range_break", "time_of_day_bucket", "fii_dii_regime"}


def _predicate_mask(frame: pd.DataFrame, predicate: Predicate) -> pd.Series:
    if predicate.feature not in frame.columns:
        raise ValueError(f"feature column absent: {predicate.feature}")
    series = frame[predicate.feature]
    op, value = predicate.operator, predicate.value
    if op in {"gt", "lt", "cross_up", "cross_down"} and predicate.feature in CATEGORICAL_FEATURES:
        raise ValueError(f"numeric operator applied to categorical feature: {predicate.feature}")
    if op == "gt":
        return series.gt(value) & series.notna()
    if op == "lt":
        return series.lt(value) & series.notna()
    if op == "regime_is":
        return series.eq(value) & series.notna()
    if op == "in_bucket":
        if predicate.second_value is None:
            raise ValueError("in_bucket requires second_value")
        return series.ge(value) & series.le(predicate.second_value) & series.notna()
    if op == "cross_up":
        previous = series.shift(1)
        return series.gt(value) & previous.le(value) & series.notna() & previous.notna()
    if op == "cross_down":
        previous = series.shift(1)
        return series.lt(value) & previous.ge(value) & series.notna() & previous.notna()
    raise ValueError(f"unsupported predicate operator: {op}")


def evaluate_signals(frame: pd.DataFrame, strategy: Strategy, available_features: set[str]) -> pd.DataFrame:
    """Return signal rows; signal uses only current/past feature rows, never future rows."""
    validate_strategy(strategy, available_features)
    if "timestamp" not in frame.columns:
        raise ValueError("timestamp column required")
    data = frame.copy()
    if data["timestamp"].isna().any():
        raise ValueError("timestamp contains missing values")
    if data["timestamp"].duplicated().any():
        raise ValueError("timestamp must be unique")
    data = data.sort_values("timestamp").reset_index(drop=True)
    masks = [_predicate_mask(data, p) for p in strategy.predicates]
    if strategy.logic == "and":
        signal = masks[0]
        for mask in masks[1:]:
            signal = signal & mask
    elif strategy.logic == "or":
        signal = masks[0]
        for mask in masks[1:]:
            signal = signal | mask
    else:
        raise ValueError("unsupported logic")
    data["next_bar_timestamp"] = data["timestamp"].shift(-1)
    out = data.loc[signal, ["timestamp", "next_bar_timestamp"]].copy()
    out["candidate_direction" = 1 if strategy.instrument in {"CALL", "STRADDLE", "STRANGLE"} else -1
    out["instrument"] = strategy.instrument
    out["hold_bars"] = int(strategy.hold_bars)
    out = out.rename(columns={"next_bar_timestamp": "entry_timestamp"})
    # Last available market bar has no known next bar and is excluded rather than fabricated.
    out = out[out["entry_timestamp"].notna()].reset_index(drop=True)
    return out
