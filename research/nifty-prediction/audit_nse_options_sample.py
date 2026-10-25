#!/usr/bin/env python3
"""Fetch a bounded set of official NSE F&O bhavcopies and audit schema/coverage.

This is a data-validation gate, not a model training script. It keeps raw files
out of Git; GitHub Actions uploads them as an artifact and commits only a manifest.
"""
from __future__ import annotations
import csv, hashlib, io, json, os, sys, time, zipfile
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

OUT = Path("reports/nifty-prediction/nse_options_sample_audit.json")
RAW = Path("data/cache/nse-options-sample")
SAMPLES = [
    ("legacy_pre_format_change", "20240705", "https://archives.nseindia.com/content/historical/DERIVATIVES/2024/JUL/fo05JUL2024bhav.csv.zip"),
    ("udiff_format_change_day", "20240708", "https://archives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_20240708_F_0000.csv.zip"),
    ("recent_session", "20261023", "https://archives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_20261023_F_0000.csv.zip"),
]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research-data-audit/1.0)", "Accept": "*/*"}

def fetch(url: str) -> bytes:
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=45) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status} for {url}")
        data = response.read()
    if not data.startswith(b"PK"):
        raise RuntimeError(f"Response is not a ZIP archive: {url}")
    return data

def audit_one(name: str, expected_date: str, url: str) -> dict:
    try:
        blob = fetch(url)
        digest = hashlib.sha256(blob).hexdigest()
        RAW.mkdir(parents=True, exist_ok=True)
        raw_path = RAW / f"{expected_date}.zip"
        raw_path.write_bytes(blob)
        with zipfile.ZipFile(io.BytesIO(blob)) as zf:
            members = [m for m in zf.namelist() if m.lower().endswith(".csv")]
            if not members:
                raise RuntimeError(f"No CSV member in ZIP: {zf.namelist()}")
            member = max(members, key=lambda m: zf.getinfo(m).file_size)
            with zf.open(member) as fh:
                # Read header and a bounded sample, avoiding a full DataFrame load.
                text = io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace", newline="")
                reader = csv.DictReader(text)
                columns = reader.fieldnames or []
                rows = []
                for row in reader:
                    rows.append(row)
                    if len(rows) >= 10000:
                        break
        norm = {c.strip().upper(): c for c in columns}
        date_cols = [c for c in columns if "DATE" in c.upper() or "TIMESTAMP" in c.upper()]
        instrument_cols = [c for c in columns if any(k in c.upper() for k in ("SYMBOL", "TCKR", "UNDERLYING"))]
        option_cols = [c for c in columns if any(k in c.upper() for k in ("OPTION", "OPT_TYP", "STRIKE", "EXPIRY"))]
        symbols = sorted({str(row.get(norm.get("TCKR SYMBOL", norm.get("SYMBOL", "")), "")).strip().upper() for row in rows})
        return {
            "sample": name, "expected_trade_date": expected_date, "url": url,
            "status": "DOWNLOADED_AND_PARSED", "http_bytes": len(blob),
            "sha256": digest, "zip_member": member, "columns": columns,
            "sample_rows_parsed": len(rows), "date_columns": date_cols,
            "instrument_columns": instrument_cols, "option_related_columns": option_cols,
            "sample_symbols": symbols[:40],
            "notes": "Header and up to 10,000 rows inspected. Date/contract semantics still require format-specific validation."
        }
    except Exception as exc:
        return {"sample": name, "expected_trade_date": expected_date, "url": url,
                "status": "FAILED", "error": f"{type(exc).__name__}: {exc}"}

def main() -> int:
    results = []
    for i, sample in enumerate(SAMPLES):
        results.append(audit_one(*sample))
        if i < len(SAMPLES) - 1:
            time.sleep(2)
    successful = sum(r["status"] == "DOWNLOADED_AND_PARSED" for r in results)
    report = {
        "study": "Bounded official NSE F&O bhavcopy source and schema audit",
        "generated_utc": os.environ.get("GITHUB_RUN_ID", "local-run"),
        "status": "ALL_SAMPLES_PARSED" if successful == len(SAMPLES) else "PARTIAL_OR_FAILED",
        "successful_samples": successful, "sample_count": len(SAMPLES),
        "format_change_reference": "NSE legacy F&O bhavcopy discontinued effective 2024-07-08; UDiFF format thereafter",
        "samples": results,
        "limitations": [
            "A successful HTTP download does not independently prove authenticity; compare hashes and records to the official reports portal.",
            "This is a three-date schema smoke test, not a complete historical backfill or model-ready dataset.",
            "The legacy and UDiFF schemas may differ; do not concatenate until a tested canonical mapping exists.",
            "Raw ZIPs are retained as a workflow artifact, not committed to Git."
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "successful_samples": successful, "sample_count": len(SAMPLES)}, indent=2))
    return 0 if successful == len(SAMPLES) else 1

if __name__ == "__main__":
    sys.exit(main())
