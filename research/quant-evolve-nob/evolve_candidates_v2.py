"""Bounded, deterministic structural candidate generator for QE-NOB-2.0.

This is a discovery proposal generator, not a backtester. It does not assign fitness
from old QE-NOB-1.0 outcomes and cannot claim profitability. Runtime feature availability
must be supplied explicitly; default is the conservative price-only feature subset.
"""
from __future__ import annotations
import argparse
import json
import random
from pathlib import Path
from typing import Callable, Iterable, Any
import math

from strategy_grammar_v2 import (
    ALLOWED_FEATURES, ExitRule, Predicate, Strategy, canonical_signature,
    crossover, mutate, novelty_distance, validate_strategy,
)

DEFAULT_FEATURES = {
    "nifty_return_1", "nifty_return_3", "nifty_return_6", "opening_gap_pct",
    "opening_range_position", "opening_range_break", "ema_fast_slow_sign",
    "vwap_distance_pct", "time_of_day_bucket",
}
THRESHOLDS = {
    "nifty_return_1": (-0.003, -0.001, 0.0, 0.001, 0.003),
    "nifty_return_3": (-0.006, -0.002, 0.0, 0.002, 0.006),
    "nifty_return_6": (-0.01, -0.003, 0.0, 0.003, 0.01),
    "opening_gap_pct": (-0.01, -0.005, 0.0025, 0.005, 0.01),
    "opening_range_position": (-0.5, 0.0, 0.5, 1.0, 1.5),
    "opening_range_break": ("up", "down"),
    "ema_fast_slow_sign": (-1, 0, 1),
    "vwap_distance_pct": (-0.005, -0.001, 0.0, 0.001, 0.005),
    "time_of_day_bucket": ("open", "morning", "midday", "afternoon"),
}
EXIT_SEEDS = (
    (ExitRule("time_exit"),),
    (ExitRule("premium_risk_stop", 0.2), ExitRule("time_exit")),
    (ExitRule("premium_target", 0.35), ExitRule("time_exit")),
    (ExitRule("premium_risk_stop", 0.2), ExitRule("premium_target", 0.35), ExitRule("time_exit")),
)


def seed_population(features: set[str], rng: random.Random) -> list[Strategy]:
    candidates = []
    for feature in sorted(features):
        for value in THRESHOLDS.get(feature, (0.0, )):
            for op in ("gt", "lt") if isinstance(value, (int, float)) else ("regime_is",):
                predicate = Predicate(feature, op, value)
                for instrument in ("CALL", "PUT", "STRADDLE", "STRANGLE"):
                    if instrument in {"STRADDLE", "STRANGLE"} and feature in {"nifty_return_1", "nifty_return_3", "nifty_return_6", "ema_fast_slow_sign"}:
                        # Directional-only seed signals are not automatically treated as volatility signals.
                        continue
                    candidates.append(Strategy(
                        entry_mode="signal",
                        predicates=(predicate,), logic="and", instrument=instrument,
                        expiry=rng.choice(("WEEK1", "MONTH1")),
                        moneyness=rng.choice(("ATM", "OTM1", "OTM2")),
                        hold_bars=rng.choice((1, 2, 3, 6, 12, 24, 36, 48, 60)),
                        exits=rng.choice(EXIT_SEEDS),
                        hypothesis=f"Mechanism hypothesis: {feature} {op} {value!r} conditions {instrument} entry; empirical validity unknown.",
                    ))
    # Stable signatures and a shuffled order make seeded initialization reproducible.
    unique = {}
    for c in candidates:
        try:
            validate_strategy(c, features)
            unique.setdefault(canonical_signature(c), c)
        except ValueError:
            continue
    out = list(unique.values())
    rng.shuffle(out)
    return out


def _objective_vector(record: dict[str, Any], names: list[str]) -> list[float]:
    values = []
    for name in names:
        raw = record.get(name)
        values.append(float(raw) if isinstance(raw, (int, float)) and not isinstance(raw, bool)
                      and math_is_finite(float(raw)) else -1e12)
    return values


def math_is_finite(value: float) -> bool:
    return value == value and value not in (float("inf"), float("-inf"))


def _pareto_select(candidates: list[Strategy], fitness: dict[str, dict[str, Any]],
                   population_size: int) -> list[Strategy]:
    """Maximize all declared numeric fitness objectives, breaking ties by structural novelty."""
    if not candidates:
        return []
    objective_names = sorted({
        key for item in fitness.values() for key, value in item.items()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    })
    if not objective_names:
        return _novelty_select(candidates, population_size)
    remaining = list(candidates)
    selected: list[Strategy] = []
    while remaining and len(selected) < population_size:
        vectors = {canonical_signature(x): _objective_vector(fitness.get(canonical_signature(x), {}),
                                                              objective_names) for x in remaining}
        front = []
        for candidate in remaining:
            vector = vectors[canonical_signature(candidate)]
            dominated = False
            for other in remaining:
                if other is candidate:
                    continue
                other_vector = vectors[canonical_signature(other)]
                if all(a >= b for a, b in zip(other_vector, vector)) and any(
                    a > b for a, b in zip(other_vector, vector)
                ):
                    dominated = True
                    break
            if not dominated:
                front.append(candidate)
        if not front:
            front = [remaining[0]]
        slots = population_size - len(selected)
        if len(front) <= slots:
            selected.extend(front)
        else:
            pool = front[:]
            while pool and len(selected) < population_size:
                if not selected:
                    chosen = pool.pop(0)
                else:
                    chosen = max(pool, key=lambda item: min(
                        novelty_distance(item, existing) for existing in selected
                    ))
                    pool.remove(chosen)
                selected.append(chosen)
        front_sigs = {canonical_signature(x) for x in front}
        remaining = [x for x in remaining if canonical_signature(x) not in front_sigs]
    return selected


