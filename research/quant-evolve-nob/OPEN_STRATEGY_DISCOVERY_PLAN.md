# QE-NOB-2.0 — Open Strategy Discovery Plan

**Status:** Phase 1 protocol amendment committed; implementation and data feasibility are next.  
**Branch:** `research/quant-evolve-nob-v2-discovery-developer`  
**Parent evidence:** QE-NOB-1.0 ended NO-GO for its restricted candidate grammar. Its scores are not reused as training labels or seed fitness.  
**Governance:** User explicitly instructed “No tester.” This is developer-led work; do not create or await a tester branch/report. Automated tests and statistical gates remain mandatory.

## Why a new version is needed

QE-NOB-1.0 searched a bounded but relatively narrow grammar: opening-range breakout, trend/VWAP, gap continuation/fade, pullback and simple always-buy controls, primarily with fixed-time exits. It did not adequately optimize structural novelty, invent exit state machines, or use explicit hypotheses about market mechanisms to drive candidate generation. Increasing the candidate count alone would amplify multiple-testing risk without solving this limitation.

## Aim

Build and evaluate a bounded discovery engine that can propose materially different long-premium NIFTY option strategy structures, explain their market hypothesis, and determine whether any candidate survives strict chronological out-of-sample and after-cost validation.

## Research questions

1. Can grammar evolution produce strategies with structural differences beyond parameter changes?
2. Do mechanisms such as volatility risk-premium filtering, opening-auction imbalance proxies, global-lead lag, intraday liquidity/time-of-day effects, post-event volatility decay, and trend/reversal state transitions yield testable hypotheses with available data?
3. Do evolved entry/exit state machines improve OOS net performance versus fixed baselines?
4. Does a novelty-aware search find robust candidates without selecting noise?
5. Which candidate families remain viable after date-effective costs, slippage stresses, trade-count constraints, Holm correction and block-bootstrap uncertainty?
6. Which hypotheses are untestable due to missing historical contract IDs, quote/depth, IV or point-in-time macro/news data?

## Scope and safety boundary

- Long calls, long puts, long ATM straddles, and long OTM strangles only. No short option legs and no live order placement.
- Continue to label rolling ATM-relative option OHLC as exploratory when exact contract/expiry identity and bid/ask/depth are absent.
- Do not claim a profitable strategy unless all predeclared statistical gates pass. A statistical pass without execution data can only be a research candidate, not a paper/live recommendation.
- Do not use old candidate scores or outcome labels to seed fitness. QE-NOB-1.0 is a negative historical result and a design diagnosis only.
- Fixed total budget: at most 1,500 unique structural candidates, 20 generations, 4 islands, fixed seeds, and one final untouched chronological block. Stop at Phase 7; no open-ended search.
- The candidate budget may be reduced if data/compute gates require it; it may not be expanded without a protocol version change.

## Strategy representation (required novelty)

Represent a candidate as a typed, serializable program, not arbitrary Python code:
- **Regime state:** trend/range, realized-volatility percentile, IV-minus-realized proxy, time-of-day, gap size, and event/global-lead states only when data are timestamp-valid.
- **Entry logic:** conjunction/disjunction of up to four typed predicates, including crossovers, threshold crossings, range breaks, pullback/reclaim, failed breakouts, volatility expansion/contraction, and move-vs-premium-breakeven filters.
- **Direction/instrument:** CALL/PUT selection by signal sign or long-volatility structure; moneyness/expiry selection is explicit.
- **Exit state machine:** time exit, opposite-signal exit, failed-breakout exit, volatility-regime invalidation, trailing underlying threshold, premium-risk stop, and target/trailing combinations. All stops and targets must execute only on information available at the next bar; OHLC intrabar ambiguity uses a conservative ordering rule.
- **Risk constraints:** one-lot maximum per candidate trade, no averaging down, no martingale, no overlapping positions unless explicitly represented and separately tested.
- **Explainability:** every candidate stores a natural-language hypothesis, grammar tree, parent IDs, mutation/crossover trace, feature dependencies and reason for each entry/exit.

## Search method

Use a multi-objective evolutionary algorithm with separate objectives for net expectancy, drawdown/tail risk, stability across time blocks, and structural novelty. Do not use in-sample Sharpe as the sole fitness. Novelty is measured from normalized syntax-tree/feature/exit-state signatures, not textual paraphrase. Preserve simple baselines and Pareto diversity; deduplicate structurally equivalent candidates before counting the budget. Candidate selection and mutation may use training/inner validation only. No final OOS feedback is allowed during evolution.

