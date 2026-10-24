"""Small live-data feasibility probe; never used as historical backtest evidence."""
from __future__ import annotations

import json
from datetime import datetime, timezone

import yfinance as yf


def probe(period: str, interval: str) -> dict:
    ticker = yf.Ticker("^NSEI")
    frame = ticker.history(period=period, interval=interval, auto_adjust=False)
    result = {
        "symbol": "^NSEI",
        "period": period,
        "interval": interval,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "index_type": type(frame.index).__name__,
        "timezone": str(getattr(frame.index, "tz", None)),
        "first_timestamp": str(frame.index[0]) if len(frame) else None,
        "last_timestamp": str(frame.index[-1]) if len(frame) else None,
        "has_ohlc": all(c in frame.columns for c in ("Open", "High", "Low", "Close")),
        "close_missing": int(frame["Close"].isna().sum()) if "Close" in frame else None,
    }
    result["usable_shape"] = bool(
        len(frame) and result["has_ohlc"] and result["close_missing"] == 0
    )
    return result


if __name__ == "__main__":
    results = [
        probe("1mo", "1d"),
        probe("5d", "5m"),
    ]
    print(json.dumps(results, indent=2))
    # This probe is diagnostic only: availability now does not establish
    # historical coverage or correct 10:00 IST candle semantics.
    if not all(item["usable_shape"] for item in results):
        raise SystemExit("Yahoo NIFTY probe failed; inspect the JSON output.")
