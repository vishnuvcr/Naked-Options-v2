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
