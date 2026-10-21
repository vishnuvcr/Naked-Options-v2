#!/usr/bin/env python3
"""Persist only allowlisted sanitized reports and update research records from an artifact."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED = {
    "run_manifest.json", "development_metrics.json", "holdout_metrics.json",
    "best_strategy_spec.json", "options_data_gate.json", "options_source_audit.json",
}


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def safe_number(value, digits: int = 6) -> str:
    try:
        n = float(value)
        if n != n or n in (float("inf"), float("-inf")):
            return "not available"
        return f"{n:.{digits}f}"
    except (TypeError, ValueError, OverflowError):
        return "not available"


def append_once(path: Path, marker: str, text: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    inbox = args.artifact_root.resolve()
    copied = []
    if inbox.exists():
        for manifest_file in inbox.rglob("run_manifest.json"):
            relative = manifest_file.parent.relative_to(inbox)
            if relative.parts[:2] == ("reports", "quantevolve"):
                relative = Path(*relative.parts[2:])
            dest_dir = ROOT / "reports" / "quantevolve" / relative
            dest_dir.mkdir(parents=True, exist_ok=True)
            for child in manifest_file.parent.iterdir():
                if child.is_file() and child.name in ALLOWED:
                    shutil.copy2(child, dest_dir / child.name)
                    copied.append(str((dest_dir / child.name).relative_to(ROOT)))
        for audit_file in inbox.rglob("options_source_audit.json"):
            dest = ROOT / "reports" / "quantevolve" / "options_source_audit.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(audit_file, dest)
            copied.append(str(dest.relative_to(ROOT)))
        for gate_file in inbox.rglob("options_data_gate.json"):
            dest = ROOT / "reports" / "quantevolve" / "options_data_gate.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(gate_file, dest)
            copied.append(str(dest.relative_to(ROOT)))

    reports_root = ROOT / "reports" / "quantevolve"
    manifest_path = next(
        (p for p in reports_root.rglob("run_manifest.json")
         if str(read_json(p).get("run_id", "")) == str(args.run_id)),
        None,
    )
    manifest = read_json(manifest_path) if manifest_path else {}
    # Reconcile only earlier bundles whose hashes, selected spec and metric arithmetic pass checks.
    import subprocess, sys
    reconciler = ROOT / "tools" / "quantevolve" / "reconcile_run.py"
    if reconciler.is_file():
        for stale_manifest in reports_root.rglob("run_manifest.json"):
            subprocess.run(
                [sys.executable, str(reconciler), "--run-dir", str(stale_manifest.parent)],
                cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                timeout=30, check=False,
            )

    status = manifest.get("status", "NO_RUN_MANIFEST")
    holdout_path = manifest_path.parent / "holdout_metrics.json" if manifest_path else None
    holdout = read_json(holdout_path) if holdout_path and holdout_path.exists() else {}
    gate = read_json(reports_root / "options_data_gate.json")
    run_marker = f"QE-DELIVERY-{args.run_id}"
    stamp = datetime.now(timezone.utc).isoformat()
    if status == "PREDICTION_HOLDOUT_EVALUATED" and holdout.get("status") == "PREDICTION_HOLDOUT_EVALUATED":
        summary = (
            f"### {run_marker} — {stamp}\n"
            f"- Prediction run status: **{status}**. Candidate source was never executed; only a validated declarative spec was retained.\n"
            f"- Final chronological holdout: n={int(holdout.get('sample_count', 0))}; "
            f"target dates {holdout.get('holdout_start_date', 'n/a')} to {holdout.get('holdout_end_date', 'n/a')}.\n"
            f"- MAE skill vs zero-return baseline: {safe_number(holdout.get('mae_skill_vs_zero'))}; "
            f"directional accuracy: {safe_number(holdout.get('directional_accuracy'))}; "
            f"MAE-improvement 95% circular block-bootstrap interval: "
            f"[{safe_number(holdout.get('mae_improvement_ci95_low'))}, {safe_number(holdout.get('mae_improvement_ci95_high'))}].\n"
            f"- Interpretation: one selected candidate evaluated once against a zero-return forecast; not proof of a profitable trading strategy or universal superiority.\n"
            f"- Published reports: {', '.join(p for p in copied if f'run-{args.run_id}' in p) or 'report path not found in current artifact.'}"
        )
    else:
        reason = manifest.get("block_reason") or manifest.get("error_type") or "no successful holdout report"
        summary = (
            f"### {run_marker} — {stamp}\n"
            f"- Prediction run status: **{status}**; sanitized reason: {reason}.\n"
            "- No valid QuantEvolve prediction holdout result is claimed."
        )
    append_once(ROOT / "research" / "EXPERIMENT_LOG.md", run_marker, summary)
    append_once(
        ROOT / "research" / "QUANTEvolve_INTEGRATION_STATUS.md",
        run_marker,
        f"## {run_marker}\n\n{summary}\n\n"
        f"Options data gate: **{gate.get('status', 'NOT_REPORTED')}**; "
        f"P&L permitted={gate.get('pnl_permitted', False)}. Options strategy P&L stays blocked until the source/contract gate passes.",
    )
    append_once(
        ROOT / "research" / "QUANTEvolve_INTEGRATION_ERROR_LOG.md",
        run_marker,
        f"## {run_marker} — automated run record\n- Date: {stamp}\n- Run status: {status}\n"
        f"- Reason/error classification: {manifest.get('block_reason') or manifest.get('error_type') or 'No runtime error reported in the sanitized manifest.'}\n"
        f"- Options data gate: {gate.get('status', 'NOT_REPORTED')}; P&L permitted={gate.get('pnl_permitted', False)}.\n"
        "- No API key or credential value is persisted.",
    )
    append_once(
        ROOT / "README.md",
        run_marker,
        f"## QuantEvolve automated run — {args.run_id}\n\n{summary}\n\n"
        "- [Integration plan](research/QUANTEvolve_INTEGRATION_PLAN.md)\n"
        "- [Phase status](research/QUANTEvolve_INTEGRATION_STATUS.md)\n"
        "- [Error log](research/QUANTEvolve_INTEGRATION_ERROR_LOG.md)",
    )
    print(json.dumps({
        "run_id": str(args.run_id), "prediction_status": status,
        "options_gate_status": gate.get("status", "NOT_REPORTED"),
        "copied_report_files": sorted(set(copied)),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
