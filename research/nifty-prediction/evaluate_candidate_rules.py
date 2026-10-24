#!/usr/bin/env python3
"""Evaluate a small predeclared set of NIFTY daily direction rules on the same holdout."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/cache/nifty-prediction/nifty50_daily.csv"
OUT = ROOT / "reports/nifty-prediction/candidate_rules.json"

def main():
    d = pd.read_csv(DATA)
    d.columns = [str(c).strip().lower().replace(" ", "_") for c in d.columns]
    date_col = next(c for c in d.columns if c in ("date", "datetime", "timestamp"))
    d["date"] = pd.to_datetime(d[date_col], errors="coerce", utc=True).dt.tz_convert("Asia/Kolkata").dt.date
    d["close"] = pd.to_numeric(d["close"], errors="coerce")
    d = d.dropna(subset=["date", "close"]).sort_values("date").drop_duplicates("date").reset_index(drop=True)
    r = d["close"].pct_change()
    d["target_return"] = d["close"].shift(-1) / d["close"] - 1
    d["target"] = (d["target_return"] > 0).astype(int)
    d.loc[d["target_return"].isna(), "target"] = np.nan
    d["prev_direction"] = (r > 0).astype(int)
    d["mom_3"] = (d["close"] / d["close"].shift(3) - 1 > 0).astype(int)
    d["mom_5"] = (d["close"] / d["close"].shift(5) - 1 > 0).astype(int)
    d["rev_1"] = (r < 0).astype(int)
    d["rev_3"] = (d["close"] / d["close"].shift(3) - 1 < 0).astype(int)
    d["trend_20"] = (d["close"] > d["close"].rolling(20).mean()).astype(int)
    # Regime uses only information available by session t; thresholds are expanding-history quantiles.
    rv = r.rolling(20).std()
    d["high_vol"] = rv > rv.expanding(min_periods=100).quantile(0.70)
    d["regime_momentum"] = np.where(d["high_vol"], d["rev_1"], d["mom_5"])
    d = d.dropna(subset=["target_return", "target", "prev_direction", "mom_3", "mom_5", "rev_1", "rev_3", "trend_20", "high_vol"]).reset_index(drop=True)
    benchmark_path = ROOT / "reports/nifty-prediction/daily_benchmark.json"
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    first_test_date = pd.to_datetime(benchmark["test_first_date"]).date()
    last_test_date = pd.to_datetime(benchmark["test_last_date"]).date()
    test = d[(d["date"] >= first_test_date) & (d["date"] <= last_test_date)].copy()
    if len(test) != int(benchmark["test_rows"]):
        raise ValueError("Candidate holdout row count does not match benchmark; investigate date/feature alignment.")
    rules = {
        "previous_session_direction_baseline": test["prev_direction"].to_numpy(dtype=int),
        "3_session_momentum": test["mom_3"].to_numpy(dtype=int),
        "5_session_momentum": test["mom_5"].to_numpy(dtype=int),
        "1_session_mean_reversion": test["rev_1"].to_numpy(dtype=int),
        "3_session_mean_reversion": test["rev_3"].to_numpy(dtype=int),
        "20_session_trend_filter": test["trend_20"].to_numpy(dtype=int),
        "volatility_conditioned_momentum_reversal": test["regime_momentum"].to_numpy(dtype=int),
    }
    y = test["target"].astype(int).to_numpy()
    results = []
    for name, pred in rules.items():
        # Map predicted direction to a long/short index proxy; this is gross and not an executable strategy.
        position = np.where(pred == 1, 1.0, -1.0)
        next_return = test["target_return"].to_numpy(dtype=float)
        gross_daily_return = position * next_return
        results.append({
            "rule": name, "n": int(len(y)),
            "accuracy": float(accuracy_score(y, pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
            "gross_long_short_mean_daily_return": float(np.mean(gross_daily_return)),
            "gross_long_short_compounded_return": float(np.prod(1 + gross_daily_return) - 1),
            "positive_gross_days_pct": float(np.mean(gross_daily_return > 0)),
            "mean_absolute_daily_index_return": float(np.mean(np.abs(next_return))),
            "costs_included": False,
            "note": "Index-direction proxy only; not a tradable instrument or net profitability estimate."
        })
    result = {
        "status": "COMPUTED",
        "source": str(DATA.relative_to(ROOT)),
        "first_test_date": str(test["date"].iloc[0]),
        "last_test_date": str(test["date"].iloc[-1]),
        "n": int(len(test)),
        "split_rule": "chronological 75/25; no parameter tuning",
        "rules": results,
        "limitations": [
            "Daily third-party index data, not exchange-certified.",
            "Rules are predeclared simple diagnostics, not optimized strategies.",
            "Gross long/short index proxy ignores futures/options basis, leverage, turnover, brokerage, taxes, slippage, and execution.",
            "The volatility-conditioned rule uses an expanding 70th-percentile threshold and is exploratory; its result is not independent confirmation."
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
