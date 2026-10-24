#!/usr/bin/env python3
"""Evaluate a small predeclared set of NIFTY daily direction rules on the benchmark holdout."""
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
    # The source date is a date-only string; parse it without timezone shifting.
    d["date"] = pd.to_datetime(d[date_col], errors="coerce").dt.date
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
    d["vol_20"] = r.rolling(20).std()
    d["vol_60"] = r.rolling(60).std()
    # Match the baseline benchmark's 60-session feature warm-up and 75/25 chronological split.
    d = d.dropna(subset=["target_return", "target", "prev_direction", "mom_3", "mom_5",
                         "rev_1", "rev_3", "trend_20", "vol_20", "vol_60"]).reset_index(drop=True)
    split = max(750, int(len(d) * .75))
    if split >= len(d) - 100:
        split = len(d) - max(100, int(len(d) * .25))
    if split >= len(d) - 50:
        raise ValueError(f"Insufficient observations for chronological holdout: {len(d)}")
    train, test = d.iloc[:split].copy(), d.iloc[split:].copy()
    # Fixed training-only cutoff prevents test-period volatility values from changing the rule threshold.
    vol_threshold = float(train["vol_20"].quantile(.70))
    test["regime_momentum"] = np.where(
        test["vol_20"] > vol_threshold, test["rev_1"], test["mom_5"]
    )
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
    next_returns = test["target_return"].to_numpy(dtype=float)
    results = []
    for name, pred in rules.items():
        # Transparent daily long/short index-return proxy. Not an executable instrument backtest.
        position = np.where(pred == 1, 1.0, -1.0)
        gross_daily_return = position * next_returns
        results.append({
            "rule": name, "n": int(len(y)),
            "accuracy": float(accuracy_score(y, pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
            "gross_long_short_mean_daily_return": float(np.mean(gross_daily_return)),
            "gross_long_short_compounded_return": float(np.prod(1 + gross_daily_return) - 1),
            "positive_gross_days_pct": float(np.mean(gross_daily_return > 0)),
            "mean_absolute_daily_index_return": float(np.mean(np.abs(next_returns))),
            "confusion_matrix_labels_down_up": [
                [int(np.sum((y == 0) & (pred == 0))), int(np.sum((y == 0) & (pred == 1)))],
                [int(np.sum((y == 1) & (pred == 0))), int(np.sum((y == 1) & (pred == 1)))]
            ],
            "costs_included": False,
            "note": "Index-direction proxy only; not a tradable instrument or net profitability estimate."
        })
    result = {
        "status": "COMPUTED",
        "source": str(DATA.relative_to(ROOT)),
        "rows": int(len(d)),
        "first_test_date": str(test["date"].iloc[0]),
        "last_test_date": str(test["date"].iloc[-1]),
        "n": int(len(test)),
        "split_rule": "chronological 75/25 after 60-session warm-up; same test date range as baseline benchmark",
        "volatility_threshold": vol_threshold,
        "volatility_threshold_method": "70th percentile of training-period 20-session rolling volatility; fixed before holdout scoring",
        "rules": results,
        "limitations": [
            "Third-party daily index data, not exchange-certified.",
            "Rules were predeclared and not tuned to maximize holdout metrics.",
            "Gross long/short index proxy excludes futures/options basis, leverage, turnover, brokerage, taxes, slippage and execution.",
            "The holdout is now used for candidate screening; a promising candidate needs a new untouched forward period before a strategy claim."
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
