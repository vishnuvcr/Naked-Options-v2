#!/usr/bin/env python3
"""Bounded QE-NOB-2.0 discovery and validation runner.

Reads the existing isolated Dhan cache only; this file does not issue API requests.
Strategy evolution receives training-split fitness only. Validation ranks finalists;
the final chronological OOS period is evaluated only after finalist selection.
All results remain indicative OHLC results because contract identity and executable
historical quotes are not verified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Script is executed from the research directory; use the existing source loader only
# for its isolated cache parsing. Prior QE-NOB-1.0 strategy scores are never imported.
import run_research as source_client
from feature_builder_v2 import build_features
from strategy_grammar_v2 import Predicate, ExitRule, Strategy
from evolve_candidates_v2 import generate
from option_simulator_v2 import prepare_option_index, simulate_strategy

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "quant_evolve_nob_v2"
SCHEMA = "qe-nob-discovery-run-v2.0"
DEFAULT_SEEDS = (1729, 20261022, 8675309, 31415927)
PRIMARY_SLIPPAGE_BPS = 50
PRIMARY_BROKERAGE = 10
FINALIST_LIMIT = 25
BOOTSTRAP_REPLICATES = 5000
BOOTSTRAP_BLOCK_SESSIONS = 5


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cache_manifest() -> dict[str, Any]:
    paths = sorted([p for root in (source_client.OPT_CACHE, source_client.IDX_CACHE)
                    for p in root.glob("*.json") if p.is_file()])
    entries = []
    for p in paths:
        entries.append({
            "path": str(p.relative_to(ROOT)),
            "bytes": int(p.stat().st_size),
            "sha256": sha256_file(p),
        })
    return {
        "file_count": len(entries),
        "underlying_file_count": sum("underlying_intraday" in x["path"] for x in entries),
        "option_file_count": sum("options_rolling" in x["path"] for x in entries),
        "manifest_sha256": hashlib.sha256(
            json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "files": entries,
    }


def chronological_split(unique_days: list[str]) -> dict[str, list[str]]:
    """Freeze disjoint train/validation/OOS date blocks in chronological order."""
    days = sorted(set(map(str, unique_days)))
    if len(days) < 60:
        raise ValueError("at least 60 unique sessions are required")
    train_end = max(1, int(len(days) * 0.60))
    validation_end = max(train_end + 1, int(len(days) * 0.80))
    blocks = {"train": days[:train_end], "validation": days[train_end:validation_end],
              "oos": days[validation_end:]}
    if not blocks["train"] or not blocks["validation"] or len(blocks["oos"]) < 20:
        raise ValueError("chronological blocks are too small")
    if set(blocks["train"]) & set(blocks["validation"]):
        raise AssertionError("train and validation overlap")
    if set(blocks["train"]) & set(blocks["oos"]) or set(blocks["validation"]) & set(blocks["oos"]):
        raise AssertionError("OOS must be disjoint from all model-selection periods")
    return blocks


def strategy_from_record(record: dict[str, Any]) -> Strategy:
    obj = record["strategy"]
    return Strategy(
        entry_mode=obj["entry_mode"],
        predicates=tuple(Predicate(**item) for item in obj["predicates"]),
        logic=obj["logic"],
        instrument=obj["instrument"],
        expiry=obj["expiry"],
        moneyness=obj["moneyness"],
        hold_bars=int(obj["hold_bars"]),
        exits=tuple(ExitRule(**item) for item in obj["exits"]),
        hypothesis=obj["hypothesis"],
        parents=tuple(obj.get("parents", [])),
    )


def daily_pnl_from_simulation(sim: dict[str, Any], sessions: list[str]) -> np.ndarray:
    totals: dict[str, float] = defaultdict(float)
    for trade in sim.get("trades", []):
        totals[str(trade["entry_date_ist"])] += float(trade["net_pnl_rupees"])
    return np.asarray([totals.get(str(session), 0.0) for session in sessions], dtype=float)


def metrics_from_simulation(sim: dict[str, Any], sessions: list[str]) -> dict[str, Any]:
    daily = daily_pnl_from_simulation(sim, sessions)
    trades = sim.get("trades", [])
    trade_count = len(trades)
    cumulative = np.cumsum(daily)
    equity_with_initial = np.concatenate(([0.0], cumulative))
    running_peak = np.maximum.accumulate(equity_with_initial)
    drawdown = running_peak - equity_with_initial
    max_dd = float(np.max(drawdown)) if len(drawdown) else 0.0
    blocks = [float(np.mean(block)) for block in np.array_split(daily, min(4, max(1, len(daily))))
              if len(block)]
    block_std = float(np.std(blocks, ddof=0)) if blocks else 0.0
    net_trade = float(np.mean([float(t["net_pnl_rupees"]) for t in trades])) if trades else None
    return {
        "trade_count": int(trade_count),
        "missing_entry_count": int(sim.get("missing_entry_count", 0)),
        "missing_exit_count": int(sim.get("missing_exit_count", 0)),
        "total_net_pnl_rupees": float(np.sum(daily)) if len(daily) else 0.0,
        "mean_daily_net_rupees": float(np.mean(daily)) if len(daily) else 0.0,
        "median_daily_net_rupees": float(np.median(daily)) if len(daily) else 0.0,
        "mean_net_per_trade_rupees": net_trade,
        "max_drawdown_rupees": max_dd,
        "negative_max_drawdown_rupees": -max_dd,
        "stability_score": -block_std,
        "minimum_block_mean_daily_rupees": float(min(blocks)) if blocks else 0.0,
        "positive_session_fraction": float(np.mean(daily > 0)) if len(daily) else 0.0,
        "_daily": daily,
        "_trades": trades,
    }


def fitness_metrics(u: pd.DataFrame, features: pd.DataFrame, options: pd.DataFrame,
                    option_index: dict, strategy: Strategy,
                    available_features: set[str], sessions: list[str],
                    error_counts: Counter) -> dict[str, float]:
    try:
        sim = simulate_strategy(
            u, options, features, strategy, available_features,
            slippage_bps=PRIMARY_SLIPPAGE_BPS,
            brokerage_per_order=PRIMARY_BROKERAGE,
            prepared_option_index=option_index,
        )
        m = metrics_from_simulation(sim, sessions)
        count = m["trade_count"]
        # All fitness objectives are maximized; empty/no-trade candidates are penalized.
        return {
            "mean_daily_net_rupees": float(m["mean_daily_net_rupees"]),
            "mean_net_per_trade_rupees": float(m["mean_net_per_trade_rupees"]) if count else -1e6,
            "negative_max_drawdown_rupees": float(m["negative_max_drawdown_rupees"]),
            "stability_score": float(m["stability_score"]),
            "trade_count_score": min(float(count) / 150.0, 1.0),
        }
    except Exception as exc:
        error_counts[type(exc).__name__ + ":" + str(exc)[:120]] += 1
        return {
            "mean_daily_net_rupees": -1e6,
            "mean_net_per_trade_rupees": -1e6,
            "negative_max_drawdown_rupees": -1e6,
            "stability_score": -1e6,
            "trade_count_score": 0.0,
        }


def evaluate_one(u: pd.DataFrame, features: pd.DataFrame, options: pd.DataFrame,
                 option_index: dict, strategy: Strategy, available_features: set[str],
                 sessions: list[str], slippage: float, brokerage: float) -> tuple[dict[str, Any], dict[str, Any]]:
    sim = simulate_strategy(
        u, options, features, strategy, available_features,
        slippage_bps=slippage, brokerage_per_order=brokerage,
        prepared_option_index=option_index,
    )
    return metrics_from_simulation(sim, sessions), sim


def moving_block_bootstrap(daily: np.ndarray, seed: int,
                           replicates: int = BOOTSTRAP_REPLICATES,
                           block_length: int = BOOTSTRAP_BLOCK_SESSIONS) -> dict[str, Any]:
    """Moving-block confidence interval and one-sided centered-null p-value."""
    values = np.asarray(daily, dtype=float)
    n = len(values)
    if n < 2:
        return {"ci95_low": None, "ci95_high": None, "p_value": 1.0,
                "median_ci95_low": None, "median_ci95_high": None, "n_sessions": n}
    block = min(max(1, int(block_length)), n)
    rng = np.random.default_rng(seed)

    def draw_means(source: np.ndarray) -> np.ndarray:
        output = np.empty(replicates, dtype=float)
        for b in range(replicates):
            chunks: list[np.ndarray] = []
            total = 0
            while total < n:
                start = int(rng.integers(0, max(1, n - block + 1)))
                part = source[start:start + block]
                chunks.append(part)
                total += len(part)
            sample = np.concatenate(chunks)[:n]
            output[b] = float(np.mean(sample))
        return output

    means = draw_means(values)
    medians = np.empty(replicates, dtype=float)
    # Reuse the same seeded stream and block design for median uncertainty.
    for b in range(replicates):
        chunks = []
        total = 0
        while total < n:
            start = int(rng.integers(0, max(1, n - block + 1)))
            part = values[start:start + block]
            chunks.append(part)
            total += len(part)
        medians[b] = float(np.median(np.concatenate(chunks)[:n]))
    observed = float(np.mean(values))
    null_means = draw_means(values - observed)
    p_value = float((1 + np.sum(null_means >= observed)) / (replicates + 1))
    return {
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "median_ci95_low": float(np.quantile(medians, 0.025)),
        "median_ci95_high": float(np.quantile(medians, 0.975)),
        "p_value": p_value,
        "n_sessions": int(n),
        "block_length_sessions": int(block),
        "replicates": int(replicates),
    }


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    count = len(ordered)
    adjusted: dict[str, float] = {}
    running = 0.0
    for index, (key, pvalue) in enumerate(ordered):
        running = max(running, min(1.0, (count - index) * float(pvalue)))
        adjusted[key] = running
    return adjusted


def data_quality_gate(quality: dict[str, Any], minimum_coverage: float = 0.90,
                      maximum_conflicting_duplicate_rate: float = 0.005) -> bool:
    """Require aligned options/underlying coverage before scoring candidate strategies."""
    try:
        option_coverage = float(quality.get("option_timestamp_coverage", 0.0) or 0.0)
        grid_coverage = float(quality.get("row_grid_coverage", 0.0) or 0.0)
        conflict_rate = float(quality.get("conflicting_duplicate_rate", 1.0))
    except (TypeError, ValueError):
        return False
    return (option_coverage >= minimum_coverage and grid_coverage >= minimum_coverage and
            conflict_rate <= maximum_conflicting_duplicate_rate)


def cache_audit_pass(audit: dict[str, Any]) -> bool:
    """Fail closed unless both source families are present and every JSON parses."""
    return bool(
        audit.get("status") == "PASS"
        and int(audit.get("file_count", 0)) > 0
        and int(audit.get("parse_failures", 0)) == 0
        and int(audit.get("underlying_file_count", 0)) > 0
        and int(audit.get("option_file_count", 0)) > 0
    )


def output_blocked(reason: str, cache: dict[str, Any], quality: dict[str, Any] | None = None) -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    result = {
        "schema_version": SCHEMA,
        "research_id": "QE-NOB-2.0",
        "status": "DATA_BLOCKED",
        "decision": "DATA-LIMITED",
        "reason": reason,
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "cache": {k: v for k, v in cache.items() if k != "files"},
        "data_quality": quality or {},
        "candidate_count": 0,
        "statistical_candidate_count": 0,
        "execution_gate_pass": False,
        "execution_gate_reason": "Exact contract identity and executable historical bid/ask/depth are not verified.",
    }
    (OUT / "run_summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (OUT / "RESULTS.md").write_text(
        "# QE-NOB-2.0 bounded discovery result\n\n"
        "**Decision: DATA-LIMITED.** No candidate fitness or profitability conclusion was produced.\n\n"
        f"Reason: {reason}\n\n"
        f"Cache files audited: {cache.get('file_count', 0)}; cache manifest SHA-256: {cache.get('manifest_sha256', '')}.\n\n"
        "No strategy is recommended. The execution gate is FAIL until exact contracts and executable quote/fill evidence are established.\n",
        encoding="utf-8",
    )
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    cache = cache_manifest()
    audit_module = None
    try:
        import feature_audit_v2 as audit_module
        audit = audit_module.audit(output=OUT / "feature_availability.json")
    except Exception as exc:
        audit = {"status": "AUDIT_ERROR", "error_type": type(exc).__name__}
    if not cache_audit_pass(audit):
        return output_blocked(
            "Cache audit gate failed: require parseable underlying and option files with zero JSON parse failures. Source unavailability is not inferred.",
            cache, audit,
        )

    u, o, quality = source_client.load_frames(return_quality=True)
    if not data_quality_gate(quality):
        return output_blocked(
            "Pre-discovery quality gate failed: require aligned option timestamp/grid coverage >=90% and conflicting duplicate rate <=0.5%.",
            cache, quality,
        )
    if len(u) < 500 or len(o) < 1000:
        return output_blocked(
            f"Insufficient cache rows for a bounded study (underlying={len(u)}, options={len(o)}).",
            cache, quality,
        )

    feature_input = u[["timestamp", "open", "high", "low", "close"] +
                      (["volume"] if "volume" in u.columns else [])].copy()
    feature_frame, feature_meta = build_features(feature_input, minimum_coverage=args.minimum_feature_coverage)
    feature_dates = pd.to_datetime(feature_frame["timestamp"], unit="s", utc=True).dt.tz_convert("Asia/Kolkata").dt.strftime("%Y-%m-%d")
    feature_frame["session_date"] = feature_dates
    u = u.copy()
    if "date" not in u.columns:
        u["date"] = pd.to_datetime(u["timestamp"], unit="s", utc=True).dt.tz_convert("Asia/Kolkata").dt.strftime("%Y-%m-%d")
    unique_days = sorted(u["date"].dropna().astype(str).unique().tolist())
    try:
        split = chronological_split(unique_days)
    except ValueError as exc:
        return output_blocked(str(exc), cache, quality)
    train_days = split["train"]
    validation_days = split["validation"]
    oos_days = split["oos"]

    u_train = u[u["date"].astype(str).isin(set(train_days))].copy().reset_index(drop=True)
    f_train = feature_frame[feature_frame["session_date"].isin(set(train_days))].drop(columns="session_date").copy().reset_index(drop=True)
    u_validation = u[u["date"].astype(str).isin(set(validation_days))].copy().reset_index(drop=True)
    f_validation = feature_frame[feature_frame["session_date"].isin(set(validation_days))].drop(columns="session_date").copy().reset_index(drop=True)
    u_oos = u[u["date"].astype(str).isin(set(oos_days))].copy().reset_index(drop=True)
    f_oos = feature_frame[feature_frame["session_date"].isin(set(oos_days))].drop(columns="session_date").copy().reset_index(drop=True)

    # Feature eligibility is frozen from the training partition only. Full-sample
    # coverage/variation is diagnostic and must not influence the search grammar.
    train_feature_input = u_train[["timestamp", "open", "high", "low", "close"] +
                                  (["volume"] if "volume" in u_train.columns else [])].copy()
    _, training_feature_meta = build_features(
        train_feature_input, minimum_coverage=args.minimum_feature_coverage
    )
    active_features = set(training_feature_meta["available_features"])
    if not active_features:
        return output_blocked("No derived feature passed training-only coverage and variation gates.", cache, quality)
    if len(args.seeds) != args.islands:
        return output_blocked("The number of fixed seeds must equal the declared island count.", cache, quality)

    # Index source option data once and reuse the immutable lookup across all candidates.
    option_index = prepare_option_index(o)
    error_counts: Counter = Counter()
    island_archives = []
    island_budget = int(math.ceil(args.budget / args.islands))
    for island_id, seed in enumerate(args.seeds, start=1):
        scorer = lambda strategy, u0=u_train, f0=f_train, s0=train_days: fitness_metrics(
            u0, f0, o, option_index, strategy, active_features, s0, error_counts
        )
        generated = generate(
            features=active_features, budget=island_budget,
            generations=args.generations, population_size=args.population_size,
            seed=seed, fitness_evaluator=scorer,
        )
        island_archives.append({
            "island_id": island_id, "seed": seed,
            "unique_candidate_count": generated["unique_candidate_count"],
            "generation_stats": generated["generation_stats"],
            "candidates": generated["candidates"],
        })

    # Pool/deduplicate independent island archives after evolution; no island consumes OOS.
    unique_records: dict[str, dict[str, Any]] = {}
    for island in island_archives:
        for record in island["candidates"]:
            signature = record["signature"]
            if signature not in unique_records:
                item = dict(record)
                item["island_ids"] = [island["island_id"]]
                unique_records[signature] = item
            else:
                unique_records[signature]["island_ids"].append(island["island_id"])
    candidates = list(unique_records.values())
    if not candidates:
        return output_blocked("The bounded grammar did not produce valid candidates from the audited features.", cache, quality)

    candidate_training = []
    for i, record in enumerate(candidates):
        fit = record.get("training_fitness") or {}
        candidate_training.append({
            "candidate_id": i,
            "signature": record["signature"],
            "island_ids": ",".join(map(str, record.get("island_ids", []))),
            "instrument": record["strategy"]["instrument"],
            "expiry": record["strategy"]["expiry"],
            "moneyness": record["strategy"]["moneyness"],
            "hold_bars": record["strategy"]["hold_bars"],
            "entry_predicate_count": len(record["strategy"]["predicates"]),
            "exit_rules": "+".join(x["kind"] for x in record["strategy"]["exits"]),
            "hypothesis": record["strategy"]["hypothesis"],
            "training_mean_daily_net_rupees": fit.get("mean_daily_net_rupees"),
            "training_mean_net_per_trade_rupees": fit.get("mean_net_per_trade_rupees"),
            "training_negative_max_drawdown_rupees": fit.get("negative_max_drawdown_rupees"),
            "training_stability_score": fit.get("stability_score"),
            "training_trade_count_score": fit.get("trade_count_score"),
        })
    candidate_training_frame = pd.DataFrame(candidate_training)
    candidate_training_frame.to_csv(OUT / "candidate_training_metrics.csv", index=False)
    (OUT / "candidate_archive.json").write_text(json.dumps({
        "schema_version": "qe-nob-candidate-archive-pooled-v2.0",
        "status": "TRAINING_FITNESS_SCORED",
        "budget_limit": args.budget,
        "actual_unique_candidate_count": len(candidates),
        "island_count": args.islands,
        "per_island_budget": island_budget,
        "seeds": list(args.seeds),
        "generation_limit": args.generations,
        "population_size": args.population_size,
        "training_split_end": train_days[-1],
        "feature_allowlist": sorted(active_features),
        "islands": [{k: v for k, v in island.items() if k != "candidates"} for island in island_archives],
        "candidates": candidates,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Validation selection: rank every unique candidate on the middle chronological block.
    validation_rows = []
    for i, record in enumerate(candidates):
        strategy = strategy_from_record(record)
        try:
            metrics, _ = evaluate_one(
                u_validation, f_validation, o, option_index, strategy, active_features,
                validation_days, PRIMARY_SLIPPAGE_BPS, PRIMARY_BROKERAGE,
            )
        except Exception as exc:
            error_counts[type(exc).__name__ + ":" + str(exc)[:120]] += 1
            metrics = {"trade_count": 0, "mean_daily_net_rupees": -1e6,
                       "mean_net_per_trade_rupees": None, "negative_max_drawdown_rupees": -1e6,
                       "stability_score": -1e6, "total_net_pnl_rupees": -1e6,
                       "max_drawdown_rupees": 1e6, "_daily": np.zeros(len(validation_days)), "_trades": []}
        validation_rows.append({
            "candidate_id": i, "signature": record["signature"],
            "validation_trade_count": metrics["trade_count"],
            "validation_total_net_pnl_rupees": metrics["total_net_pnl_rupees"],
            "validation_mean_daily_net_rupees": metrics["mean_daily_net_rupees"],
            "validation_median_daily_net_rupees": metrics["median_daily_net_rupees"],
            "validation_mean_net_per_trade_rupees": metrics["mean_net_per_trade_rupees"],
            "validation_max_drawdown_rupees": metrics["max_drawdown_rupees"],
            "validation_negative_max_drawdown_rupees": metrics["negative_max_drawdown_rupees"],
            "validation_stability_score": metrics["stability_score"],
        })
    validation_table = pd.DataFrame(validation_rows)
    valid_for_rank = validation_table["validation_trade_count"] >= args.minimum_validation_trades
    rank_table = validation_table[valid_for_rank].copy()
    if not rank_table.empty:
        rank_table["rank_net"] = rank_table["validation_mean_daily_net_rupees"].rank(pct=True)
        rank_table["rank_dd"] = rank_table["validation_negative_max_drawdown_rupees"].rank(pct=True)
        rank_table["rank_stability"] = rank_table["validation_stability_score"].rank(pct=True)
        rank_table["rank_trade_count"] = rank_table["validation_trade_count"].rank(pct=True)
        rank_table["validation_selection_score"] = (
            rank_table["rank_net"] + rank_table["rank_dd"] +
            rank_table["rank_stability"] + rank_table["rank_trade_count"]
        )
        selected_rows = rank_table.sort_values(
            ["validation_selection_score", "validation_mean_daily_net_rupees"],
            ascending=[False, False],
        ).head(min(args.finalists, FINALIST_LIMIT))
    else:
        selected_rows = rank_table
    validation_table = validation_table.merge(
        selected_rows[["signature", "validation_selection_score"]], on="signature",
        how="left"
    ) if not selected_rows.empty else validation_table.assign(validation_selection_score=np.nan)
    validation_table.to_csv(OUT / "candidate_validation_metrics.csv", index=False)

    if selected_rows.empty:
        decision = "DATA-LIMITED"
        reason = "No candidate met the minimum validation trade-count floor; OOS was not opened for candidate selection."
        summary = {
            "schema_version": SCHEMA, "research_id": "QE-NOB-2.0",
            "status": "VALIDATION_GATE_BLOCKED", "decision": decision,
            "reason": reason, "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
            "cache": {k: v for k, v in cache.items() if k != "files"},
            "data_quality": quality, "feature_metadata": feature_meta,
            "training_feature_metadata": training_feature_meta,
            "session_split": {"train": [train_days[0], train_days[-1]],
                              "validation": [validation_days[0], validation_days[-1]],
                              "oos": [oos_days[0], oos_days[-1]]},
            "candidate_count": len(candidates), "validation_eligible_count": len(rank_table),
            "finalist_count": 0, "statistical_candidate_count": 0,
            "execution_gate_pass": False,
            "execution_gate_reason": "Exact contract identity and executable historical bid/ask/depth are not verified.",
            "simulation_errors": dict(error_counts),
        }
        (OUT / "run_summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
        (OUT / "RESULTS.md").write_text(
            "# QE-NOB-2.0 bounded discovery result\n\n**Decision: DATA-LIMITED.**\n\n" + reason +
            "\n\nNo strategy is recommended. No final OOS evaluation was performed because the validation trade-count gate did not pass.\n",
            encoding="utf-8",
        )
        return summary

    by_signature = {record["signature"]: record for record in candidates}
    oos_rows = []
    trade_rows = []
    stress_rows = []
    pvalues: dict[str, float] = {}
    oos_metrics_by_sig: dict[str, dict[str, Any]] = {}
    # OOS is accessed only after the validation-ranked finalist list has been frozen.
    for rank, selected in enumerate(selected_rows.itertuples(index=False), start=1):
        record = by_signature[str(selected.signature)]
        strategy = strategy_from_record(record)
        primary_metrics, primary_sim = evaluate_one(
            u_oos, f_oos, o, option_index, strategy, active_features,
            oos_days, PRIMARY_SLIPPAGE_BPS, PRIMARY_BROKERAGE,
        )
        boot = moving_block_bootstrap(primary_metrics["_daily"], seed=20261022 + rank)
        pvalues[str(selected.signature)] = float(boot["p_value"])
        oos_block_trade_counts = []
        for block in np.array_split(np.asarray(oos_days, dtype=object), 3):
            block_set = set(map(str, block.tolist()))
            oos_block_trade_counts.append(sum(
                str(t["entry_date_ist"]) in block_set for t in primary_metrics["_trades"]
            ))
        stress = []
        for slippage in (0, 25, 50, 100, 200):
            for brokerage in (10, 20):
                m, _ = evaluate_one(
                    u_oos, f_oos, o, option_index, strategy, active_features,
                    oos_days, float(slippage), float(brokerage),
                )
                stress.append({
                    "candidate_id": int(selected.candidate_id),
                    "signature": str(selected.signature),
                    "slippage_bps_per_side": slippage,
                    "brokerage_per_order_rupees": brokerage,
                    "trade_count": m["trade_count"],
                    "total_net_pnl_rupees": m["total_net_pnl_rupees"],
                    "mean_daily_net_rupees": m["mean_daily_net_rupees"],
                    "max_drawdown_rupees": m["max_drawdown_rupees"],
                })
                stress_rows.append(stress[-1])
        stress_100_20 = next(x for x in stress if x["slippage_bps_per_side"] == 100 and x["brokerage_per_order_rupees"] == 20)
        oos_gate = bool(
            primary_metrics["trade_count"] >= args.minimum_oos_trades and
            all(n >= args.minimum_oos_trades_per_subperiod for n in oos_block_trade_counts) and
            boot["ci95_low"] is not None and boot["ci95_low"] > 0 and
            stress_100_20["mean_daily_net_rupees"] > 0
        )
        oos_metrics_by_sig[str(selected.signature)] = {
            "primary": primary_metrics,
            "bootstrap": boot,
            "subperiod_trade_counts": oos_block_trade_counts,
            "gate": oos_gate,
        }
        oos_rows.append({
            "validation_rank": rank, "candidate_id": int(selected.candidate_id),
            "signature": str(selected.signature), "instrument": strategy.instrument,
            "expiry": strategy.expiry, "moneyness": strategy.moneyness,
            "hold_bars": strategy.hold_bars,
            "entry_predicates": json.dumps([p.__dict__ for p in strategy.predicates], sort_keys=True),
            "logic": strategy.logic, "exit_rules": "+".join(r.kind for r in strategy.exits),
            "hypothesis": strategy.hypothesis,
            "validation_selection_score": float(selected.validation_selection_score),
            "oos_trade_count": primary_metrics["trade_count"],
            "oos_trade_counts_subperiods": json.dumps(oos_block_trade_counts),
            "oos_total_net_pnl_rupees": primary_metrics["total_net_pnl_rupees"],
            "oos_mean_daily_net_rupees": primary_metrics["mean_daily_net_rupees"],
            "oos_median_daily_net_rupees": primary_metrics["median_daily_net_rupees"],
            "oos_mean_net_per_trade_rupees": primary_metrics["mean_net_per_trade_rupees"],
            "oos_max_drawdown_rupees": primary_metrics["max_drawdown_rupees"],
            "oos_mean_daily_ci95_low_rupees": boot["ci95_low"],
            "oos_mean_daily_ci95_high_rupees": boot["ci95_high"],
            "oos_median_daily_ci95_low_rupees": boot["median_ci95_low"],
            "oos_median_daily_ci95_high_rupees": boot["median_ci95_high"],
            "oos_p_value_block_bootstrap": boot["p_value"],
            "oos_mean_daily_net_100bps_20brokerage_rupees": stress_100_20["mean_daily_net_rupees"],
            "oos_statistical_gate_pre_holm": oos_gate,
            "execution_gate_pass": False,
        })
        for trade in primary_metrics["_trades"]:
            # Do not expose the raw contract OHLC/prices; retain only sanitized outcomes/costs.
            trade_rows.append({
                "candidate_id": int(selected.candidate_id),
                "entry_date_ist": trade["entry_date_ist"],
                "entry_timestamp": trade["entry_timestamp"],
                "exit_timestamp": trade["exit_timestamp"],
                "instrument": trade["instrument"],
                "expiry_family_proxy": trade["expiry_family"],
                "moneyness": trade["moneyness"],
                "exit_reason": trade["exit_reason"],
                "lot_size_proxy": trade["lot_size_proxy"],
                "gross_pnl_rupees": trade["gross_pnl_rupees"],
                "net_pnl_rupees": trade["net_pnl_rupees"],
                "total_cost_rupees": trade["total_cost_rupees"],
                "brokerage_rupees": trade["brokerage_rupees"],
                "exchange_fee_rupees": trade["exchange_fee_rupees"],
                "sebi_fee_rupees": trade["sebi_fee_rupees"],
                "stamp_rupees": trade["stamp_rupees"],
                "stt_rupees": trade["stt_rupees"],
                "gst_rupees": trade["gst_rupees"],
                "slippage_bps_per_side": PRIMARY_SLIPPAGE_BPS,
            })

    adjusted = holm_adjust(pvalues)
    for row in oos_rows:
        row["oos_holm_adjusted_p"] = adjusted.get(row["signature"], 1.0)
        row["oos_statistical_gate_pass"] = bool(
            row["oos_statistical_gate_pre_holm"] and row["oos_holm_adjusted_p"] < 0.05
        )
    oos_table = pd.DataFrame(oos_rows)
    oos_table.to_csv(OUT / "finalist_oos_metrics.csv", index=False)
    pd.DataFrame(stress_rows).to_csv(OUT / "oos_cost_stress.csv", index=False)
    pd.DataFrame(trade_rows).to_csv(OUT / "oos_trade_ledger_sanitized.csv", index=False)

    stat_count = int(oos_table["oos_statistical_gate_pass"].sum()) if not oos_table.empty else 0
    enough_oos = len(oos_days) >= 20 and bool((oos_table["oos_trade_count"] >= args.minimum_oos_trades).any())
    if stat_count > 0:
        decision = "DATA-LIMITED — statistical candidate(s) found; executable profitability remains unverified"
    elif not enough_oos:
        decision = "DATA-LIMITED — OOS trade-count/data gate failed"
    else:
        decision = "NO_STATISTICAL_CANDIDATE — no finalist passed the predeclared after-cost OOS gates"
    summary = {
        "schema_version": SCHEMA, "research_id": "QE-NOB-2.0",
        "status": "COMPLETED_BOUNDED_DISCOVERY",
        "decision": decision, "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "cache": {k: v for k, v in cache.items() if k != "files"},
        "data_quality": quality, "feature_metadata": feature_meta,
        "training_feature_metadata": training_feature_meta,
        "session_split": {
            "train": {"start": train_days[0], "end": train_days[-1], "sessions": len(train_days)},
            "validation": {"start": validation_days[0], "end": validation_days[-1], "sessions": len(validation_days)},
            "oos": {"start": oos_days[0], "end": oos_days[-1], "sessions": len(oos_days)},
        },
        "feature_allowlist": sorted(active_features),
        "candidate_budget_limit": args.budget,
        "candidate_unique_count": len(candidates),
        "island_count": args.islands,
        "island_seeds": list(args.seeds),
        "generation_limit": args.generations,
        "population_size": args.population_size,
        "finalist_limit": args.finalists,
        "finalist_count": len(oos_rows),
        "statistical_candidate_count": stat_count,
        "primary_costs": {"slippage_bps_per_side": PRIMARY_SLIPPAGE_BPS, "brokerage_per_order_rupees": PRIMARY_BROKERAGE},
        "stress_grid": {"slippage_bps_per_side": [0, 25, 50, 100, 200], "brokerage_per_order_rupees": [10, 20]},
        "bootstrap": {"replicates": BOOTSTRAP_REPLICATES, "block_length_sessions": BOOTSTRAP_BLOCK_SESSIONS,
                      "correction": "Holm", "alpha": 0.05},
        "simulation_error_counts": dict(error_counts),
        "execution_gate_pass": False,
        "execution_gate_reason": "Rolling OHLC cannot verify exact exchange contract identity, historical bid/ask/depth or actual broker fills.",
        "important_limitations": [
            "The search fitness is computed only from the training split; validation selects finalists; OOS is evaluated once after that selection.",
            "All option fills use rolling OHLC proxies, date/family lot-size assumptions, modeled fees and slippage. This is not executable fill evidence.",
            "The source cache is Dhan-derived and licensed/raw values are not published in the sanitized ledger.",
            "Global-market, option IV, India VIX, FII/DII, event/news and historical bid/ask/depth features are not added unless separately sourced and time-qualified.",
            "A statistical gate pass would authorize only further simulation, not paper/live trading.",
        ],
    }
    (OUT / "run_summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    (OUT / "RESULTS.md").write_text(build_results_md(summary, oos_table, validation_table), encoding="utf-8")
    return summary


def build_results_md(summary: dict[str, Any], oos: pd.DataFrame,
                     validation: pd.DataFrame) -> str:
    lines = [
        "# QE-NOB-2.0 — bounded open strategy discovery",
        "",
        f"**Decision:** {summary['decision']}",
        "",
        f"**Unique candidates:** {summary.get('candidate_unique_count', 0)} / {summary.get('candidate_budget_limit', 0)}",
        f"**Finalists selected on validation:** {summary.get('finalist_count', 0)}",
        f"**Finalists passing predeclared statistical gates after Holm correction:** {summary.get('statistical_candidate_count', 0)}",
        "",
        "## Chronology and methods",
        "",
        "Candidate fitness was calculated only on the training period. All unique candidates were evaluated on the middle validation period for selection. The final chronological OOS block was not used by evolution or human candidate selection. OOS finalist p-values use a session moving-block bootstrap and Holm correction.",
        "",
        "Primary costs are 50 bps adverse slippage per side and ₹10 brokerage per order, with a stress grid of 0/25/50/100/200 bps per side and ₹10/₹20 brokerage per order. Statutory and exchange fees are modeled by date using the simulator's assumptions.",
        "",
        "## Frozen OOS finalists",
        "",
        "| Rank | Candidate | Instrument | OOS trades | Mean daily net (₹) | 95% CI lower (₹) | Holm p | Statistical gate |",
        "|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for row in oos.to_dict("records"):
        lines.append("| " + " | ".join([
            str(row.get("validation_rank", "")), str(row.get("candidate_id", "")),
            str(row.get("instrument", "")), str(row.get("oos_trade_count", "")),
            f"{float(row['oos_mean_daily_net_rupees']):.2f}",
            "NA" if pd.isna(row.get("oos_mean_daily_ci95_low_rupees")) else f"{float(row['oos_mean_daily_ci95_low_rupees']):.2f}",
            f"{float(row.get('oos_holm_adjusted_p', 1.0)):.4f}",
            str(bool(row.get("oos_statistical_gate_pass", False))),
        ]) + " |")
    lines += [
        "",
        "## Outputs",
        "",
        "- candidate_archive.json: pooled structural candidates, ancestry, island IDs and training-only fitness",
        "- candidate_training_metrics.csv: training metrics for each unique candidate",
        "- candidate_validation_metrics.csv: validation metrics and frozen selection scores",
        "- finalist_oos_metrics.csv: one-time chronological OOS evaluation and adjusted significance",
        "- oos_cost_stress.csv: 10-case slippage/brokerage robustness grid per finalist",
        "- oos_trade_ledger_sanitized.csv: per-trade P&L/cost records without raw option prices",
        "- feature_availability.json: runtime local-cache/source-field audit",
        "",
        "## Execution and inference limits",
        "",
        "The execution gate remains **FAIL**. Rolling ATM-relative OHLC does not verify stable exchange contract identity, exact expiry, historical bid/ask/depth, queue position or broker fills. The lot-size map and effective transaction-fee rates are modeled assumptions requiring official circular/Paytm Money tariff reconciliation. Results must not be used to place live orders.",
        "",
        "No tester branch/report was created, per the user's explicit instruction. QE-NOB-1.0 results were not used as labels or training fitness.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--budget", type=int, default=1200)
    parser.add_argument("--generations", type=int, default=20)
    parser.add_argument("--population-size", type=int, default=64)
    parser.add_argument("--islands", type=int, default=4)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    parser.add_argument("--finalists", type=int, default=20)
    parser.add_argument("--minimum-feature-coverage", dest="minimum_feature_coverage", type=float, default=0.80)
    parser.add_argument("--minimum-validation-trades", type=int, default=20)
    parser.add_argument("--minimum-oos-trades", type=int, default=150)
    parser.add_argument("--minimum-oos-trades-per-subperiod", type=int, default=40)
    args = parser.parse_args()
    if not 1 <= args.budget <= 1500 or not 1 <= args.generations <= 20:
        parser.error("budget must be 1..1500 and generations 1..20")
    if args.islands < 1 or len(args.seeds) != args.islands:
        parser.error("provide exactly one fixed seed per island")
    args.finalists = min(max(1, args.finalists), FINALIST_LIMIT)
    result = run(args)
    print(json.dumps({key: value for key, value in result.items()
                       if key not in {"feature_metadata", "simulation_error_counts"}}, indent=2, default=str))


if __name__ == "__main__":
    main()
