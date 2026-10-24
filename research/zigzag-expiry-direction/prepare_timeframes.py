#!/usr/bin/env python3
"""Validate Dhan NIFTY 50 bars, preserve raw data, write audited clean series, derive 30m."""
import csv, hashlib, json, pathlib
from datetime import datetime, time
from zoneinfo import ZoneInfo

ROOT = pathlib.Path("data/cache/zigzag_expiry_direction")
OUT = pathlib.Path("reports/zigzag_timeframe_validation.json")
IST = ZoneInfo("Asia/Kolkata")
FIELDS = ["timestamp_ist", "date_ist", "open", "high", "low", "close", "volume"]

def read_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["dt"] = datetime.fromisoformat(row["timestamp_ist"])
        for k in ("open", "high", "low", "close"):
            row[k] = float(row[k])
        row["volume"] = int(float(row.get("volume") or 0))
    return rows

def valid_ohlc(row):
    return row["low"] <= min(row["open"], row["close"]) <= max(row["open"], row["close"]) <= row["high"]

def structural_issues(rows):
    issues = []
    stamps = [r["timestamp_ist"] for r in rows]
    if len(stamps) != len(set(stamps)):
        issues.append("duplicate timestamps")
    if stamps != sorted(stamps):
        issues.append("timestamps not sorted")
    for r in rows:
        if r["dt"].tzinfo is None or r["dt"].utcoffset() is None:
            issues.append("timezone-naive timestamp at " + r["timestamp_ist"])
            break
    return issues

def write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in FIELDS})
    return {"path": str(path), "rows": len(rows), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

def derive_30m(rows):
    buckets = {}
    for r in rows:
        t = r["dt"].astimezone(IST)
        if t.time() < time(9, 15) or t.time() >= time(15, 15):
            continue
        mins = t.hour * 60 + t.minute - (9 * 60 + 15)
        buckets.setdefault((t.date().isoformat(), mins // 30), []).append(r)
    result, dropped = [], []
    for (day, bucket), bars in sorted(buckets.items()):
        bars = sorted(bars, key=lambda x: x["dt"])
        expected = [9 * 60 + 15 + bucket * 30 + i * 5 for i in range(6)]
        got = [r["dt"].astimezone(IST).hour * 60 + r["dt"].astimezone(IST).minute for r in bars]
        if len(bars) != 6 or got != expected:
            dropped.append({"date": day, "bucket": bucket, "bars": len(bars), "reason": "incomplete/noncontiguous 5m inputs"})
            continue
        stamp = bars[0]["dt"].astimezone(IST)
        result.append({"timestamp_ist": stamp.isoformat(), "date_ist": day,
          "open": bars[0]["open"], "high": max(x["high"] for x in bars),
          "low": min(x["low"] for x in bars), "close": bars[-1]["close"],
          "volume": sum(x["volume"] for x in bars), "dt": stamp})
    path = ROOT / "nifty50_30m_resampled.csv"
    info = write_rows(path, result)
    return result, dropped, info

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--required", default="5,15,60,daily", help="Comma-separated datasets that must exist")
    args = ap.parse_args()
    required = args.required.split(",")
    reports = {"required": required, "datasets": {}, "warnings": [], "errors": [], "derived": [],
               "cleaning_policy": "Raw downloads are preserved. Invalid OHLC rows are excluded only from *_validated.csv outputs and listed with full OHLC values; structural issues remain fatal."}
    labels = list(dict.fromkeys(required + ["5"] if "5" in required else required))
    for label in labels:
        name = "nifty50_daily.csv" if label == "daily" else f"nifty50_{label}m.csv"
        path = ROOT / name
        if not path.exists():
            if label in required:
                reports["errors"].append(f"missing required dataset: {name}")
            continue
        try:
            rows = read_rows(path)
            issues = structural_issues(rows)
            bad = [{k: r[k] for k in FIELDS} for r in rows if not valid_ohlc(r)]
            clean = [r for r in rows if valid_ohlc(r)]
            clean_path = ROOT / ("nifty50_daily_validated.csv" if label == "daily" else f"nifty50_{label}m_validated.csv")
            clean_info = write_rows(clean_path, clean)
            reports["datasets"][label] = {
                "raw_path": str(path), "raw_rows": len(rows),
                "raw_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "first_timestamp_ist": rows[0]["timestamp_ist"] if rows else None,
                "last_timestamp_ist": rows[-1]["timestamp_ist"] if rows else None,
                "validated_output": clean_info, "excluded_invalid_ohlc_count": len(bad),
                "excluded_invalid_ohlc": bad, "structural_issues": issues
            }
            if bad:
                reports["warnings"].append(f"{label}: excluded {len(bad)} invalid OHLC row(s) from validated output; raw file preserved.")
            if issues:
                reports["errors"].extend([label + ": " + x for x in issues])
        except Exception as exc:
            reports["errors"].append(f"{label}: {type(exc).__name__}: {exc}")
    five_clean = ROOT / "nifty50_5m_validated.csv"
    if five_clean.exists():
        try:
            rows = read_rows(five_clean)
            derived, dropped, info = derive_30m(rows)
            reports["derived"].append({"timeframe": "30m", **info,
              "dropped_incomplete_bars": len(dropped), "dropped_examples": dropped[:20],
              "construction": "six contiguous validated 5m bars; bins anchored 09:15 IST; incomplete bins excluded"})
        except Exception as exc:
            reports["errors"].append(f"30m derivation: {type(exc).__name__}: {exc}")
    else:
        reports["errors"].append("cannot derive 30m: validated 5m dataset missing")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(reports, indent=2), encoding="utf-8")
    print(json.dumps(reports, indent=2))
    return 1 if reports["errors"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
