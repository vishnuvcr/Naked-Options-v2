#!/usr/bin/env python3
"""Single-call, sanitized diagnostic for Dhan's rolling expired-options API.

This is only an endpoint/data-shape probe. It never stores raw candle arrays or the token,
does not retry, and cannot authorize options P&L because the documented response schema
does not guarantee a row-level fixed expiry identifier.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

API_URL = "https://api.dhan.co/v2/charts/rollingoption"
FROM_DATE = "2026-08-03"
TO_DATE = "2026-08-05"  # end date is non-inclusive, per Dhan documentation
NIFTY_SECURITY_ID = 13


def write_report(output: Path, report: dict) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def inspect_response(payload: dict, http_status: int) -> dict:
    base = {
        "protocol": "QE-NIFTY-1.0",
        "audit_type": "single_call_dhan_expired_options_api_probe",
        "source": "DhanHQ v2 rolling expired-options endpoint",
        "documentation_url": "https://dhanhq.co/docs/v2/expired-options-data/",
        "api_url": API_URL,
        "request": {
            "exchangeSegment": "NSE_FNO",
            "securityId": NIFTY_SECURITY_ID,
            "instrument": "OPTIDX",
            "interval": "1",
            "expiryFlag": "WEEK",
            "expiryCode": 0,
            "strike": "ATM",
            "drvOptionType": "CALL",
            "fromDate": FROM_DATE,
            "toDate_exclusive": TO_DATE,
            "requiredData": ["open", "high", "low", "close", "volume", "iv", "strike", "oi", "spot"],
            "request_count": 1,
            "retry_count": 0,
        },
        "http_status": int(http_status),
        "response_top_level_keys": sorted(str(k) for k in payload.keys()),
        "api_error_code": None,
        "rows": 0,
        "data_received": False,
        "explicit_expiry_metadata_present": False,
        "row_level_lot_size_present": False,
        "pnl_permitted": False,
        "claim": None,
    }
    for key in ("errorCode", "error_code", "code"):
        value = payload.get(key)
        if isinstance(value, (str, int)) and str(value)[:32].isalnum():
            base["api_error_code"] = str(value)[:32]
            break
    data = payload.get("data")
    if not isinstance(data, dict):
        base["status"] = "API_RESPONSE_HAS_NO_DATA_OBJECT"
        return base
    base["data_top_level_keys"] = sorted(str(k) for k in data.keys())
    expiry_keys = {"expiry", "expirydate", "expiry_date", "expirydate"}
    lot_keys = {"lotsize", "lot_size", "lotunits", "sem_lot_units"}
    base["explicit_expiry_metadata_present"] = any(str(k).replace("-", "").lower() in expiry_keys for k in data)
    base["row_level_lot_size_present"] = any(str(k).replace("-", "").lower() in lot_keys for k in data)
    ce = data.get("ce")
    if not isinstance(ce, dict):
        base["status"] = "HTTP_SUCCESS_BUT_CALL_SERIES_MISSING"
        base["call_series_type"] = type(ce).__name__
        return base
    timestamps = ce.get("timestamp")
    if not isinstance(timestamps, list):
        timestamps = []
    base["rows"] = len(timestamps)
    base["data_received"] = len(timestamps) > 0
    base["call_series_keys"] = sorted(str(k) for k in ce.keys())
    count_by_field = {}
    for field in ("open", "high", "low", "close", "volume", "iv", "strike", "oi", "spot"):
        value = ce.get(field)
        count_by_field[field] = len(value) if isinstance(value, list) else 0
    base["field_value_counts"] = count_by_field
    if timestamps:
        try:
            first_epoch, last_epoch = int(timestamps[0]), int(timestamps[-1])
            tz = ZoneInfo("Asia/Kolkata")
            base["first_timestamp_ist"] = datetime.fromtimestamp(first_epoch, tz=tz).isoformat()
            base["last_timestamp_ist"] = datetime.fromtimestamp(last_epoch, tz=tz).isoformat()
            base["timestamps_monotonic_non_decreasing"] = all(
                int(timestamps[i]) <= int(timestamps[i + 1]) for i in range(len(timestamps) - 1)
            )
            base["timestamp_min_epoch"] = min(int(x) for x in timestamps)
            base["timestamp_max_epoch"] = max(int(x) for x in timestamps)
        except (TypeError, ValueError, OverflowError, OSError):
            base["timestamp_parse_status"] = "INVALID"
    strikes = ce.get("strike")
    if isinstance(strikes, list):
        numeric = [float(x) for x in strikes if isinstance(x, (int, float)) and x > 0]
        base["unique_strike_count"] = len(set(numeric))
        base["strike_min"] = min(numeric) if numeric else None
        base["strike_max"] = max(numeric) if numeric else None
    closes = ce.get("close")
    if isinstance(closes, list):
        numeric_closes = [float(x) for x in closes if isinstance(x, (int, float)) and x > 0]
        base["valid_close_count"] = len(numeric_closes)
        base["close_min"] = min(numeric_closes) if numeric_closes else None
        base["close_max"] = max(numeric_closes) if numeric_closes else None
    aligned = bool(timestamps) and all(count_by_field.get(field) == len(timestamps) for field in ("open", "high", "low", "close", "volume", "strike"))
    base["required_fields_aligned"] = aligned
    if http_status == 200 and timestamps and aligned and base.get("timestamps_monotonic_non_decreasing", False):
        base["status"] = "PASS_SAMPLE_DATA_RETRIEVED_IDENTITY_GATE_STILL_BLOCKED" if not base["explicit_expiry_metadata_present"] else "PASS_SAMPLE_DATA_RETRIEVED_REVIEW_IDENTITY"
    else:
        base["status"] = "SAMPLE_DATA_EMPTY_OR_INVALID"
    base["limitations"] = [
        "This request probes only one near-expiry ATM call series over a two-day window.",
        "The endpoint documents rolling options data relative to ATM; a rolling strike/expiry class is not a fixed contract ledger.",
        "The published response example does not include a row-level expiry field; verify exact expiry identity before any fixed-contract backtest.",
        "OHLC candles are not historical bid/ask quotes and cannot prove executable fills.",
        "This report contains only sanitized aggregate counts/ranges; raw candles and credentials are never written.",
    ]
    return base


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("reports/quantevolve/dhan_options_api_probe.json"))
    args = parser.parse_args()
    token = os.environ.get("DHAN_ACCESS_TOKEN", "").strip()
    if not token:
        write_report(args.output, {
            "protocol": "QE-NIFTY-1.0",
            "audit_type": "single_call_dhan_expired_options_api_probe",
            "status": "BLOCKED_MISSING_DHAN_ACCESS_TOKEN",
            "pnl_permitted": False,
            "claim": None,
        })
        print(json.dumps({"status": "BLOCKED_MISSING_DHAN_ACCESS_TOKEN"}))
        return 0
    body = {
        "exchangeSegment": "NSE_FNO",
        "interval": "1",
        "securityId": NIFTY_SECURITY_ID,
        "instrument": "OPTIDX",
        "expiryFlag": "WEEK",
        "expiryCode": 0,
        "strike": "ATM",
        "drvOptionType": "CALL",
        "requiredData": ["open", "high", "low", "close", "volume", "iv", "strike", "oi", "spot"],
        "fromDate": FROM_DATE,
        "toDate": TO_DATE,
    }
    try:
        response = requests.post(
            API_URL,
            headers={"Accept": "application/json", "Content-Type": "application/json", "access-token": token},
            json=body, timeout=25,
        )
        try:
            payload = response.json()
            if not isinstance(payload, dict):
                payload = {}
        except ValueError:
            payload = {}
        report = inspect_response(payload, response.status_code)
        report["request_body_sha256"] = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        report["token_value_logged"] = False
        write_report(args.output, report)
        print(json.dumps({
            "status": report["status"],
            "http_status": report["http_status"],
            "rows": report["rows"],
            "explicit_expiry_metadata_present": report["explicit_expiry_metadata_present"],
            "pnl_permitted": False,
        }, sort_keys=True))
        return 0
    except requests.RequestException as exc:
        report = {
            "protocol": "QE-NIFTY-1.0",
            "audit_type": "single_call_dhan_expired_options_api_probe",
            "status": "REQUEST_FAILED",
            "error_type": type(exc).__name__,
            "pnl_permitted": False,
            "token_value_logged": False,
            "claim": None,
        }
        write_report(args.output, report)
        print(json.dumps({"status": report["status"], "error_type": report["error_type"]}, sort_keys=True))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
