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
    returns = d["close"].pct_change().to_numpy()
    valid_start = 61
    returns = returns[valid_start:]
    dates = d["date"].iloc[valid_start:].reset_index(drop=True)
    split = int(len(returns) * .75)
    # At index i, fit only returns up to i-1; forecast the next observed return.
    actual, garch_var, rolling_var, constant_var, test_dates = [], [], [], [], []
    fitted = None
    refit_every = 20
    min_train = 500
    for i in range(max(split, min_train), len(returns) - 1):
        if fitted is None or (i - max(split, min_train)) % refit_every == 0:
            train = returns[:i]
            train = train[np.isfinite(train)]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fitted = arch_model(train * 100, mean="Zero", vol="GARCH", p=1, q=1, rescale=False).fit(
                    disp="off", show_warning=False, options={"maxiter": 500}
                )
        forecast = fitted.forecast(horizon=1, reindex=False)
        # ARCH fits percentage-scaled returns; convert forecast variance back to decimal-return units.
        gvar = float(forecast.variance.iloc[-1, 0]) / 10000.0
        hist = returns[max(0, i - 20):i]
        hist = hist[np.isfinite(hist)]
        rv = float(np.var(hist, ddof=1)) if len(hist) > 1 else float(np.var(returns[:i], ddof=1))
        cv = float(np.var(returns[:i], ddof=1))
        actual.append(float(returns[i] ** 2))
        garch_var.append(gvar)
        rolling_var.append(rv)
        constant_var.append(cv)
        test_dates.append(str(dates.iloc[i]))
    if len(actual) < 100:
        raise ValueError(f"Insufficient volatility holdout: {len(actual)}")
    y = np.asarray(actual)
    result = {
        "status": "COMPUTED",
        "model": "GARCH(1,1), zero mean; refit every 20 sessions",
        "source": str(DATA.relative_to(ROOT)),
        "n": len(y),
        "first_test_date": test_dates[0],
        "last_test_date": test_dates[-1],
        "target": "next-session squared close-to-close return; noisy volatility proxy",
        "metric": "QLIKE = mean(log(forecast variance) + realized squared return / forecast variance); lower is better",
        "results": [
            {"model": "GARCH(1,1)", "qlike": qlike(y, garch_var), "mean_forecast_volatility": float(np.mean(np.sqrt(garch_var)))},
            {"model": "rolling_20_session_variance", "qlike": qlike(y, rolling_var), "mean_forecast_volatility": float(np.mean(np.sqrt(rolling_var)))},
            {"model": "expanding_unconditional_variance", "qlike": qlike(y, constant_var), "mean_forecast_volatility": float(np.mean(np.sqrt(constant_var)))}
        ],
        "limitations": [
            "Volatility forecast evaluation is not directional prediction or proof of a trading edge.",
            "Squared returns are a noisy proxy for latent volatility.",
            "Daily third-party source is not exchange-certified.",
            "Chronological final-quarter evaluation; model refits use only observations available before each forecast.",
            "No transaction-cost or trading P&L claim is made."
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
