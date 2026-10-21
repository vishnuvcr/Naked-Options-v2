#!/usr/bin/env python3
"""Safe declarative strategy schema and point-in-time prediction evaluator.

LLM-generated source text is AST-parsed and literal-evaluated only. It is NEVER imported,
compiled, exec'd, or otherwise executed.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ALLOWED_FEATURES = {
    "ret_1", "ret_5", "ret_10", "ret_20",
    "vol_5", "vol_20", "vol_60", "intraday", "gap", "range",
}
SPEC_KEYS = {"version", "track", "model", "features", "weights", "intercept", "clip"}
MAX_SOURCE_BYTES = 20_000
MAX_FEATURES = 6
MAX_WEIGHT = 3.0


class SpecValidationError(ValueError):
    """Raised when a declarative candidate falls outside the permitted schema."""


def parse_spec_text(source: str) -> dict[str, Any]:
    """Parse exactly one literal STRATEGY_SPEC assignment without executing candidate source."""
    if not isinstance(source, str) or not source or len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        raise SpecValidationError("candidate source is empty or exceeds the source-size limit")
    try:
        module = ast.parse(source, mode="exec")
    except (SyntaxError, ValueError, MemoryError) as exc:
        raise SpecValidationError("candidate source is not valid bounded Python syntax") from exc
    if len(module.body) != 1:
        raise SpecValidationError("candidate must contain exactly one top-level literal assignment")
    stmt = module.body[0]
    if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
        raise SpecValidationError("candidate must contain exactly one simple assignment")
    target = stmt.targets[0]
    if not isinstance(target, ast.Name) or target.id != "STRATEGY_SPEC":
        raise SpecValidationError("only the STRATEGY_SPEC assignment is allowed")
    try:
        spec = ast.literal_eval(stmt.value)
    except (ValueError, TypeError, SyntaxError, MemoryError) as exc:
        raise SpecValidationError("strategy specification must be a Python literal") from exc
    return validate_spec(spec)


def parse_spec_file(path: str | Path) -> dict[str, Any]:
    return parse_spec_text(Path(path).read_text(encoding="utf-8"))


def _finite_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SpecValidationError(f"{field} must be a finite number")
    value = float(value)
    if not math.isfinite(value):
        raise SpecValidationError(f"{field} must be a finite number")
    return value


def validate_spec(spec: Any) -> dict[str, Any]:
    if not isinstance(spec, dict) or set(spec) != SPEC_KEYS:
        raise SpecValidationError("strategy specification has missing or unsupported fields")
    if spec["version"] != 1 or isinstance(spec["version"], bool):
        raise SpecValidationError("unsupported strategy-spec version")
    if spec["track"] != "prediction" or spec["model"] != "linear":
        raise SpecValidationError("only the prediction/linear DSL is supported")
    features = spec["features"]
    if not isinstance(features, list) or not 1 <= len(features) <= MAX_FEATURES:
        raise SpecValidationError(f"features must contain 1 to {MAX_FEATURES} entries")
    if any(not isinstance(x, str) or x not in ALLOWED_FEATURES for x in features):
        raise SpecValidationError("candidate uses a feature outside the allowlist")
    if len(set(features)) != len(features):
        raise SpecValidationError("feature names must be unique")
    weights = spec["weights"]
    if not isinstance(weights, dict) or any(k not in ALLOWED_FEATURES for k in weights):
        raise SpecValidationError("weights must map allowlisted feature names to numbers")
    if not set(features).issubset(weights):
        raise SpecValidationError("every selected feature must have an explicit weight")
    clean_weights = {}
    for key, value in weights.items():
        numeric = _finite_number(value, f"weight:{key}")
        if abs(numeric) > MAX_WEIGHT:
            raise SpecValidationError("coefficient exceeds the frozen absolute limit")
        clean_weights[key] = numeric
    intercept = _finite_number(spec["intercept"], "intercept")
    if abs(intercept) > 0.02:
        raise SpecValidationError("intercept exceeds the frozen absolute limit")
    clip = _finite_number(spec["clip"], "clip")
    if not 0.001 <= clip <= 0.10:
        raise SpecValidationError("clip must be between 0.001 and 0.10")
    return {
        "version": 1, "track": "prediction", "model": "linear",
        "features": list(features), "weights": clean_weights,
        "intercept": intercept, "clip": clip,
    }


def validate_daily_frame(data: pd.DataFrame, minimum_rows: int = 500) -> pd.DataFrame:
    required = {"date", "open", "high", "low", "close"}
    missing = sorted(required - set(data.columns))
    if missing:
        raise ValueError(f"daily NIFTY input lacks required columns: {missing}")
    frame = data.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    if frame["date"].isna().any():
        raise ValueError("invalid dates in daily NIFTY input")
    for name in ("open", "high", "low", "close"):
        frame[name] = pd.to_numeric(frame[name], errors="coerce")
    if frame[["open", "high", "low", "close"]].isna().any().any():
        raise ValueError("missing or non-numeric OHLC values")
    frame = frame.sort_values("date", kind="mergesort").reset_index(drop=True)
    if frame["date"].duplicated().any():
        raise ValueError("duplicate session dates in daily NIFTY input")
    if (frame[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("non-positive OHLC values")
    bad = (
        (frame["high"] < frame[["open", "close", "low"]].max(axis=1))
        | (frame["low"] > frame[["open", "close", "high"]].min(axis=1))
    )
    if bad.any():
        raise ValueError("inconsistent OHLC ranges")
    if len(frame) < minimum_rows:
        raise ValueError(f"insufficient rows: found {len(frame)}, require at least {minimum_rows}")
    return frame


def load_daily_csv(path: str | Path, minimum_rows: int = 500) -> pd.DataFrame:
    return validate_daily_frame(pd.read_csv(path), minimum_rows=minimum_rows)


def build_causal_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Build features at close t with past-only rolling normalization."""
    close = frame["close"].astype(float)
    open_ = frame["open"].astype(float)
    high = frame["high"].astype(float)
    low = frame["low"].astype(float)
    log_close = np.log(close)
    r1 = log_close.diff()
    raw = pd.DataFrame(index=frame.index)
    raw["ret_1"] = r1
    for horizon in (5, 10, 20):
        raw[f"ret_{horizon}"] = log_close.diff(horizon)
    for horizon in (5, 20, 60):
        raw[f"vol_{horizon}"] = r1.rolling(horizon, min_periods=horizon).std(ddof=0)
    raw["intraday"] = np.log(close / open_)
    raw["gap"] = np.log(open_ / close.shift(1))
    raw["range"] = (high - low) / close
    features = pd.DataFrame(index=frame.index)
    for name in sorted(ALLOWED_FEATURES):
        values = raw[name]
        past_mean = values.shift(1).rolling(252, min_periods=40).mean()
        past_std = values.shift(1).rolling(252, min_periods=40).std(ddof=0).replace(0.0, np.nan)
        features[name] = ((values - past_mean) / past_std).clip(-8.0, 8.0)
    return features.replace([np.inf, -np.inf], np.nan)