Candidate generation has two sources:
1. **Mechanism-led hypothesis templates** written before examining OOS results.
2. **Grammar mutations/crossover** that add/remove/replace predicates, change logical operators, alter state transitions, and change exit structures within fixed bounds.

Every candidate must have a machine-readable hypothesis card. Invalid or unsupported features are rejected, not silently substituted. If a feature is missing or not point-in-time safe, the associated family is marked DATA-LIMITED.

## Phases and exit gates

### Phase 1 — Protocol amendment (COMPLETE)
Document why QE-NOB-1.0 was not open-ended structural discovery, freeze budget/grammar/governance, and define novelty metrics and stop conditions.

### Phase 2 — Data and feature feasibility (NEXT)
Audit current cache coverage and available feature fields; enumerate free official sources and licensing-compatible open datasets; identify which proposed mechanisms can be tested without synthetic values. Output a feature availability matrix and source-failure log. Gate: no feature enters the grammar without timestamp, units, provenance and missingness checks.

### Phase 3 — Typed grammar and tests
Implement serialization, validation, structural fingerprints, candidate lineage, mutation/crossover, novelty distance, deterministic seeds, and property/regression tests. Gate: identical trees deduplicate; meaningful exit/logic changes create distinct signatures; no candidate can access future data.

### Phase 4 — Baselines and simulator hardening
Retain simple baselines; verify next-bar execution, no lookahead, same-bar stop/target ambiguity, contract lot proxies, date-effective fees, slippage and no-overlap policy. Gate: hand-calculated trade fixtures match the simulator.

### Phase 5 — Bounded discovery run
Run the fixed 1,500-candidate/20-generation maximum budget, reduced if the data gate requires it. Log every candidate and failed candidate. Cache data; preserve seeds, configs, hashes, environment and artifacts. Gate: all candidate identities and search lineage reproducible.

### Phase 6 — Frozen statistical validation and robustness
Evaluate only frozen finalists on chronological validation and untouched OOS; compare against no-trade/simple baselines; report Holm-adjusted p-values, moving-block bootstrap, drawdown/tail risk, regime/time-block stability, placebos and 0/25/50/100/200 bps per-side slippage with ₹10/₹20 order cost assumptions. Gate: no strategy pass unless every predeclared threshold is satisfied. A pass cannot bypass the execution-data gate.

### Phase 7 — Manuscript and bounded decision (STOP)
Publish a complete research manuscript, feature/source catalog, candidate diversity statistics, results tables/charts, limitations, error log and future research. Final decision is PASS_FOR_FURTHER_SIMULATION, NO-GO, or DATA-LIMITED. No live trading approval. No additional evolution after this phase without a new protocol version.

## Statistical and execution gates

- Chronological split frozen before discovery; final OOS sealed from all candidate fitness and human selection.
- Holm correction over the full prespecified finalist comparison family.
- Moving-block bootstrap with session-level blocks; report 95% interval for mean net P&L and median daily P&L.
- Minimum 150 OOS trades overall and 40 per subperiod unless data constraints require DATA-LIMITED.
- Reject a candidate if its edge depends on one day/month, one cost setting, one expiry-lot regime, extreme single winners, or a small number of trades.
- Stress slippage at 0/25/50/100/200 bps per side and brokerage at ₹10/₹20 per order, with statutory/exchange costs modeled by effective date.
- Missing bid/ask/depth or exact contract mapping means execution gate FAIL, even if the OHLC statistical gate passes.

## Audit and reproducibility requirements

Record each step, status change, command/workflow run, test count, cache hit/miss, data hash, candidate count, rejected candidate reason, defect, correction and result in repo files. Keep logs as concise action/audit summaries; never store hidden chain-of-thought, credentials, or private internal reasoning. No user conversation is copied verbatim into the repository.

## Current disposition

QE-NOB-1.0 remains closed NO-GO for its tested grammar. QE-NOB-2.0 is a new protocol, not a claim that any new strategy is profitable. Implementation has not yet been validated or run; do not describe candidate discovery as complete until workflow evidence exists.


## Protocol amendment 1 — acquisition-bounded moneyness universe (2026-10-23)

After the first bounded acquisition attempt, the sanitized runtime cache audit reported 716 historical option files plus three rolling probe files, all historical option files in the weekly family; it had no historical underlying cache and no monthly option history. The acquisition job was still at its option-source step after 211 minutes. This is a data-throughput diagnosis only; no strategy scores or P&L were examined.

