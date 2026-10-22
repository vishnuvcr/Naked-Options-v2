"""OHLC-based long-option simulator for QE-NOB-2.0.

This simulator is deliberately conservative and research-only. It requires exact
timestamp alignment within the supplied rolling series and same-strike exit rows.
Because Dhan rolling ATM-relative data do not prove stable exchange contract IDs,
results remain indicative and the execution gate is always false absent exact
contract-master and historical quote/fill evidence.
"""
from __future__ import annotations
from datetime import date
import math
import pandas as pd

from signal_evaluator_v2 import evaluate_signals
from strategy_grammar_v2 import Strategy

SEBI_RATE = 0.000001
STAMP_RATE = 0.00003
GST_RATE = 0.18


def dated_lot_size(day: date, expiry: str) -> int:
    if day < date(2024, 4, 26):
        return 50
    if expiry.upper().startswith("WEEK"):
        if day < date(2024, 12, 20): return 25
        if day < date(2025, 12, 24): return 75
        return 65
    if day < date(2025, 1, 31): return 25
    if day < date(2025, 12, 31): return 75
    return 65


def fee_rates(day: date) -> tuple[float, float]:
    stt = 0.000625 if day < date(2024, 10, 1) else (0.001 if day < date(2026, 4, 1) else 0.0015)
    exchange = 0.000535 if day < date(2023, 4, 1) else (
        0.000505 if day < date(2024, 4, 1) else (
            0.000500 if day < date(2024, 10, 1) else 0.0003553))
    return stt, exchange


def reprice(buy_raw: float, sell_raw: float, day: date, slippage_bps: float,
            brokerage_per_order: float, legs: int) -> dict:
    slip = slippage_bps / 10000.0
    buy = buy_raw * (1 + slip)
    sell = max(0.0, sell_raw * (1 - slip))
    stt_rate, exchange_rate = fee_rates(day)
    turnover = buy + sell
    brokerage = brokerage_per_order * 2 * legs
    exchange = turnover * exchange_rate
    sebi = turnover * SEBI_RATE
    stamp = buy * STAMP_RATE
    stt = sell * stt_rate
    gst = GST_RATE * (brokerage + exchange + sebi)
    fees = brokerage + exchange + sebi + stamp + stt + gst
    return {"gross_pnl_rupees": sell - buy, "net_pnl_rupees": sell - buy - fees,
            "total_cost_rupees": fees, "buy_turnover_rupees": buy,
            "sell_turnover_rupees": sell, "brokerage_rupees": brokerage,
            "exchange_fee_rupees": exchange, "sebi_fee_rupees": sebi,
            "stamp_rupees": stamp, "stt_rupees": stt, "gst_rupees": gst,
            "slippage_bps_per_side": slippage_bps,
            "brokerage_per_order": brokerage_per_order,
            "stt_rate_assumption": stt_rate, "exchange_rate_assumption": exchange_rate}


def _required_columns(frame: pd.DataFrame, required: set[str], label: str) -> None:
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{label} missing required columns: {sorted(missing)}")


