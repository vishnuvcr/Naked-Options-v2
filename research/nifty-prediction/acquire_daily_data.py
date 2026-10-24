#!/usr/bin/env python3
"""Acquire a cached free-source daily NIFTY 50 spot series from Yahoo Finance."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import yfinance as yf

OUT = Path("data/cache/nifty-prediction/nifty50_daily.csv")
MANIFEST = Path("data/cache/nifty-prediction/source_manifest.json")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists() and MANIFEST.exists() and not args.refresh:
        data = pd.read_csv(OUT)
        manifest = json.loads(MANIFEST.read_text())
        current_sha256 = hashlib.sha256(OUT.read_bytes()).hexdigest()
        cache_provenance_valid = (
            len(data) >= 1000
            and manifest.get("symbol") == "^NSEI"
            and isinstance(manifest.get("source"), str) and bool(manifest.get("source"))
            and bool(manifest.get("source_url"))
            and (not manifest.get("sha256") or manifest.get("sha256") == current_sha256)
            and all(c in data.columns for c in ("Date", "Open", "High", "Low", "Close"))
        )
        if cache_provenance_valid:
            manifest.update({"reused_cache": True, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
                             "rows": int(len(data)), "sha256": current_sha256})
            MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
            print(json.dumps(manifest, indent=2))
            return
        print("Cached data lacks valid provenance/hash or required fields; reacquiring source data.")
    df = yf.download("^NSEI", period="max", interval="1d", auto_adjust=False, progress=False, threads=False)
    if df is None or df.empty:
        raise RuntimeError("Yahoo Finance returned no daily NIFTY 50 data")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [str(col[0]).strip().lower().replace(" ", "_") for col in df.columns]
    else:
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    df = df.reset_index()
    date_col = next((c for c in df.columns if c in ("date", "datetime")), None)
    if date_col is None:
        raise RuntimeError(f"Missing date column in Yahoo response: {df.columns.tolist()}")
    keep = [date_col, "open", "high", "low", "close"]
    df = df[keep].rename(columns={date_col: "Date", "open": "Open", "high": "High", "low": "Low", "close": "Close"})
    df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_convert("Asia/Kolkata").dt.strftime("%Y-%m-%d")
    df = df.dropna().sort_values("Date").drop_duplicates("Date", keep="last")
    df.to_csv(OUT, index=False)
    manifest = {
        "symbol": "^NSEI", "instrument": "NIFTY 50 spot index (Yahoo Finance symbol mapping)",
        "source": "Yahoo Finance chart data via yfinance", "source_url": "https://finance.yahoo.com/quote/%5ENSEI/history/",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "reused_cache": False,
        "rows": int(len(df)), "first_date": str(df.Date.iloc[0]), "last_date": str(df.Date.iloc[-1]),
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "limitations": ["Free third-party source, not exchange-certified; validate against official index data before high-confidence conclusions.",
                        "Daily bars only; does not resolve intraday or expiry-specific questions."]
    }
    if len(df) < 1000:
        raise RuntimeError(f"Unexpectedly short NIFTY daily series: {len(df)} rows")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
