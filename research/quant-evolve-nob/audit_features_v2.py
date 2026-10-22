#!/usr/bin/env python3
"""Sanitized QE-NOB-2.0 feature/cache audit; never emits credentials or raw quote rows."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "quant_evolve_nob_v1"
OUT = ROOT / "reports" / "quant_evolve_nob_v2"
OPTION_FIELDS = ("timestamp", "open", "high", "low", "close", "iv", "volume", "strike", "oi", "spot")
UNDERLYING_FIELDS = ("timestamp", "open", "high", "low", "close", "volume")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def summarize_json_files(paths, kind, required_fields):
    files_seen = 0
    rows = 0
    field_stats = {field: {"present_files": 0, "values": 0, "missing": 0, "numeric": 0} for field in required_fields}
    timestamps = []
    errors = []
    hashes = []
    for path in sorted(paths):
        files_seen += 1
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            part = payload.get("data", payload)
            if kind == "option":
                # Dhan response may wrap CE/PE arrays. Count both sides when available.
                parts = [part.get("ce"), part.get("pe")] if isinstance(part, dict) and ("ce" in part or "pe" in part) else [part]
                parts = [x for x in parts if isinstance(x, dict)]
            else:
                parts = [part] if isinstance(part, dict) else []
            hashes.append({"file": path.name, "sha256": sha256(path), "bytes": path.stat().st_size})
            if not parts:
                errors.append({"file": path.name, "error": "no recognized data object"})
                continue
            for data in parts:
                n = len(data.get("timestamp", [])) if isinstance(data.get("timestamp"), list) else 0
                rows += n
                for field in required_fields:
                    vals = data.get(field)
                    if isinstance(vals, list):
                        field_stats[field]["present_files"] += 1
                        field_stats[field]["values"] += len(vals)
                        field_stats[field]["missing"] += sum(v is None or (isinstance(v, float) and not math.isfinite(v)) for v in vals)
                        if field != "timestamp":
                            field_stats[field]["numeric"] += sum(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v)) for v in vals)
                ts = data.get("timestamp")
                if isinstance(ts, list):
                    for v in ts:
                        try: timestamps.append(int(v))
                        except (TypeError, ValueError): pass
        except Exception as exc:
            errors.append({"file": path.name, "error": type(exc).__name__})
    fields = {}
    for field, stats in field_stats.items():
        values = stats["values"]
        fields[field] = {**stats, "missing_fraction": (stats["missing"] / values if values else None)}
    date_range = None
    if timestamps:
        parsed = pd.to_datetime(pd.Series(timestamps), unit="s", utc=True, errors="coerce").dropna()
        if not parsed.empty:
            date_range = {"start_utc": parsed.min().isoformat(), "end_utc": parsed.max().isoformat(),
                          "unique_timestamps": int(len(set(timestamps)))}
    return {"kind": kind, "files_seen": files_seen, "rows": rows, "fields": fields,
            "timestamp_range": date_range, "file_hashes": hashes, "errors": errors}


def run(cache_dir=CACHE, out_dir=OUT):
    underlying = summarize_json_files(cache_dir.glob("underlying_intraday/nifty_5m_*.json"),
                                      "underlying", UNDERLYING_FIELDS)
    option_paths = [p for p in cache_dir.glob("options_rolling/*.json") if not p.name.startswith("probe_")]
    options = summarize_json_files(option_paths, "option", OPTION_FIELDS)
    # Features are conditional until every prerequisite is met; this script does not grant point-in-time approval.
    availability = {
        "nifty_5m_ohlc": underlying["files_seen"] > 0 and underlying["fields"]["close"]["values"] > 0,
        "option_ohlc_rolling": options["files_seen"] > 0 and options["fields"]["close"]["values"] > 0,
        "option_iv": options["fields"]["iv"]["values"] > 0,
        "option_volume": options["fields"]["volume"]["values"] > 0,
        "option_oi": options["fields"]["oi"]["values"] > 0,
        "exact_contract_identity": False,
        "historical_bid_ask_depth": False,
        "india_vix": False,
        "fii_dii": False,
        "timestamped_global_leads": False,
        "point_in_time_news": False,
        "constituent_breadth": False,
    }
    report = {
        "study": "QE-NOB-2.0", "status": "AUDITED" if underlying["files_seen"] or options["files_seen"] else "NO_CACHE_FOUND",
        "cache_root": str(cache_dir), "underlying": underlying, "options": options,
        "feature_gate": availability,
        "notes": [
            "File presence and numeric values do not prove point-in-time safety, licensed use, exact contract continuity, or executable fills.",
            "Rolling option response rows are summarized by cached files; no raw quote rows are emitted.",
            "Timestamp range is UTC conversion of source epoch values; session/timezone alignment must be separately validated.",
            "Unsupported feature families remain disabled until a verified source and publication lag are documented."
        ],
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "feature_availability_v2.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, default=CACHE)
    parser.add_argument("--out-dir", type=Path, default=OUT)
    args = parser.parse_args()
    result = run(args.cache_dir, args.out_dir)
    print(json.dumps({"study": result["study"], "status": result["status"],
                      "underlying_files": result["underlying"]["files_seen"],
                      "option_files": result["options"]["files_seen"],
                      "errors": len(result["underlying"]["errors"]) + len(result["options"]["errors"]),
                      "feature_gate": result["feature_gate"]}, indent=2))
