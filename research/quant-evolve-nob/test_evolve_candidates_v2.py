import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAMMAR_PATH = Path(__file__).with_name("strategy_grammar_v2.py")
SPEC = importlib.util.spec_from_file_location("strategy_grammar_v2", GRAMMAR_PATH)
GRAMMAR = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = GRAMMAR
SPEC.loader.exec_module(GRAMMAR)
sys.modules["strategy_grammar_v2"] = GRAMMAR

ENGINE_PATH = Path(__file__).with_name("evolve_candidates_v2.py")
ENGINE_SPEC = importlib.util.spec_from_file_location("evolve_candidates_v2", ENGINE_PATH)
ENGINE = importlib.util.module_from_spec(ENGINE_SPEC)
assert ENGINE_SPEC and ENGINE_SPEC.loader
sys.modules[ENGINE_SPEC.name] = ENGINE
ENGINE_SPEC.loader.exec_module(ENGINE)


def test_candidate_generator_is_deterministic_and_unique():
    a = ENGINE.generate(budget=100, generations=3, population_size=12, seed=73)
    b = ENGINE.generate(budget=100, generations=3, population_size=12, seed=73)
    assert a["unique_candidate_count"] == b["unique_candidate_count"]
    assert [x["signature"] for x in a["candidates"]] == [x["signature"] for x in b["candidates"]]
    assert len({x["signature"] for x in a["candidates"]}) == a["unique_candidate_count"]
    assert a["status"] == "CANDIDATES_GENERATED_NOT_BACKTESTED"


def test_candidate_generator_respects_hard_budget():
    result = ENGINE.generate(budget=40, generations=5, population_size=8, seed=8)
    assert result["unique_candidate_count"] <= 40


def test_candidate_generator_requires_approved_features():
    try:
        ENGINE.generate(features={"future_price"}, budget=10, generations=1, population_size=4)
    except ValueError:
        return
    raise AssertionError("unapproved-only feature set should be rejected")


def test_generator_never_uses_old_fitness():
    result = ENGINE.generate(budget=20, generations=2, population_size=4, seed=11)
    assert not any("fitness" in x for x in result["candidates"])
    assert "No QE-NOB-1.0 candidate score or OOS result is used as fitness or seed label." in result["important_limitations"]
