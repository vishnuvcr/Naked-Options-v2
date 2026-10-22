"""Typed, deterministic strategy grammar for QE-NOB-2.0.

This module generates candidate descriptions only; it does not execute trades.
Only approved feature names can enter the grammar. Candidate expressions are data,
never eval'ed Python. A later simulator must implement each operator explicitly.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import random
from typing import Any

SCHEMA_VERSION = "qe-nob-grammar-v2.0"
ALLOWED_FEATURES = {
    "nifty_return_1", "nifty_return_3", "nifty_return_6",
    "opening_gap_pct", "opening_range_position", "opening_range_break",
    "ema_fast_slow_sign", "vwap_distance_pct", "realized_vol_percentile",
    "india_vix_percentile", "option_iv_percentile", "iv_minus_realized",
    "option_volume_change", "option_oi_change", "implied_move_edge",
    "time_of_day_bucket", "global_lead_return", "fii_dii_regime",
}
ALLOWED_OPERATORS = {
    "gt", "lt", "cross_up", "cross_down", "in_bucket",
    "and", "or", "not", "always", "regime_is",
}
ALLOWED_EXITS = {
    "time_exit", "opposite_signal", "failed_breakout",
    "regime_invalidation", "underlying_trailing_stop",
    "premium_risk_stop", "premium_target", "trail_after_target",
}
ALLOWED_INSTRUMENTS = {"CALL", "PUT", "STRADDLE", "STRANGLE"}
ALLOWED_EXPIRIES = {"WEEK1", "MONTH1"}
ALLOWED_MONEYNESS = {"ATM", "OTM1", "OTM2"}
CATEGORICAL_FEATURES = {"opening_range_break", "time_of_day_bucket", "fii_dii_regime"}
NUMERIC_OPERATORS = {"gt", "lt", "cross_up", "cross_down", "in_bucket"}
CATEGORICAL_DEFAULTS = {
    "opening_range_break": "up",
    "time_of_day_bucket": "morning",
    "fii_dii_regime": "neutral",
}
MAX_PREDICATES = 4
MAX_HOLD_BARS = 60


@dataclass(frozen=True)
class Predicate:
    feature: str
    operator: str
    value: float | int | str | bool | None = None
    second_value: float | int | str | bool | None = None


@dataclass(frozen=True)
class ExitRule:
    kind: str
    value: float | int | str | None = None


@dataclass(frozen=True)
class Strategy:
    entry_mode: str
    predicates: tuple[Predicate, ...]
    logic: str
    instrument: str
    expiry: str
    moneyness: str
    hold_bars: int
    exits: tuple[ExitRule, ...]
    hypothesis: str
    parents: tuple[str, ...] = ()
    schema_version: str = SCHEMA_VERSION


def validate_strategy(s: Strategy, available_features: set[str] | None = None) -> None:
    available = ALLOWED_FEATURES if available_features is None else ALLOWED_FEATURES & available_features
    if s.schema_version != SCHEMA_VERSION:
        raise ValueError("unsupported schema_version")
    if s.entry_mode not in {"signal", "regime_then_signal", "breakout_then_retest", "volatility_expansion"}:
        raise ValueError("invalid entry_mode")
    if not 1 <= len(s.predicates) <= MAX_PREDICATES:
        raise ValueError("predicate count outside grammar bounds")
    if s.logic not in {"and", "or"}:
        raise ValueError("invalid predicate logic")
    for p in s.predicates:
        if p.feature not in available:
            raise ValueError(f"feature unavailable or not allowlisted: {p.feature}")
        if p.operator not in ALLOWED_OPERATORS:
            raise ValueError(f"operator not allowlisted: {p.operator}")
        if p.operator in {"gt", "lt", "cross_up", "cross_down", "in_bucket", "regime_is"} and p.value is None:
            raise ValueError("operator requires a value")
        if p.operator in NUMERIC_OPERATORS:
            if p.feature in CATEGORICAL_FEATURES:
                raise ValueError("numeric operator cannot be used on a categorical feature")
            if not isinstance(p.value, (int, float)) or isinstance(p.value, bool):
                raise ValueError("numeric operator requires a numeric threshold")
        if p.operator == "in_bucket":
            if p.second_value is None:
                raise ValueError("in_bucket requires lower and upper bounds")
            if not isinstance(p.second_value, (int, float)) or isinstance(p.second_value, bool):
                raise ValueError("in_bucket upper bound must be numeric")
            if p.second_value < p.value:
                raise ValueError("in_bucket upper bound must be >= lower bound")
        if p.operator == "regime_is":
            if p.feature in CATEGORICAL_FEATURES and not isinstance(p.value, str):
                raise ValueError("categorical regime_is requires a string label")
            if p.feature not in CATEGORICAL_FEATURES and (
                not isinstance(p.value, (int, float)) or isinstance(p.value, bool)
            ):
                raise ValueError("numeric regime_is requires a numeric value")
        if p.operator in {"and", "or", "not", "always"}:
            raise ValueError("logical operators must be represented by Strategy.logic or entry_mode")
    if s.instrument not in ALLOWED_INSTRUMENTS:
        raise ValueError("invalid instrument")
    if s.expiry not in ALLOWED_EXPIRIES:
        raise ValueError("invalid expiry")
    if s.moneyness not in ALLOWED_MONEYNESS:
        raise ValueError("invalid moneyness")
    if not 1 <= int(s.hold_bars) <= MAX_HOLD_BARS:
        raise ValueError("hold_bars outside bounds")
    if not 1 <= len(s.exits) <= 3:
        raise ValueError("exit state machine must contain 1-3 rules")
    if any(e.kind not in ALLOWED_EXITS for e in s.exits):
        raise ValueError("exit kind not allowlisted")
    if not s.hypothesis.strip():
        raise ValueError("hypothesis is required")
    # Stops/targets must have positive magnitudes; execution semantics belong to simulator.
    for e in s.exits:
        if e.kind in {"underlying_trailing_stop", "premium_risk_stop", "premium_target", "trail_after_target"}:
            if not isinstance(e.value, (int, float)) or e.value <= 0:
                raise ValueError(f"{e.kind} requires a positive numeric value")


def to_dict(s: Strategy, include_lineage: bool = True) -> dict[str, Any]:
    obj = asdict(s)
    obj["predicates"] = [asdict(p) for p in s.predicates]
    obj["exits"] = [asdict(e) for e in s.exits]
    obj["parents"] = list(s.parents) if include_lineage else []
    return obj


def canonical_signature(s: Strategy) -> str:
    """Stable structural signature; hypothesis wording and lineage do not affect identity."""
    obj = to_dict(s, include_lineage=False)
    obj.pop("hypothesis", None)
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def structural_tokens(s: Strategy) -> set[str]:
    tokens = {f"entry:{s.entry_mode}", f"logic:{s.logic}", f"instrument:{s.instrument}",
              f"expiry:{s.expiry}", f"moneyness:{s.moneyness}", f"hold:{s.hold_bars}"}
    for p in s.predicates:
        tokens.add(f"feature:{p.feature}")
        tokens.add(f"operator:{p.operator}")
        tokens.add(f"value:{p.value}")
        if p.second_value is not None:
            tokens.add(f"value2:{p.second_value}")
    for i, e in enumerate(s.exits):
        tokens.add(f"exit_position:{i}:{e.kind}")
        tokens.add(f"exit_value:{e.value}")
    return tokens


def novelty_distance(a: Strategy, b: Strategy) -> float:
    """Jaccard distance over normalized structural tokens; 0 identical, 1 disjoint."""
    ta, tb = structural_tokens(a), structural_tokens(b)
    union = ta | tb
    return 0.0 if not union else 1.0 - len(ta & tb) / len(union)


def mutate(s: Strategy, rng: random.Random, available_features: set[str] | None = None) -> Strategy:
    """Apply exactly one bounded structural mutation; deterministic for a fixed RNG seed."""
    available = sorted((ALLOWED_FEATURES if available_features is None else ALLOWED_FEATURES & available_features))
    if not available:
        raise ValueError("no approved features available")
    predicates = list(s.predicates)
    exits = list(s.exits)
    operation = rng.choice(["replace_feature", "replace_operator", "add_predicate", "remove_predicate",
                            "flip_logic", "replace_exit", "change_entry", "change_hold", "change_instrument"])
    entry_modes = ["signal", "regime_then_signal", "breakout_then_retest", "volatility_expansion"]
    operators = ["gt", "lt", "cross_up", "cross_down", "in_bucket", "regime_is"]
    if operation == "replace_feature":
        i = rng.randrange(len(predicates)); p = predicates[i]
        feature = rng.choice([f for f in available if f != p.feature] or available)
        predicates[i] = Predicate(feature, p.operator, p.value, p.second_value)
    elif operation == "replace_operator":
        i = rng.randrange(len(predicates)); p = predicates[i]
        op = rng.choice([x for x in operators if x != p.operator])
        val = p.value if p.value is not None else 0.0
        second = p.second_value
        if op == "in_bucket":
            val, second = -0.01, 0.01
        elif second is not None:
            second = None
        predicates[i] = Predicate(p.feature, op, val, second)
    elif operation == "add_predicate" and len(predicates) < MAX_PREDICATES:
        feature = rng.choice(available); op = rng.choice(["gt", "lt", "cross_up", "cross_down", "regime_is"])
        predicates.append(Predicate(feature, op, 0.0))
    elif operation == "remove_predicate" and len(predicates) > 1:
        predicates.pop(rng.randrange(len(predicates)))
    elif operation == "flip_logic":
        logic = "or" if s.logic == "and" else "and"
    elif operation == "replace_exit":
        i = rng.randrange(len(exits)); kind = rng.choice(sorted(ALLOWED_EXITS - {exits[i].kind}))
        value = 0.02 if kind in {"underlying_trailing_stop", "premium_risk_stop", "premium_target", "trail_after_target"} else None
        exits[i] = ExitRule(kind, value)
    elif operation == "change_entry":
        entry_mode = rng.choice([x for x in entry_modes if x != s.entry_mode])
    elif operation == "change_hold":
        hold_bars = rng.choice([x for x in (1, 2, 3, 6, 12, 24, 36, 48, 60) if x != s.hold_bars])
    elif operation == "change_instrument":
        instrument = rng.choice([x for x in sorted(ALLOWED_INSTRUMENTS) if x != s.instrument])
    else:
        # For bounded mutations that cannot apply (e.g. adding a fifth predicate),
        # change the exit rather than silently returning the parent unchanged.
        i = rng.randrange(len(exits)); kind = rng.choice(sorted(ALLOWED_EXITS - {exits[i].kind}))
        value = 0.02 if kind in {"underlying_trailing_stop", "premium_risk_stop", "premium_target", "trail_after_target"} else None
        exits[i] = ExitRule(kind, value)
    # Repair type mismatches introduced by feature/operator mutation instead of
    # emitting invalid candidates that silently fail later during evaluation.
    for j, p in enumerate(predicates):
        if p.feature in CATEGORICAL_FEATURES:
            op = "regime_is"
            val = p.value if isinstance(p.value, str) else CATEGORICAL_DEFAULTS[p.feature]
            predicates[j] = Predicate(p.feature, op, val, None)
        else:
            op = p.operator
            val = p.value
            second = p.second_value
            if op in NUMERIC_OPERATORS and (not isinstance(val, (int, float)) or isinstance(val, bool)):
                val = 0.0
            if op == "in_bucket":
                if not isinstance(second, (int, float)) or isinstance(second, bool) or second < val:
                    second = val + 0.01
            elif second is not None:
                second = None
            if op == "regime_is" and (not isinstance(val, (int, float)) or isinstance(val, bool)):
                val = 0.0
            predicates[j] = Predicate(p.feature, op, val, second)
    child = Strategy(
        entry_mode=locals().get("entry_mode", s.entry_mode),
        predicates=tuple(predicates),
        logic=locals().get("logic", s.logic),
        instrument=locals().get("instrument", s.instrument),
        expiry=s.expiry,
        moneyness=s.moneyness,
        hold_bars=locals().get("hold_bars", s.hold_bars),
        exits=tuple(exits),
        hypothesis=f"Mutated from {canonical_signature(s)[:12]}: {operation}",
        parents=(canonical_signature(s),),
    )
    validate_strategy(child, set(available))
    if canonical_signature(child) == canonical_signature(s):
        raise RuntimeError("mutation produced structurally identical candidate")
    return child


def crossover(a: Strategy, b: Strategy, rng: random.Random) -> Strategy:
    """Combine predicate/exit subtrees from two parents; preserve bounded grammar."""
    predicates = list(a.predicates[:])
    if b.predicates:
        if predicates and rng.random() < 0.5:
            predicates[rng.randrange(len(predicates))] = rng.choice(b.predicates)
        else:
            predicates.append(rng.choice(b.predicates))
    # Canonicalize duplicate predicate tuples and enforce max size.
    unique = []
    seen = set()
    for p in predicates:
        key = (p.feature, p.operator, p.value, p.second_value)
        if key not in seen:
            seen.add(key); unique.append(p)
    predicates = unique[:MAX_PREDICATES] or [rng.choice(a.predicates or b.predicates)]
    exits = list(a.exits)
    if b.exits and rng.random() < 0.75:
        if exits and rng.random() < 0.5:
            exits[rng.randrange(len(exits))] = rng.choice(b.exits)
        else:
            exits.append(rng.choice(b.exits))
    exits = exits[:3]
    child = Strategy(
        entry_mode=rng.choice([a.entry_mode, b.entry_mode]),
        predicates=tuple(predicates),
        logic=rng.choice([a.logic, b.logic]),
        instrument=rng.choice([a.instrument, b.instrument]),
        expiry=rng.choice([a.expiry, b.expiry]),
        moneyness=rng.choice([a.moneyness, b.moneyness]),
        hold_bars=rng.choice([a.hold_bars, b.hold_bars]),
        exits=tuple(exits or [ExitRule("time_exit")]),
        hypothesis=f"Crossover of {canonical_signature(a)[:12]} and {canonical_signature(b)[:12]}",
        parents=(canonical_signature(a), canonical_signature(b)),
    )
    validate_strategy(child)
    return child
