import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

BASE = Path(__file__).parent
for module_name, filename in (
    ("strategy_grammar_v2", "strategy_grammar_v2.py"),
    ("signal_evaluator_v2", "signal_evaluator_v2.py"),
    ("option_simulator_v2", "option_simulator_v2.py"),
):
    spec = importlib.util.spec_from_file_location(module_name, BASE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

spec = importlib.util.spec_from_file_location("training_fitness_v2", BASE / "training_fitness_v2.py")
FIT = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = FIT
spec.loader.exec_module(FIT)
GRAMMAR = sys.modules["strategy_grammar_v2"]


def sample_data(extra_future=False):
    times = []
    for day in ("2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08"):
        for hhmm in ("09:15:00", "09:20:00", "09:25:00"):
            times.append(int(pd.Timestamp(f"{day} {hhmm}", tz="Asia/Kolkata").timestamp()))
    underlying = pd.DataFrame({"timestamp": times, "open": [100.0]*len(times),
                               "high": [101.0]*len(times), "low": [99.0]*len(times),
                               "close": [100.0]*len(times)})
    features = pd.DataFrame({"timestamp": times,
                             "nifty_return_1": [1.0, -1.0, -1.0]*4})
    options = pd.DataFrame({"timestamp": times, "expiry_flag": ["WEEK1"]*len(times),
                            "side": ["CALL"]*len(times), "offset": [0]*len(times),
                            "strike": [100.0]*len(times), "open": [10.0, 11.0, 12.0]*4})
    if extra_future:
        future = [int(pd.Timestamp(f"2026-01-09 {t}", tz="Asia/Kolkata").timestamp())
                  for t in ("09:15:00", "09:20:00", "09:25:00")]
        underlying = pd.concat([underlying, pd.DataFrame({
            "timestamp": future, "open": [100.0]*3, "high": [101.0]*3,
            "low": [99.0]*3, "close": [100.0]*3})], ignore_index=True)
        features = pd.concat([features, pd.DataFrame({
            "timestamp": future, "nifty_return_1": [1e9]*3})], ignore_index=True)
        options = pd.concat([options, pd.DataFrame({
            "timestamp": future, "expiry_flag": ["WEEK1"]*3, "side": ["CALL"]*3,
            "offset": [0]*3, "strike": [100.0]*3, "open": [999.0]*3})], ignore_index=True)
    return underlying, options, features


def test_chronological_split_excludes_all_future_sessions():
    u, o, f = sample_data(extra_future=True)
    train_u, train_o, train_f, cutoff = FIT.chronological_training_split(u, o, f, 0.5)
    assert cutoff.isoformat() == "2026-01-06"
    assert max(FIT._session_dates(train_u)) == cutoff
    assert max(FIT._session_dates(train_o)) == cutoff
    assert max(FIT._session_dates(train_f)) == cutoff
    assert int(train_u["timestamp"].max()) < int(u["timestamp"].max())


def test_training_score_is_unchanged_by_extreme_future_rows():
    base = sample_data(extra_future=False)
    extended = sample_data(extra_future=True)
    strategy = GRAMMAR.Strategy("signal", (GRAMMAR.Predicate("nifty_return_1", "gt", 0.0),),
                                "and", "CALL", "WEEK1", "ATM", 1,
                                (GRAMMAR.ExitRule("time_exit"),), "training split fixture")
    a = FIT.build_training_fitness_evaluator(*base, {"nifty_return_1"}, train_fraction=0.5,
                                             minimum_trades=1)
    b = FIT.build_training_fitness_evaluator(*extended, {"nifty_return_1"}, train_fraction=0.5,
                                             minimum_trades=1)
    score_a, score_b = a(strategy), b(strategy)
    assert score_a["training_cutoff_date"] == score_b["training_cutoff_date"] == "2026-01-06"
    for key in FIT.FITNESS_OBJECTIVES:
        assert score_a[key] == pytest.approx(score_b[key])
    assert score_a["execution_gate_pass"] is False
    assert score_a["score_status"] == "TRAINING_ONLY_OHLC_PROXY"


def test_training_fraction_and_minimum_trades_are_bounded():
    u, o, f = sample_data()
    with pytest.raises(ValueError, match="train_fraction"):
        FIT.chronological_training_split(u, o, f, 0.95)
    with pytest.raises(ValueError, match="minimum_trades"):
        FIT.build_training_fitness_evaluator(u, o, f, {"nifty_return_1"}, minimum_trades=0)
