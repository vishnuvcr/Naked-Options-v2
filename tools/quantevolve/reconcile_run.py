#!/usr/bin/env python3
"""Reconcile a known QuantEvolve report-status mismatch only after consistency checks."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("report JSON is not an object")
    return value


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def approximately(left, right, tolerance=1e-10) -> bool:
    try:
        return math.isfinite(float(left)) and math.isfinite(float(right)) and abs(float(left) - float(right)) <= tolerance
    except (TypeError, ValueError):
        return False


def reconcile_run_dir(run_dir: Path) -> dict:
    manifest_path = run_dir / "run_manifest.json"
    dev_path = run_dir / "development_metrics.json"
    holdout_path = run_dir / "holdout_metrics.json"
    spec_path = run_dir / "best_strategy_spec.json"
    required = [manifest_path, dev_path, holdout_path, spec_path]
    if not all(path.is_file() for path in required):
        return {"status": "NOT_RECONCILED", "reason": "required sanitized report bundle is incomplete"}
    manifest, dev, holdout, spec = [read_json(path) for path in required]
    if manifest.get("status") != "HOLDOUT_REPORT_INVALID" or manifest.get("error_type") != "MetricReportValidationError":
        return {"status": "NOT_RECONCILED", "reason": "run is not the narrowly targeted status mismatch"}
    if dev.get("status") != "PASS" or dev.get("evaluation_stage") != "development":
        raise ValueError("development report failed status/stage validation")
    if holdout.get("status") != "PREDICTION_HOLDOUT_EVALUATED" or holdout.get("evaluation_stage") != "holdout":
        raise ValueError("holdout report failed status/stage validation")
    if dev.get("data_sha256") != holdout.get("data_sha256") or dev.get("data_sha256") != manifest.get("data_sha256"):
        raise ValueError("data SHA-256 does not match across the result bundle")
    if dev.get("candidate_source_sha256") != holdout.get("candidate_source_sha256"):
        raise ValueError("candidate source SHA-256 differs between development and holdout reports")
    if dev.get("selected_spec") != spec or holdout.get("selected_spec") != spec:
        raise ValueError("published declarative spec does not match the metric report")
    if holdout.get("final_holdout_used_for_candidate_selection") != 0.0:
        raise ValueError("holdout selection flag must be zero")
    n = int(holdout.get("sample_count", 0))
    if n < 50:
        raise ValueError("holdout sample count below frozen minimum")
    mae = float(holdout["mae"])
    baseline = float(holdout["zero_baseline_mae"])
    skill = float(holdout["mae_skill_vs_zero"])
    if baseline <= 0 or not approximately(skill, 1.0 - mae / baseline):
        raise ValueError("MAE skill arithmetic does not reconcile")
    ci_low, ci_high = float(holdout["mae_improvement_ci95_low"]), float(holdout["mae_improvement_ci95_high"])
    if ci_low > ci_high:
        raise ValueError("bootstrap confidence interval bounds are reversed")
    try:
        data_path = Path("data/cache/nifty50_daily.csv")
        # On hosted report-only publication the cache is intentionally not downloaded into this job.
        # Use the archived SHA rather than requiring raw market data in this postprocessor.
        data_sha = str(holdout["data_sha256"])
        if len(data_sha) != 64:
            raise ValueError("invalid data SHA-256 metadata")
        int(data_sha, 16)
    except Exception as exc:
        raise ValueError("invalid source data hash metadata") from exc

    zero_forecast = (float(spec.get("intercept", 1.0)) == 0.0 and
                     all(float(v) == 0.0 for v in spec.get("weights", {}).values()))
    if zero_forecast:
        for report in (dev, holdout):
            report["directional_accuracy"] = None
            report["directional_accuracy_defined"] = False
            report["directional_prediction_count"] = 0.0
            report["directional_prediction_coverage"] = 0.0
        for fold in dev.get("development_folds", []):
            fold["directional_accuracy"] = None
            fold["directional_accuracy_defined"] = False
            fold["directional_prediction_count"] = 0.0
            fold["directional_prediction_coverage"] = 0.0
        dev["mean_fold_directional_accuracy"] = None
        dev["mean_fold_directional_prediction_coverage"] = 0.0
        write_json(dev_path, dev)
        write_json(holdout_path, holdout)

    manifest["previous_status"] = manifest["status"]
    manifest["status"] = "PREDICTION_HOLDOUT_EVALUATED"
    manifest["error_type"] = None
    manifest["manifest_reconciled_posthoc"] = True
    manifest["reconciled_at_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["reconciliation_reason"] = (
        "The previous runner incorrectly required the final holdout evaluator's status to equal PASS. "
        "The evaluator's explicit expected status is PREDICTION_HOLDOUT_EVALUATED. Both stage reports, "
        "data/candidate hashes, spec identity, MAE skill arithmetic, sample count and confidence interval "
        "bounds were checked before reconciling this status label; no model was rerun."
    )
    manifest["performance_claim"] = None
    write_json(manifest_path, manifest)
    return {
        "status": manifest["status"],
        "run_id": manifest.get("run_id"),
        "reconciled": True,
        "holdout_sample_count": n,
        "mae_skill_vs_zero": skill,
        "mae_improvement_ci95": [ci_low, ci_high],
        "zero_forecast": zero_forecast,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = reconcile_run_dir(args.run_dir)
    except Exception as exc:
        report = {"status": "RECONCILIATION_FAILED", "error_type": type(exc).__name__}
        print(json.dumps(report, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
