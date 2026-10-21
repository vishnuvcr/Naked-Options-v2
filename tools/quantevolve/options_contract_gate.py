#!/usr/bin/env python3
"""Gate historical options data before any candidate evaluation or P&L."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED = {
    "timestamp", "expiry", "strike", "option_type",
    "open", "high", "low", "close", "volume", "lot_size",
}
KEY = ["timestamp", "expiry", "strike", "option_type"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_options(input_path: Path, manifest_path: Path, underlying_path: Path) -> dict[str, Any]:
    report: dict[str, Any] = {
        "protocol": "QE-NIFTY-1.0",
        "status": "BLOCKED_NO_VERIFIED_CONTRACT_DATA",
        "pnl_permitted": False,
        "input_path": str(input_path),
        "source_manifest_path": str(manifest_path),
        "required_contract_fields": sorted(REQUIRED),
        "coverage_gate": 0.80,
        "conflicting_duplicate_group_rate_gate": 0.01,
        "claim": None,
    }
    if not input_path.is_file() or not manifest_path.is_file():
        report["block_reason"] = "options data file or provenance/source manifest is absent"
        return report
    try:
        source = json.loads(manifest_path.read_text(encoding="utf-8"))
        actual_hash = sha256(input_path)
        if source.get("status") != "PASS":
            report["block_reason"] = "source manifest status is not PASS"
            return report
        if source.get("source_sha256") != actual_hash:
            report["block_reason"] = "options file hash does not match source manifest"
            return report
        if source.get("official_expiry_reconciled") is not True:
            report["block_reason"] = "official expiry-date reconciliation is not verified"
            return report
        if source.get("lot_size_history_verified") is not True:
            report["block_reason"] = "historical lot-size mapping is not verified"
            return report
        if source.get("license_review_status") not in {"PASS", "PASS_NONCOMMERCIAL"}:
            report["block_reason"] = "source license/use review is not cleared"
            return report
        if source.get("timestamp_timezone") != "Asia/Kolkata":
            report["block_reason"] = "exchange-local timestamp timezone is not declared"
            return report
        if source.get("executable_price_policy") not in {"BID_ASK", "OHLC_ADVERSE_PROXY"}:
            report["block_reason"] = "no explicit executable-side pricing policy is approved"
            return report
        frame = pd.read_parquet(input_path) if input_path.suffix.lower() == ".parquet" else pd.read_csv(input_path)
        missing = sorted(REQUIRED - set(frame.columns))
        if missing:
            report["block_reason"] = "required contract identity/lot-size fields are missing"
            report["missing_columns"] = missing
            return report
        frame = frame.copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce", utc=True).dt.tz_convert("Asia/Kolkata")
        frame["expiry"] = pd.to_datetime(frame["expiry"], errors="coerce").dt.date
        for col in ("strike", "open", "high", "low", "close", "volume", "lot_size"):
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
        frame["option_type"] = frame["option_type"].astype(str).str.upper().str.strip()
        frame["local_date"] = frame["timestamp"].dt.date
        invalid = (
            frame["timestamp"].isna() | frame["expiry"].isna()
            | frame["strike"].isna() | (frame["strike"] <= 0)
            | ~frame["option_type"].isin({"CE", "PE", "CALL", "PUT"})
            | frame[["open", "high", "low", "close"]].isna().any(axis=1)
            | (frame[["open", "high", "low", "close"]] <= 0).any(axis=1)
            | frame["lot_size"].isna() | (frame["lot_size"] <= 0)
            | (frame["local_date"] > frame["expiry"])
        )
        report["raw_rows"] = int(len(frame))
        report["invalid_rows"] = int(invalid.sum())
        if invalid.any() or frame.empty:
            report["block_reason"] = "invalid option rows or empty dataset"
            return report
        duplicate_rows = frame[frame.duplicated(KEY, keep=False)]
        dup_groups = 0
        conflict_groups = 0
        if not duplicate_rows.empty:
            unique_keys = duplicate_rows[KEY].drop_duplicates()
            dup_groups = int(len(unique_keys))
            compare_cols = ["open", "high", "low", "close", "volume", "lot_size"]
            for key_values in unique_keys.itertuples(index=False, name=None):
                group = duplicate_rows
                for col, value in zip(KEY, key_values):
                    group = group[group[col] == value]
                if len(group[compare_cols].drop_duplicates()) > 1:
                    conflict_groups += 1
        conflict_rate = conflict_groups / dup_groups if dup_groups else 0.0
        report["duplicate_groups"] = dup_groups
        report["conflicting_duplicate_groups"] = conflict_groups
        report["conflicting_duplicate_group_rate"] = conflict_rate
        if not underlying_path.is_file():
            report["block_reason"] = "validated NIFTY session file is absent for coverage calculation"
            return report
        underlying = pd.read_csv(underlying_path)
        if "date" not in underlying.columns:
            report["block_reason"] = "underlying file lacks date column"
            return report
        session_dates = set(pd.to_datetime(underlying["date"], errors="coerce").dropna().dt.date)
        option_dates = set(frame["local_date"])
        overlap = sorted(d for d in session_dates if frame["local_date"].min() <= d <= frame["local_date"].max())
        covered = len(set(overlap) & option_dates)
        coverage = covered / len(overlap) if overlap else 0.0
        report["nifty_sessions_in_overlap"] = len(overlap)
        report["options_covered_sessions"] = covered
        report["eligible_date_coverage"] = coverage
        report["source_license"] = source.get("source_license")
        report["pricing_policy"] = source.get("executable_price_policy")
        if conflict_rate > 0.01 or coverage < 0.80:
            report["block_reason"] = "fixed data-quality gate failed"
            return report
        report.update({
            "status": "PASS", "block_reason": None, "pnl_permitted": True,
            "claim": "Source/contract quality gate only; this does not imply candidate profitability.",
        })
        return report
    except Exception as exc:
        report["status"] = "BLOCKED_GATE_ERROR"
        report["block_reason"] = "sanitized gate exception: " + type(exc).__name__
        return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/cache/nifty_options_contracts.csv")
    parser.add_argument("--source-manifest", default="data/cache/options_source_manifest.json")
    parser.add_argument("--underlying", default="data/cache/nifty50_daily.csv")
    parser.add_argument("--output", default="reports/quantevolve/options_data_gate.json")
    args = parser.parse_args()
    report = inspect_options(Path(args.input), Path(args.source_manifest), Path(args.underlying))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "block_reason", "pnl_permitted")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
