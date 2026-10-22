"""Feature availability audit for QE-NOB-2.0.

Audits the local cache without downloading licensed data or printing credentials.
It reports file counts, parseability, fields, timestamp coverage and hashes. This is
a diagnostic, not proof that rolling option rows identify exact exchange contracts.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "quant_evolve_nob_v1"
OUTPUT = ROOT / "reports" / "quant_evolve_nob_v2" / "feature_availability.json"
REQUIRED_UNDERLYING = {"timestamp", "open", "high", "low", "close"}
OPTION_FIELDS = {"timestamp", "open", "high", "low", "close", "iv", "volume", "strike", "oi", "spot"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect_json(path: Path) -> dict[str, Any]:
    try:
        display_path = str(path.relative_to(ROOT))
    except ValueError:
        # Tests and ad-hoc audits may intentionally inspect files outside the checkout.
        display_path = str(path)
    record: dict[str, Any] = {"path": display_path, "bytes": path.stat().st_size}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        record.update({"parse_status": "FAIL", "error_type": type(exc).__name__, "sha256": sha256(path)})
        return record
    data = payload.get("data", payload) if isinstance(payload, dict) else {}
    if not isinstance(data, dict):
        record.update({"parse_status": "FAIL", "reason": "top-level data is not an object", "sha256": sha256(path)})
        return record
    fields = sorted(data.keys())
    record.update({"parse_status": "PASS", "fields": fields, "sha256": sha256(path)})
    ts = data.get("timestamp")
    if isinstance(ts, list):
        record["timestamp_count"] = len(ts)
        record["timestamp_non_null"] = sum(x is not None for x in ts)
        record["timestamp_unique"] = len({str(x) for x in ts if x is not None})
        record["timestamp_min"] = min(ts) if ts else None
        record["timestamp_max"] = max(ts) if ts else None
    for key, value in data.items():
        if isinstance(value, list) and key in OPTION_FIELDS | REQUIRED_UNDERLYING:
            record.setdefault("array_lengths", {})[key] = len(value)
            record.setdefault("null_counts", {})[key] = sum(v is None for v in value)
    record["underlying_required_fields_present"] = sorted(REQUIRED_UNDERLYING & set(data))
    record["option_required_fields_present"] = sorted(OPTION_FIELDS & set(data))
    return record


def audit(cache: Path = CACHE, output: Path | None = None) -> dict[str, Any]:
    files = sorted(cache.rglob("*.json")) if cache.exists() else []
    records = [inspect_json(p) for p in files if p.is_file()]
    options = [r for r in records if "options_rolling" in r["path"]]
    underlying = [r for r in records if "underlying_intraday" in r["path"]]
    report = {
        "schema_version": "qe-nob-feature-audit-v2.0",
        "status": "PASS" if records else "BLOCKED_NO_LOCAL_CACHE",
        "cache_root": str(cache.relative_to(ROOT)) if cache.is_relative_to(ROOT) else str(cache),
        "file_count": len(records),
        "parse_failures": sum(r.get("parse_status") != "PASS" for r in records),
        "underlying_file_count": len(underlying),
        "option_file_count": len(options),
        "underlying_required_fields": sorted(REQUIRED_UNDERLYING),
        "option_required_fields": sorted(OPTION_FIELDS),
        "contract_identity_verified": False,
        "historical_bid_ask_depth_verified": False,
        "records": records,
        "limitations": [
            "Local cache audit only; absence of cache does not prove source unavailability.",
            "Field presence and non-null counts do not prove timestamp semantics or contract continuity.",
            "Rolling ATM-relative option data do not establish stable exchange contract IDs.",
            "No historical bid/ask/depth or actual broker fills are inferred.",
        ],
    }
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    result = audit(output=OUTPUT)
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, indent=2))