def _novelty_select(candidates: list[Strategy], population_size: int) -> list[Strategy]:
    combined = list({canonical_signature(c): c for c in candidates}.values())
    selected = []
    while combined and len(selected) < population_size:
        if not selected:
            chosen = combined.pop(0)
        else:
            chosen = max(combined, key=lambda c: min(novelty_distance(c, s) for s in selected))
            combined.remove(chosen)
        selected.append(chosen)
    return selected


def generate(features: set[str] | None = None, budget: int = 1500, generations: int = 20,
             population_size: int = 64, seed: int = 20261022,
             fitness_evaluator: Callable[[Strategy], dict[str, Any]] | None = None) -> dict:
    if not 1 <= budget <= 1500:
        raise ValueError("budget must be between 1 and 1500")
    if not 1 <= generations <= 20:
        raise ValueError("generations must be between 1 and 20")
    if population_size < 4:
        raise ValueError("population_size must be at least 4")
    active_features = set(features if features is not None else DEFAULT_FEATURES) & ALLOWED_FEATURES
    if not active_features:
        raise ValueError("no approved features available")
    rng = random.Random(seed)
    initial = seed_population(active_features, rng)
    if not initial:
        raise ValueError("no seed strategies generated from available features")
    archive: dict[str, Strategy] = {}
    fitness_archive: dict[str, dict[str, Any]] = {}
    for candidate in initial:
        signature = canonical_signature(candidate)
        if signature not in archive:
            archive[signature] = candidate
            if fitness_evaluator is not None:
                fitness_archive[signature] = dict(fitness_evaluator(candidate))
        if len(archive) >= budget:
            break
    population = list(archive.values())[:population_size]
    generation_stats = []
    for gen in range(generations):
        if len(archive) >= budget or not population:
            break
        children = []
        attempts = 0
        max_attempts = max(100, population_size * 30)
        while len(children) < population_size and len(archive) + len(children) < budget and attempts < max_attempts:
            attempts += 1
            parent = rng.choice(population)
            try:
                if rng.random() < 0.3:
                    other = rng.choice(population)
                    child = crossover(parent, other, rng)
                else:
                    child = mutate(parent, rng, active_features)
                validate_strategy(child, active_features)
                sig = canonical_signature(child)
                if sig in archive or any(canonical_signature(x) == sig for x in children):
                    continue
                # Novelty-aware parent pool: preserve structural diversity, not P&L fitness.
                nearest = min((novelty_distance(child, p) for p in population), default=1.0)
                if nearest <= 0:
                    continue
                children.append(child)
            except (ValueError, RuntimeError, IndexError):
                continue
        for child in children:
            signature = canonical_signature(child)
            if signature not in archive:
                archive[signature] = child
                if fitness_evaluator is not None:
                    fitness_archive[signature] = dict(fitness_evaluator(child))
        combined = list({canonical_signature(c): c for c in population + children}.values())
        if fitness_evaluator is None:
            population = _novelty_select(combined, population_size)
        else:
            # The callback must use training-only data. The final OOS split must never
            # be passed into this generator's fitness function.
            population = _pareto_select(combined, fitness_archive, population_size)
        generation_stats.append({
            "generation": gen + 1, "population_size": len(population),
            "unique_archive_size": len(archive), "new_children": len(children),
            "mutation_attempts": attempts,
        })
    candidates = []
    for idx, (signature, strategy) in enumerate(archive.items()):
        candidate_item = {
            "candidate_id": idx,
            "signature": signature,
            "strategy": {
                "entry_mode": strategy.entry_mode,
                "predicates": [p.__dict__ for p in strategy.predicates],
                "logic": strategy.logic,
                "instrument": strategy.instrument,
                "expiry": strategy.expiry,
                "moneyness": strategy.moneyness,
                "hold_bars": strategy.hold_bars,
                "exits": [e.__dict__ for e in strategy.exits],
                "hypothesis": strategy.hypothesis,
                "parents": list(strategy.parents),
            },
        }
        if fitness_evaluator is not None:
            candidate_item["training_fitness"] = fitness_archive.get(signature)
        candidates.append(candidate_item)
    return {
        "schema_version": "qe-nob-candidate-archive-v2.0",
        "status": "TRAINING_FITNESS_SCORED" if fitness_evaluator is not None else "CANDIDATES_GENERATED_NOT_BACKTESTED",
        "seed": seed, "budget_limit": budget, "generation_limit": generations,
        "population_size": population_size, "feature_allowlist": sorted(active_features),
        "unique_candidate_count": len(candidates), "generation_stats": generation_stats,
        "candidates": candidates,
        "important_limitations": [
            "Without a supplied callback, no fitness/P&L is calculated by this module.",
            "If a callback is supplied, its fitness values are used for Pareto environmental selection; caller must guarantee training-only data.",
            "Candidate novelty is syntactic and does not guarantee economic novelty.",
            "Feature allowlist must be replaced by a runtime-verified Phase 2 feature set before empirical search.",
            "No QE-NOB-1.0 candidate score or OOS result is used as fitness or seed label.",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget", type=int, default=1500)
    parser.add_argument("--generations", type=int, default=20)
    parser.add_argument("--population-size", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument("--output", type=Path, default=Path("reports/quant_evolve_nob_v2/candidate_archive.json"))
    args = parser.parse_args()
    result = generate(budget=args.budget, generations=args.generations,
                      population_size=args.population_size, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "candidates"}, indent=2))