def compute_forecasts(features: pd.DataFrame, spec: dict[str, Any]) -> np.ndarray:
    checked = validate_spec(spec)
    matrix = features[checked["features"]].to_numpy(dtype=float)
    weights = np.asarray([checked["weights"][f] for f in checked["features"]], dtype=float)
    forecasts = checked["intercept"] + matrix @ weights
    forecasts = np.clip(forecasts, -checked["clip"], checked["clip"])
    invalid_rows = ~np.isfinite(matrix).all(axis=1)
    forecasts[invalid_rows] = np.nan
    return forecasts


def _metrics(y: np.ndarray, forecast: np.ndarray) -> dict[str, float]:
    finite = np.isfinite(y) & np.isfinite(forecast)
    y, forecast = y[finite], forecast[finite]
    if len(y) < 30:
        raise ValueError(f"too few finite evaluation rows: {len(y)}")
    mae = float(np.mean(np.abs(y - forecast)))
    zero_mae = float(np.mean(np.abs(y)))
    skill = float(1.0 - mae / zero_mae) if zero_mae > 0 else 0.0
    rmse = float(np.sqrt(np.mean(np.square(y - forecast))))
    direction = float(np.mean(np.sign(forecast) == np.sign(y)))
    return {
        "sample_count": float(len(y)), "mae": mae, "zero_baseline_mae": zero_mae,
        "mae_skill_vs_zero": skill, "rmse": rmse, "directional_accuracy": direction,
        "mean_mae_improvement": float(zero_mae - mae),
    }


