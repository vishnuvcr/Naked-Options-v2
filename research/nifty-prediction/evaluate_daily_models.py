#!/usr/bin/env python3
"""Leakage-controlled next-session NIFTY 50 direction benchmark.

Input CSV must contain Date, Open, High, Low, Close (Yahoo chart export accepted).
All predictors are computed from data available at the close of session t. The
target is the sign of close[t+1]/close[t]-1. This is research evaluation only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, precision_recall_fscore_support, log_loss, brier_score_loss

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data" / "cache" / "nifty-prediction" / "nifty50_daily.csv"
REPORT_DIR = ROOT / "reports" / "nifty-prediction"


def load_data(path: Path) -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(path)
    # Yahoo downloads may use MultiIndex headers flattened by yfinance; normalize labels.
    raw.columns = [str(c).strip().lower().replace(" ", "_") for c in raw.columns]
    date_col = next((c for c in raw.columns if c in ("date", "datetime", "timestamp")), None)
    close_col = next((c for c in raw.columns if c in ("close", "adj_close", "adjclose")), None)
    if date_col is None or close_col is None:
        raise ValueError(f"Expected Date and Close columns; received {raw.columns.tolist()}")
    def pick(*names):
        return next((n for n in names if n in raw.columns), None)
    open_col, high_col, low_col = pick("open"), pick("high"), pick("low")
    if not all((open_col, high_col, low_col)):
        raise ValueError("Open/High/Low/Close are all required")
    data = pd.DataFrame({
        "date": pd.to_datetime(raw[date_col], errors="coerce", utc=True).dt.tz_convert("Asia/Kolkata").dt.date,
        "open": pd.to_numeric(raw[open_col], errors="coerce"),
        "high": pd.to_numeric(raw[high_col], errors="coerce"),
        "low": pd.to_numeric(raw[low_col], errors="coerce"),
        "close": pd.to_numeric(raw[close_col], errors="coerce"),
    }).dropna(subset=["date", "open", "high", "low", "close"])
    data = data.sort_values("date").drop_duplicates("date", keep="last").reset_index(drop=True)
    if len(data) < 1000:
        raise ValueError(f"Only {len(data)} valid daily rows; need at least 1000 for this protocol")
    invalid = (data["high"] < data[["open", "close", "low"]].max(axis=1)) | (data["low"] > data[["open", "close", "high"]].min(axis=1))
    if invalid.any():
        raise ValueError(f"OHLC invariants failed for {int(invalid.sum())} rows")
    report = {
        "input_path": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "rows": int(len(data)),
        "first_date": str(data.date.iloc[0]),
        "last_date": str(data.date.iloc[-1]),
        "invalid_ohlc_rows": int(invalid.sum()),
        "duplicate_dates_dropped": int(raw.shape[0] - len(data)),
        "source_note": "Input source must be documented by acquisition workflow; daily Yahoo data is not exchange-certified.",
    }
    return data, report


def build_frame(data: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    d = data.copy()
    close = d.close
    ret = close.pct_change()
    d["ret_1"] = ret
    for n in (2, 3, 5, 10, 20, 60):
        d[f"ret_{n}"] = close.pct_change(n)
    for n in (5, 10, 20, 60):
        d[f"vol_{n}"] = ret.rolling(n).std()
        d[f"ma_gap_{n}"] = close / close.rolling(n).mean() - 1
    d["range_pct"] = (d.high - d.low) / close
    d["open_gap"] = d.open / close.shift(1) - 1
    d["close_position"] = (d.close - d.low) / (d.high - d.low).replace(0, np.nan)
    # Shift all predictors one row: prediction after t close uses only through t.
    features = [c for c in d.columns if c.startswith(("ret_", "vol_", "ma_gap_")) or c in ("range_pct", "open_gap", "close_position")]
    d[features] = d[features].shift(0)
    d["target_return"] = close.shift(-1) / close - 1
    d["target_up"] = (d["target_return"] > 0).astype(int)
    d.loc[d["target_return"].isna(), "target_up"] = np.nan
    d["previous_direction"] = (ret > 0).astype(int)
    return d, features


def block_bootstrap_ci(y: np.ndarray, pred: np.ndarray, block: int = 10, reps: int = 1500, seed: int = 20261025) -> dict:
    if len(y) < 40:
        return {"lower": None, "upper": None, "method": "circular block bootstrap; insufficient n"}
    rng = np.random.default_rng(seed)
    n = len(y)
    values = []
    nblocks = math.ceil(n / block)
    for _ in range(reps):
        starts = rng.integers(0, n, size=nblocks)
        ix = np.concatenate([(np.arange(s, s + block) % n) for s in starts])[:n]
        if len(np.unique(y[ix])) < 2:
            continue
        values.append(balanced_accuracy_score(y[ix], pred[ix]))
    if not values:
        return {"lower": None, "upper": None, "method": "circular block bootstrap; no valid resamples"}
    return {"lower": float(np.quantile(values, .025)), "upper": float(np.quantile(values, .975)), "method": f"circular block bootstrap, block={block}, reps={reps}"}


def score(name: str, y: np.ndarray, pred: np.ndarray, prob: np.ndarray | None = None) -> dict:
    precision, recall, f1, _ = precision_recall_fscore_support(y, pred, labels=[0, 1], zero_division=0)
    result = {
        "model": name, "n": int(len(y)),
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "confusion_matrix_labels_down_up": confusion_matrix(y, pred, labels=[0, 1]).tolist(),
        "precision_down_up": precision.tolist(), "recall_down_up": recall.tolist(), "f1_down_up": f1.tolist(),
        "balanced_accuracy_95pct_ci": block_bootstrap_ci(y, pred),
    }
    if prob is not None:
        result["log_loss"] = float(log_loss(y, np.column_stack([1 - prob, prob]), labels=[0, 1]))
        result["brier_score"] = float(brier_score_loss(y, prob))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--min-train", type=int, default=750)
    parser.add_argument("--refit-every", type=int, default=20)
    parser.add_argument("--test-fraction", type=float, default=.25)
    args = parser.parse_args()
    data, source = load_data(args.input)
    frame, features = build_frame(data)
    frame = frame.dropna(subset=features + ["target_return", "target_up"]).reset_index(drop=True)
    y_all = frame.target_up.astype(int).to_numpy()
    split = max(args.min_train, int(len(frame) * (1 - args.test_fraction)))
    if split >= len(frame) - 100:
        split = max(args.min_train, len(frame) - max(100, int(len(frame) * args.test_fraction)))
    if split >= len(frame) - 50:
        raise ValueError(f"Not enough observations after feature construction: {len(frame)}")
    X = frame[features].replace([np.inf, -np.inf], np.nan)
    y = y_all
    models = {
        "logistic_regression": lambda: make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
        "random_forest": lambda: make_pipeline(SimpleImputer(strategy="median"), RandomForestClassifier(n_estimators=300, min_samples_leaf=10, max_features="sqrt", class_weight="balanced_subsample", n_jobs=-1, random_state=42)),
        "hist_gradient_boosting": lambda: make_pipeline(SimpleImputer(strategy="median"), HistGradientBoostingClassifier(max_iter=150, learning_rate=.05, max_leaf_nodes=15, l2_regularization=1.0, random_state=42)),
    }
    results = []
    y_test = y[split:]
    # Naive benchmarks are evaluated on exactly the same holdout rows.
    base_up = int(y[:split].mean() >= .5)
    results.append(score("majority_class_baseline", y_test, np.full(len(y_test), base_up)))
    prev_pred = frame["previous_direction"].to_numpy()[split:]
    results.append(score("previous_session_direction", y_test, prev_pred))
    for name, factory in models.items():
        preds, probs = [], []
        model = None
        for i in range(split, len(frame)):
            if model is None or (i - split) % max(1, args.refit_every) == 0:
                model = factory()
                model.fit(X.iloc[:i], y[:i])
            row = X.iloc[[i]]
            preds.append(int(model.predict(row)[0]))
            if hasattr(model, "predict_proba"):
                probs.append(float(model.predict_proba(row)[0, 1]))
        pred = np.asarray(preds)
        prob = np.asarray(probs) if probs else None
        results.append(score(name, y_test, pred, prob))
    output = {
        "study": "NIFTY 50 next-session direction; daily OHLC baseline benchmark",
        "status": "EMPIRICAL_RESULTS_COMPUTED" if len(y_test) >= 100 else "UNDERPOWERED_HOLDOUT",
        "target": "sign(next session close / current close - 1); zero return classified DOWN for binary baseline, exact ties separately counted below",
        "primary_metric": "balanced_accuracy",
        "evaluation": "chronological expanding walk-forward; model refit every N test rows; each prediction uses only data through current close",
        "source_manifest": source,
        "feature_columns": features,
        "all_rows": int(len(frame)),
        "train_rows": int(split),
        "test_rows": int(len(y_test)),
        "test_first_date": str(frame.date.iloc[split]),
        "test_last_date": str(frame.date.iloc[-1]),
        "test_up_rate": float(y_test.mean()),
        "test_tie_count": int((frame.target_return.iloc[split:] == 0).sum()),
        "models": results,
        "limitations": [
            "Daily Yahoo source is a free baseline and not exchange-certified.",
            "No transaction costs or trading P&L are evaluated; this is prediction-only.",
            "Regime and hyperparameter variants are not optimized on the holdout.",
            "Bootstrap intervals are approximate and serial-dependence assumptions must be considered.",
            "This benchmark does not establish tradable profitability or generalization to options.",
        ],
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "daily_benchmark.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