To preserve the fixed phase limit and avoid an unbounded acquisition, the active v2 instrument universe is amended to **ATM and one-step OTM only** (option offsets 0, +1 for calls, and 0, -1 for puts). OTM2 is removed from the candidate grammar and seed generator. The candidate count/generation caps, four islands, fixed seeds, chronology, statistical gates, fee/slippage stresses, source-provenance rules and final OOS seal are unchanged. This amendment is committed before the corrected acquisition is allowed to run and does not use empirical performance results.

From the sanitized cache manifest, the amended five-year collection is estimated to require 732 option request groups across two expiry families (61 30-day chunks × 3 offsets × 2 sides × 2 families). Of those, 307 files appear to be reusable weekly history in the amended offset universe; roughly 425 option groups remain, plus up to 23 underlying-history chunks and a small source probe. These are estimates based on filename counts and the existing code, not confirmed pending API calls. The new client logs actual progress, reuses validated cached files, times out and retries boundedly, and fails closed if acquisition is incomplete. If source coverage remains insufficient within the bounded run, disposition will be DATA-LIMITED rather than silently relaxing the thresholds.


## Protocol amendment 2 — weekly-expiry-only data universe (2026-10-23)

The second interrupted acquisition's sanitized cache inventory shows 728 historical WEEK1 option files over seven relative-strike offsets, including 314 files in the amended ATM/OTM1 offset set; there are 53 chunks with some weekly data, against about 61 chunks in the 5-year target grid. There are **11 partial historical monthly-option files confined to the first two 30-day chunks**, but no source-complete monthly history; there are zero historical underlying bars, and the only underlying JSON is the short probe. The source client's previous artifact summary says all old requests were CACHED_PASS, but it is stale output from the prior v1 report namespace and is not fresh evidence.

To keep the protocol bounded and align the experiment to observed available history, the active universe is now restricted to **WEEK1 weekly expiry only**, ATM/OTM1 only (option offsets -1/0/+1 for both CALL/PUT). MONTH1 is excluded from v2 seed generation, grammar validation and acquisition; no inference is made about the availability of monthly history beyond the inspected cache. The 5-year range, next-bar timing, four islands, four fixed seeds, candidate cap of 1,200, 20 generations, train/validation/sealed-OOS chronology, block bootstrap, Holm correction, 0/25/50/100/200 bps slippage grid, ₹10/₹20 brokerage assumptions and execution gate are unchanged.

From the last manifest, 314 eligible weekly files are present; the 61-chunk request grid is 366 files, leaving an estimated 52 weekly option requests plus about 23 underlying-history chunks and the source probes. This is derived from cache names, not a record of completed requests. The old valid files stay in the legacy cache namespace for reuse; all fresh reports move to a v2 report directory to prevent stale v1 summaries being mistaken for new evidence. If the new acquisition fails its hard cache/coverage gate, the protocol ends DATA-LIMITED and does not launch discovery.


## Protocol amendment 2 — weekly-only expiry universe (2026-10-23)

The source-cache audit found historical weekly option files but no historical monthly option cache. The active QE-NOB-2.0 configuration is therefore restricted to the nearest weekly expiry family (WEEK1) for this bounded discovery; MONTH1 is excluded from the strategy grammar, seed generator and acquisition request list. This is a data-coverage scope amendment, not a performance-based selection. The current cache namespace remains unchanged so validated weekly data can be reused. Candidate generation budget is fixed at 1,200 unique candidates, four islands, population size 64, 20 generations, and four deterministic seeds; these settings are the current config contract and are not tuned on the holdout. The active relative-strike set is {-1, 0, +1}, corresponding to ATM and one-step OTM only.

The previous acquisition run started before the weekly-only config amendment and is not eligible to satisfy the amended protocol. It may be cancelled only through the guarded recovery handoff, with its partial cache saved. The next data workflow must check out the weekly-only configuration, restore the prior cache, run the full source-client/grammar/simulator/discovery regression suite, and then acquire only missing WEEK1 data. The expected full grid is 61 chunks × 3 offsets × 2 option sides = 366 request groups before reuse/retries. About 307 files in the amended strike universe appear reusable from prior weekly cache manifests, leaving roughly 59 option groups plus up to 23 underlying-history chunks. These are estimates; only the completed acquisition summary and feature audit determine coverage.

All other pre-registered chronology, no-synthetic-data rule, candidate fitness budget, cost/slippage stresses, statistical validation, embargoed final OOS, and promotion gates remain unchanged. If historical underlying bars or required option coverage are unavailable, terminate with DATA-LIMITED and do not infer a strategy result from file parseability.
