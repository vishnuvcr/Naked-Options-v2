import importlib.util
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

BASE = Path(__file__).parent
gs = importlib.util.spec_from_file_location("strategy_grammar_v2", BASE / "strategy_grammar_v2.py")
grammar = importlib.util.module_from_spec(gs); assert gs and gs.loader
sys.modules[gs.name] = grammar; gs.loader.exec_module(grammar)
sys.modules["strategy_grammar_v2"] = grammar
es = importlib.util.spec_from_file_location("signal_evaluator_v2", BASE / "signal_evaluator_v2.py")
evaluator = importlib.util.module_from_spec(es); assert es and es.loader
sys.modules[es.name] = evaluator; es.loader.exec_module(evaluator)
sys.modules["signal_evaluator_v2"] = evaluator
ss = importlib.util.spec_from_file_location("option_simulator_v2", BASE / "option_simulator_v2.py")
sim = importlib.util.module_from_spec(ss); assert ss and ss.loader
sys.modules[ss.name] = sim; ss.loader.exec_module(sim)


def test_dated_lot_size_transitions():
    assert sim.dated_lot_size(date(2024, 4, 1), "WEEK1") == 50
    assert sim.dated_lot_size(date(2024, 5, 3), "WEEK1") == 25
    assert sim.dated_lot_size(date(2025, 1, 3), "WEEK1") == 75
    assert sim.dated_lot_size(date(2026, 2, 1), "MONTH1") == 65


def test_cost_model_has_adverse_slippage_and_fee_drag():
    zero = sim.reprice(10000, 11000, date(2026, 5, 1), 0, 10, 1)
    slip = sim.reprice(10000, 11000, date(2026, 5, 1), 50, 10, 1)
    assert slip["net_pnl_rupees"] < zero["net_pnl_rupees"]
    assert zero["net_pnl_rupees"] < zero["gross_pnl_rupees"]
    assert zero["brokerage_rupees"] == 20


def test_rejects_negative_cost_assumptions():
    s = grammar.Strategy("signal", (grammar.Predicate("nifty_return_1", "gt", 0),), "and",
                         "CALL", "WEEK1", "ATM", 1, (grammar.ExitRule("time_exit"),), "test")
    with pytest.raises(ValueError):
        sim.simulate_strategy(pd.DataFrame({"timestamp":[1],"open":[1],"close":[1]}),
                              pd.DataFrame(columns=["timestamp","expiry_flag","side","offset","strike","open"]),
                              pd.DataFrame({"timestamp":[1],"nifty_return_1":[1]}), s,
                              {"nifty_return_1"}, slippage_bps=-1)


def test_simulator_prevents_overlapping_positions_and_never_passes_execution_gate():
    strategy = grammar.Strategy("signal", (grammar.Predicate("nifty_return_1", "gt", 0),), "and",
                                "CALL", "WEEK1", "ATM", 1, (grammar.ExitRule("time_exit"),),
                                "Unit fixture only; not market evidence.")
    underlying = pd.DataFrame({"timestamp":[1,2,3,4,5],"open":[100]*5,"close":[100]*5})
    features = pd.DataFrame({"timestamp":[1,2,3,4,5],"nifty_return_1":[1,1,-1,1,-1]})
    options = pd.DataFrame({
        "timestamp":[2,3,3,4], "expiry_flag":["WEEK1"]*4, "side":["CALL"]*4,
        "offset":[0]*4, "strike":[100.0]*4, "open":[10.0,11.0,11.0,12.0]
    })
    result = sim.simulate_strategy(underlying, options, features, strategy, {"nifty_return_1"})
    assert result["trade_count"] == 1
    assert result["trades"][0]["entry_timestamp"] == 2
    assert result["trades"][0]["exit_timestamp"] == 3
    assert result["execution_gate_pass"] is False


def _stop_fixture(exit_rules, option_rows):
    strategy = grammar.Strategy("signal", (grammar.Predicate("nifty_return_1", "gt", 0),), "and",
                                "CALL", "WEEK1", "ATM", 2, tuple(exit_rules),
                                "OHLC stop fixture only; not market evidence.")
    underlying = pd.DataFrame({"timestamp":[1,2,3,4], "open":[100]*4, "close":[100]*4})
    features = pd.DataFrame({"timestamp":[1,2,3,4], "nifty_return_1":[1,-1,-1,-1]})
    options = pd.DataFrame(option_rows)
    return sim.simulate_strategy(underlying, options, features, strategy, {"nifty_return_1"})


