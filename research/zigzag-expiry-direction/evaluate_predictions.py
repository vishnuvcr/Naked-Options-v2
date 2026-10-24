#!/usr/bin/env python3
"""Score a pre-built ZigZag expiry-direction table without look-ahead leakage.

Input CSV columns:
interval_id, cutoff_at, signal_available_at, signal_label, reference_price,
target_close, target_at
Timestamps must be ISO-8601 with timezone offsets. This utility does not
reconstruct ZigLib; it only audits timing and scores verified exported signals.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, precision_recall_fscore_support

REQUIRED = {
    "interval_id", "cutoff_at", "signal_available_at", "signal_label",
    "reference_price", "target_close", "target_at"
}
VALID = {"HH", "LH", "HL", "LL"}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("results.json"))
    args = parser.parse_args()
    df = pd.read_csv(args.csv)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")
    for c in ("cutoff_at", "signal_available_at", "target_at"):
        df[c] = pd.to_datetime(df[c], utc=True, errors="coerce")
    if df[["cutoff_at", "signal_available_at", "target_at"]].isna().any().any():
        raise SystemExit("Invalid/missing timestamps; no rows silently dropped.")
    if (df["signal_available_at"] > df["cutoff_at"]).any():
        bad = df.loc[df["signal_available_at"] > df["cutoff_at"], "interval_id"].tolist()
        raise SystemExit(f"Look-ahead violation: signals unavailable at cutoff: {bad[:10]}")
    if (df["target_at"] <= df["cutoff_at"]).any():
        raise SystemExit("Target timestamp must be later than forecast cutoff.")
    if df["interval_id"].duplicated().any():
        raise SystemExit("Duplicate interval_id values.")
    if df[["reference_price", "target_close"]].isna().any().any():
        raise SystemExit("Missing prices; repair provenance rather than silently dropping rows.")
    df["prediction"] = df["signal_label"].map(
        lambda x: "UP" if x in {"LL", "HL"} else ("DOWN" if x in {"HH", "LH"} else None)
    )
    df["actual"] = df.apply(
        lambda r: "UP" if r.target_close > r.reference_price else
                  ("DOWN" if r.target_close < r.reference_price else "TIE"), axis=1
    )
    eligible = df[df["prediction"].notna() & df["actual"].isin(["UP", "DOWN"])].copy()
    if eligible.empty:
        raise SystemExit("No eligible non-tie predictions to score.")
    y, pred = eligible["actual"], eligible["prediction"]
    labels = ["UP", "DOWN"]
    cm = confusion_matrix(y, pred, labels=labels).tolist()
    precision, recall, f1, support = precision_recall_fscore_support(
        y, pred, labels=labels, zero_division=0
    )
    majority = y.value_counts(normalize=True).max()
    result = {
        "n_input": int(len(df)),
        "n_scored": int(len(eligible)),
        "coverage": float(len(eligible) / len(df)),
        "ties_excluded": int((df["actual"] == "TIE").sum()),
        "abstentions": int(df["prediction"].isna().sum()),
        "class_counts_actual": {k: int(v) for k, v in y.value_counts().to_dict().items()},
        "confusion_matrix_labels": labels,
        "confusion_matrix_rows_actual_columns_prediction": cm,
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "majority_class_baseline_accuracy": float(majority),
        "per_class": {
            label: {"precision": float(precision[i]), "recall": float(recall[i]),
                    "f1": float(f1[i]), "support": int(support[i])}
            for i, label in enumerate(labels)
        },
        "warning": "Descriptive metrics only; use a chronological sealed holdout and dependence-aware confidence intervals before inference."
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
