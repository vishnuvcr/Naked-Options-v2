#!/usr/bin/env python3
"""Run a tightly bounded QuantEvolve prediction experiment and final holdout evaluation."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from strategy_dsl import parse_spec_file, sha256_file

UPSTREAM_PIN = "2df1e85758620e8ac0ca88ffc428b379d6cb9620"
ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs" / "quantevolve" / "prediction.yml"
INITIAL = ROOT / "tools" / "quantevolve" / "initial_prediction_strategy.py"
EVALUATOR = ROOT / "tools" / "quantevolve" / "prediction_evaluator.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_manifest(out: Path, payload: dict) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "run_manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def data_gate(data_path: Path) -> tuple[bool, str, dict]:
    manifest_path = ROOT / "reports" / "data_manifest.json"
    quality_path = ROOT / "reports" / "data_quality.json"
    if not data_path.is_file() or not manifest_path.is_file() or not quality_path.is_file():
        return False, "VALIDATED_DAILY_DATA_OR_MANIFEST_MISSING", {}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        quality = json.loads(quality_path.read_text(encoding="utf-8"))
        digest = sha256_file(data_path)
        if manifest.get("status") != "DATA_ACQUIRED" or manifest.get("target_sha256") != digest:
            return False, "ACQUISITION_MANIFEST_HASH_OR_STATUS_FAILED", {}
        if quality.get("validation") != "PASS" or quality.get("sha256") != digest:
            return False, "DAILY_DATA_VALIDATION_FAILED", {}
        if int(quality.get("rows", 0)) < 500:
            return False, "INSUFFICIENT_DAILY_HISTORY", {}
        return True, "PASS", {
            "data_sha256": digest, "data_rows": int(quality["rows"]),
            "data_first_date": quality.get("first_date"), "data_last_date": quality.get("last_date"),
            "data_source_ids": quality.get("source_ids", []),
            "selected_target_source": manifest.get("selected_target_source"),
        }
    except Exception as exc:
        return False, "DATA_GATE_ERROR_" + type(exc).__name__, {}


def clean_child_env(source: dict[str, str], keep_google_key: bool) -> dict[str, str]:
    env = dict(source)
    for key in (
        "DHAN_ACCESS_TOKEN", "HF_TOKEN", "GITHUB_TOKEN", "GH_TOKEN",
        "ACTIONS_RUNTIME_TOKEN", "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
        "ACTIONS_ID_TOKEN_REQUEST_URL", "GH_ENTERPRISE_TOKEN",
    ):
        env.pop(key, None)
    if not keep_google_key:
        env.pop("GOOGLE_API_KEY", None)
    return env


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream-dir", required=True, type=Path)
    parser.add_argument("--data", default="data/cache/nifty50_daily.csv")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--iterations", type=int, default=4)
    parser.add_argument("--run-id", default=os.getenv("GITHUB_RUN_ID", "local"))
    args = parser.parse_args()
    data_path = (ROOT / args.data).resolve()
    out = args.output if args.output.is_absolute() else (ROOT / args.output)
    out.mkdir(parents=True, exist_ok=True)
    iterations = max(1, min(4, int(args.iterations)))
    base = {
        "protocol": "QE-NIFTY-1.0", "track": "prediction", "run_id": str(args.run_id),
        "started_at_utc": utc_now(), "upstream_url": "https://github.com/tarsyang/quantevolve",
        "upstream_revision_expected": UPSTREAM_PIN, "python_version": sys.version.split()[0],
        "model": "gemini-3.8-flash", "iterations_requested": iterations,
        "config_sha256": sha256_file(CONFIG), "candidate_source_executed": False,
        "performance_claim": None,
    }
    ok, reason, meta = data_gate(data_path)
    if not ok:
        write_manifest(out, {**base, "status": "BLOCKED_DATA_GATE", "block_reason": reason})
        print(json.dumps({"status": "BLOCKED_DATA_GATE", "reason": reason}, sort_keys=True))
        return 0
    base.update(meta)
    if not os.getenv("GOOGLE_API_KEY"):
        write_manifest(out, {**base, "status": "BLOCKED_MISSING_GOOGLE_API_KEY", "block_reason": "secret unavailable to generation step"})
        print(json.dumps({"status": "BLOCKED_MISSING_GOOGLE_API_KEY"}, sort_keys=True))
        return 0
    if not args.upstream_dir.is_dir():
        write_manifest(out, {**base, "status": "BLOCKED_UPSTREAM_SETUP", "block_reason": "pinned upstream checkout is missing"})
        return 0
    try:
        actual_pin = subprocess.check_output(
            ["git", "-C", str(args.upstream_dir), "rev-parse", "HEAD"],
            text=True, stderr=subprocess.DEVNULL, timeout=10,
        ).strip()
    except Exception:
        actual_pin = ""
    if actual_pin != UPSTREAM_PIN:
        write_manifest(out, {**base, "status": "BLOCKED_UPSTREAM_REVISION_MISMATCH", "upstream_revision_actual": actual_pin})
        return 0

    env = clean_child_env(os.environ, keep_google_key=True)
    env["QE_DATA_PATH"] = str(data_path)
    env["QE_EVAL_STAGE"] = "development"
    out_abs = out.resolve()
    work_out = Path("/tmp") / ("quantevolve-work-" + str(args.run_id))
    shutil.rmtree(work_out, ignore_errors=True)
    work_out.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "quantevolve.cli",
        "--initial_strategy", str(INITIAL.resolve()),
        "--evaluator_file", str(EVALUATOR.resolve()),
        "--config", str(CONFIG.resolve()),
        "--output", str(work_out), "--iterations", str(iterations), "--log-level", "WARNING",
    ]
    try:
        result = subprocess.run(
            cmd, cwd=str(args.upstream_dir.resolve()), env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=900, check=False,
        )
    except subprocess.TimeoutExpired:
        shutil.rmtree(work_out, ignore_errors=True)
        write_manifest(out, {**base, "status": "EVOLUTION_TIMEOUT", "error_type": "TimeoutExpired"})
        return 0
    if result.returncode != 0:
        shutil.rmtree(work_out, ignore_errors=True)
        write_manifest(out, {**base, "status": "EVOLUTION_FAILED", "return_code": int(result.returncode), "error_type": "QuantEvolveCLIError"})
        return 0

    candidates = list(work_out.rglob("best_strategy.py"))
    candidates.sort(key=lambda p: (0 if p.parent.name == "best" else 1, len(p.parts)))
    if not candidates:
        shutil.rmtree(work_out, ignore_errors=True)
        write_manifest(out, {**base, "status": "EVOLUTION_NO_BEST_CANDIDATE", "error_type": "BestCandidateMissing"})
        return 0
    candidate = candidates[0]
    try:
        spec = parse_spec_file(candidate)
    except Exception as exc:
        shutil.rmtree(work_out, ignore_errors=True)
        write_manifest(out, {**base, "status": "EVOLUTION_BEST_SPEC_INVALID", "error_type": type(exc).__name__})
        return 0
    (out_abs / "best_strategy_spec.json").write_text(
        json.dumps(spec, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )

    # The API key and data-acquisition secrets are stripped from both evaluation child processes.
    final_env = clean_child_env(os.environ, keep_google_key=False)
    final_env["QE_DATA_PATH"] = str(data_path)
    reports = {}
    for stage in ("development", "holdout"):
        metric_path = out_abs / f"{stage}_metrics.json"
        check = subprocess.run(
            [sys.executable, str(EVALUATOR.resolve()), "--candidate", str(candidate.resolve()),
             "--output-json", str(metric_path), "--data", str(data_path), "--stage", stage],
            env=final_env, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, timeout=120, check=False,
        )
        if check.returncode != 0:
            shutil.rmtree(work_out, ignore_errors=True)
            write_manifest(out, {**base, "status": stage.upper() + "_METRICS_FAILED", "error_type": "MetricEvaluationError"})
            return 0
        reports[stage] = json.loads(metric_path.read_text(encoding="utf-8"))
        expected_status = "PASS" if stage == "development" else "PREDICTION_HOLDOUT_EVALUATED"
        if reports[stage].get("status") != expected_status:
            shutil.rmtree(work_out, ignore_errors=True)
            write_manifest(out, {**base, "status": stage.upper() + "_REPORT_INVALID", "error_type": "MetricReportValidationError"})
            return 0

    # Upstream source, checkpoints and logs were stored under /tmp and are never published.
    shutil.rmtree(work_out, ignore_errors=True)

    holdout = reports["holdout"]
    final_manifest = {
        **base, "status": "PREDICTION_HOLDOUT_EVALUATED", "completed_at_utc": utc_now(),
        "upstream_revision_actual": actual_pin, "iterations_completed": iterations,
        "holdout_sample_count": int(holdout["sample_count"]),
        "holdout_start_date": holdout["holdout_start_date"], "holdout_end_date": holdout["holdout_end_date"],
        "holdout_mae_skill_vs_zero": float(holdout["mae_skill_vs_zero"]),
        "holdout_mae_improvement_ci95": [
            float(holdout["mae_improvement_ci95_low"]), float(holdout["mae_improvement_ci95_high"])
        ],
        "candidate_source_sha256": holdout["candidate_source_sha256"],
        "final_holdout_used_for_candidate_selection": False,
        "warning": "Single selected candidate tested once; not a profitable trading claim or proof of universal model superiority.",
    }
    write_manifest(out_abs, final_manifest)
    print(json.dumps({
        "status": final_manifest["status"], "run_id": str(args.run_id),
        "data_rows": final_manifest["data_rows"], "holdout_n": final_manifest["holdout_sample_count"],
        "mae_skill_vs_zero": final_manifest["holdout_mae_skill_vs_zero"],
        "mae_improvement_ci95": final_manifest["holdout_mae_improvement_ci95"],
        "candidate_source_executed": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
