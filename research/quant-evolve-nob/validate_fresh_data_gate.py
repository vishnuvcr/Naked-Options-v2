#!/usr/bin/env python3
"""QE-NOB-3.0 fresh-data gate audit; never emits raw market data or credentials."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data/cache/quant_evolve_nob_v1"
OUT = ROOT / "reports/quant_evolve_nob_v2/fresh_data_gate_audit.json"

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def extract_option_part(payload):
    if not isinstance(payload, dict):
        return None
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        return None
    return data.get("ce") or data.get("pe") or data

def main():
    probe = read_json(ROOT / "reports/quant_evolve_nob_v2/source_probe.json")
    option = read_json(CACHE / "options_rolling/probe_week1.json")
    underlying = read_json(CACHE / "underlying_intraday/probe_underlying.json")
    part = extract_option_part(option)
    option_fields = sorted(part.keys()) if isinstance(part, dict) else []
    underlying_fields = sorted(underlying.keys()) if isinstance(underlying, dict) else []
    # The probe endpoint is explicitly rolling ATM-relative history. It cannot
    # establish a stable dated instrument identity or executable quote/fill prices.
    identity_fields = {"securityId", "instrumentToken", "contractId", "expiryDate", "expiry"}
    quote_fields = {"bid", "ask", "bidPrice", "askPrice", "bestBid", "bestAsk"}
    present_identity = sorted(identity_fields.intersection(option_fields))
    present_quotes = sorted(quote_fields.intersection(option_fields))
    probe_status = (probe or {}).get("status", "MISSING")
    underlying_rows = len((underlying or {}).get("timestamp", [])) if isinstance(underlying, dict) else 0
    option_rows = len((part or {}).get("timestamp", [])) if isinstance(part, dict) else 0
    checks = {
        "probe_report_present": probe is not None,
        "source_probe_pass": probe_status == "PASS",
        "underlying_probe_payload_present": underlying is not None,
        "underlying_probe_rows_positive": underlying_rows > 0,
        "rolling_option_probe_rows_positive": option_rows > 0,
        "stable_dated_contract_identity_in_rolling_payload": bool(present_identity),
        "executable_bid_ask_quotes_in_rolling_payload": bool(present_quotes),
    }
    # This gate is intentionally fail-closed; positive row counts do not imply
    # that a suitable historical contract-level dataset exists.
    passed = all(checks.values())
    report = {
        "research_id": "QE-NOB-3.0",
        "audited_at_utc": datetime.now(timezone.utc).isoformat(),
        "decision": "PASS" if passed else "BLOCKED_DATA_LIMITED",
        "probe_status": probe_status,
        "row_counts": {"underlying_probe": underlying_rows, "rolling_option_probe": option_rows},
        "observed_option_field_names": option_fields,
        "observed_underlying_field_names": underlying_fields,
        "contract_identity_fields_present": present_identity,
        "quote_fields_present": present_quotes,
        "checks": checks,
        "limitations": [
            "This is a small schema gate only, not full historical coverage validation.",
            "A rolling ATM-relative option series does not establish a stable dated contract.",
            "No bid/ask quote or execution fill evidence means executable option P&L cannot be validated.",
            "Raw payload values and credentials are intentionally omitted."
        ],
        "next_action": "Do not run strategy discovery until stable dated contract identifiers, historical coverage and quote/execution evidence are validated." if not passed else "Proceed to full historical coverage audit."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"decision": report["decision"], "checks": checks, "row_counts": report["row_counts"]}, indent=2))
    # Audit execution itself succeeds even when research eligibility is blocked.
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
