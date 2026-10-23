# QE-NOB-2.0 — Simulator and feature-timing audit

**Date:** 2026-10-23  
**Scope:** Developer-side source review of `feature_builder_v2.py`, `signal_evaluator_v2.py`, `option_simulator_v2.py`, and the existing simulator tests on `research/quant-evolve-nob-v2-discovery-developer`.  
**No independent tester branch/report is created, per user instruction.**

## Findings

### 1. Candidate archive identity — corrected

The sanitized artifact contains 1,185 candidate records and all 20 finalists resolve by signature. Candidate IDs are not a safe global key because records may be island-local. The previous missing-definitions claim is withdrawn. See [exact finalist rules](EXACT_FINALIST_RULES.md).

### 2. Exit semantics and duplicate exit kinds

The simulator collapses multiple stop rules to the smallest configured risk-stop fraction and multiple target rules to the smallest target fraction. It scans the option OHLC proxy and checks stop before target on each bar, so a bar touching both exits at the stop threshold. Existing unit tests cover a stop trigger, target trigger, and stop-over-target priority.

Candidates 496 and 264 serialize duplicate exit kinds. In the currently stored definitions the duplicate values appear to be identical, so their repeated rules are redundant under the simulator's min-threshold reduction; they do not change the threshold in this implementation. This should still be flagged as a candidate-generation/serialization quality issue and tested explicitly. Do not silently edit the archived candidate after the fact.

### 3. Feature formula audit

Source-derived formulas in `feature_builder_v2.py`:

- `nifty_return_1/3/6`: close-to-close percentage change over 1, 3, or 6 rows within the same IST session.
- `opening_gap_pct`: signed `(first_open - previous_observed_session_close) / previous_observed_session_close`; it is not an absolute gap. It is repeated within that session.
- `opening_range_position`: `(close - first-three-bar low) / (first-three-bar high - first-three-bar low)`; available only from the fourth row, when the opening range is frozen.
- `ema_fast_slow_sign`: sign of the difference between session-reset EMA spans 8 and 21; values are -1, 0, or +1 when both EMAs are available.
- Features are computed from the current or prior completed underlying bar. Signal evaluator maps the signal to the next bar in the same IST date, preventing a session-close signal from entering on the next day's open.

These mechanics are internally consistent with point-in-time construction, but source timestamp epoch/bar-label semantics still need validation against Dhan's actual feed documentation and observed records.

## Interpretation corrections for candidates

Because `opening_gap_pct` is signed, predicates such as `opening_gap_pct < 0.0025` include all negative gaps as well as positive gaps below +0.25%. They must not be described simply as “absolute gap below 0.25%.” Likewise, `opening_gap_pct > 0.0025` means a positive gap greater than 0.25%. The predicate `opening_gap_pct < 0.01` admits all negative gaps and positive gaps below +1%.

Candidate 1008's `ema_fast_slow_sign > -1` admits neutral and positive EMA signs, and excludes the -1 bearish state; it is not a generic “EMA bullish crossover” because it also admits zero.

Candidate 496 (`nifty_return_6 > 0`, PUT) is a contrarian/reversal hypothesis. Candidate 264 combines positive return, positive opening-range position and positive EMA sign with a PUT; this is not a conventional directional trend-following rule and needs to be treated as an empirically discovered pattern, not rationalized post hoc.

## Execution and data caveats that remain

- Simulator deliberately labels output `SIMULATED_OHLC_PROXY` and always keeps the execution gate false.
- The underlying/option timestamps must be exactly aligned and the exit uses the same rolling series/strike lookup, but rolling ATM-relative offsets do not establish stable exchange contract identity across time.
- OHLC-based stop/target fills are modeled proxies; a touched threshold is assumed fillable. Historical bid/ask, depth, queue position, latency and broker fill logs are absent.
- For intrabar overlap, stop-first is conservative versus target-first but still cannot reconstruct the true path inside a bar.
- Cost model uses date-effective lot-size proxy and configured fees/slippage; it is not a verified record of actual Paytm Money charges or fills.
- Dhan source timestamp units/bar-label semantics remain an explicit metadata limitation.
- Global markets, India VIX, option IV/OI, FII/DII and timestamped news/event features were not present in the active feature set.

## Disposition

No obvious look-ahead defect was found in the inspected feature formulas or next-bar signal mapping. This is a source inspection, not a complete independent proof of no leakage. Duplicate exit entries are redundant under current min-threshold logic, with stop-over-target priority already covered by a unit test. The most material unresolved issue remains execution validity and stable historical contract identity.

**Gate:** DATA-LIMITED; no paper/live trading authorization. Next step is a bounded reproducibility rerun with explicit signature joins, duplicate-exit regression coverage, feature-timing assertions, and a final cost/execution limitation assessment. Do not tune against the existing OOS period.
