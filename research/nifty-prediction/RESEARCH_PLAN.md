# NIFTY 50 prediction benchmark — replacement research track

**Status:** Active research mandate updated 2026-10-25. Replaces ZigZag-dependent scoring as the primary path. ZigZag remains parked; it is not a prerequisite for this track.

**Updated success criterion (user-directed):** Continue beyond the initial benchmark until a candidate prediction/trading strategy is discovered or developed and evaluated. A fixed benchmark phase may be complete while the broader strategy-discovery objective remains active. Do not endlessly add models: each experiment must answer a named hypothesis, compare against a baseline, and stop if evidence fails to justify further work. Never label an unvalidated candidate profitable or production-ready.

## Research question
Can a leakage-controlled NIFTY 50 forecasting method or strategy be discovered/developed that improves on naive baselines in chronological out-of-sample evaluation and remains useful after realistic execution costs?

## Objectives
1. Establish a reproducible free-source daily NIFTY 50 dataset and provenance/hash record.
2. Compare naive direction, logistic regression, random forest, gradient boosting, and autoregressive return baselines.
3. Model conditional volatility with ARCH/GARCH only as a separate volatility forecast, not as directional accuracy.
4. Add calibrated prediction intervals/sets with MAPIE where compatible, and symbolic feature/model discovery with PySR as an optional later experiment.
5. Assess regime stability, class balance, uncertainty, calibration and feature availability without look-ahead.
6. Keep external agent frameworks (TradingAgents, astra-quant-agent, Quantevolve) as research/orchestration references until their dependencies and data contracts are reviewed; do not assume their outputs are validated evidence.
7. Publish reproducible scores, caveats and an explicit go/no-go decision for each candidate. Continue bounded hypothesis-driven research until a candidate strategy is identified or the evidence supports a clear no-edge conclusion for tested hypotheses.

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

### P5 — Candidate strategy evaluation and final manuscript
- Test named candidates that are motivated by market structure, not unconstrained blind tuning: previous-direction/momentum, short-horizon reversal, volatility/regime-conditioned variants, and available cross-market or options-derived signals where point-in-time data exists.
- Compare all candidates to simple baselines using chronological walk-forward evaluation and a final untouched period where feasible; report uncertainty and multiple-testing limitations.
- For candidates that survive prediction gates, evaluate a separate implementable signal with realistic costs, slippage, taxes, brokerage, liquidity, execution timing and Paytm Money fee assumptions where applicable. If these cannot be sourced, report explicit scenarios rather than zero costs.
- Publish the final manuscript with data provenance, methods, results, charts, tables, failures, limitations, and reproducible commands.
- Do not stop merely because the first benchmark is complete. Stop at the end of this bounded candidate-evaluation protocol with either a defensible candidate strategy or a clear evidence-based statement that tested candidates failed. Never fabricate an edge or profitability.

## Rules
- Never fabricate missing observations or scores.
- Daily Yahoo data is a convenient free baseline, not an exchange-certified source; cross-check before any high-confidence claim.
- Do not mix spot and futures series, or compare prices with incompatible adjustment conventions.
- No random train/test split, leakage, tuning on the final holdout, or cherry-picked period.
- All errors go to the error log; phase status is updated after each meaningful run.
- A workflow must have manual dispatch and run automatically on relevant research-code changes.
- Do not claim the workflow passed until its actual run and artifacts are inspected.
