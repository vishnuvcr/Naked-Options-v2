import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
SPEC = importlib.util.spec_from_file_location("run_discovery_v2", BASE / "run_discovery_v2.py")
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = RUNNER
SPEC.loader.exec_module(RUNNER)


def test_chronological_split_is_disjoint_and_preserves_final_block():
    days = [f"2024-{month:02d}-{day:02d}" for month in range(1, 13)
            for day in range(1, 9)]
    split = RUNNER.chronological_split(days)
    assert len(split["train"]) == 57
    assert len(split["validation"]) == 19
    assert len(split["oos"]) == 20
    assert max(split["train"]) < min(split["validation"])
    assert max(split["validation"]) < min(split["oos"])
    assert not (set(split["train"]) & set(split["oos"]))


def test_chronological_split_rejects_small_sample():
    with pytest.raises(ValueError, match="60 unique sessions"):
        RUNNER.chronological_split([str(i) for i in range(59)])


def test_holm_adjustment_is_monotonic_and_bounded():
    adjusted = RUNNER.holm_adjust({"a": 0.01, "b": 0.04, "c": 0.03})
    assert adjusted == {"a": pytest.approx(0.03), "c": pytest.approx(0.06),
                        "b": pytest.approx(0.06)}
    assert all(0 <= x <= 1 for x in adjusted.values())


def test_daily_metrics_include_zero_trade_sessions():
    sim = {
        "trades": [{"entry_date_ist": "2024-01-01", "net_pnl_rupees": 12.0}],
        "missing_entry_count": 0,
        "missing_exit_count": 0,
    }
    metrics = RUNNER.metrics_from_simulation(sim, ["2024-01-01", "2024-01-02", "2024-01-03"])
    assert metrics["mean_daily_net_rupees"] == pytest.approx(4.0)
    assert metrics["median_daily_net_rupees"] == pytest.approx(0.0)
    assert metrics["total_net_pnl_rupees"] == pytest.approx(12.0)
    assert metrics["trade_count"] == 1


def test_block_bootstrap_is_deterministic_and_detects_constant_positive_series():
    values = np.full(40, 10.0)
    a = RUNNER.moving_block_bootstrap(values, seed=17, replicates=300, block_length=5)
    b = RUNNER.moving_block_bootstrap(values, seed=17, replicates=300, block_length=5)
    assert a == b
    assert a["ci95_low"] == pytest.approx(10.0)
    assert a["ci95_high"] == pytest.approx(10.0)
    assert a["p_value"] < 0.01


def test_bootstrap_is_reproducible_on_mixed_returns():
    x = np.asarray([2.0, -1.0, 3.0, 0.0, 4.0, -2.0, 1.0, 3.0])
    assert RUNNER.moving_block_bootstrap(x, 29, 200, 3) == RUNNER.moving_block_bootstrap(x, 29, 200, 3)


def test_cache_audit_requires_both_source_families_and_zero_parse_failures():
    good = {'status':'PASS','file_count':3,'parse_failures':0,'underlying_file_count':1,'option_file_count':2}
    assert RUNNER.cache_audit_pass(good)
    assert not RUNNER.cache_audit_pass({**good,'parse_failures':1})
    assert not RUNNER.cache_audit_pass({**good,'option_file_count':0})
    assert not RUNNER.cache_audit_pass({'status':'BLOCKED_NO_LOCAL_CACHE'})


def test_data_quality_gate_blocks_low_coverage_and_conflicting_duplicates():
    good = {"option_timestamp_coverage": 0.99, "row_grid_coverage": 0.97,
            "conflicting_duplicate_rate": 0.001}
    assert RUNNER.data_quality_gate(good)
    assert not RUNNER.data_quality_gate({**good, "option_timestamp_coverage": 0.89})
    assert not RUNNER.data_quality_gate({**good, "row_grid_coverage": 0.89})
    assert not RUNNER.data_quality_gate({**good, "conflicting_duplicate_rate": 0.006})
    assert not RUNNER.data_quality_gate({"option_timestamp_coverage": 0.99})
