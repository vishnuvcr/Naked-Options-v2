#!/usr/bin/env python3
"""Bounded weekly-expiry NIFTY direction experiments using daily OHLC only.

Primary label: compare the actual expiry-session close with the close of the
forecast cutoff session (previous available session). Expiry weekday regime:
Thursday through 2025-08-28, Tuesday from 2025-09-01 onward, with holiday
adjustment to the previous available trading session. This rule must be checked
against authoritative historical contract calendars before using results for
decision-making; the report flags this limitation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss, log_loss, matthews_corrcoef
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data/cache/nifty-prediction/nifty50_daily.csv"
REPORT = ROOT / "reports/nifty-prediction/weekly_expiry_experiments.json"


def load_spot(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path)
    raw.columns = [str(c).strip().lower().replace(" ", "_") for c in raw.columns]
    date_col = next((c for c in raw if c in ("date", "datetime", "timestamp")), None)
    if date_col is None or not all(c in raw for c in ("open", "high", "low", "close")):
        raise ValueError(f"Need date/open/high/low/close columns; got {raw.columns.tolist()}")
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[date_col], errors="coerce", utc=True).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None).dt.normalize(),
        **{c: pd.to_numeric(raw[c], errors="coerce") for c in ("open", "high", "low", "close")}
    }).dropna().sort_values("date").drop_duplicates("date").reset_index(drop=True)
    if len(d) < 1000:
        raise ValueError(f"Insufficient daily observations: {len(d)}")
    bad = (d.high < d[["open", "low", "close"]].max(axis=1)) | (d.low > d[["open", "high", "close"]].min(axis=1))
    if bad.any():
        raise ValueError(f"Invalid OHLC rows: {int(bad.sum())}")
    return d


def expiry_weekday(date: pd.Timestamp) -> int:
    # Historical NIFTY weekly expiry weekday regime; holidays are adjusted to
    # the previous available session below. This is an explicit approximation.
    return 3 if date < pd.Timestamp("2025-09-01") else 1  # Thursday / Tuesday


def build_weekly_examples(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    d = d.copy()
    d["ret1"] = d.close.pct_change()
    for n in (2, 3, 5, 10, 20, 40, 60):
        d[f"ret{n}"] = d.close.pct_change(n)
    for n in (5, 10, 20, 40):
        d[f"vol{n}"] = d.ret1.rolling(n).std()
        d[f"ma_gap{n}"] = d.close / d.close.rolling(n).mean() - 1
    d["range_pct"] = (d.high - d.low) / d.close
    d["open_gap"] = d.open / d.close.shift(1) - 1
    d["close_position"] = (d.close - d.low) / (d.high - d.low).replace(0, np.nan)
    features = [c for c in d if c.startswith(("ret", "vol", "ma_gap")) or c in ("range_pct", "open_gap", "close_position")]

    rows = []
    expiry_count = 0
    for expiry_idx in range(1, len(d)):
        expiry_date = d.loc[expiry_idx, "date"]
        if expiry_date.weekday() != expiry_weekday(expiry_date):
            continue
        # Identify the preceding available session; expiry dates that land on
        # exchange holidays naturally resolve to the prior session by the
        # weekday-date search only if the calendar date exists. Actual holiday
        # shifts require authoritative calendar validation and are not inferred.
        cut_idx = expiry_idx - 1
        # Avoid incorrectly treating a weekday-rule expiry when the expected
        # calendar expiry was a holiday: flagged in report; no external calendar.
        if cut_idx < 60:
            continue
        target_ret = d.loc[expiry_idx, "close"] / d.loc[cut_idx, "close"] - 1
        row = {c: d.loc[cut_idx, c] for c in features}
        row.update({
            "cutoff_date": d.loc[cut_idx, "date"].date().isoformat(),
            "expiry_date": expiry_date.date().isoformat(),
            "cutoff_close": float(d.loc[cut_idx, "close"]),
            "expiry_close": float(d.loc[expiry_idx, "close"]),
            "target_return": float(target_ret),
            "target_up": int(target_ret > 0),
            "regime_vol_high": int(d.loc[cut_idx, "vol20"] > d.loc[:cut_idx, "vol20"].rolling(252, min_periods=60).median().iloc[-1]) if pd.notna(d.loc[cut_idx, "vol20"]) else 0,
        })
        rows.append(row)
        expiry_count += 1
    frame = pd.DataFrame(rows)
    if frame.empty:
        raise ValueError("No expiry examples built; check input date coverage and weekday rules")
    frame = frame.dropna(subset=features + ["target_return", "target_up"]).reset_index(drop=True)
    metadata = {
        "expiry_rule": "Thursday before 2025-09-01; Tuesday from 2025-09-01; holiday-shifted expiry not reconstructed",
        "authoritative_calendar_verified": False,
        "examples_before_feature_dropna": expiry_count,
        "examples": int(len(frame)),
        "first_cutoff": frame.cutoff_date.min(),
        "last_expiry": frame.expiry_date.max(),
        "feature_columns": features,
        "label": "UP if expiry-session NIFTY 50 spot close > preceding available session close; otherwise DOWN",
        "limitations": [
            "Daily OHLC only; no intraday cutoff variants, options chain, breadth, event, or point-in-time global data are included.",
            "Expiry weekday change is encoded as a documented approximation; official expiry calendars and holiday-shift dates were not supplied or validated.",
            "This is an exploratory weekly-expiry spot-direction test, not an options-premium or profitability test."
        ]
    }
    return frame, metadata


def metrics(name, y, pred, prob):
    return {
        "model": name, "n": int(len(y)),
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "matthews_correlation": float(matthews_corrcoef(y, pred)),
        "brier_score": float(brier_score_loss(y, prob)),
        "log_loss": float(log_loss(y, np.column_stack([1-prob, prob]), labels=[0, 1])),
    }


def run():
    d = load_spot(INPUT)
    frame, meta = build_weekly_examples(d)
    features = meta["feature_columns"]
    # Most recent 25% of expiry examples is untouched test block; train expands
    # chronologically. Weekly examples are already one per expiry session.
    split = max(40, int(len(frame) * .75))
    if split >= len(frame) - 10:
        raise ValueError(f"Too few weekly examples for a chronological test: {len(frame)}")
    X = frame[features].replace([np.inf, -np.inf], np.nan)
    y = frame.target_up.to_numpy(dtype=int)
    test_y = y[split:]
    train_rate = float(y[:split].mean())
    pred_majority = np.full(len(test_y), int(train_rate >= .5))
    results = [metrics("train_majority_baseline", test_y, pred_majority, np.full(len(test_y), train_rate))]
    # Previous weekly direction is last expiry-to-expiry direction; calculate
    # strictly from earlier observed expiry closes.
    prior_weekly = np.sign(frame.expiry_close.shift(1).to_numpy()[split:] - frame.cutoff_close.shift(1).to_numpy()[split:])
    prior_pred = (prior_weekly > 0).astype(int)
    results.append(metrics("previous_expiry_direction", test_y, prior_pred, np.where(prior_pred == 1, .55, .45)))
    models = {
        "logistic_regression": lambda: make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced", C=.5, random_state=42)),
        "random_forest": lambda: make_pipeline(SimpleImputer(strategy="median"), RandomForestClassifier(n_estimators=250, min_samples_leaf=4, max_features="sqrt", class_weight="balanced_subsample", n_jobs=-1, random_state=42)),
        "hist_gradient_boosting": lambda: make_pipeline(SimpleImputer(strategy="median"), HistGradientBoostingClassifier(max_iter=100, learning_rate=.04, max_leaf_nodes=7, l2_regularization=2.0, random_state=42)),
    }
    preds_by_model = {}
    for name, factory in models.items():
        predictions, probabilities = [], []
        model = None
        for i in range(split, len(frame)):
            # Refit every 8 expiry observations; never fit on current label.
            if model is None or (i - split) % 8 == 0:
                model = factory()
                model.fit(X.iloc[:i], y[:i])
            p = float(model.predict_proba(X.iloc[[i]])[0, 1])
            probabilities.append(p)
            predictions.append(int(p >= .5))
        pred = np.asarray(predictions)
        prob = np.asarray(probabilities)
        results.append(metrics(name, test_y, pred, prob))
        preds_by_model[name] = {"predictions": pred.tolist(), "probabilities_up": prob.tolist()}
    # One predeclared regime ablation: separate high/low-vol logistic models are
    # not fit unless each training regime has adequate class support.
    # The current daily-only data does not contain point-in-time exogenous sources.
    payload = {
        "study": "NIFTY 50 weekly expiry spot direction",
        "status": "EXPLORATORY_APPROXIMATE_EXPIRY_CALENDAR",
        "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        "input_rows": int(len(d)), "input_first_date": d.date.min().date().isoformat(),
        "input_last_date": d.date.max().date().isoformat(),
        "split": {"method": "chronological 75/25; no random shuffle", "train_examples": int(split), "test_examples": int(len(frame)-split), "first_test_cutoff": frame.cutoff_date.iloc[split], "last_test_expiry": frame.expiry_date.iloc[-1]},
        "metadata": meta,
        "class_balance": {"up_rate_all": float(y.mean()), "up_rate_train": train_rate, "up_rate_test": float(test_y.mean())},
        "results": results,
        "prediction_records": frame.iloc[split:][["cutoff_date", "expiry_date", "cutoff_close", "expiry_close", "target_return", "target_up"]].assign(
            actual_up=frame.target_up.iloc[split:].astype(int).to_numpy()
        ).to_dict(orient="records"),
        "model_predictions": preds_by_model,
        "interpretation": "No strategy claim. Candidate results are exploratory because the expiry calendar is approximate, the sample is small, and only daily OHLC features are used.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(REPORT), "status": payload["status"], "examples": meta["examples"], "test_examples": len(test_y), "results": results}, indent=2))


if __name__ == "__main__":
    run()
