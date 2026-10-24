# NIFTY 50 prediction benchmark — replacement research track

**Status:** Initiated 2026-10-25. Replaces ZigZag-dependent scoring as the primary path. ZigZag remains parked; it is not a prerequisite for this track.

## Research question
Can simple, leakage-controlled statistical and machine-learning models predict next-session NIFTY 50 direction or returns better than naive baselines on chronological out-of-sample data, after accounting for data provenance and uncertainty?

## Objectives
1. Establish a reproducible free-source daily NIFTY 50 dataset and provenance/hash record.
2. Compare naive direction, logistic regression, random forest, gradient boosting, and autoregressive return baselines.
3. Model conditional volatility with ARCH/GARCH only as a separate volatility forecast, not as directional accuracy.
4. Add calibrated prediction intervals/sets with MAPIE where compatible, and symbolic feature/model discovery with PySR as an optional later experiment.
5. Assess regime stability, class balance, uncertainty, calibration and feature availability without look-ahead.
6. Keep external agent frameworks (TradingAgents, astra-quant-agent, Quantevolve) as research/orchestration references until their dependencies and data contracts are reviewed; do not assume their outputs are validated evidence.
7. Publish reproducible scores, caveats and an explicit go/no-go decision. No trading strategy or profitability claim in this phase.

## Repository research sources to assess
- [Quantevolve](https://github.com/tarsyang/quantevolve): evolutionary research/optimization concepts; prohibit optimizing on final holdout.
- [TradingAgents](https://github.com/TauricResearch/TradingAgents): multi-agent research architecture; agents may summarize evidence but cannot replace quantitative baselines.
- [astra-quant-agent](https://github.com/0xethanq/astra-quant-agent): inspect quant-agent/data integration patterns before adopting.
- [PySR](https://github.com/astroautomata/PySR): symbolic regression, optional after baseline.
- [arch](https://github.com/bashtage/arch): ARCH/GARCH conditional-volatility baselines.
- [tick](https://github.com/X-DataInitiative/tick): regularized statistical learning; compatibility and maintenance to be assessed before use.
- [MAPIE](https://github.com/scikit-learn-contrib/MAPIE): prediction intervals/sets and uncertainty evaluation.
- Main project protocol: [Naked-Options-v2](https://github.com/vishnuvcr/Naked-Options-v2).

## Fixed phases and gates
### P0 — Scope and provenance
- Retire ZigZag as a blocking dependency; preserve its logs.
- Use daily NIFTY 50 spot OHLC from a free public source as a baseline dataset; record retrieval time, source URL, row count, date range and SHA-256.
- Gate: source fields and dates are valid, no duplicate dates, OHLC invariants pass, gaps and source limitations reported.

### P1 — Leakage-safe benchmark harness
- Predict next-session direction from information available through session t.
- Use expanding/rolling chronological evaluation; no random shuffle.
- Compare majority-class, previous-direction, zero-return, logistic regression, random forest and gradient boosting.
- Features: lagged returns, rolling volatility, lagged range, moving-average gaps and calendar features only when known at prediction time.
- Gate: tests prove feature rows at t do not use t+1 values; baselines and ML models use identical eligible dates.

### P2 — Statistical evaluation
- Primary metrics: balanced accuracy and directional accuracy.
- Secondary: confusion matrix, per-class precision/recall, Brier/log loss when probabilities are available, coverage and sample counts.
- Report 95% dependence-aware block-bootstrap confidence intervals; compare with naive baselines. Avoid claims from overlapping or dependent observations without qualification.
- Gate: sufficient chronological holdout and a complete metric report; otherwise state underpowered.

### P3 — Volatility and uncertainty
- Optional GARCH forecasts for volatility only; evaluate with QLIKE or another documented volatility loss if inputs support it.
- MAPIE intervals/sets only if a compatible version and time-series calibration procedure can be verified. Do not apply IID calibration naively to serially dependent financial data.
- Gate: separate volatility and direction claims.

### P4 — Regime robustness and model governance
- Predeclare volatility/regime splits using lagged information only.
- Test feature ablations, stability through time, data revision sensitivity, and source sensitivity.
- PySR or Quantevolve optimization is exploratory only; nested validation required and final holdout must remain untouched.
- Gate: report all attempted variants and multiplicity limitations.

### P5 — Research manuscript and decision
- Publish source manifest, data dictionary, reproducible commands, tables, plots, uncertainty, failures and limitations.
- Stop after P5. No automatic strategy deployment; trading-cost/P&L analysis is a separate, later protocol.

## Rules
- Never fabricate missing observations or scores.
- Daily Yahoo data is a convenient free baseline, not an exchange-certified source; cross-check before any high-confidence claim.
- Do not mix spot and futures series, or compare prices with incompatible adjustment conventions.
- No random train/test split, leakage, tuning on the final holdout, or cherry-picked period.
- All errors go to the error log; phase status is updated after each meaningful run.
- A workflow must have manual dispatch and run automatically on relevant research-code changes.
- Do not claim the workflow passed until its actual run and artifacts are inspected.