def simulate_strategy(underlying: pd.DataFrame, options: pd.DataFrame, features: pd.DataFrame,
                      strategy: Strategy, available_features: set[str],
                      slippage_bps: float = 50, brokerage_per_order: float = 10) -> dict:
    """Simulate one-lot long option candidates on exact bar timestamps; no quote inference."""
    _required_columns(underlying, {"timestamp", "open", "close"}, "underlying")
    _required_columns(options, {"timestamp", "expiry_flag", "side", "offset", "strike", "open"}, "options")
    _required_columns(features, {"timestamp"}, "features")
    if slippage_bps < 0 or brokerage_per_order < 0:
        raise ValueError("cost assumptions must be non-negative")
    u = underlying.sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    if u["timestamp"].isna().any() or u["timestamp"].duplicated().any():
        raise ValueError("underlying timestamps must be non-null and unique")
    # If duplicate option keys disagree on strike or open, remove that key rather than choose a row.
    o = options.copy()
    o["strike"] = pd.to_numeric(o["strike"], errors="coerce")
    o["open"] = pd.to_numeric(o["open"], errors="coerce")
    key = ["expiry_flag", "side", "offset", "timestamp"]
    dup = o[o.duplicated(key, keep=False)]
    bad_keys = set()
    for values, group in dup.groupby(key, dropna=False):
        if group["strike"].nunique(dropna=True) > 1 or group["open"].nunique(dropna=True) > 1:
            bad_keys.add(tuple(values if isinstance(values, tuple) else (values,)))
    if bad_keys:
        o = o[~o[key].apply(tuple, axis=1).isin(bad_keys)]
    o = o.drop_duplicates(key, keep="first")
    o = o[(o["open"] > 0) & (o["strike"] > 0)].copy()
    signals = evaluate_signals(features, strategy, available_features)
    idx = {int(ts): i for i, ts in enumerate(u["timestamp"].astype(int))}
    by_contract = {}
    for row in o.itertuples(index=False):
        by_contract[(str(row.expiry_flag), str(row.side).upper(), int(row.timestamp), round(float(row.strike), 2))] = float(row.open)
    offset_for = {"ATM": 0, "OTM1": 1, "OTM2": 2}
    trades = []
    missing_entries = 0
    missing_exits = 0
    for signal in signals.itertuples(index=False):
        entry_ts = int(signal.entry_timestamp)
        if entry_ts not in idx:
            missing_entries += 1
            continue
        entry_idx = idx[entry_ts]
        exit_idx = entry_idx + int(strategy.hold_bars)
        if exit_idx >= len(u):
            missing_exits += 1
            continue
        exit_ts = int(u.timestamp.iloc[exit_idx])
        local_day = pd.to_datetime(entry_ts, unit="s", utc=True).tz_convert("Asia/Kolkata").date()
        lot = dated_lot_size(local_day, strategy.expiry)
        if strategy.instrument == "CALL":
            sides = [("CALL", offset_for[strategy.moneyness])]
        elif strategy.instrument == "PUT":
            sides = [("PUT", -offset_for[strategy.moneyness])]
        elif strategy.instrument == "STRADDLE":
            sides = [("CALL", 0), ("PUT", 0)]
        else:
            off = max(1, offset_for[strategy.moneyness])
            sides = [("CALL", off), ("PUT", -off)]
        legs = []
        failed = False
        for side, off in sides:
            # Data uses family/code labels such as WEEK1 or MONTH1; only rolling family is known.
            family = strategy.expiry
            candidates = [(k, v) for k, v in by_contract.items()
                          if k[0] == family and k[1] == side and k[2] == entry_ts
                          and int(next((r.offset for r in o.itertuples(index=False)
                                        if str(r.expiry_flag) == family and str(r.side).upper() == side
                                        and int(r.timestamp) == entry_ts and int(r.offset) == off), 999)) == off]
            # Use exact requested offset for entry.
            entry_row = o[(o.expiry_flag.astype(str) == family) &
                          (o.side.astype(str).str.upper() == side) &
                          (o.offset.astype(int) == off) & (o.timestamp.astype(int) == entry_ts)]
            if entry_row.empty:
                failed = True; break
            strike = float(entry_row.iloc[0].strike)
            entry = float(entry_row.iloc[0]["open"])
            exit_price = by_contract.get((family, side, exit_ts, round(strike, 2)))
            if exit_price is None or not math.isfinite(entry) or not math.isfinite(exit_price):
                failed = True; break
            legs.append((entry, exit_price, strike, side, off))
        if failed or not legs:
            missing_entries += 1
            continue
        raw_buy = sum(x[0] for x in legs) * lot
        raw_sell = sum(x[1] for x in legs) * lot
        costs = reprice(raw_buy, raw_sell, local_day, slippage_bps, brokerage_per_order, len(legs))
        trades.append({"signal_timestamp": int(signal.timestamp), "entry_timestamp": entry_ts,
                       "exit_timestamp": exit_ts, "entry_date_ist": local_day.isoformat(),
                       "instrument": strategy.instrument, "expiry_family": strategy.expiry,
                       "moneyness": strategy.moneyness, "hold_bars": int(strategy.hold_bars),
                       "lot_size_proxy": lot, "legs": [
                           {"side": x[3], "offset": x[4], "strike": x[2], "entry_open": x[0], "exit_open": x[1]}
                           for x in legs], **costs})
    daily = {}
    for trade in trades:
        daily[trade["entry_date_ist"]] = daily.get(trade["entry_date_ist"], 0.0) + trade["net_pnl_rupees"]
    values = list(daily.values())
    return {
        "status": "SIMULATED_OHLC_PROXY",
        "trade_count": len(trades),
        "missing_entry_count": missing_entries,
        "missing_exit_count": missing_exits,
        "mean_net_per_trade_rupees": sum(t["net_pnl_rupees"] for t in trades) / len(trades) if trades else None,
        "total_net_pnl_rupees": sum(t["net_pnl_rupees"] for t in trades),
        "mean_traded_day_net_rupees": sum(values) / len(values) if values else None,
        "median_traded_day_net_rupees": sorted(values)[len(values)//2] if values else None,
        "slippage_bps_per_side": slippage_bps,
        "brokerage_per_order_rupees": brokerage_per_order,
        "execution_gate_pass": False,
        "execution_gate_reason": "Rolling OHLC proxy does not verify exact exchange contract identity, historical bid/ask/depth or actual broker fills.",
        "limitations": ["OHLC open is a proxy, not an executable quote.", "No overlapping-position policy is enforced across independent candidates.",
                        "Rolling expiry family is not an exact expiry identifier.", "Lot size is a date/family proxy."],
        "trades": trades,
    }
