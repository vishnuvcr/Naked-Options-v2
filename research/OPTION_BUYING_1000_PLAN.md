# OPT-BUY-4.0 — 1,000+ Naked Long-Option Strategy Screen

**Version:** OPT-BUY-4.0  
**Date:** 2026-10-15 (Asia/Kolkata)  
**Developer branch:** `research/option-buying-1000-developer`  
**Status:** protocol revised to require 1,000+ distinct strategy logics; implementation and empirical runs pending  
**Instrument scope:** NIFTY 50 single-leg long calls or long puts only. No spreads, no short-option legs, no live orders.

## 1. Research question

Does any preregistered NIFTY 50 naked long-option buying configuration show positive, robust out-of-sample net expectancy after brokerage, statutory fees, exchange charges, GST, and adverse slippage, while passing fixed data-quality, trade-count, and statistical gates?

“1,000+ unique strategies” means at least 1,000 distinct, explicitly specified decision algorithms whose entry/selection logic is materially different. A change only to strike bucket, holding period, stop/target, threshold value, or other execution parameter does **not** create a new strategy and must not increase the unique-strategy count. Each strategy must have a unique rule specification, causal input set, signal/decision procedure, direction mapping, and deterministic pseudocode or executable function. All strategy definitions and IDs must be frozen in CSV/JSON before outcome analysis. Configurations are downstream evaluations of a strategy and are counted separately.

## 2. Minimum unique-strategy count and evaluation configurations

The primary target is **at least 1,000 unique strategy algorithms**, not 1,000 configurations. The strategy registry must include a `strategy_id`, human-readable name, hypothesis, exact causal inputs, signal logic/pseudocode, direction rule, required data, expected frequency, and unit tests. Strategy IDs must represent distinct algorithms, not aliases or parameter variants.

Build the 1,000+ strategy catalogue from materially different decision mechanisms across (where data permits): price action and candle structure; opening gaps and opening range; momentum and trend; mean reversion; realized/intraday volatility; volatility expansion/contraction; volume and breadth; futures basis and market internals; options-chain OI/volume/IV/Greeks and skew/term structure; expiry/calendar effects; global-market lead/lag; cross-asset and gold/rates/FX signals; regime-conditioned logic; multi-signal conjunctions/voting/state machines; and simple interpretable statistical/ML models trained only on past data. Every family must include explicit baselines and ablations. Data-dependent families are marked blocked if point-in-time inputs are unavailable, not simulated with invented values. Do not pad the catalogue with superficial permutations. A deterministic deduplication/review test must flag identical or near-identical rule signatures; count only materially distinct logic.

After freezing the unique algorithms, evaluate each eligible strategy on a common, bounded set of execution configurations. The following grid is an initial evaluation matrix, **not** the strategy-count definition:

- **12 entry/control families**: seeded random-time/random-direction control; fixed-time entries; opening-gap continuation; opening-gap fade; opening-range breakout; opening-range fade; causal spot momentum; causal trend alignment; causal mean-reversion; prior-bar range breakout; volatility expansion; spot/OI alignment only when timestamped OI is available (otherwise replace with a prespecified range/volatility rule and document the substitution before outcome inspection).
- **2 option directions**: long CALL and long PUT. Signal-aligned direction rules and direction-agnostic controls must be distinguished in the registry; no future return may choose the direction.
- **5 strike buckets**: ATM and fixed numeric offsets defined from the spot/strike interval at entry (ATM, one-step ITM, one-step OTM, two-step ITM, two-step OTM). Exact numeric contract identity must be verified at both entry and exit; rolling-relative series must not be mistaken for the same contract.
- **10 exit policies**: exit after 1, 2, 3, 6, or 12 five-minute bars; fixed-time/EOD; premium take-profit; premium stop-loss; paired premium TP/SL; trailing premium stop. Trigger levels and precedence for bars touching both barriers are frozen before analysis and use conservative ordering.

The 12 × 2 × 5 × 10 grid yields 1,200 evaluation cells for a small set of baseline families only; it does not meet the 1,000-unique-strategy requirement. The full catalogue must separately contain at least 1,000 unique algorithm definitions, each linked to a controlled execution-configuration set. If a data source cannot support a strategy or configuration, retain its registry record as blocked/not estimable; never fabricate or silently replace data. Any substitution must occur before inspecting outcomes and be logged.

## 3. Primary outcome and controls

Primary outcome: mean net rupee P&L per scheduled eligible session, including zero P&L on no-trade sessions, with a secondary per-trade outcome. Report trade count, quote coverage, win rate, profit factor, expectancy, drawdown, holding time, and costs separately. Compare each entry rule with matched seeded-random and fixed-time controls on common eligible dates. Relative loss reduction is not profitability.

## 4. Cost model

