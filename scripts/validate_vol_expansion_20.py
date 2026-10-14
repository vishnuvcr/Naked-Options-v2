"""Focused post-run diagnostics for the 20-session volatility-expansion classifier.

Uses the frozen chronological holdout and existing cached data/predictions. Does not tune
models or approve a trading strategy. Writes a machine-readable diagnostic report.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, brier_score_loss,
                             log_loss, precision_score, recall_score, confusion_matrix)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports"
CACHE = ROOT / "data" / "cache"
HORIZON = 20
TASK = "vol_expansion"
MODEL = "LogisticRegression"


def scores(y, p):
    y = np.asarray(y, dtype=int)
    p = np.clip(np.asarray(p, dtype=float), 1e-6, 1 - 1e-6)
    base = np.full(len(y), float(np.mean(y)))
    cm = confusion_matrix(y, p >= 0.5, labels=[0, 1])
    tn, fp, fn, tp = [int(v) for v in cm.ravel()]
    return {
        "n": int(len(y)),
        "positive_rate": float(np.mean(y)),
        "accuracy_at_0_5": float(accuracy_score(y, p >= 0.5)),
        "balanced_accuracy_at_0_5": float(balanced_accuracy_score(y, p >= 0.5)),
        "precision_at_0_5": float(precision_score(y, p >= 0.5, zero_division=0)),
        "recall_at_0_5": float(recall_score(y, p >= 0.5, zero_division=0)),
        "specificity_at_0_5": float(tn / (tn + fp)) if tn + fp else None,
        "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
        "brier": float(brier_score_loss(y, p)),
        "base_rate_brier": float(brier_score_loss(y, base)),
        "brier_skill_vs_holdout_prevalence": float(1 - brier_score_loss(y, p) / brier_score_loss(y, base)) if brier_score_loss(y, base) > 0 else None,
        "log_loss": float(log_loss(y, p, labels=[0, 1])),
        "base_rate_log_loss": float(log_loss(y, base, labels=[0, 1])),
    }


def main():
    pred_path = REPORT / "predictions_technical.csv"
    matrix_path = CACHE / "model_matrix.csv"
    if not pred_path.exists() or not matrix_path.exists():
        raise SystemExit("Blocked: required saved predictions or validated feature matrix missing")
    pred = pd.read_csv(pred_path)
    pred = pred[(pred.task == TASK) & (pred.horizon == HORIZON)].copy()
    if pred.empty:
        raise SystemExit("Blocked: no 20-session volatility-expansion predictions")
    # The stored positive probability is the model's forecast of the positive class.
    pred = pred[pred.model.astype(str).str.contains("logistic", case=False)].copy()
    if pred.empty or "probability_positive" not in pred:
        raise SystemExit("Blocked: logistic predictions/probabilities missing")
    pred["origin_date"] = pd.to_datetime(pred.origin_date, errors="raise")
    pred = pred.sort_values("origin_date").drop_duplicates("origin_date", keep=False)
    pred["actual"] = pd.to_numeric(pred.actual, errors="raise").astype(int)
    pred["probability_positive"] = pd.to_numeric(pred.probability_positive, errors="raise")
    if not pred.actual.isin([0, 1]).all():
        raise SystemExit("Invalid target labels: expected binary 0/1")
    if ((pred.probability_positive < 0) | (pred.probability_positive > 1)).any():
        raise SystemExit("Invalid probabilities outside [0,1]")

    matrix = pd.read_csv(matrix_path, parse_dates=["date"])
    matrix["date"] = pd.to_datetime(matrix.date, errors="raise")
    matrix["vol_20"] = pd.to_numeric(matrix.vol_20, errors="coerce")
    matrix["target_vol_expansion_20"] = pd.to_numeric(matrix.target_vol_expansion_20, errors="coerce")
    joined = pred.merge(matrix[["date", "vol_20", "target_vol_expansion_20"]], left_on="origin_date", right_on="date", how="left", validate="one_to_one")
    if joined.vol_20.isna().any():
        raise SystemExit("Missing origin-date vol_20 values; regime analysis cannot be trusted")
    if not np.array_equal(joined.actual.to_numpy(), joined.target_vol_expansion_20.astype(int).to_numpy()):
        raise SystemExit("Saved prediction labels do not match recomputed feature-matrix target labels")

    p = joined.probability_positive.to_numpy()
    y = joined.actual.to_numpy()
    overall = scores(y, p)
    # Descriptive reliability bins. Equal-width bins are fixed before inspection.
    bins = np.linspace(0, 1, 11)
    joined["probability_bin"] = pd.cut(joined.probability_positive, bins=bins, include_lowest=True, duplicates="drop")
    calibration = []
    for label, grp in joined.groupby("probability_bin", observed=False):
        if len(grp):
            calibration.append({"bin": str(label), "n": int(len(grp)),
                                "mean_probability": float(grp.probability_positive.mean()),
                                "observed_rate": float(grp.actual.mean())})
    # Test-year diagnostics are descriptive only; do not claim independent significance.
    yearly = []
    joined["year"] = joined.origin_date.dt.year
    for year, grp in joined.groupby("year"):
        if len(grp) >= 20 and grp.actual.nunique() == 2:
            yearly.append({"year": int(year), **scores(grp.actual, grp.probability_positive)})
    # Compare low/high historical-volatility regimes using the matrix's training-only threshold
    # if present; otherwise report a within-holdout median split explicitly as exploratory.
    train_end = joined.origin_date.min()
    all_train = matrix[matrix.date < train_end].dropna(subset=["vol_20"])
    if len(all_train) < 100:
        raise SystemExit("Insufficient pre-holdout history for volatility regime threshold")
    threshold = float(all_train.vol_20.quantile(0.75))
    joined["origin_vol_regime"] = np.where(joined.vol_20 >= threshold, "high_volatility", "not_high_volatility")
    regimes = []
    for regime, grp in joined.groupby("origin_vol_regime"):
        if len(grp) >= 20 and grp.actual.nunique() == 2:
            regimes.append({"regime": regime, "threshold_vol_20_75th_percentile": threshold, **scores(grp.actual, grp.probability_positive)})
    # The original classifier target is future 20-session std > origin rolling 20-session std.
    report = {
        "status": "DIAGNOSTICS_COMPLETE",
        "scope": "diagnostic validation only; frozen holdout; no retuning; no strategy test",
        "target_definition": "sample standard deviation of the next 20 daily log returns > trailing 20-session standard deviation available at origin",
        "model_filter": "saved technical-feature logistic classifier predictions for horizon 20",
        "n_predictions": int(len(joined)),
        "origin_first": joined.origin_date.min().date().isoformat(),
        "origin_last": joined.origin_date.max().date().isoformat(),
        "overall": overall,
        "calibration_bins": calibration,
        "yearly_descriptive": yearly,
        "origin_volatility_regimes_descriptive": regimes,
        "limitations": [
            "Subgroups are descriptive and have overlapping 20-session target windows.",
            "No new independent holdout is created; this diagnoses the existing frozen holdout.",
            "No options-chain, execution, transaction-cost, slippage or brokerage test is performed.",
            "Probability threshold 0.5 is a descriptive default, not a trading threshold.",
        ],
    }
    REPORT.mkdir(parents=True, exist_ok=True)
    out = REPORT / "vol_expansion_20_validation.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps({"status": report["status"], "n": report["n_predictions"],
                      "overall": overall, "report": str(out.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
