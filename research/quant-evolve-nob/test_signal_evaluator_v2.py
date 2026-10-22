import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

BASE = Path(__file__).parent
gs = importlib.util.spec_from_file_location("strategy_grammar_v2", BASE / "strategy_grammar_v2.py")
grammar = importlib.util.module_from_spec(gs)
assert gs and gs.loader
sys.modules[gs.name] = grammar
gs.loader.exec_module(grammar)
sys.modules["strategy_grammar_v2"] = grammar
es = importlib.util.spec_from_file_location("signal_evaluator_v2", BASE / "signal_evaluator_v2.py")
evaluator = importlib.util.module_from_spec(es)
assert es and es.loader
sys.modules[es.name] = evaluator
es.loader.exec_module(evaluator)


def strategy():
    return grammar.Strategy(
        entry_mode="signal",
        predicates=(grammar.Predicate("nifty_return_1", "gt", 0.0),),
        logic="and", instrument="CALL", expiry="WEEK1", moneyness="ATM",
        hold_bars=3, exits=(grammar.ExitRule("time_exit"),),
        hypothesis="Positive one-bar return may persist.",
    )


def test_signal_uses_current_completed_bar_and_next_bar_entry():
    frame = pd.DataFrame({"timestamp": [3, 1, 2, 4], "nifty_return_1": [0.2, -0.1, 0.1, 0.3]})
    result = evaluator.evaluate_signals(frame, strategy(), {"nifty_return_1"})
    assert result["timestamp"].tolist() == [2, 3]
    assert result["entry_timestamp"].tolist() == [3, 4]


def test_missing_feature_is_rejected():
    with pytest.raises(ValueError):
        evaluator.evaluate_signals(pd.DataFrame({"timestamp": [1, 2]}), strategy(), {"nifty_return_1"})


def test_duplicate_timestamps_are_rejected():
    frame = pd.DataFrame({"timestamp": [1, 1], "nifty_return_1": [0.1, 0.2]})
    with pytest.raises(ValueError):
        evaluator.evaluate_signals(frame, strategy(), {"nifty_return_1"})


def test_cross_up_does_not_use_future_row():
    p = grammar.Predicate("nifty_return_1", "cross_up", 0.0)
    frame = pd.DataFrame({"timestamp": [1, 2, 3], "nifty_return_1": [-1.0, 1.0, 2.0]})
    mask = evaluator._predicate_mask(frame, p)
    assert mask.tolist() == [False, True, False]


def test_categorical_feature_rejects_numeric_comparison():
    p = grammar.Predicate("time_of_day_bucket", "gt", "morning")
    frame = pd.DataFrame({"time_of_day_bucket": ["open", "morning"]})
    with pytest.raises(ValueError):
        evaluator._predicate_mask(frame, p)


def test_sparse_signals_still_enter_on_next_market_bar():
    frame = pd.DataFrame({"timestamp": [1, 2, 3, 4, 5],
                          "nifty_return_1": [0.1, -0.1, -0.2, 0.2, -0.1]})
    result = evaluator.evaluate_signals(frame, strategy(), {"nifty_return_1"})
    assert result["timestamp"].tolist() == [1, 4]
    assert result["entry_timestamp"].tolist() == [2, 5]
