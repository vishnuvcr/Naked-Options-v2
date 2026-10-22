import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("feature_audit_v2.py")
SPEC = importlib.util.spec_from_file_location("feature_audit_v2", MODULE_PATH)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(AUDIT)
audit, inspect_json = AUDIT.audit, AUDIT.inspect_json


def test_inspect_json_reports_field_presence_nulls_and_hash(tmp_path):
    p = tmp_path / "sample.json"
    p.write_text(json.dumps({"timestamp": [1, 2, None], "open": [1.0, None, 3.0],
                             "high": [1.0, 2.0, 3.0], "low": [1.0, 2.0, 3.0],
                             "close": [1.0, 2.0, 3.0]}))
    result = inspect_json(p)
    assert result["parse_status"] == "PASS"
    assert result["timestamp_count"] == 3
    assert result["timestamp_non_null"] == 2
    assert result["null_counts"]["open"] == 1
    assert len(result["sha256"]) == 64
    assert set(result["underlying_required_fields_present"]) == {"timestamp", "open", "high", "low", "close"}


def test_invalid_json_is_logged_not_crashed(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{")
    result = inspect_json(p)
    assert result["parse_status"] == "FAIL"
    assert result["error_type"]


def test_missing_cache_is_explicitly_blocked(tmp_path):
    result = audit(tmp_path / "not-here")
    assert result["status"] == "BLOCKED_NO_LOCAL_CACHE"
    assert result["file_count"] == 0
    assert result["contract_identity_verified"] is False