Use the frozen Paytm Money-compatible fee schedule and date-appropriate NSE/statutory charges: brokerage per executed order, STT, stamp duty, SEBI turnover fee, exchange transaction charges, GST, and other applicable levies. Because historical bid/ask and market impact may not be available, explicitly label slippage as a stress assumption, not observed spread. Recompute at **0, 25, 50, and 100 bps adverse slippage per premium side** and **₹10/₹20 brokerage per executed order**. Single-leg round trips have two executed orders. Record fee schedule version/effective dates and lot-size source. Prefer premium-point results when historical lot sizing cannot be reconstructed; do not overstate rupee precision.

## 5. Data quality gates (not relaxable to rescue a candidate)

- Valid, non-stale, correctly typed and time-aligned daily target and intraday option data.
- Exact numeric strike/contract matching between entry and exit, no forward-filled option prices, and no use of future bars for entry signals.
- At least 80% eligible-date quote coverage for any confirmatory candidate.
- Conflicting duplicate quote groups no greater than 1% under the frozen denominator; report numerator and denominator.
- No missing/invalid premium accepted as a trade; preserve missingness and failure logs.
- Adequate prespecified trade/session count; candidates below the threshold are exploratory or blocked.
- If inherited source quality fails, results can be exploratory or inconclusive only; do not call a winner or relax thresholds.

## 6. Statistical protocol for 1,200 comparisons

- Chronological development / validation / final holdout. The final holdout must not set signal thresholds, strike selection, exit thresholds, or model parameters.
- Freeze registry and code hash before final-holdout scoring.
- Calculate paired common-date effects against matched controls, circular or moving-block bootstrap confidence intervals with fixed seed and stated block length, and a prespecified one-sided test of positive net expectancy.
- Apply Holm family-wise error correction across the entire confirmatory family (not per subset); publish raw and adjusted p-values for all estimable cells.
- Report every registered cell, including losses, nulls, failures, blocked cells and reasons. No winner chosen on raw p-values alone.
- Robustness gates: positive net expectancy after primary costs; positive 95% lower confidence bound; remains non-negative/positive as preregistered under 100-bps slippage; positive in both chronological halves; adequate coverage and trade count; corrected significance; not dominated by a matched random/fixed-time control.
- The huge search creates substantial selection risk. Any surviving candidate is hypothesis-generating and would require a separate prospective paper-trading protocol; this screen cannot authorize live deployment.

## 7. Implementation phases and gates

1. **Freeze registry and protocol** — this document, research questions, immutable unique strategy IDs and rule signatures (minimum 1,000 materially distinct algorithms), separately identified evaluation-configuration IDs, entry/exit definitions, cost schedule and stopping rule.
2. **Data audit/cache** — reuse validated cache; otherwise try configured Dhan access and documented free sources. Record source, schema, coverage, request outcomes, hashes, licence and cache provenance. Do not log credentials.
3. **Implement registry runner** — deterministic, causal signals; exact contract matching; conservative barrier execution; common-date ledger; no-lookahead tests.
4. **Unit/regression checks** — single-leg fee arithmetic, monotonic cost sensitivity, stop/target precedence, reproducible random controls, split integrity, missing bars, duplicate handling, bootstrap and Holm tests.
5. **Run full registry once** — first verify at least 1,000 unique strategy definitions after signature-based deduplication; then evaluate all data-eligible strategies on the frozen configuration matrix. Publish separate counts for unique algorithms, execution configurations, tested cells, blocked strategies and estimable strategies. No ad-hoc expansion after seeing results.
6. **Correct verified defects only** — log errors and corrective commits; rerun affected tests and the frozen registry as needed, not new parameter searches.
7. **Final analysis** — cost sensitivities, chronological halves, uncertainty, multiplicity, data-quality disposition, charts and machine-readable results.
8. **Manuscript and close** — methods, results, limitations, conclusions and further research; update README, phase status, experiment/error/activity logs and Pages status. Stop at the frozen gate even if no strategy passes.

## 8. Required outputs

- `research/OPTION_BUYING_1000_PLAN.md` (this protocol)
- `research/OPTION_BUYING_1000_QUESTIONS.md`
- `research/option-buying-1000/strategy_registry.csv` and machine-readable registry
- `research/option-buying-1000/RESULTS.md`, data-quality report, cost sensitivity, full cell ledger and run manifest
- Charts for net P&L, drawdown, cost sensitivity, coverage and corrected significance
- Automated test report, error log, experiment log, phase status and a complete structured manuscript
- README navigation/status update after the implementation and run are actually verified

## 9. Stop rules and interpretation

The study stops after the single frozen catalogue of at least 1,000 unique algorithms, its prespecified bounded evaluation matrix, and necessary defect-correction reruns. It does not continue into unbounded grid search. If data-quality gates fail, report **INCONCLUSIVE / NO-GO**, not “best strategy.” If every candidate loses after costs, conclude that none of the tested strategies is supported. Never infer that all possible naked-option buying is impossible from a finite sample.

## 10. Governance

No separate human/independent tester branch is required, consistent with the user's stated preference. This does not waive automated regression tests, statistical controls, data-quality gates, or transparent error logging. Only operational actions and outcomes are logged; private hidden reasoning is not written to repository files.
