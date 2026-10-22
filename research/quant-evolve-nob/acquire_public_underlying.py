#!/usr/bin/env python3
"""Pinned public-source NIFTY underlying fallback for QE-NOB-2.0.

Downloads only yearly 1-minute OHLC files needed for the frozen cached-option sample.
Valid full five-minute bars are resampled from five consecutive one-minute bars.
This source is an independent community dataset, not an official exchange feed;
its row provenance and market-data rights must be treated as a documented limitation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "quant_evolve_nob_v1"
RAW_CACHE = CACHE / "underlying_public_raw"
IDX_CACHE = CACHE / "underlying_intraday"
OUT = ROOT / "reports" / "quant_evolve_nob_v2"
START_DATE = date(2021, 10, 23)
END_DATE_EXCLUSIVE = date(2025, 12, 31)
SOURCE_COMMIT = "a8d738ff6b248c4636464cbd9d82e7bcb7f902a8"
SOURCE_BASE = "https://raw.githubusercontent.com/technovusin/nifty50-historical-data/" + SOURCE_COMMIT
TIME_ZONE = "Asia/Kolkata"
SPECIAL_SESSIONS = {"2023-11-12", "2024-11-01"}
REQUIRED = {"Epoch", "Timestamp", "Open", "High", "Low", "Close"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def chunks(start: date, end_exclusive: date, days: int):
    current = start
    while current < end_exclusive:
        nxt = min(current + timedelta(days=days), end_exclusive)
        yield current, nxt
        current = nxt


def normalise_source_frame(frame: pd.DataFrame, start: date = START_DATE,
                           end_exclusive: date = END_DATE_EXCLUSIVE) -> tuple[pd.DataFrame, dict[str, Any]]:
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError("public NIFTY CSV missing columns: " + ",".join(sorted(missing)))
    work = pd.DataFrame({
        "timestamp": pd.to_numeric(frame["Epoch"], errors="coerce"),
        "open": pd.to_numeric(frame["Open"], errors="coerce"),
        "high": pd.to_numeric(frame["High"], errors="coerce"),
        "low": pd.to_numeric(frame["Low"], errors="coerce"),
        "close": pd.to_numeric(frame["Close"], errors="coerce"),
    })
    if "Volume" in frame.columns:
        work["volume"] = pd.to_numeric(frame["Volume"], errors="coerce")
    if work["timestamp"].isna().any():
        raise ValueError("public NIFTY Epoch contains non-numeric values")
    work["timestamp"] = work["timestamp"].round().astype("int64")
    if len(work) and (int(work["timestamp"].median()) < 1_000_000_000 or
                      int(work["timestamp"].median()) > 2_000_000_000):
        raise ValueError("public NIFTY Epoch is not plausible Unix seconds")
    work["datetime_ist"] = pd.to_datetime(work["timestamp"], unit="s", utc=True).dt.tz_convert(TIME_ZONE)

    # Cross-check the documented IST timestamp column against the Unix epoch.
    local_text = pd.to_datetime(frame["Timestamp"], errors="coerce")
    if getattr(local_text.dt, "tz", None) is None:
        local_text = local_text.dt.tz_localize(TIME_ZONE)
    else:
        local_text = local_text.dt.tz_convert(TIME_ZONE)
    comparable = local_text.notna()
    if comparable.any():
        delta = (local_text[comparable].astype("int64") // 1_000_000_000 -
                 work.loc[comparable, "timestamp"]).abs()
        mismatches = int((delta > 1).sum())
        if mismatches > max(5, int(comparable.sum() * 0.01)):
            raise ValueError(f"public NIFTY Timestamp/Epoch mismatch count {mismatches}")

    work["session_date"] = work["datetime_ist"].dt.strftime("%Y-%m-%d")
    dates = work["datetime_ist"].dt.date
    work = work[(dates >= start) & (dates < end_exclusive)].copy()
    clock = work["datetime_ist"].dt.strftime("%H:%M")
    regular = (clock >= "09:15") & (clock <= "15:29")
    special = work["session_date"].isin(SPECIAL_SESSIONS)
    work = work[regular | special].copy()

    ohlc = ["open", "high", "low", "close"]
    work = work.dropna(subset=ohlc)
    work = work[(work[ohlc] > 0).all(axis=1)]
    valid_ohlc = (
        (work["high"] >= work[["open", "close", "low"]].max(axis=1)) &
        (work["low"] <= work[["open", "close", "high"]].min(axis=1))
    )
    work = work[valid_ohlc].copy()

    # Exact duplicate minute rows are dropped; conflicting duplicate prices fail closed.
    dup = work[work["timestamp"].duplicated(keep=False)]
    conflicts = 0
    if not dup.empty:
        for _, group in dup.groupby("timestamp", sort=False):
            if len(group[ohlc].drop_duplicates()) > 1:
                conflicts += 1
        if conflicts:
            raise ValueError(f"public NIFTY has {conflicts} conflicting duplicate timestamps")
        work = work.drop_duplicates("timestamp", keep="first")
    work = work.sort_values("timestamp").reset_index(drop=True)
    meta = {
        "input_rows": int(len(frame)),
        "usable_minute_rows": int(len(work)),
        "duplicate_rows_removed": int(len(frame.loc[frame["Epoch"].notna()]) - len(work)),
        "conflicting_duplicate_timestamps": int(conflicts),
        "timezone": TIME_ZONE,
        "range_start_inclusive": start.isoformat(),
        "range_end_exclusive": end_exclusive.isoformat(),
    }
    return work, meta


def resample_one_minute_to_five(frame: pd.DataFrame) -> pd.DataFrame:
    """Aggregate only five complete consecutive one-minute bars; never fill gaps."""
    needed = {"timestamp", "datetime_ist", "session_date", "open", "high", "low", "close"}
    missing = needed - set(frame.columns)
    if missing:
        raise ValueError("normalized minute frame missing: " + ",".join(sorted(missing)))
    rows = frame.copy().sort_values("timestamp").reset_index(drop=True)
    if rows.empty:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close"])
    anchors = {}
    for session, group in rows.groupby("session_date", sort=False):
        if session in SPECIAL_SESSIONS:
            anchors[session] = group["datetime_ist"].iloc[0]
        else:
            first = group["datetime_ist"].iloc[0]
            anchors[session] = first.normalize() + pd.Timedelta(hours=9, minutes=15)
    rows["anchor"] = rows["session_date"].map(anchors)
    elapsed = (rows["datetime_ist"] - rows["anchor"]).dt.total_seconds()
    rows = rows[elapsed.ge(0)].copy()
    elapsed = (rows["datetime_ist"] - rows["anchor"]).dt.total_seconds()
    rows["bucket"] = np.floor(elapsed / 300.0).astype("int64")
    output = []
    keys = ["session_date", "bucket"]
    for (session, bucket), group in rows.groupby(keys, sort=True):
        group = group.sort_values("timestamp")
        if len(group) != 5 or group["timestamp"].nunique() != 5:
            continue
        stamps = group["timestamp"].astype("int64").to_numpy()
        if not np.all(np.diff(stamps) == 60):
            continue
        expected_start = anchors[session] + pd.Timedelta(minutes=int(bucket) * 5)
        if group["datetime_ist"].iloc[0] != expected_start:
            continue
        item = {
            "timestamp": int(group["timestamp"].iloc[0]),
            "open": float(group["open"].iloc[0]),
            "high": float(group["high"].max()),
            "low": float(group["low"].min()),
            "close": float(group["close"].iloc[-1]),
        }
        if "volume" in group.columns and group["volume"].notna().all():
            item["volume"] = float(group["volume"].sum())
        output.append(item)
    return pd.DataFrame(output).sort_values("timestamp").reset_index(drop=True) if output else pd.DataFrame(
        columns=["timestamp", "open", "high", "low", "close"]
    )


def download_or_reuse_year(year: int, timeout=(10, 90)) -> tuple[Path, dict[str, Any]]:
    RAW_CACHE.mkdir(parents=True, exist_ok=True)
    filename = f"NIFTY50_1min_{year}.csv"
    path = RAW_CACHE / filename
    expected_url = f"{SOURCE_BASE}/1min/{year}/{filename}"
    if path.exists() and path.stat().st_size > 20_000:
        # A readable cached file is reused; its content hash is recorded each run.
        head = pd.read_csv(path, nrows=2)
        if REQUIRED.issubset(set(head.columns)):
            return path, {"year": year, "url": expected_url, "cache_hit": True,
                          "bytes": int(path.stat().st_size), "sha256": sha256_file(path)}
    last_error = None
    for attempt in range(3):
        try:
            response = requests.get(expected_url, timeout=timeout, headers={"User-Agent": "QE-NOB-2.0-data-audit"})
            response.raise_for_status()
            payload = response.content
            if len(payload) < 20_000:
                raise ValueError(f"unexpectedly small yearly CSV for {year}: {len(payload)} bytes")
            # Validate header before replacing any prior local cache.
            header = pd.read_csv(pd.io.common.BytesIO(payload), nrows=2)
            if not REQUIRED.issubset(set(header.columns)):
                raise ValueError(f"required fields missing in yearly CSV {year}")
            tmp = path.with_suffix(".csv.tmp")
            tmp.write_bytes(payload)
            tmp.replace(path)
            return path, {"year": year, "url": expected_url, "cache_hit": False,
                          "bytes": int(path.stat().st_size), "sha256": sha256_file(path)}
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {str(exc)[:180]}"
            if attempt < 2:
                time.sleep(attempt + 1)
    raise RuntimeError(f"public NIFTY source download failed for {year}: {last_error}")


def acquire_public_underlying(start: date = START_DATE, end_exclusive: date = END_DATE_EXCLUSIVE) -> dict[str, Any]:
    CACHE.mkdir(parents=True, exist_ok=True)
    IDX_CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    files = []
    frames = []
    for year in range(start.year, end_exclusive.year + 1):
        path, info = download_or_reuse_year(year)
        files.append(info)
        raw = pd.read_csv(path)
        normalized, year_meta = normalise_source_frame(raw, start, end_exclusive)
        info["usable_minute_rows"] = year_meta["usable_minute_rows"]
        info["input_rows"] = year_meta["input_rows"]
        if not normalized.empty:
            frames.append(normalized)
    if not frames:
        raise RuntimeError("public NIFTY source returned no minute bars in the frozen study window")
    minutes = pd.concat(frames, ignore_index=True).sort_values("timestamp").reset_index(drop=True)
    if minutes["timestamp"].duplicated().any():
        dup = minutes[minutes["timestamp"].duplicated(keep=False)]
        ohlc = ["open", "high", "low", "close"]
        conflicts = sum(1 for _, group in dup.groupby("timestamp") if len(group[ohlc].drop_duplicates()) > 1)
        if conflicts:
            raise ValueError(f"cross-file public NIFTY cache has {conflicts} conflicting minute timestamps")
        minutes = minutes.drop_duplicates("timestamp", keep="first").reset_index(drop=True)
    five = resample_one_minute_to_five(minutes)
    if len(five) < 50_000:
        raise RuntimeError(f"too few complete five-minute bars from public source: {len(five)}")
    five_dt = pd.to_datetime(five["timestamp"], unit="s", utc=True).dt.tz_convert(TIME_ZONE)
    five["trade_date"] = five_dt.dt.date
    chunk_summary = []
    for d0, d1 in chunks(start, end_exclusive, 80):
        part = five[(five["trade_date"] >= d0) & (five["trade_date"] < d1)].copy()
        path = IDX_CACHE / f"nifty_5m_{d0:%Y%m%d}_{d1:%Y%m%d}.json"
        if part.empty:
            raise RuntimeError(f"no complete underlying bars for required chunk {d0}..{d1}")
        payload = {key: [int(v) if key == "timestamp" else float(v)
                         for v in part[key].tolist()]
                   for key in ("timestamp", "open", "high", "low", "close")}
        if "volume" in part.columns and part["volume"].notna().all():
            payload["volume"] = [float(v) for v in part["volume"].tolist()]
        path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
        chunk_summary.append({"from": d0.isoformat(), "to_exclusive": d1.isoformat(),
                              "rows": int(len(part)), "path": str(path.relative_to(ROOT)),
                              "sha256": sha256_file(path)})
    manifest = {
        "schema_version": "qe-nob-public-underlying-v1",
        "research_id": "QE-NOB-2.0",
        "status": "PASS",
        "source_name": "technovusin/nifty50-historical-data",
        "source_url": "https://github.com/technovusin/nifty50-historical-data",
        "source_commit": SOURCE_COMMIT,
        "source_license": "Repository LICENSE states MIT; market-data rights/provenance are not independently certified.",
        "source_files": files,
        "study_start_inclusive": start.isoformat(),
        "study_end_exclusive": end_exclusive.isoformat(),
        "raw_minute_rows": int(len(minutes)),
        "complete_five_minute_bars": int(len(five)),
        "five_minute_timestamp_min": int(five["timestamp"].min()),
        "five_minute_timestamp_max": int(five["timestamp"].max()),
        "resampling": "OHLC aggregated only from five consecutive one-minute rows; incomplete bins are dropped, never interpolated.",
        "timezone": TIME_ZONE,
        "special_sessions_retained": sorted(SPECIAL_SESSIONS),
        "chunks": chunk_summary,
        "limitations": [
            "Community-maintained market-data mirror, not an official NSE feed.",
            "Repository describes known missing bars and some historical data corrections.",
            "The repository's MIT code license does not independently certify market-data redistribution rights.",
            "Underlying data are used only for the frozen historical option-cache window; executable option contracts/quotes are not inferred."
        ]
    }
    manifest_path = OUT / "public_underlying_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default=START_DATE.isoformat())
    parser.add_argument("--end-exclusive", default=END_DATE_EXCLUSIVE.isoformat())
    args = parser.parse_args()
    try:
        result = acquire_public_underlying(date.fromisoformat(args.start), date.fromisoformat(args.end_exclusive))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error_type": type(exc).__name__,
                          "error_summary": str(exc)[:300]}, indent=2))
        return 2
    print(json.dumps({k: v for k, v in result.items() if k not in {"source_files", "chunks"}}, indent=2))
    return 0 if result.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
