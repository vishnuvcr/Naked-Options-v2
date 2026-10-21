#!/usr/bin/env python3
"""Bounded, non-P&L audit of public NIFTY option parquet samples on Hugging Face.

Downloads at most three expiry files. Raw licensed data stays in the cache and is never
published. The report deliberately remains blocked unless official expiry and historical
lot-size reconciliation can be established independently.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import date
from pathlib import Path

import pandas as pd
from huggingface_hub import HfApi, hf_hub_download
import pyarrow.parquet as pq

REPO_ID = "thetrademarkk/india-index-options-1m"
SOURCE_URL = "https://huggingface.co/datasets/thetrademarkk/india-index-options-1m"
LICENSE = "CC-BY-NC-4.0"
ATTRIBUTION = "thetrademarkk, India Index & Options - 1-minute OHLC dataset"
REQUIRED = {"timestamp", "open", "high", "low", "close", "volume", "strike", "option_type", "expiry"}

OFFICIAL_SAMPLE_MAP = {
    "2021-05-27": {
        "lot_size": 75, "expected_expiry_weekday": "Thursday",
        "circulars": [
            "https://nsearchives.nseindia.com/content/circulars/FAOP47854.pdf",
            "https://nsearchives.nseindia.com/content/circulars/FAOP68589.pdf",
        ],
        "basis": "NSE FAOP47854: May/June 2021 monthly expiries retain old 75 lot; weekly switch starts Aug 2021. Expiry remained Thursday.",
    },
    "2024-01-04": {
        "lot_size": 50, "expected_expiry_weekday": "Thursday",
        "circulars": [
            "https://nsearchives.nseindia.com/content/circulars/FAOP47854.pdf",
            "https://nsearchives.nseindia.com/content/circulars/FAOP56233.pdf",
            "https://nsearchives.nseindia.com/content/circulars/FAOP61415.pdf",
            "https://nsearchives.nseindia.com/content/circulars/FAOP68589.pdf",
        ],
        "basis": "NSE 2021 circular sets 50 for weekly contracts from Aug 2021 onward; March 2023 retains 50; April 2024 changes contracts available from Apr 26, 2024 onward to 25.",
    },
    "2026-08-04": {
        "lot_size": 65, "expected_expiry_weekday": "Tuesday",
        "circulars": [
            "https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf",
            "https://nsearchives.nseindia.com/content/circulars/FAOP68589.pdf",
            "https://nsearchives.nseindia.com/content/circulars/FAOP68685.pdf",
        ],
        "basis": "NSE FAOP70616: first revised NIFTY weekly lot expiry is 06-Jan-2026 at 65; weekly expiry day changed to Tuesday for expiries on/after 01-Sep-2025.",
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def expiry_from_path(path: str) -> date | None:
    try:
        return date.fromisoformat(Path(path).stem)
    except ValueError:
        return None


def select_sample_files(paths: list[str], limit: int = 3) -> list[str]:
    """Choose earliest, median-era, and latest dated NIFTY expiry files, deterministically."""
    dated = sorted((expiry_from_path(path), path) for path in paths if expiry_from_path(path) is not None)
    if not dated:
        return []
    targets = [dated[0][0], date(2024, 1, 1), dated[-1][0]]
    selected = []
    for target in targets:
        candidate = min(dated, key=lambda item: (abs((item[0] - target).days), item[0], item[1]))[1]
        if candidate not in selected:
            selected.append(candidate)
    return selected[: max(1, min(limit, 3))]


def audit(cache_dir: Path, output_path: Path, manifest_path: Path, token: str | None) -> dict:
    cache_dir.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    api = HfApi(token=token or None)
    repo_files = api.list_repo_files(repo_id=REPO_ID, repo_type="dataset")
    options_files = [
        path for path in repo_files
        if path.startswith("options/NIFTY/") and path.lower().endswith(".parquet")
    ]
    selected = select_sample_files(options_files, limit=3)
    if not selected:
        raise RuntimeError("public HF repository listing returned no dated options/NIFTY parquet files")

    file_reports = []
    schema_union: set[str] = set()
    total_rows = 0
    total_bytes = 0
    lot_size_present = True
    expiry_present = True
    timezone_examples = []
    for remote_path in selected:
        local = Path(hf_hub_download(
            repo_id=REPO_ID, filename=remote_path, repo_type="dataset",
            token=token or None, local_dir=str(cache_dir),
        ))
        parquet = pq.ParquetFile(local)
        columns = set(parquet.schema_arrow.names)
        schema_union.update(columns)
        lot_size_present = lot_size_present and ("lot_size" in columns)
        expiry_present = expiry_present and ("expiry" in columns)
        rows = int(parquet.metadata.num_rows or 0)
        total_rows += rows
        total_bytes += local.stat().st_size
        item = {
            "repo_path": remote_path,
            "expiry_from_filename": expiry_from_path(remote_path).isoformat(),
            "rows": rows,
            "download_bytes": local.stat().st_size,
            "sha256": sha256_file(local),
            "columns": sorted(columns),
            "lot_size_column_present": "lot_size" in columns,
            "expiry_column_present": "expiry" in columns,
        }
        # Only inspect a tiny row-group/table head for timestamp timezone metadata.
        try:
            timestamp_field = parquet.schema_arrow.field("timestamp")
            item["timestamp_type"] = str(timestamp_field.type)
            if "tz=+05:30" in str(timestamp_field.type) or "Asia/Kolkata" in str(timestamp_field.type):
                timezone_examples.append("Asia/Kolkata")
        except (KeyError, IndexError):
            item["timestamp_type"] = None
        # Inspect selected identity fields across every row of each bounded file.
        # Only counts and small categorical summaries are published, never market rows.
        reconciliation = {
            "file_expiry": remote_path.split("/")[-1].removesuffix(".parquet"),
            "file_expiry_matches_all_rows": False,
            "expected_expiry_weekday": None,
            "observed_expiry_weekday": None,
            "official_lot_size": None,
            "lot_size_source_circulars": [],
            "official_lot_size_mapping_status": "NOT_MAPPED",
            "valid_strike_rows": 0,
            "valid_option_type_rows": 0,
            "nifty_symbol_rows": 0,
            "unique_expiry_count": 0,
            "unique_symbol_sample": [],
        }
        cohort = OFFICIAL_SAMPLE_MAP.get(reconciliation["file_expiry"])
        if cohort:
            reconciliation["expected_expiry_weekday"] = cohort["expected_expiry_weekday"]
            reconciliation["official_lot_size"] = cohort["lot_size"]
            reconciliation["lot_size_source_circulars"] = cohort["circulars"]
            reconciliation["lot_size_basis"] = cohort["basis"]
            reconciliation["official_lot_size_mapping_status"] = "MAPPED_TO_OFFICIAL_NSE_CIRCULARS"
        try:
            projected = parquet.read(columns=["expiry", "strike", "option_type", "symbol"])
            expiries = pd.to_datetime(projected["expiry"].to_pandas(), errors="coerce").dt.date
            file_expiry = expiry_from_path(remote_path)
            reconciliation["unique_expiry_count"] = int(expiries.dropna().nunique())
            reconciliation["file_expiry_matches_all_rows"] = bool(
                len(expiries) > 0 and expiries.notna().all() and (expiries == file_expiry).all()
            )
            reconciliation["observed_expiry_weekday"] = file_expiry.strftime("%A") if file_expiry else None
            strikes = pd.to_numeric(projected["strike"].to_pandas(), errors="coerce")
            reconciliation["valid_strike_rows"] = int((strikes.gt(0) & strikes.notna()).sum())
            option_types = projected["option_type"].to_pandas().astype(str).str.upper().str.strip()
            reconciliation["valid_option_type_rows"] = int(option_types.isin({"CE", "PE", "CALL", "PUT"}).sum())
            symbols = projected["symbol"].to_pandas().astype(str).str.upper().str.strip()
            reconciliation["nifty_symbol_rows"] = int(symbols.str.contains("NIFTY", regex=False).sum())
            reconciliation["unique_symbol_sample"] = sorted(symbols.dropna().unique().tolist())[:5]
            if cohort and reconciliation["file_expiry_matches_all_rows"] and (
                reconciliation["observed_expiry_weekday"] == cohort["expected_expiry_weekday"]
            ) and reconciliation["valid_strike_rows"] == rows and (
                reconciliation["valid_option_type_rows"] == rows
            ) and reconciliation["nifty_symbol_rows"] == rows:
                reconciliation["sample_contract_checks_status"] = "PASS"
            else:
                reconciliation["sample_contract_checks_status"] = "FAIL_OR_UNVERIFIED"
        except Exception as exc:
            reconciliation["sample_contract_checks_status"] = "CHECK_ERROR_" + type(exc).__name__
        item["sample_contract_reconciliation"] = reconciliation
        file_reports.append(item)

    has_identity_columns = REQUIRED.issubset(schema_union)
    sample_reconciliations = [item.get("sample_contract_reconciliation", {}) for item in file_reports]
    sample_reconciliation_pass = bool(
        len(sample_reconciliations) == len(file_reports) and file_reports and
        all(x.get("sample_contract_checks_status") == "PASS" for x in sample_reconciliations)
    )
    report = {
        "protocol": "QE-NIFTY-1.0",
        "audit_type": "bounded_public_source_schema_audit",
        "status": "BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED",
        "pnl_permitted": False,
        "claim": None,
        "source": {
            "repo_id": REPO_ID,
            "url": SOURCE_URL,
            "license": LICENSE,
            "attribution": ATTRIBUTION,
            "source_scope": "NIFTY option OHLCV bars sampled from files partitioned by expiry",
            "raw_source_data_committed": False,
        },
        "sample": {
            "file_count": len(file_reports),
            "total_rows": total_rows,
            "sample_expiry_and_lot_reconciliation_status": (
                "PASS_ALL_THREE_SAMPLED_COHORTS" if sample_reconciliation_pass else "PARTIAL_OR_BLOCKED"
            ),
            "sample_lot_size_mapping_all_verified": bool(sample_reconciliation_pass and all(
                x.get("official_lot_size_mapping_status") == "MAPPED_TO_OFFICIAL_NSE_CIRCULARS"
                for x in sample_reconciliations
            )),
            "total_download_bytes": total_bytes,
            "schema_union": sorted(schema_union),
            "required_identity_and_ohlcv_columns_present": has_identity_columns,
            "lot_size_column_present_in_all_samples": lot_size_present,
            "expiry_column_present_in_all_samples": expiry_present,
            "timezone_metadata_examples": sorted(set(timezone_examples)),
            "files": file_reports,
        },
        "official_exchange_circulars_reviewed": [
            {"url": "https://nsearchives.nseindia.com/content/circulars/FAOP47854.pdf", "finding": "2021 NIFTY weekly/monthly lot-size transition: old 75 lot retained for May/June monthly contracts; 50 applies from later monthly/weekly cohorts."},
            {"url": "https://nsearchives.nseindia.com/content/circulars/FAOP56233.pdf", "finding": "March 2023 NIFTY market lot remains 50."},
            {"url": "https://nsearchives.nseindia.com/content/circulars/FAOP61415.pdf", "finding": "NIFTY lot changes 50 to 25 for contracts available from 26-Apr-2024 onward."},
            {"url": "https://nsearchives.nseindia.com/content/circulars/FAOP64625.pdf", "finding": "NIFTY lot changes 25 to 75 for newly introduced contracts from 20-Nov-2024 with expiry-cohort transition dates."},
            {"url": "https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf", "finding": "NIFTY lot changes 75 to 65; first revised weekly expiry 06-Jan-2026 and monthly expiry 27-Jan-2026."},
            {"url": "https://nsearchives.nseindia.com/content/circulars/FAOP68589.pdf", "finding": "NIFTY expiry day transitions from Thursday to Tuesday for new expiries on/after 01-Sep-2025."}
        ],
        "limitations": [
            "The circular reconciliation covers only the three sampled expiry cohorts, not every expiry/contract in the source history.",
            "Full official MII contract-master row matching was not completed for the 2021 and January 2024 sample dates; circular-based lot size and expiry weekday corroboration is not a complete row-by-row master match.",
            "OHLC bars are not historical bid/ask quotes and cannot by themselves prove executable fills.",
            "Three expiry samples do not establish full-history coverage or contract continuity.",
            "The dataset is CC-BY-NC-4.0; raw files must not be redistributed in public reports or repository commits.",
        ],
        "next_gate": "Reconcile exact expiry and historical lot size against official NSE contract files; measure full eligible-date coverage and conflicting duplicates before constructing a backtest ledger.",
    }
    report["sample"]["sample_hash_manifest_sha256"] = hashlib.sha256(
        json.dumps(file_reports, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Deliberately blocked manifest: it cannot open the options P&L gate.
    manifest = {
        "status": "BLOCKED",
        "source": REPO_ID,
        "source_url": SOURCE_URL,
        "source_license": LICENSE,
        "attribution": ATTRIBUTION,
        "sample_hash_manifest_sha256": report["sample"]["sample_hash_manifest_sha256"],
        "official_expiry_reconciled": False,
        "lot_size_history_verified": False,
        "sampled_expiry_cohorts_lot_size_mapped": report["sample"]["sample_lot_size_mapping_all_verified"],
        "license_review_status": "REVIEW_REQUIRED_CC_BY_NC_4.0",
        "timestamp_timezone": "Asia/Kolkata" if timezone_examples else "UNVERIFIED",
        "executable_price_policy": "OHLC_ADVERSE_PROXY",
        "block_reason": "bounded schema audit only; official expiry, historical lot size, full coverage and executable quotes are not verified",
        "raw_source_data_committed": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, default=Path("data/cache/quantevolve-options-source-audit"))
    parser.add_argument("--output", type=Path, default=Path("reports/quantevolve/options_source_audit.json"))
    parser.add_argument("--manifest", type=Path, default=Path("data/cache/options_source_manifest.json"))
    args = parser.parse_args()
    try:
        report = audit(args.cache_dir, args.output, args.manifest, os.getenv("HF_TOKEN"))
        print(json.dumps({
            "status": report["status"],
            "sample_files": report["sample"]["file_count"],
            "sample_rows": report["sample"]["total_rows"],
            "pnl_permitted": report["pnl_permitted"],
        }, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "protocol": "QE-NIFTY-1.0",
            "status": "SOURCE_AUDIT_FAILED",
            "pnl_permitted": False,
            "error_type": type(exc).__name__,
            "claim": None,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, sort_keys=True))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
