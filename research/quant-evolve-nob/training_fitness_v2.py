"""Training-only fitness callback for bounded QE-NOB-2.0 discovery.

This module is not a live trading engine. It splits by IST session date, scores only
the chronological training partition, and leaves final OOS data out of the callback.
All fitness metrics use after-cost OHLC-proxy P&L and cannot pass the execution gate.
"""
from __future__ import annotations
from datetime import date
from typing import Any
import pandas as pd

from option_simulator_v2 import prepare_option_index, simulate_strategy
from strategy_grammar_v2 import Strategy, validate_strategy

FITNESS_OBJECTIVES = {
    "mean_net_per_trade_rupees",
    "mean_daily_net_rupees",
    "median_daily_net_rupees",
    "negative_max_drawdown_rupees",
    "profit_factor_capped",
    "minimum_trade_gate",
}


def _session_dates(frame: pd.DataFrame) -> pd.Series:
    ts = pd.to_numeric(frame["timestamp"], errors="coerce")
    if ts.isna().any():
        raise ValueError("timestamps must be numeric epoch seconds")
    return pd.to_datetime(ts.astype("int64"), unit="s", utc=True).dt.tz_convert("Asia/Kolkata").dt.date


def chronological_training_split(
    underlying: pd.DataFrame,
    options: pd.DataFrame,
    features: pd.DataFrame,
    train_fraction: float = 0.70,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, date]:
    """Return only the earliest train_fraction of sessions and the last train date."""
    if not 0.50 <= train_fraction <= 0.85:
        raise ValueError("train_fraction must be between 0.50 and 0.85")
    for label, frame in (("underlying", underlying), ("options", options), ("features", features)):
        if "timestamp" not in frame.columns:
            raise ValueError(f"{label} requires timestamp")
    if underlying.empty:
        raise ValueError("underlying training split is empty")
    sessions = sorted(set(_session_dates(underlying)))
    if len(sessions) < 3:
        raise ValueError("at least three distinct sessions are required")
    count = max(2, min(len(sessions) - 1, int(len(sessions) * train_fraction)))
    cutoff = sessions[count - 1]
    u_days, o_days, f_days = _session_dates(underlying), _session_dates(options), _session_dates(features)
    u = underlying.loc[u_days <= cutoff].copy().sort_values("timestamp").reset_index(drop=True)
    o = options.loc[o_days <= cutoff].copy().sort_values("timestamp").reset_index(drop=True)
    f = features.loc[f_days <= cutoff].copy().sort_values("timestamp").reset_index(drop=True)
    if u.empty or f.empty:
        raise ValueError("training split has no underlying/features")
    if max(_session_dates(u)) > cutoff or max(_session_dates(f)) > cutoff:
        raise AssertionError("training split includes post-cutoff rows")
    return u, o, f, cutoff


def build_training_fitness_evaluator(
    underlying: pd.DataFrame,
    options: pd.DataFrame,
    features: pd.DataFrame,
    available_features: set[str],
    train_fraction: float = 0.70,
    slippage_bps: float = 50.0,
    brokerage_per_order_rupees: float = 10.0,
    minimum_trades: int = 20,
):
    """Create the callable expected by evolve_candidates_v2.generate()."""
    if minimum_trades < 1:
        raise ValueError("minimum_trades must be positive")
    train_u, train_o, train_f, cutoff = chronological_training_split(
        underlying, options, features, train_fraction
    )
    active = set(available_features) & set(train_f.columns)
    if not active:
        raise ValueError("no runtime-approved feature columns are available in training data")
    if not train_o.empty:
        train_o = train_o.loc[_session_dates(train_o) <= cutoff].copy()
    option_index = prepare_option_index(train_o)
    session_count = len(set(_session_dates(train_u)))
    if session_count < 2:
        raise ValueError("training split needs at least two sessions")

    def score(strategy: Strategy) -> dict[str, Any]:
        validate_strategy(strategy, active)
        result = simulate_strategy(
            train_u, train_o, train_f, strategy, active,
            slippage_bps=slippage_bps,
            brokerage_per_order=brokerage_per_order_rupees,
            prepared_option_index=option_index,
        )
        trades = result["trades"]
        by_day: dict[date, float] = {}
        for trade in trades:
            day = date.fromisoformat(trade["entry_date_ist"])
            by_day[day] = by_day.get(day, 0.0) + float(trade["net_pnl_rupees"])
        daily = [by_day.get(day, 0.0) for day in sorted(set(_session_dates(train_u)))]
        cumulative = 0.0
        peak = 0.0
        max_drawdown = 0.0
        for pnl in daily:
            cumulative += pnl
            peak = max(peak, cumulative)
            max_drawdown = max(max_drawdown, peak - cumulative)
        gross_wins = sum(float(t["net_pnl_rupees"]) for t in trades if float(t["net_pnl_rupees"]) > 0)
        gross_losses = -sum(float(t["net_pnl_rupees"]) for t in trades if float(t["net_pnl_rupees"]) < 0)
        profit_factor = min(10.0, gross_wins / gross_losses) if gross_losses > 0 else (10.0 if gross_wins > 0 else 0.0)
        count = len(trades)
        return {
            "mean_net_per_trade_rupees": sum(float(t["net_pnl_rupees"]) for t in trades) / count if count else -1e6,
            "mean_daily_net_rupees": sum(daily) / len(daily) if daily else -1e6,
            "median_daily_net_rupees": float(pd.Series(daily).median()) if daily else -1e6,
            "negative_max_drawdown_rupees": -max_drawdown,
            "profit_factor_capped": profit_factor,
            "minimum_trade_gate": 1.0 if count >= minimum_trades else -1.0,
            "trade_count_diagnostic": count,
            "total_net_pnl_diagnostic_rupees": sum(float(t["net_pnl_rupees"]) for t in trades),
            "missing_entry_count_diagnostic": int(result["missing_entry_count"]),
            "missing_exit_count_diagnostic": int(result["missing_exit_count"]),
            "training_cutoff_date": cutoff.isoformat(),
            "training_session_count": session_count,
            "execution_gate_pass": False,
            "score_status": "TRAINING_ONLY_OHLC_PROXY",
        }

    score.training_cutoff_date = cutoff.isoformat()
    score.training_session_count = session_count
    score.objective_names = sorted(FITNESS_OBJECTIVES)
    return score
