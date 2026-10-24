"""Strict, deterministic forecast contract for the TradingAgents NIFTY benchmark.

This module validates the *record* emitted by a future forecast adapter. It does
not generate forecasts or imply model performance. Timestamps must be timezone
aware ISO-8601 strings; data lineage must point to frozen inputs.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

ALLOWED_CLASSES = {"UP", "DOWN", "ABSTAIN"}
REQUIRED_FIELDS = {
    "schema_version",
    "instrument",
    "forecast_id",
    "cutoff_time",
    "target_start",
    "target_end",
    "prediction",
    "model_id",
    "model_revision",
    "prompt_sha256",
    "input_manifest_sha256",
    "input_asof_time",
    "created_at",
    "status",
}


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 timestamp string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} is not a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone offset")
    return parsed


def validate_forecast(record: dict[str, Any]) -> dict[str, Any]:
    """Return record unchanged when valid; raise ValueError on contract breach."""
    if not isinstance(record, dict):
        raise ValueError("forecast must be a JSON object")
    missing = sorted(REQUIRED_FIELDS - record.keys())
    extra = sorted(record.keys() - REQUIRED_FIELDS)
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")
    if extra:
        raise ValueError(f"unexpected fields: {', '.join(extra)}")
    if record["schema_version"] != "1.0":
        raise ValueError("schema_version must be '1.0'")
    if record["instrument"] != "NIFTY 50":
        raise ValueError("instrument must be exactly 'NIFTY 50'")
    for field in ("forecast_id", "model_id", "model_revision", "prompt_sha256",
                  "input_manifest_sha256", "status"):
        if not isinstance(record[field], str) or not record[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    for field in ("prompt_sha256", "input_manifest_sha256"):
        value = record[field]
        if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError(f"{field} must be a lowercase SHA-256 hex digest")
    if record["prediction"] not in ALLOWED_CLASSES:
        raise ValueError("prediction must be UP, DOWN, or ABSTAIN")
    if record["status"] != "ok":
        raise ValueError("only status='ok' forecast records are accepted")
    cutoff = _parse_timestamp(record["cutoff_time"], "cutoff_time")
    target_start = _parse_timestamp(record["target_start"], "target_start")
    target_end = _parse_timestamp(record["target_end"], "target_end")
    input_asof = _parse_timestamp(record["input_asof_time"], "input_asof_time")
    created_at = _parse_timestamp(record["created_at"], "created_at")
    if not target_start < target_end:
        raise ValueError("target_start must precede target_end")
    if input_asof > cutoff:
        raise ValueError("input_asof_time must not be later than cutoff_time")
    if created_at < cutoff:
        raise ValueError("created_at must not precede cutoff_time")
    return record
