#!/usr/bin/env python3
"""Cross-check cached NIFTY daily OHLC against a second free public source."""
from __future__ import annotations
import hashlib, io, json, urllib.request
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/cache/nifty-prediction/nifty50_daily.csv"
OUT = ROOT / "reports/nifty-prediction/source_parity_audit.json"
ALT_URL = "https://raw.githubusercontent.com/aswinv90/indian-market-historical-data/main/data/INDICES/NIFTY_50.parquet"
FIELDS = ["Open", "High", "Low", "Close"]


def load_primary(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [str(c).strip().title() for c in df.columns]
    if "Date" not in df or any(c not in df for c in FIELDS):
        raise ValueError(f"Primary CSV missing required columns: {df.columns.tolist()}")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    for col in FIELDS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["Date", *FIELDS]).drop_duplicates("Date").set_index("Date").sort_index()


def load_secondary() -> pd.DataFrame:
    req = urllib.request.Request(ALT_URL, headers={"User-Agent": "Naked-Options-v2-research/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        blob = response.read()
    df = pd.read_parquet(io.BytesIO(blob))
    if isinstance(df.index, pd.DatetimeIndex) or df.index.name:
        df = df.reset_index()
    df.columns = [str(c).strip().title().replace("_", " ") for c in df.columns]
    date_col = next((c for c in df.columns if c.strip().lower() in ("date", "datetime", "timestamp", "index")), None)
    if date_col is None:
        raise ValueError(f"Secondary parquet missing date column: {df.columns.tolist()}")
    rename = {c: c.title() for c in FIELDS}
    df = df.rename(columns=rename)
    missing = [c for c in FIELDS if c not in df.columns]
    if missing:
        raise ValueError(f"Secondary parquet missing fields {missing}: {df.columns.tolist()}")
    df["Date"] = pd.to_datetime(df[date_col], errors="coerce", utc=True).dt.tz_convert("Asia/Kolkata").dt.date
    for col in FIELDS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["Date", *FIELDS]).drop_duplicates("Date").set_index("Date").sort_index(), hashlib.sha256(blob).hexdigest()


def main() -> int:
    if not DATA.exists():
        raise FileNotFoundError(f"Primary dataset not found: {DATA}")
    primary = load_primary(DATA)
    secondary, secondary_sha = load_secondary()
    overlap = primary.join(secondary, how="inner", lsuffix="_primary", rsuffix="_secondary")
    report = {
        "status": "AUDIT_COMPLETED",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "primary_source_manifest": json.loads((DATA.parent / "source_manifest.json").read_text()) if (DATA.parent / "source_manifest.json").exists() else None,
        "secondary_source": "aswinv90/indian-market-historical-data daily NIFTY 50 parquet",
        "secondary_source_url": ALT_URL,
        "secondary_parquet_sha256": secondary_sha,
        "primary_rows": int(len(primary)),
        "primary_first_date": str(primary.index.min()),
        "primary_last_date": str(primary.index.max()),
        "secondary_rows": int(len(secondary)),
        "secondary_first_date": str(secondary.index.min()),
        "secondary_last_date": str(secondary.index.max()),
        "overlap_rows": int(len(overlap)),
        "fields": {},
        "limitations": [
            "Both sources are public third-party mirrors and neither is treated as exchange-certified.",
            "Agreement is not proof of correctness because sources may share upstream dependencies.",
            "Date labels are normalized to Indian calendar dates; source session conventions still need validation."
        ]
    }
    for field in FIELDS:
        a, b = overlap[f"{field}_primary"].to_numpy(), overlap[f"{field}_secondary"].to_numpy()
        delta = a - b
        report["fields"][field] = {
            "mae_points": float(np.mean(np.abs(delta))) if len(delta) else None,
            "median_abs_error_points": float(np.median(np.abs(delta))) if len(delta) else None,
            "p95_abs_error_points": float(np.quantile(np.abs(delta), .95)) if len(delta) else None,
            "max_abs_error_points": float(np.max(np.abs(delta))) if len(delta) else None,
            "exact_within_0_05_points_pct": float(np.mean(np.abs(delta) <= .05) * 100) if len(delta) else None,
            "within_1_point_pct": float(np.mean(np.abs(delta) <= 1) * 100) if len(delta) else None,
        }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
