#!/usr/bin/env python3
"""Diagnostic timestamp/session audit; never silently removes market observations.

This is not a final NSE session-calendar validator. Weekend sessions can be
legitimate special sessions. Raw-bar OHLC anomalies are findings, not a reason
to discard source data or fail CI; validated copies are checked separately.
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
    "5m_dhan": ROOT / "nifty50_5m_dhan.csv",
    "5m_public_archive": ROOT / "nifty50_5m_public_archive.csv",
    "15m": ROOT / "nifty50_15m.csv",
    "30m": ROOT / "nifty50_30m_resampled.csv",
    "60m": ROOT / "nifty50_60m.csv",
    "daily": ROOT / "nifty50_daily.csv",
}
OPTIONAL = {"1m", "5m_dhan", "5m_public_archive"}
BROAD_START, BROAD_END = time(9, 0), time(16, 0)


def audit_file(path, timeframe):
    if not path.exists():
        return {"path": str(path), "status": "MISSING", "fatal_errors": ["file missing"]}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp_ist", "open", "high", "low", "close"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            return {"path": str(path), "status": "INVALID_SCHEMA",
                    "fatal_errors": ["missing required timestamp/OHLC columns"]}
        rows = list(reader)
    stamps, parse_errors, ohlc_findings = [], [], []
    weekend = Counter()
    outside_count, outside_examples = 0, []
    for row in rows:
        try:
            stamp = datetime.fromisoformat(row["timestamp_ist"])
            if stamp.tzinfo is None or stamp.utcoffset() is None:
                raise ValueError("timezone-naive timestamp")
            stamp = stamp.astimezone(IST)
            stamps.append(stamp.isoformat())
        except Exception as exc:
            parse_errors.append({"timestamp": row.get("timestamp_ist"), "issue": type(exc).__name__})
            continue
        weekend["weekend"] += int(stamp.weekday() >= 5)
        if timeframe != "daily" and not (BROAD_START <= stamp.time().replace(tzinfo=None) <= BROAD_END):
            outside_count += 1
            if len(outside_examples) < 20:
                outside_examples.append(stamp.isoformat())
        try:
            o, h, l, c = (float(row[k]) for k in ("open", "high", "low", "close"))
            if not all(map(lambda x: x == x and abs(x) != float("inf"), (o, h, l, c))) or not (l <= min(o, c) <= max(o, c) <= h):
                ohlc_findings.append({"timestamp": stamp.isoformat(), "issue": "invalid OHLC"})
        except (ValueError, TypeError):
            ohlc_findings.append({"timestamp": stamp.isoformat(), "issue": "non-numeric OHLC"})
    duplicates = len(stamps) - len(set(stamps))
    unsorted = stamps != sorted(stamps)
    fatal = []
    if parse_errors:
        fatal.append(f"{len(parse_errors)} timestamp parse/timezone errors")
    if duplicates:
        fatal.append(f"{duplicates} duplicate timestamps")
    if unsorted:
        fatal.append("timestamps not sorted")
    return {
        "path": str(path), "status": "AUDITED", "rows": len(rows),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "first_timestamp_ist": min(stamps) if stamps else None,
        "last_timestamp_ist": max(stamps) if stamps else None,
        "duplicate_timestamps": duplicates, "timestamps_not_sorted": unsorted,
        "weekend_dated_rows": weekend["weekend"],
        "outside_broad_09_to_16_rows": outside_count,
        "outside_broad_examples": outside_examples,
        "timestamp_parse_errors": parse_errors[:50],
        "raw_ohlc_findings": ohlc_findings[:50],
        "raw_ohlc_finding_count": len(ohlc_findings),
        "fatal_errors": fatal,
        "session_calendar_status": "NOT_VERIFIED",
        "interpretation": "Clock/weekend and raw OHLC findings are diagnostics, not exclusions. Official NSE sessions and Dhan timestamp semantics remain unverified."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    files = dict(FILES)
    primary_5m = next((candidate for candidate in (
        ROOT / "nifty50_5m_public_archive.csv",
        ROOT / "nifty50_5m_dhan.csv",
        ROOT / "nifty50_5m.csv",
    ) if candidate.exists()), ROOT / "nifty50_5m.csv")
    files["5m"] = primary_5m
    datasets = {tf: audit_file(path, tf.replace("_dhan", "").replace("_public_archive", "")) for tf, path in files.items()}
    errors = []
    for tf, result in datasets.items():
        if result.get("status") == "INVALID_SCHEMA":
            errors.append(f"{tf}: invalid schema")
        elif result.get("status") == "MISSING" and tf not in OPTIONAL:
            errors.append(f"{tf}: required file missing")
        errors.extend(f"{tf}: {item}" for item in result.get("fatal_errors", []))
    report = {
        "audit_type": "diagnostic_only_not_exchange_calendar_certification",
        "timezone": "Asia/Kolkata",
        "broad_clock_screen": {"start_inclusive": "09:00", "end_inclusive": "16:00",
                               "note": "Diagnostic only, not official eligibility criteria."},
        "official_nse_session_calendar_provided": False,
        "datasets": datasets,
        "primary_5m_source": str(primary_5m),
        "errors": errors,
        "decision": "NOT_ELIGIBLE_FOR_SCORING_UNTIL_OFFICIAL_SESSION_CALENDAR_AND_DHAN_TIMESTAMP_CONVENTION_ARE_VERIFIED"
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
