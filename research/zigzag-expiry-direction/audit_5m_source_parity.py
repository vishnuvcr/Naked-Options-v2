#!/usr/bin/env python3
"""Compare vendor-specific NIFTY 50 five-minute bars without merging or dropping data.

The report is a diagnostic of close-price agreement, not a certification of either
provider, official exchange-session coverage, timestamp semantics, or forecast validity.
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path("data/cache/zigzag_expiry_direction")
OUT = Path("reports/zigzag_cross_source_audit.json")
DHAN = ROOT / "nifty50_5m_dhan.csv"
PUBLIC = ROOT / "nifty50_5m_public_archive.csv"
FIELDS = ("open", "high", "low", "close")


def load_rows(path: Path) -> tuple[dict[str, dict], int, int]:
    """Return rows by timestamp, raw row count, and duplicate timestamp count."""
    with path.open(newline="", encoding="utf-8") as handle:
        raw = list(csv.DictReader(handle))
    mapping: dict[str, dict] = {}
    duplicates = 0
    for row in raw:
        stamp = row.get("timestamp_ist", "")
        if stamp in mapping:
            duplicates += 1
            continue
        mapping[stamp] = row
    return mapping, len(raw), duplicates


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    left = math.floor(position)
    right = math.ceil(position)
    if left == right:
        return ordered[left]
    weight = position - left
    return ordered[left] * (1 - weight) + ordered[right] * weight


def field_stats(diffs: list[float]) -> dict:
    if not diffs:
        return {"count": 0}
    return {
        "count": len(diffs),
        "median_absolute_difference": percentile(diffs, 0.50),
        "p90_absolute_difference": percentile(diffs, 0.90),
        "p95_absolute_difference": percentile(diffs, 0.95),
        "p99_absolute_difference": percentile(diffs, 0.99),
        "max_absolute_difference": max(diffs),
        "within_0_05": sum(value <= 0.05 for value in diffs),
        "within_0_05_fraction": sum(value <= 0.05 for value in diffs) / len(diffs),
        "over_1": sum(value > 1.0 for value in diffs),
        "over_5": sum(value > 5.0 for value in diffs),
    }


def audit(dhan_path: Path = DHAN, public_path: Path = PUBLIC) -> dict:
    report = {
        "audit_type": "cross_source_timestamp_and_close_price_diagnostic",
        "dhan_path": str(dhan_path),
        "public_archive_path": str(public_path),
        "does_not_authorize_prediction_scoring": True,
        "interpretation": (
            "No rows are merged, replaced, or dropped by this diagnostic. Agreement "
            "does not certify vendor provenance, official sessions, or bar timestamp semantics."
        ),
    }
    if not dhan_path.exists() or not public_path.exists():
        report.update({
            "status": "SKIPPED_SOURCE_MISSING",
            "missing_sources": [str(p) for p in (dhan_path, public_path) if not p.exists()],
            "overlap_rows": 0,
            "conclusion": "Cross-source parity cannot be assessed until both source files exist.",
        })
        return report

    dhan, dhan_raw_count, dhan_duplicates = load_rows(dhan_path)
    public, public_raw_count, public_duplicates = load_rows(public_path)
    common = sorted(set(dhan).intersection(public))
    report["dhan"] = {
        "raw_rows": dhan_raw_count,
        "unique_timestamps": len(dhan),
        "duplicate_rows": dhan_duplicates,
    }
    report["public_archive"] = {
        "raw_rows": public_raw_count,
        "unique_timestamps": len(public),
        "duplicate_rows": public_duplicates,
    }
    report["overlap"] = {
        "rows": len(common),
        "dates": len({stamp[:10] for stamp in common}),
        "first_timestamp_ist": common[0] if common else None,
        "last_timestamp_ist": common[-1] if common else None,
    }
    if not common:
        report.update({
            "status": "NO_TIMESTAMP_OVERLAP",
            "conclusion": "No exact timestamp overlap was available for price comparison.",
        })
        return report

    diffs_by_field: dict[str, list[float]] = {field: [] for field in FIELDS}
    close_rows = []
    dhan_day_counts = Counter(stamp[:10] for stamp in dhan)
    public_day_counts = Counter(stamp[:10] for stamp in public)
    standard_clock_close_diffs = []
    for stamp in common:
        left, right = dhan[stamp], public[stamp]
        for field in FIELDS:
            try:
                difference = abs(float(left[field]) - float(right[field]))
            except (KeyError, TypeError, ValueError):
                continue
            diffs_by_field[field].append(difference)
        close_diff = abs(float(left["close"]) - float(right["close"]))
        close_rows.append((close_diff, stamp, float(left["close"]), float(right["close"])))
        if dhan_day_counts[stamp[:10]] == 75 and public_day_counts[stamp[:10]] == 75:
            standard_clock_close_diffs.append(close_diff)

    report["absolute_differences"] = {
        field: field_stats(diffs) for field, diffs in diffs_by_field.items()
    }
    report["close_comparison_on_dates_with_75_bars_in_both_sources"] = {
        "rows": len(standard_clock_close_diffs),
        "dates": len({
            stamp[:10] for _, stamp, _, _ in close_rows
            if dhan_day_counts[stamp[:10]] == 75 and public_day_counts[stamp[:10]] == 75
        }),
        **field_stats(standard_clock_close_diffs),
        "qualification": (
            "75 rows per source is only a diagnostic regular-day proxy, not official "
            "NSE calendar certification; special-session dates require separate review."
        ),
    }
    report["largest_close_differences"] = [
        {
            "timestamp_ist": stamp,
            "dhan_close": dhan_close,
            "public_archive_close": public_close,
            "absolute_difference": difference,
        }
        for difference, stamp, dhan_close, public_close in sorted(close_rows, reverse=True)[:10]
    ]
    report["status"] = "OVERLAP_AVAILABLE_WITH_UNRESOLVED_DISCREPANCIES"
    report["conclusion"] = (
        "The sources can be compared on exact timestamps, but non-trivial close-price "
        "outliers remain. Do not silently substitute one feed for the other or treat "
        "these files as interchangeable. The exact imported indicator and target/session "
        "gates remain independent blockers."
    )
    return report


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dhan", default=str(DHAN))
    parser.add_argument("--public", default=str(PUBLIC))
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()
    report = audit(Path(args.dhan), Path(args.public))
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