def test_premium_stop_triggers_at_gap_open_or_stop_level():
    result = _stop_fixture([grammar.ExitRule("premium_risk_stop", 0.2), grammar.ExitRule("time_exit")], {
        "timestamp":[2,3], "expiry_flag":["WEEK1"]*2, "side":["CALL"]*2,
        "offset":[0]*2, "strike":[100.0]*2, "open":[10.0,7.5],
        "high":[10.5,9.0], "low":[9.5,7.0],
    })
    assert result["trade_count"] == 1
    assert result["trades"][0]["exit_reason"] == "premium_risk_stop"
    assert result["trades"][0]["exit_timestamp"] == 3
    assert result["trades"][0]["legs"][0]["exit_open"] == pytest.approx(7.5)


def test_premium_target_triggers_at_target_when_touched_intrabar():
    result = _stop_fixture([grammar.ExitRule("premium_target", 0.2), grammar.ExitRule("time_exit")], {
        "timestamp":[2,3,4], "expiry_flag":["WEEK1"]*3, "side":["CALL"]*3,
        "offset":[0]*3, "strike":[100.0]*3, "open":[10.0,10.5,11.0],
        "high":[10.5,12.5,11.5], "low":[9.5,10.0,10.5],
    })
    assert result["trade_count"] == 1
    assert result["trades"][0]["exit_reason"] == "premium_target"
    assert result["trades"][0]["exit_timestamp"] == 3
    assert result["trades"][0]["legs"][0]["exit_open"] == pytest.approx(12.0)


def test_premium_stop_takes_priority_if_stop_and_target_hit_same_bar():
    result = _stop_fixture([grammar.ExitRule("premium_risk_stop", 0.2), grammar.ExitRule("premium_target", 0.2)], {
        "timestamp":[2,3], "expiry_flag":["WEEK1"]*2, "side":["CALL"]*2,
        "offset":[0]*2, "strike":[100.0]*2, "open":[10.0,10.0],
        "high":[13.0,13.0], "low":[7.0,7.0],
    })
    assert result["trade_count"] == 1
    assert result["trades"][0]["exit_reason"] == "premium_risk_stop"
    assert result["trades"][0]["legs"][0]["exit_open"] == pytest.approx(8.0)


def test_unimplemented_exit_rules_fail_closed():
    strategy = grammar.Strategy("signal", (grammar.Predicate("nifty_return_1", "gt", 0),), "and",
                                "CALL", "WEEK1", "ATM", 1,
                                (grammar.ExitRule("opposite_signal"),),
                                "Unimplemented exit must not be ignored.")
    u = pd.DataFrame({"timestamp":[1,2], "open":[100,100], "close":[100,100]})
    f = pd.DataFrame({"timestamp":[1,2], "nifty_return_1":[1,-1]})
    o = pd.DataFrame(columns=["timestamp","expiry_flag","side","offset","strike","open"])
    with pytest.raises(ValueError, match="does not implement exit rule"):
        sim.simulate_strategy(u, o, f, strategy, {"nifty_return_1"})


def test_reusable_option_index_matches_inline_index():
    strategy = grammar.Strategy("signal", (grammar.Predicate("nifty_return_1", "gt", 0),), "and",
                                "CALL", "WEEK1", "ATM", 1, (grammar.ExitRule("time_exit"),),
                                "Prepared-index consistency fixture.")
    underlying = pd.DataFrame({"timestamp":[1,2,3,4], "open":[100]*4, "close":[100]*4})
    features = pd.DataFrame({"timestamp":[1,2,3,4], "nifty_return_1":[1,-1,-1,-1]})
    options = pd.DataFrame({
        "timestamp":[2,3,4], "expiry_flag":["WEEK1"]*3, "side":["CALL"]*3,
        "offset":[0]*3, "strike":[100.0]*3, "open":[10.0,11.0,12.0],
    })
    prepared = sim.prepare_option_index(options)
    inline = sim.simulate_strategy(underlying, options, features, strategy, {"nifty_return_1"})
    reused = sim.simulate_strategy(underlying, options, features, strategy, {"nifty_return_1"},
                                   prepared_option_index=prepared)
    assert inline["trade_count"] == reused["trade_count"]
    assert inline["total_net_pnl_rupees"] == pytest.approx(reused["total_net_pnl_rupees"])


