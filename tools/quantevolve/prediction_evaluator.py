#!/usr/bin/env python3
"""QuantEvolve callback for NIFTY forecasting. Candidate source is never executed."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strategy_dsl import load_daily_csv, parse_spec_file, evaluate_spec, sha256_file  # noqa: E402


def _failed_metrics() -> dict[str, float]:
    return {
        "combined_score": -100.0, "can_run": 0.0, "sample_count": 0.0,
        "mae_skill_vs_zero": -100.0, "fold_skill_std": 100.0, "active_features": 0.0,
    }


def evaluate(program_path: str) -> dict[str, float]:
    """Upstream calls this callback; it parses literals and evaluates trusted code only."""
    try:
        data_path = os.environ.get("QE_DATA_PATH", "data/cache/nifty50_daily.csv")
        stage = os.environ.get("QE_EVAL_STAGE", "development")
        frame = load_daily_csv(data_path)
        spec = parse_spec_file(program_path)
        metrics = evaluate_spec(frame, spec, stage)["metrics"]
        if stage == "development":
            return {
                "combined_score": float(metrics["combined_score"]), "can_run": 1.0,
                "sample_count": float(metrics["sample_count"]),
                "mae_skill_vs_zero": float(metrics["mean_fold_mae_skill"]),
                "fold_skill_std": float(metrics["fold_skill_std"]),
                "active_features": float(metrics["active_features"]),
                "complexity_penalty": float(metrics["complexity_penalty"]),
            }
        return {
            "combined_score": float(metrics["mae_skill_vs_zero"]), "can_run": 1.0,
            "sample_count": float(metrics["sample_count"]),
            "mae_skill_vs_zero": float(metrics["mae_skill_vs_zero"]),
            "fold_skill_std": 0.0, "active_features": float(metrics["active_features"]),
        }
    except Exception:
        return _failed_metrics()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--data", default=os.environ.get("QE_DATA_PATH", "data/cache/nifty50_daily.csv"))
    parser.add_argument("--stage", choices=["development", "holdout"], default=None)
    args = parser.parse_args()
    stage = args.stage or os.environ.get("QE_EVAL_STAGE", "holdout")
    try:
        frame = load_daily_csv(args.data)
        spec = parse_spec_file(args.candidate)
        result = evaluate_spec(frame, spec, stage)
        report = {
            "status": "PASS", "evaluation_stage": stage,
            "upstream_candidate_executed": False,
            "candidate_source_sha256": sha256_file(args.candidate),
            "data_sha256": sha256_file(args.data),
            "n_total_rows": int(len(frame)), "n_development_rows": int(len(frame) * 0.80),
            "selected_spec": spec, **result["metrics"],
        }
        if "folds" in result:
            report["development_folds"] = result["folds"]
        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_json).write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
        print(json.dumps({k: report[k] for k in report if k not in {"selected_spec", "development_folds"}}, sort_keys=True))
        return 0
    except Exception as exc:
        report = {
            "status": "BLOCKED_OR_INVALID", "evaluation_stage": stage,
            "error_type": type(exc).__name__, "upstream_candidate_executed": False,
        }
        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_json).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
