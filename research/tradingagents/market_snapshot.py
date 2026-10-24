"""Frozen, market-only OHLCV snapshot validation for causal replay.

The caller must provide bars already archived from a documented source. This
module does not download data or invoke TradingAgents tools.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from forecast_contract import _parse_timestamp


def validate_market_snapshot(
    bars: list[dict[str, Any]], cutoff_time: str, expected_instrument: str = "NIFTY 50"
) -> list[dict[str, Any]]:
    """Validate ordered OHLCV bars and return a copy, rejecting future bars."""
    cutoff = _parse_timestamp(cutoff_time, "cutoff_time")
    if not isinstance(bars, list) or not bars:
        raise ValueError("bars must be a non-empty list")
    required = {"instrument", "timestamp", "open", "high", "low", "close", "volume"}
    result: list[dict[str, Any]] = []
    previous: datetime | None = None
    for index, bar in enumerate(bars):
        if not isinstance(bar, dict):
            raise ValueError(f"bar {index} must be an object")
        if set(bar) != required:
            raise ValueError(f"bar {index} must contain exactly: {', '.join(sorted(required))}")
        if bar["instrument"] != expected_instrument:
            raise ValueError(f"bar {index} instrument mismatch")
        ts = _parse_timestamp(bar["timestamp"], f"bar {index} timestamp")
        if ts > cutoff:
            raise ValueError(f"bar {index} timestamp is later than cutoff")
        if previous is not None and ts <= previous:
            raise ValueError(f"bar {index} timestamps must be strictly increasing")
        previous = ts
        prices = []
        for field in ("open", "high", "low", "close"):
            value = bar[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"bar {index} {field} must be numeric")
            if value <= 0:
                raise ValueError(f"bar {index} {field} must be positive")
            prices.append(float(value))
        open_, high, low, close = prices
        if high < max(open_, close, low) or low > min(open_, close, high):
            raise ValueError(f"bar {index} has inconsistent OHLC values")
        volume = bar["volume"]
        if isinstance(volume, bool) or not isinstance(volume, (int, float)) or volume < 0:
            raise ValueError(f"bar {index} volume must be non-negative numeric")
        result.append(dict(bar))
    return result