def test_prepared_index_drops_conflicting_same_strike_across_offsets():
    options = pd.DataFrame({
        "timestamp":[2,2,3], "expiry_flag":["WEEK1"]*3, "side":["CALL"]*3,
        "offset":[0,1,0], "strike":[100.0,100.0,100.0], "open":[10.0,12.0,11.0],
        "high":[10.5,12.5,11.5], "low":[9.5,11.5,10.5],
    })
    prepared = sim.prepare_option_index(options)
    assert prepared["contract_collision_keys_dropped"] == 1
    assert ("WEEK1", "CALL", 2, 100.0) not in prepared["contract_lookup"]


def test_expiry_code_maps_week_family_to_week1():
    rows = pd.DataFrame({
        'timestamp': [2, 3], 'expiry_flag': ['WEEK', 'WEEK'], 'expiry_code': [1, 1],
        'side': ['CALL', 'CALL'], 'offset': [0, 0], 'strike': [100.0, 100.0], 'open': [10.0, 11.0]
    })
    index = sim.prepare_option_index(rows)
    assert ('WEEK1', 'CALL', 0, 2) in index['entry_lookup']


def test_long_holding_period_is_forced_to_close_same_session():
    day1 = [
        int(pd.Timestamp("2026-01-05 15:20:00", tz="Asia/Kolkata").timestamp()),
        int(pd.Timestamp("2026-01-05 15:25:00", tz="Asia/Kolkata").timestamp()),
    ]
    day2 = [
        int(pd.Timestamp("2026-01-06 09:15:00", tz="Asia/Kolkata").timestamp()),
        int(pd.Timestamp("2026-01-06 09:20:00", tz="Asia/Kolkata").timestamp()),
    ]
    ts = day1 + day2
    strategy = grammar.Strategy("signal", (grammar.Predicate("nifty_return_1", "gt", 0),), "and",
                                "CALL", "WEEK1", "ATM", 12, (grammar.ExitRule("time_exit"),),
                                "The long hold must not cross the overnight gap.")
    underlying = pd.DataFrame({"timestamp": ts, "open": [100]*4, "close": [100]*4})
    features = pd.DataFrame({"timestamp": ts, "nifty_return_1": [1.0, 1.0, -1.0, -1.0]})
    options = pd.DataFrame({"timestamp": ts, "expiry_flag":["WEEK1"]*4, "side":["CALL"]*4,
                            "offset":[0]*4, "strike":[100.0]*4, "open":[10.0,11.0,20.0,21.0],
                            "close":[10.5,11.5,20.5,21.5], "high":[11.0,12.0,21.0,22.0],
                            "low":[9.0,10.0,19.0,20.0]})
    result = sim.simulate_strategy(underlying, options, features, strategy, {"nifty_return_1"})
    assert result["trade_count"] == 1
    assert result["trades"][0]["exit_reason"] == "session_close"
    assert result["trades"][0]["exit_timestamp"] == day1[-1]
    assert result["trades"][0]["legs"][0]["exit_open"] == pytest.approx(11.5)


def test_equal_strike_offset_aliases_preserve_entry_keys():
    options = pd.DataFrame({
        "timestamp":[2,2,3], "expiry_flag":["WEEK"]*3, "expiry_code":[1,1,1],
        "side":["CALL"]*3, "offset":[0,1,0], "strike":[100.0,100.0,100.0],
        "open":[10.0,10.0,11.0], "high":[10.5,10.5,11.5], "low":[9.5,9.5,10.5],
        "close":[10.2,10.2,11.2],
    })
    prepared = sim.prepare_option_index(options)
    assert ("WEEK1", "CALL", 0, 2) in prepared["entry_lookup"]
    assert ("WEEK1", "CALL", 1, 2) in prepared["entry_lookup"]
    assert ("WEEK1", "CALL", 2, 100.0) in prepared["contract_lookup"]
