#!/usr/bin/env python3
"""Artifact-level audit for NIFTY prediction outputs; no model training is performed.

Example:
  python research/audits/audit_nifty_predictions.py predictions.csv --metrics metrics.csv --output audit.json

Consumes sanitized GitHub Actions artifact CSVs. Does not download data or write raw market data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import norm


def holm_adjust(p_values: np.ndarray) -> np.ndarray:
    values = np.asarray(p_values, dtype=float)
    out = np.full(values.shape, np.nan)
    valid = np.flatnonzero(np.isfinite(values))
    order = valid[np.argsort(values[valid])]
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (len(order) - rank) * float(values[idx])))
        out[idx] = running
    return out


def hac_mean_test(values: np.ndarray, lag: int = 0) -> dict[str, float | None]:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 10:
        return {"z": None, "p_value": None}
    centered = x - x.mean()
    long_run_var = float(np.dot(centered, centered) / n)
    # Match forecast_metrics.hac_test: Newey-West Bartlett weights, lag floor 5.
    max_lag = min(max(5, int(lag)), n - 1)
    for k in range(1, max_lag + 1):
        long_run_var += 2.0 * (1.0 - k / (max_lag + 1.0)) * float(
            np.dot(centered[k:], centered[:-k]) / n
        )
    se = np.sqrt(max(long_run_var, 0.0) / n)
    z = float(x.mean() / se) if se > 0 else None
    p_value = float(2.0 * norm.sf(abs(z))) if z is not None else None
    return {"z": z, "p_value": p_value}


def moving_block_ci(values: np.ndarray, seed: int, reps: int = 300, block: int = 1) -> list[float | None]:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 10:
        return [None, None]
    rng = np.random.default_rng(seed)
    block_len = max(5, min(int(block), n))
    draws = []
    for _ in range(reps):
        starts = rng.integers(0, n, size=int(np.ceil(n / block_len)))
        sample = np.concatenate([x[(start + np.arange(block_len)) % n] for start in starts])[:n]
        draws.append(float(sample.mean()))
    lo, hi = np.quantile(draws, [0.025, 0.975])
    return [float(lo), float(hi)]


def qlike_difference(frame: pd.DataFrame) -> np.ndarray:
    actual = np.maximum(frame["actual"].to_numpy(float), 1e-8) ** 2
    prediction = np.maximum(frame["prediction"].to_numpy(float), 1e-8) ** 2
    baseline = np.maximum(frame["baseline"].to_numpy(float), 1e-8) ** 2
    model_loss = np.log(prediction) + actual / prediction
    baseline_loss = np.log(baseline) + actual / baseline
    return model_loss - baseline_loss


def summarize_h1(frame: pd.DataFrame, metrics_path: str | None) -> dict[str, Any]:
    selected = frame[
        (frame["task"] == "volatility")
        & (pd.to_numeric(frame["horizon"], errors="coerce") == 1)
        & (frame["model"] == "extra_trees")
        & (frame["feature_set"] == "global")
    ].sort_values("origin_date").reset_index(drop=True)
    if selected.empty:
        return {"status": "BLOCKED_SELECTED_H1_CELL_NOT_FOUND"}
    if selected["target_date"].isna().any():
        return {"status": "BLOCKED_SELECTED_H1_CELL_HAS_MISSING_TARGET_DATE", "n": int(len(selected))}
    if selected[["actual", "prediction", "baseline"]].isna().any().any():
        return {"status": "BLOCKED_SELECTED_H1_CELL_HAS_MISSING_NUMERICS", "n": int(len(selected))}

    differences = qlike_difference(selected)
    hac = hac_mean_test(differences, lag=0)
    q10, q90 = np.quantile(differences, [0.10, 0.90])
    metrics: dict[str, Any] = {
        "status": "REPRODUCED_FROM_ARTIFACT",
        "model": "global ExtraTrees",
        "n": int(len(selected)),
        "origin_start": str(selected["origin_date"].iloc[0]),
        "origin_end": str(selected["origin_date"].iloc[-1]),
        "missing_target_dates": int(selected["target_date"].isna().sum()),
        "mae": float(np.mean(np.abs(selected["actual"] - selected["prediction"]))),
        "baseline_mae": float(np.mean(np.abs(selected["actual"] - selected["baseline"]))),
        "rmse": float(np.sqrt(np.mean((selected["actual"] - selected["prediction"]) ** 2))),
        "baseline_rmse": float(np.sqrt(np.mean((selected["actual"] - selected["baseline"]) ** 2))),
        "mean_qlike_loss_difference_model_minus_baseline": float(differences.mean()),
        "median_qlike_loss_difference_model_minus_baseline": float(np.median(differences)),
        "share_days_model_loss_worse_than_baseline": float(np.mean(differences > 0)),
        "winsorized_mean_qlike_difference_10pct": float(np.clip(differences, q10, q90).mean()),
        "hac_z": hac["z"],
        "hac_p_value": hac["p_value"],
        "moving_block_ci_95pct_seed_20261015": moving_block_ci(differences, seed=20261015, reps=300, block=1),
    }

    if metrics_path:
        metric_frame = pd.read_csv(metrics_path, low_memory=False)
        required = {"status", "p_value", "task", "horizon", "model", "feature_set"}
        if required.issubset(metric_frame.columns):
            family = metric_frame[
                (metric_frame["status"] == "OOS_EVALUATED")
                & pd.to_numeric(metric_frame["p_value"], errors="coerce").notna()
            ].copy()
            p = pd.to_numeric(family["p_value"], errors="coerce").to_numpy(float)
            family["holm_all_oos"] = holm_adjust(p)
            cell = family[
                (family["task"] == "volatility")
                & (pd.to_numeric(family["horizon"], errors="coerce") == 1)
                & (family["model"] == "extra_trees")
                & (family["feature_set"] == "global")
            ]
            metrics["all_oos_comparison_count"] = int(len(family))
            metrics["holm_p_across_all_oos_comparisons"] = (
                float(cell["holm_all_oos"].iloc[0]) if len(cell) == 1 else None
            )
    chunks = np.array_split(np.arange(len(selected)), 4)
    subperiods = []
    adjusted_ps = []
    for idx, positions in enumerate(chunks, start=1):
        values = differences[positions]
        test = hac_mean_test(values, lag=0)
        interval = moving_block_ci(values, seed=20261015, reps=1000, block=1)
        subperiods.append({
            "window": idx,
            "n": int(len(values)),
            "origin_start": str(selected["origin_date"].iloc[positions[0]]),
            "origin_end": str(selected["origin_date"].iloc[positions[-1]]),
            "mean_qlike_difference": float(values.mean()),
            "median_qlike_difference": float(np.median(values)),
            "ci_95pct": interval,
            "hac_p_value": test["p_value"],
        })
        adjusted_ps.append(float(test["p_value"]) if test["p_value"] is not None else np.nan)
    adj = holm_adjust(np.asarray(adjusted_ps, dtype=float))
    for row, value in zip(subperiods, adj):
        row["holm_p_within_four_subperiod_sensitivity_tests"] = float(value) if np.isfinite(value) else None
    metrics["subperiod_sensitivity_same_holdout_not_independent_replication"] = subperiods
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions_csv", help="Path to predictions.csv from a workflow artifact")
    parser.add_argument("--metrics", help="Optional metrics.csv to recalculate the all-OOS Holm family")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()

    path = Path(args.predictions_csv)
    df = pd.read_csv(path, low_memory=False)
    required = {"origin_date", "target_date", "task", "horizon", "model", "actual", "prediction", "baseline"}
    missing_cols = sorted(required - set(df.columns))
    if missing_cols:
        raise SystemExit(f"Missing required columns: {missing_cols}")

    null_dates = df["target_date"].isna()
    numeric_populated = df[["actual", "prediction", "baseline"]].notna().all(axis=1)
    invalid = df[null_dates & numeric_populated]
    breakdown = {
        f"{task}|h{int(h)}": int(n)
        for (task, h), n in invalid.groupby(["task", "horizon"], dropna=False).size().items()
    }
    result: dict[str, Any] = {
        "input": str(path),
        "prediction_rows": int(len(df)),
        "missing_target_date_rows": int(null_dates.sum()),
        "missing_target_dates_with_all_numeric_forecasts": int(len(invalid)),
        "invalid_rows_by_task_horizon": breakdown,
        "target_integrity_pass": bool(null_dates.sum() == 0),
        "selected_one_session_volatility": summarize_h1(df, args.metrics),
        "scope_note": "Subperiod splits partition the same prior holdout and are sensitivity diagnostics, not an untouched independent-period replication.",
    }
    output = json.dumps(result, indent=2, allow_nan=False)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if result["target_integrity_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
