#!/usr/bin/env python3
"""Feasibility audit of a public HF NIFTY intraday options file; never publish raw rows."""
from __future__ import annotations
import json, os, hashlib
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
from huggingface_hub import hf_hub_download

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "vol_regime_hf_probe"
OUT = ROOT / "reports" / "vol_regime_options" / "hf_dataset_audit.json"
REPO = "rissin/nse-options-intraday"
FILE = "upstox_intraday/NIFTY/NIFTY_2025.parquet"
TOKEN = os.getenv("HF_TOKEN", "").strip()

def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "study": "VOL-REGIME-OPT-1.0",
        "phase": "2-free-source-discovery",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "Hugging Face dataset rissin/nse-options-intraday",
        "repo_id": REPO,
        "file": FILE,
        "token_present": bool(TOKEN),
        "public_card_license": "other (not a recognized explicit license)",
        "provenance_note": "Dataset card attributes intraday records to Upstox historical API and asks users to follow provider terms for redistribution.",
        "raw_data_policy": "Do not commit or upload raw data; license/provenance review is required before publishing derived confirmatory results.",
    }
    try:
        local = hf_hub_download(
            repo_id=REPO,
            filename=FILE,
            repo_type="dataset",
            token=TOKEN or None,
            cache_dir=str(CACHE / "hf_home"),
        )
        h = hashlib.sha256()
        with open(local, "rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                h.update(block)
        cols = ["date","timestamp","underlying","expiry","strike","option_type",
                "open","high","low","close","volume","oi","source","granularity"]
        df = pd.read_parquet(local, columns=cols)
        report["file_bytes"] = Path(local).stat().st_size
        report["file_sha256"] = h.hexdigest()
        report["file_rows"] = int(len(df))
        report["columns"] = list(df.columns)
        report["underlying_values"] = sorted(df["underlying"].dropna().astype(str).unique().tolist())
        report["granularity_values"] = sorted(df["granularity"].dropna().astype(str).unique().tolist())
        nift = df[(df["underlying"].astype(str) == "NIFTY") & (df["granularity"].astype(str) == "1min")].copy()
        report["nifty_1min_rows"] = int(len(nift))
        report["date_min"] = str(nift["date"].min()) if len(nift) else None
        report["date_max"] = str(nift["date"].max()) if len(nift) else None
        report["expiry_count"] = int(nift["expiry"].nunique(dropna=True))
        report["expiry_min"] = str(nift["expiry"].min()) if len(nift) else None
        report["expiry_max"] = str(nift["expiry"].max()) if len(nift) else None
        report["option_types"] = sorted(nift["option_type"].dropna().astype(str).unique().tolist())
        report["source_values"] = sorted(nift["source"].dropna().astype(str).unique().tolist())
        key = ["timestamp","expiry","strike","option_type"]
        report["duplicate_key_rows"] = int(nift.duplicated(key, keep=False).sum())
        required = ["timestamp","expiry","strike","option_type","open","high","low","close","volume"]
        report["missing_required_by_column"] = {c:int(nift[c].isna().sum()) for c in required}
        prices = nift[["open","high","low","close"]]
        report["nonpositive_ohlc_rows"] = int((prices.le(0).any(axis=1) | prices.isna().any(axis=1)).sum())
        report["invalid_ohlc_order_rows"] = int(((nift["high"] < nift[["open","close","low"]].max(axis=1)) |
                                                  (nift["low"] > nift[["open","close","high"]].min(axis=1))).sum())
        ts = pd.to_datetime(nift["timestamp"], errors="coerce")
        report["unparseable_timestamps"] = int(ts.isna().sum())
        report["timestamp_min"] = str(ts.min()) if len(ts) else None
        report["timestamp_max"] = str(ts.max()) if len(ts) else None
        # Bar availability counts are diagnostic only; strategy coverage requires contract-level matching.
        report["entry_0920_rows"] = int((ts.dt.strftime("%H:%M") == "09:20").sum())
        report["last_bar_1524_rows"] = int((ts.dt.strftime("%H:%M") == "15:24").sum())
        report["license_gate"] = "REVIEW_REQUIRED_BEFORE_PUBLICATION"
        report["status"] = "SCHEMA_PROBED_LICENSE_REVIEW_REQUIRED" if len(nift) else "BLOCKED_NO_NIFTY_1MIN_ROWS"
    except Exception as exc:
        report["status"] = "BLOCKED_SOURCE_PROBE"
        report["error"] = f"{type(exc).__name__}: {str(exc)[:400]}"
    OUT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    if report["status"] == "BLOCKED_SOURCE_PROBE":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