def _circular_block_ci(values: np.ndarray, reps: int = 1000, block_length: int = 10) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) < 30:
        return float("nan"), float("nan")
    rng = np.random.default_rng(20261022)
    n = len(values)
    length = max(1, min(block_length, n))
    blocks_needed = int(np.ceil(n / length))
    means = np.empty(reps, dtype=float)
    for b in range(reps):
        starts = rng.integers(0, n, size=blocks_needed)
        sample = np.concatenate([values[(start + np.arange(length)) % n] for start in starts])[:n]
        means[b] = float(np.mean(sample))
    low, high = np.quantile(means, [0.025, 0.975])
    return float(low), float(high)


def evaluate_spec(frame: pd.DataFrame, spec: dict[str, Any], stage: str) -> dict[str, Any]:
    """Fitness uses development rows only; final holdout is called separately after selection."""
    if stage not in {"development", "holdout"}:
        raise ValueError("stage must be development or holdout")
    n_total = len(frame)
    n_dev = int(np.floor(n_total * 0.80))
    if n_dev < 300 or n_total - n_dev < 50:
        raise ValueError("not enough history for the frozen 80/20 chronological split")
    view = frame.iloc[:n_dev].reset_index(drop=True) if stage == "development" else frame.reset_index(drop=True)
    features = build_causal_features(view)
    checked = validate_spec(spec)
    forecast = compute_forecasts(features, checked)
    close = view["close"].astype(float).to_numpy()
    next_return = np.full(len(view), np.nan, dtype=float)
    next_return[:-1] = np.log(close[1:] / close[:-1])
    target_position = np.arange(len(view)) + 1

    if stage == "development":
        boundaries = [int(np.floor(n_dev * f)) for f in (0.55, 0.70, 0.85, 1.00)]
        fold_metrics = []
        for fold_no, (start, end) in enumerate(zip(boundaries[:-1], boundaries[1:]), start=1):
            mask = (target_position >= start) & (target_position < end)
            mask &= np.isfinite(next_return) & np.isfinite(forecast)
            fold = _metrics(next_return[mask], forecast[mask])
            fold.update({"fold": float(fold_no), "target_start_index": float(start),
                         "target_end_index_exclusive": float(end)})
            fold_metrics.append(fold)
        skills = np.asarray([x["mae_skill_vs_zero"] for x in fold_metrics], dtype=float)
        complexity = sum(abs(checked["weights"][f]) > 1e-10 for f in checked["features"])
        score = float(np.mean(skills) - 0.15 * np.std(skills) - 0.002 * complexity)
        return {"metrics": {
            "evaluation_stage": "development", "combined_score": score,
            "mean_fold_mae_skill": float(np.mean(skills)), "fold_skill_std": float(np.std(skills)),
            "mean_fold_mae": float(np.mean([x["mae"] for x in fold_metrics])),
            "mean_fold_zero_baseline_mae": float(np.mean([x["zero_baseline_mae"] for x in fold_metrics])),
            "mean_fold_directional_accuracy": float(np.mean([x["directional_accuracy"] for x in fold_metrics])),
            "sample_count": float(sum(x["sample_count"] for x in fold_metrics)),
            "fold_count": float(len(fold_metrics)), "active_features": float(complexity),
            "complexity_penalty": float(0.002 * complexity),
        }, "folds": fold_metrics}

    mask = (target_position >= n_dev) & (target_position < n_total)
    mask &= np.isfinite(next_return) & np.isfinite(forecast)
    y, pred = next_return[mask], forecast[mask]
    if len(y) < 50:
        raise ValueError("fewer than 50 valid holdout predictions remain after causal feature construction")
    metrics = _metrics(y, pred)
    improvement = np.abs(y) - np.abs(y - pred)
    ci_low, ci_high = _circular_block_ci(improvement, reps=1000, block_length=10)
    target_dates = pd.to_datetime(view["date"]).to_numpy()[target_position[mask]]
    metrics.update({
        "evaluation_stage": "holdout", "status": "PREDICTION_HOLDOUT_EVALUATED",
        "holdout_start_date": str(pd.Timestamp(target_dates.min()).date()),
        "holdout_end_date": str(pd.Timestamp(target_dates.max()).date()),
        "mae_improvement_ci95_low": ci_low, "mae_improvement_ci95_high": ci_high,
        "bootstrap_reps": 1000.0, "block_length": 10.0,
        "active_features": float(sum(abs(checked["weights"][f]) > 1e-10 for f in checked["features"])),
        "final_holdout_used_for_candidate_selection": 0.0,
    })
    return {"metrics": metrics}


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
