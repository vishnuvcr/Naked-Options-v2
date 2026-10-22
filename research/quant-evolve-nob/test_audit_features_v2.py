import json
from pathlib import Path
from research.quant_evolve_nob.audit_features_v2 import run


def test_audit_is_sanitized_and_handles_empty_cache(tmp_path):
    cache = tmp_path / "cache"
    out = tmp_path / "out"
    (cache / "underlying_intraday").mkdir(parents=True)
    (cache / "options_rolling").mkdir()
    report = run(cache, out)
    assert report["status"] == "NO_CACHE_FOUND"
    assert report["feature_gate"]["exact_contract_identity"] is False
    assert report["feature_gate"]["historical_bid_ask_depth"] is False
    assert (out / "feature_availability_v2.json").exists()


def test_audit_reports_fields_and_hashes(tmp_path):
    cache = tmp_path / "cache"
    out = tmp_path / "out"
    (cache / "underlying_intraday").mkdir(parents=True)
    (cache / "options_rolling").mkdir()
    underlying = {"timestamp":[1760000000,1760000300],"open":[100,101],"high":[102,103],
                  "low":[99,100],"close":[101,102],"volume":[10,12]}
    options = {"data":{"ce":{"timestamp":[1760000000],"open":[5],"high":[6],"low":[4],
                            "close":[5.5],"iv":[12.0],"volume":[200],"strike":[25000],
                            "oi":[1000],"spot":[25010]},
                      "pe":{"timestamp":[1760000000],"open":[4],"high":[5],"low":[3],
                            "close":[4.5],"iv":[13.0],"volume":[220],"strike":[25000],
                            "oi":[1200],"spot":[25010]}}}
    (cache / "underlying_intraday" / "nifty_5m_test.json").write_text(json.dumps(underlying))
    (cache / "options_rolling" / "WEEK1_2025-01-01_2025-01-05_0_CALL.json").write_text(json.dumps(options))
    report = run(cache, out)
    assert report["status"] == "AUDITED"
    assert report["underlying"]["fields"]["close"]["values"] == 2
    assert report["options"]["fields"]["close"]["values"] == 2
    assert len(report["options"]["file_hashes"]) == 1
    assert report["feature_gate"]["exact_contract_identity"] is False
