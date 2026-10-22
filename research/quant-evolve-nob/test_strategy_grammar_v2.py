import importlib.util
import random
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("strategy_grammar_v2.py")
SPEC = importlib.util.spec_from_file_location("strategy_grammar_v2", MODULE_PATH)
GRAMMAR = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = GRAMMAR
SPEC.loader.exec_module(GRAMMAR)
Predicate, ExitRule, Strategy = GRAMMAR.Predicate, GRAMMAR.ExitRule, GRAMMAR.Strategy
canonical_signature, crossover, mutate = GRAMMAR.canonical_signature, GRAMMAR.crossover, GRAMMAR.mutate
novelty_distance, validate_strategy = GRAMMAR.novelty_distance, GRAMMAR.validate_strategy


def base():
    return Strategy(
        entry_mode="regime_then_signal",
        predicates=(
            Predicate("nifty_return_3", "gt", 0.001),
            Predicate("realized_vol_percentile", "lt", 0.8),
        ),
        logic="and",
        instrument="CALL",
        expiry="WEEK1",
        moneyness="ATM",
        hold_bars=6,
        exits=(ExitRule("time_exit"), ExitRule("premium_risk_stop", 0.2)),
        hypothesis="Positive short-term momentum in a non-extreme volatility regime may persist.",
    )


def test_identical_structure_has_same_signature_even_with_different_hypothesis_and_lineage():
    a = base()
    b = Strategy(**{**a.__dict__, "hypothesis": "different wording", "parents": ("old-parent",)})
    assert canonical_signature(a) == canonical_signature(b)
    assert novelty_distance(a, b) == 0


def test_material_exit_change_is_novel():
    a = base()
    b = Strategy(**{**a.__dict__, "exits": (ExitRule("opposite_signal"), ExitRule("premium_target", 0.5))})
    assert canonical_signature(a) != canonical_signature(b)
    assert novelty_distance(a, b) > 0


def test_rejects_unavailable_or_unapproved_feature():
    with pytest.raises(ValueError):
        validate_strategy(base(), available_features={"nifty_return_3"})


def test_rejects_future_or_arbitrary_feature_name():
    s = Strategy("signal", (Predicate("future_close", "gt", 1.0),), "and", "CALL",
                 "WEEK1", "ATM", 6, (ExitRule("time_exit"),), "bad feature")
    with pytest.raises(ValueError):
        validate_strategy(s)


def test_rejects_invalid_stop_value():
    s = Strategy("signal", (Predicate("nifty_return_3", "gt", 0.0),), "and", "CALL",
                 "WEEK1", "ATM", 6, (ExitRule("premium_risk_stop", -0.1),), "bad stop")
    with pytest.raises(ValueError):
        validate_strategy(s)


def test_mutation_is_deterministic_and_structurally_changes_candidate():
    a = base()
    child1 = mutate(a, random.Random(42))
    child2 = mutate(a, random.Random(42))
    assert canonical_signature(child1) == canonical_signature(child2)
    assert canonical_signature(child1) != canonical_signature(a)
    assert canonical_signature(a) in child1.parents


def test_crossover_records_both_parents_and_is_valid():
    a = base()
    b = Strategy("breakout_then_retest", (Predicate("opening_range_break", "regime_is", "up"),),
                 "or", "STRANGLE", "WEEK1", "OTM1", 12,
                 (ExitRule("failed_breakout"),), "Breakout retest hypothesis.")
    child = crossover(a, b, random.Random(9))
    validate_strategy(child)
    assert set(child.parents) == {canonical_signature(a), canonical_signature(b)}


def test_mutation_respects_feature_gate():
    with pytest.raises(ValueError):
        mutate(base(), random.Random(1), available_features={"nifty_return_3"})


def test_numeric_operator_rejects_string_threshold():
    invalid = Strategy(**{**base().__dict__, "predicates": (
        Predicate("nifty_return_3", "gt", "up"),
    )})
    with pytest.raises(ValueError, match="numeric threshold"):
        validate_strategy(invalid)


def test_categorical_feature_rejects_numeric_operator():
    invalid = Strategy(**{**base().__dict__, "predicates": (
        Predicate("time_of_day_bucket", "gt", 1.0),
    )})
    with pytest.raises(ValueError, match="categorical feature"):
        validate_strategy(invalid)


def test_bucket_bounds_must_be_ordered():
    invalid = Strategy(**{**base().__dict__, "predicates": (
        Predicate("nifty_return_3", "in_bucket", 1.0, -1.0),
    )})
    with pytest.raises(ValueError, match="upper bound"):
        validate_strategy(invalid)


def test_mutation_repairs_feature_type_mismatches():
    categorical = Strategy("signal", (Predicate("time_of_day_bucket", "regime_is", "morning"),),
                           "and", "CALL", "WEEK1", "ATM", 6,
                           (ExitRule("time_exit"),), "categorical seed")
    for seed in range(50):
        child = mutate(categorical, random.Random(seed))
        validate_strategy(child)


def test_otm2_is_excluded_by_the_bounded_phase_two_data_scope():
    invalid = Strategy(**{**base().__dict__, "moneyness": "OTM2"})
    with pytest.raises(ValueError, match="invalid moneyness"):
        validate_strategy(invalid)
    for seed in range(50):
        child = mutate(base(), random.Random(seed))
        assert child.moneyness in {"ATM", "OTM1"}


def test_monthly_expiry_is_excluded_by_weekly_only_protocol():
    invalid = Strategy(**{**base().__dict__, "expiry": "MONTH1"})
    with pytest.raises(ValueError, match="invalid expiry"):
        validate_strategy(invalid)
    for seed in range(50):
        child = mutate(base(), random.Random(seed))
        assert child.expiry == "WEEK1"
