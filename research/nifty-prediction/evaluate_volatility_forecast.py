#!/usr/bin/env python3
"""Compare one-step GARCH variance forecasts with simple variance baselines."""
import json
from pathlib import Path
import warnings
import numpy as np
import pandas as pd
from arch import arch_model

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/cache/nifty-prediction/nifty50_daily.csv"
OUT = ROOT / "reports/nifty-prediction/volatility_forecast.json"


def qlike(actual_sq, forecast_var):
    v = np.maximum(np.asarray(forecast_var, dtype=float), 1e-12)
    y = np.maximum(np.asarray(actual_sq, dtype=float), 1e-12)
    return float(np.mean(np.log(v) + y / v))


def main():
    d = pd.read_csv(DATA)
    d.columns = [str(c).strip().lower().replace(" ", "_") for c in d.columns]
    d["date"] = pd.to_datetime(d["date"], errors="coerce")
    d["close"] = pd.to_numeric(d["close"], errors="coerce")
    d = d.dropna(subset=["date", "close"]).sort_values("date").drop_duplicates("date").reset_index(drop=True)
    all_returns = d["close"].pct_change().to_numpy()
    valid_start = 61
    returns = all_returns[valid_start:]
    dates = d["date"].iloc[valid_start:].reset_index(drop=True)
    split = int(len(returns) * .75)
    actual, garch_var, rolling_var, expanding_var, test_dates = [], [], [], [], []
    params = None
    h_prev_pct2 = None
    refit_every = 20
    min_train = 500
    first_i = max(split, min_train)
    for i in range(first_i, len(returns)):
        if params is None or (i - first_i) % refit_every == 0:
            train = returns[:i]
            train = train[np.isfinite(train)]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fitted = arch_model(train * 100, mean="Zero", vol="GARCH", p=1, q=1, rescale=False).fit(
                    disp="off", show_warning=False, options={"maxiter": 500}
                )
            params = fitted.params
            omega = float(params["omega"])
            alpha = float(params["alpha[1]"])
            beta = float(params["beta[1]"])
            h_prev_pct2 = float(fitted.conditional_volatility[-1] ** 2)
        # Update one-step conditional variance each session with only the latest realized return.
        previous_pct_return = float(returns[i - 1] * 100)
        h_next_pct2 = omega + alpha * previous_pct_return ** 2 + beta * h_prev_pct2
        h_next_pct2 = max(h_next_pct2, 1e-10)
        h_prev_pct2 = h_next_pct2
        gvar = h_next_pct2 / 10000.0
        hist = returns[max(0, i - 20):i]
        hist = hist[np.isfinite(hist)]
        rv = float(np.var(hist, ddof=1)) if len(hist) > 1 else float(np.var(returns[:i], ddof=1))
        cv = float(np.var(returns[:i], ddof=1))
        actual.append(float(returns[i] ** 2))
        garch_var.append(gvar)
        rolling_var.append(rv)
        expanding_var.append(cv)
        test_dates.append(str(dates.iloc[i].date()))
    if len(actual) < 100:
        raise ValueError(f"Insufficient volatility holdout: {len(actual)}")
    y = np.asarray(actual)
    result = {
        "status": "COMPUTED",
        "model": "GARCH(1,1), zero mean; parameters refit every 20 sessions; variance recursively updated daily",
        "source": str(DATA.relative_to(ROOT)),
        "n": len(y),
        "first_test_date": test_dates[0],
        "last_test_date": test_dates[-1],
        "target": "next-session squared close-to-close return; noisy volatility proxy",
        "metric": "QLIKE = mean(log(forecast variance) + realized squared return / forecast variance); lower is better",
        "results": [
            {"model": "GARCH(1,1)", "qlike": qlike(y, garch_var), "mean_forecast_volatility": float(np.mean(np.sqrt(garch_var)))},
            {"model": "rolling_20_session_variance", "qlike": qlike(y, rolling_var), "mean_forecast_volatility": float(np.mean(np.sqrt(rolling_var)))},
            {"model": "expanding_unconditional_variance", "qlike": qlike(y, expanding_var), "mean_forecast_volatility": float(np.mean(np.sqrt(expanding_var)))}
        ],
        "limitations": [
            "Volatility forecast evaluation is not directional prediction or proof of a trading edge.",
            "Squared returns are a noisy proxy for latent volatility.",
            "Daily third-party source is not exchange-certified.",
            "Chronological final-quarter evaluation; each variance forecast uses only prior observations.",
            "No transaction-cost or trading P&L claim is made."
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
