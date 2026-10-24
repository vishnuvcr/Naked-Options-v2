#!/usr/bin/env python3
"""Diagnostic audit of the public five-year NIFTY 50 5-minute archive.

This is deliberately not an official NSE session-calendar certification and
must never silently exclude records. It reports row counts, timestamps,
session-clock anomalies, OHLC integrity, and candidate missing bars.
"""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/cache/zigzag_expiry_direction")
SOURCE = ROOT / "nifty50_5m.csv"
OUT = Path("reports/public_5m_diagnostic_audit.json")
IST = ZoneInfo("Asia/Kolkata")
OPEN = time(9, 15)
LAST_BAR = time(15, 25)
EXPECTED = 75  # regular 09:15 through 15:25, inclusive, 5-minute bar starts

def main():
    if not SOURCE.exists():
        raise SystemExit(f"Missing required archive: {SOURCE}")
    with SOURCE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    required = {"timestamp_ist", "open", "high", "low", "close"}
    if not rows or not required.issubset(rows[0]):
        raise SystemExit("Missing rows or required columns")
    parsed, errors, bad_ohlc = [], [], []
    for i, r in enumerate(rows, start=2):
        try:
            dt = datetime.fromisoformat(r["timestamp_ist"])
            if dt.tzinfo is None or dt.utcoffset() is None:
                raise ValueError("timestamp is timezone-naive")
            dt = dt.astimezone(IST)
            vals = {k: float(r[k]) for k in ("open", "high", "low", "close")}
            if not (vals["low"] <= min(vals["open"], vals["close"]) <= max(vals["open"], vals["close"]) <= vals["high"]):
                bad_ohlc.append({"line": i, "timestamp": dt.isoformat()})
            parsed.append((dt, vals))
        except Exception as e:
            errors.append({"line": i, "reason": type(e).__name__})
    stamps = [x[0] for x in parsed]
    duplicate_count = len(stamps) - len(set(stamps))
    unsorted = stamps != sorted(stamps)
    by_date = {}
    for dt, _ in parsed:
        by_date.setdefault(dt.date().isoformat(), []).append(dt)
    counts = Counter(len(v) for v in by_date.values())
    nonstandard_dates = []
    off_session = []
    for day, dts in sorted(by_date.items()):
        clock = [d.time().replace(tzinfo=None) for d in dts]
        if len(dts) != EXPECTED or min(clock) != OPEN or max(clock) != LAST_BAR:
            nonstandard_dates.append({"date": day, "bars": len(dts),
              "first_time": min(clock).isoformat(), "last_time": max(clock).isoformat()})
        for dt in dts:
            if dt.weekday() >= 5 or dt.time().replace(tzinfo=None) < OPEN or dt.time().replace(tzinfo=None) > LAST_BAR:
                off_session.append(dt.isoformat())
    gap_examples = []
    for day, dts in sorted(by_date.items()):
        seq = sorted(dts)
        for left, right in zip(seq, seq[1:]):
            delta = right - left
            if delta != timedelta(minutes=5):
                if len(gap_examples) < 200:
                    gap_examples.append({"date": day, "after": left.isoformat(),
                      "before": right.isoformat(), "minutes": delta.total_seconds()/60})
    report = {
      "audit_type": "public_five_minute_diagnostic_not_official_calendar_validation",
      "source_path": str(SOURCE),
      "sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
      "rows": len(rows), "parsed_rows": len(parsed),
      "first_timestamp_ist": min(stamps).isoformat() if stamps else None,
      "last_timestamp_ist": max(stamps).isoformat() if stamps else None,
      "duplicate_timestamps": duplicate_count, "timestamps_not_sorted": unsorted,
      "timestamp_errors": errors[:50], "timestamp_error_count": len(errors),
      "invalid_ohlc_count": len(bad_ohlc), "invalid_ohlc_examples": bad_ohlc[:50],
      "unique_dates": len(by_date), "bars_per_date_frequency": dict(sorted(counts.items())),
      "expected_regular_bars_per_full_session": EXPECTED,
      "nonstandard_session_dates_count": len(nonstandard_dates),
      "nonstandard_session_dates_examples": nonstandard_dates[:100],
      "weekend_or_out_of_clock_rows_count": len(off_session),
      "weekend_or_out_of_clock_rows_examples": off_session[:100],
      "within_day_non_5m_gaps_count_capped": len(gap_examples),
      "within_day_non_5m_gap_examples": gap_examples,
      "official_nse_calendar_checked": False,
      "decision": "DIAGNOSTICS_ONLY; KEEP RAW DATA; DO NOT SCORE UNTIL OFFICIAL SESSION DATES, EXPIRY MAPPING, BAR TIME SEMANTICS AND ZIGLIB CAUSAL TIMING ARE VERIFIED"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors or duplicate_count or unsorted or bad_ohlc:
        raise SystemExit("Structural issue found; diagnostic report saved; raw data preserved")
if __name__ == "__main__":
    main()
