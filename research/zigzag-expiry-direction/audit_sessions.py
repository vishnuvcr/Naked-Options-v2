#!/usr/bin/env python3
"""Diagnostic timestamp/session audit; never silently removes market observations.

This is deliberately not a final NSE session-calendar validator. Weekend sessions
can be legitimate special sessions; an official session calendar is required before
any rows can be certified eligible for prediction research.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/cache/zigzag_expiry_direction")
OUT = Path("reports/zigzag_session_audit.json")
IST = ZoneInfo("Asia/Kolkata")
FILES = {
    "1m": ROOT / "nifty50_1m.csv",
    "5m": ROOT / "nifty50_5m.csv",
    "15m": ROOT / "nifty50_15m.csv",
    "30m": ROOT / "nifty50_30m_resampled.csv",
    "60m": ROOT / "nifty50_60m.csv",
    "daily": ROOT / "nifty50_daily.csv",
}
BROAD_START = time(9, 0)
BROAD_END = time(16, 0)


def audit_file(path, timeframe):
    if not path.exists():
        return {"path": str(path), "status": "MISSING", "errors": ["file missing"]}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp_ist", "open", "high", "low", "close"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            return {"path": str(path), "status": "INVALID_SCHEMA",
                    "errors": ["missing required timestamp/OHLC columns"]}
        rows = list(reader)
    stamps = []
    bad_timestamps = []
    weekend = Counter()
    outside = Counter()
    out_of_session_examples = []
    for row in rows:
        try:
            stamp = datetime.fromisoformat(row["timestamp_ist"])
            if stamp.tzinfo is None or stamp.utcoffset() is None:
                raise ValueError("timezone-naive")
            stamp = stamp.astimezone(IST)
            stamps.append(stamp.isoformat())
            weekend[stamp.strftime("%A")] += int(stamp.weekday() >= 5)
            if timeframe != "daily" and not (BROAD_START <= stamp.time().replace(tzinfo=None) <= BROAD_END):
                outside["broad_09_to_16"] += 1
                if len(out_of_session_examples) < 20:
                    out_of_session_examples.append(stamp.isoformat())
            try:
                o, h, l, c = (float(row[k]) for k in ("open", "high", "low", "close"))
                if not (l <= min(o, c) <= max(o, c) <= h):
                    bad_timestamps.append({"timestamp": stamp.isoformat(), "issue": "invalid OHLC"})
            except (ValueError, TypeError):
                bad_timestamps.append({"timestamp": stamp.isoformat(), "issue": "non-numeric OHLC"})
        except Exception as exc:
            bad_timestamps.append({"timestamp": row.get("timestamp_ist"), "issue": type(exc).__name__})
    duplicates = len(stamps) - len(set(stamps))
    unsorted = stamps != sorted(stamps)
    weekend_count = sum(weekend.values())
    return {
        "path": str(path), "rows": len(rows),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "first_timestamp_ist": min(stamps) if stamps else None,
        "last_timestamp_ist": max(stamps) if stamps else None,
        "duplicate_timestamps": duplicates, "timestamps_not_sorted": unsorted,
        "weekend_dated_rows": weekend_count,
        "outside_broad_09_to_16_rows": outside.get("broad_09_to_16", 0),
        "outside_broad_examples": out_of_session_examples,
        "timestamp_or_ohlc_errors": bad_timestamps[:50],
        "session_calendar_status": "NOT_VERIFIED",
        "interpretation": "Diagnostic clock/weekend flags only; not an exclusion list. Official NSE session calendar and vendor timestamp semantics are still required."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    report = {
        "audit_type": "diagnostic_only_not_exchange_calendar_certification",
        "timezone": "Asia/Kolkata",
        "broad_clock_screen": {"start_inclusive": "09:00", "end_inclusive": "16:00",
                               "note": "Diagnostic only, not official eligibility criteria."},
        "official_nse_session_calendar_provided": False,
        "datasets": {tf: audit_file(path, tf) for tf, path in FILES.items()},
        "errors": []
    }
    for tf, result in report["datasets"].items():
        if result.get("status") in {"MISSING", "INVALID_SCHEMA"} or result.get("duplicate_timestamps") or result.get("timestamps_not_sorted") or result.get("timestamp_or_ohlc_errors"):
            report["errors"].append(f"{tf}: structural issue or missing file; inspect dataset report")
    report["decision"] = "NOT_ELIGIBLE_FOR_SCORING_UNTIL_OFFICIAL_SESSION_CALENDAR_AND_DHAN_TIMESTAMP_CONVENTION_ARE_VERIFIED"
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    # Diagnostic flags do not fail the workflow: they are expected findings to inspect.
    # Structural problems do fail it.
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
