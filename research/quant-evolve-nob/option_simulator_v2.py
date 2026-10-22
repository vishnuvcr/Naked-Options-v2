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
    """Simulate long-option candidates using rolling OHLC proxies; never passes execution gate."""
    _required_columns(underlying, {"timestamp", "open", "close"}, "underlying")
    _required_columns(options, {"timestamp", "expiry_flag", "side", "offset", "strike", "open"}, "options")
    _required_columns(features, {"timestamp"}, "features")
    if slippage_bps < 0 or brokerage_per_order < 0:
        raise ValueError("cost assumptions must be non-negative")

    supported_exits = {"time_exit", "premium_risk_stop", "premium_target"}
    unsupported = sorted({rule.kind for rule in strategy.exits} - supported_exits)
    if unsupported:
        raise ValueError(f"simulator does not implement exit rule(s): {unsupported}")
    has_stops = any(rule.kind in {"premium_risk_stop", "premium_target"} for rule in strategy.exits)
    if has_stops:
        _required_columns(options, {"high", "low"}, "options for premium stops/targets")

    u = underlying.copy()
    if u["timestamp"].isna().any() or u["timestamp"].duplicated().any():
        raise ValueError("underlying timestamps must be non-null and unique")
    u = u.sort_values("timestamp").reset_index(drop=True)
    u["timestamp"] = pd.to_numeric(u["timestamp"], errors="coerce")
    if u["timestamp"].isna().any():
        raise ValueError("underlying timestamp must be numeric epoch seconds")
    u["timestamp"] = u["timestamp"].astype("int64")
    u["open"] = pd.to_numeric(u["open"], errors="coerce")
    if u["open"].isna().any() or (u["open"] <= 0).any():
        raise ValueError("underlying open prices must be positive and non-null")

    o = options.copy()
    o["timestamp"] = pd.to_numeric(o["timestamp"], errors="coerce")
    o["offset"] = pd.to_numeric(o["offset"], errors="coerce")
    o["strike"] = pd.to_numeric(o["strike"], errors="coerce")
    for col in ("open", "high", "low", "close"):
        if col in o.columns:
            o[col] = pd.to_numeric(o[col], errors="coerce")
    # Invalid keys are excluded, never coerced to a made-up offset or timestamp.
    o = o.dropna(subset=["timestamp", "expiry_flag", "side", "offset", "strike", "open"]).copy()
    if o.empty:
        raise ValueError("options contains no rows with valid timestamp/contract fields")
    if (o["offset"] % 1 != 0).any():
        raise ValueError("option offset must be an integer")
    o["timestamp"] = o["timestamp"].astype("int64")
    o["offset"] = o["offset"].astype("int64")
    o["side"] = o["side"].astype(str).str.upper()
    o["expiry_flag"] = o["expiry_flag"].astype(str)
    key = ["expiry_flag", "side", "offset", "timestamp"]
    compared_cols = ["strike", "open"] + [c for c in ("high", "low", "close") if c in o.columns]
    bad_keys = set()
    dup = o[o.duplicated(key, keep=False)]
    for values, group in dup.groupby(key, dropna=False):
        if any(group[col].nunique(dropna=True) > 1 for col in compared_cols):
            bad_keys.add(tuple(values if isinstance(values, tuple) else (values,)))
    if bad_keys:
        o = o[~o[key].apply(tuple, axis=1).isin(bad_keys)]
    o = o.drop_duplicates(key, keep="first")
    o = o[(o["open"] > 0) & (o["strike"] > 0)].copy()
    o["strike_key"] = o["strike"].round(2)

    signals = evaluate_signals(features, strategy, available_features)
    idx = {int(ts): i for i, ts in enumerate(u["timestamp"])}
    # Pre-index once. The former per-entry DataFrame filtering made large discovery runs
    # unnecessarily quadratic in candidates x option rows.
    entry_lookup = {}
    contract_lookup = {}
    price_cols = ["open"] + [col for col in ("high", "low", "close") if col in o.columns]
    for row in o.itertuples(index=False):
        family = str(row.expiry_flag)
        side = str(row.side).upper()
        ts = int(row.timestamp)
        strike_key = round(float(row.strike), 2)
        vals = {col: getattr(row, col) for col in price_cols}
        entry_lookup[(family, side, int(row.offset), ts)] = (strike_key, float(row.open))
        contract_lookup[(family, side, ts, strike_key)] = vals

    offset_for = {"ATM": 0, "OTM1": 1, "OTM2": 2}
    trades = []
    missing_entries = 0
    missing_exits = 0
    last_exit_idx = -1
    for signal in signals.itertuples(index=False):
        entry_ts = int(signal.entry_timestamp)
        if entry_ts not in idx:
            missing_entries += 1
            continue
        entry_idx = idx[entry_ts]
        if entry_idx <= last_exit_idx:
            continue
        time_exit_idx = entry_idx + int(strategy.hold_bars)
        if time_exit_idx >= len(u):
            missing_exits += 1
            continue
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
        family = strategy.expiry
        for side, off in sides:
            entry_data = entry_lookup.get((family, side, off, entry_ts))
            if entry_data is None:
                failed = True
                break
            strike, entry = entry_data
            legs.append({"side": side, "offset": off, "strike": strike, "entry_open": entry,
                         "contract_key": (family, side, strike)})
        if failed or not legs:
            missing_entries += 1
            continue
        if strategy.instrument == "STRADDLE" and len(legs) == 2 and legs[0]["strike"] != legs[1]["strike"]:
            missing_entries += 1
            continue

        entry_premium = sum(leg["entry_open"] for leg in legs)
        stop_rules = [r for r in strategy.exits if r.kind == "premium_risk_stop"]
        target_rules = [r for r in strategy.exits if r.kind == "premium_target"]
        # Multiple rules of the same kind use the strictest threshold; stop has priority
        # over target on a bar where both could have occurred.
        stop_level = entry_premium * (1 - min(float(r.value) for r in stop_rules)) if stop_rules else None
        target_level = entry_premium * (1 + min(float(r.value) for r in target_rules)) if target_rules else None
        if stop_level is not None and stop_level < 0:
            raise ValueError("premium_risk_stop must be <= 1.0")
        if any(leg["entry_open"] <= 0 for leg in legs):
            missing_entries += 1
            continue

        exit_idx = time_exit_idx
        exit_ts = int(u["timestamp"].iloc[exit_idx])
        exit_price_by_leg = None
        exit_reason = "time_exit"
        path_failed = False
        # Entry occurs at bar open; inspect that bar and later completed bars before
        # the scheduled time-exit open. If stop and target both touch, assume stop first.
        if has_stops:
            for bar_idx in range(entry_idx, time_exit_idx):
                bar_ts = int(u["timestamp"].iloc[bar_idx])
                marks = []
                for leg in legs:
                    contract = contract_lookup.get((family, leg["side"], bar_ts, leg["strike"]))
                    if contract is None or any(
                        col not in contract or pd.isna(contract[col])
                        for col in ("open", "high", "low")
                    ):
                        path_failed = True
                        break
                    marks.append({col: float(contract[col]) for col in ("open", "high", "low")})
                if path_failed:
                    break
                basket_open = sum(x["open"] for x in marks)
                basket_high = sum(x["high"] for x in marks)
                basket_low = sum(x["low"] for x in marks)
                # Premium-stop threshold is an intrabar mark proxy; a gap below the
                # threshold exits at the worse bar open. Otherwise fill at threshold.
                if stop_level is not None and (basket_open <= stop_level or basket_low <= stop_level):
                    fill = basket_open if basket_open <= stop_level else stop_level
                    exit_idx, exit_ts, exit_reason = bar_idx, bar_ts, "premium_risk_stop"
                    basis = basket_open if basket_open > 0 else sum(x["open"] for x in marks)
                    exit_price_by_leg = [float(x["open"]) * (fill / basis) for x in marks]
                    break
                if target_level is not None and (basket_open >= target_level or basket_high >= target_level):
                    fill = basket_open if basket_open >= target_level else target_level
                    exit_idx, exit_ts, exit_reason = bar_idx, bar_ts, "premium_target"
                    basis = basket_open if basket_open > 0 else sum(x["open"] for x in marks)
                    exit_price_by_leg = [float(x["open"]) * (fill / basis) for x in marks]
                    break
        if path_failed:
            # Unknown intratrade path means neither stops nor overlap safety can be inferred.
            missing_exits += 1
            last_exit_idx = time_exit_idx
            continue
        if exit_price_by_leg is None:
            # Time exit is explicitly filled at the scheduled bar open.
            exit_contracts = []
            for leg in legs:
                contract = contract_lookup.get((family, leg["side"], exit_ts, leg["strike"]))
                if contract is None or pd.isna(contract.get("open")):
                    failed = True
                    break
                exit_contracts.append(float(contract["open"]))
            if failed:
                missing_exits += 1
                continue
            exit_price_by_leg = exit_contracts

        raw_buy = sum(x["entry_open"] for x in legs) * lot
        raw_sell = sum(exit_price_by_leg) * lot
        costs = reprice(raw_buy, raw_sell, local_day, slippage_bps, brokerage_per_order, len(legs))
        last_exit_idx = exit_idx
        trades.append({
            "signal_timestamp": int(signal.timestamp), "entry_timestamp": entry_ts,
            "exit_timestamp": exit_ts, "entry_date_ist": local_day.isoformat(),
            "instrument": strategy.instrument, "expiry_family": strategy.expiry,
            "moneyness": strategy.moneyness, "hold_bars": int(strategy.hold_bars),
            "exit_reason": exit_reason, "lot_size_proxy": lot,
            "legs": [{"side": leg["side"], "offset": leg["offset"], "strike": leg["strike"],
                      "entry_open": leg["entry_open"], "exit_open": exit_px}
                     for leg, exit_px in zip(legs, exit_price_by_leg)],
            **costs
        })

    daily = {}
    for trade in trades:
        day_key = trade["entry_date_ist"]
        daily[day_key] = daily.get(day_key, 0.0) + trade["net_pnl_rupees"]
    values = sorted(daily.values())
    n_days = len(values)
    median_daily = None
    if n_days:
        middle = n_days // 2
        median_daily = values[middle] if n_days % 2 else (values[middle - 1] + values[middle]) / 2
    return {
        "status": "SIMULATED_OHLC_PROXY",
        "trade_count": len(trades),
        "missing_entry_count": missing_entries,
        "missing_exit_count": missing_exits,
        "mean_net_per_trade_rupees": sum(t["net_pnl_rupees"] for t in trades) / len(trades) if trades else None,
        "total_net_pnl_rupees": sum(t["net_pnl_rupees"] for t in trades),
        "mean_traded_day_net_rupees": sum(values) / len(values) if values else None,
        "median_traded_day_net_rupees": median_daily,
        "slippage_bps_per_side": slippage_bps,
        "brokerage_per_order_rupees": brokerage_per_order,
        "execution_gate_pass": False,
        "execution_gate_reason": "Rolling OHLC proxy does not verify exact exchange contract identity, historical bid/ask/depth or actual broker fills.",
        "limitations": [
            "OHLC open is a proxy, not an executable quote.",
            "Premium stops/targets use conservative bar-level range checks; an intrabar gap, spread or queue is not observed.",
            "If a stop/target path has missing contract OHLC, that trade is rejected and entries remain blocked until its scheduled time exit.",
            "No overlapping-position policy is enforced across independent candidates.",
            "Rolling expiry family is not an exact expiry identifier; lot size is a date/family proxy.",
        ],
        "trades": trades,
    }
