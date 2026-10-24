# NIFTY 50 Next-Session Direction Prediction — Research Manuscript (Living Draft)

**Version/date:** 2026-10-25  
**Status:** Initial benchmark verified in Actions run #34; fixed candidate-rule experiment added and awaiting its automated result.  
**Scope:** Prediction only. No trading strategy, option profitability, or execution recommendation is evaluated.

## Abstract

This study is designed to test whether daily NIFTY 50 spot-index observations available through session close can support reliable prediction of the next session's direction. A free Yahoo Finance daily series is used as an initial, explicitly non-exchange-certified data source. Naive directional benchmarks are compared with logistic regression, random forest, and histogram gradient boosting using chronological expanding walk-forward evaluation. Balanced accuracy is the primary metric; accuracy, class-wise metrics, probabilistic scores, and block-bootstrap uncertainty are secondary. The production workflow has completed successfully: data acquisition, unit tests, source-parity audit, chronological benchmark, persistence and artifact upload passed in run #34. The data is third-party and not exchange-certified. The baseline results do not establish a reliable learned-model advantage.

## 1. Research question

Do simple statistical and machine-learning models predict next-session NIFTY 50 direction better than naive baselines on chronological out-of-sample observations, with data provenance and uncertainty explicitly reported?

### Objectives

1. Acquire and fingerprint a reproducible daily OHLC dataset.
2. Validate date ordering, duplicates, missing OHLC fields, and price-range invariants.
3. Compare majority-class, previous-session-direction, zero-return, logistic regression, random forest, and histogram-gradient-boosting predictions.
4. Report directional metrics and probability scores with dependence-aware uncertainty estimates.
5. Record source limitations, failures, and a decision that distinguishes statistical prediction from tradable profitability.
6. Assess ARCH/GARCH, MAPIE, PySR, tick, Quantevolve, TradingAgents, and astra-quant-agent only in separate, gated follow-up phases.

## 2. Data and provenance

The initial acquisition script uses Yahoo Finance chart data for the `^NSEI` symbol, retaining Date, Open, High, Low, and Close. The workflow writes a source manifest containing retrieval time, date range, row count, SHA-256, source URL, and limitations. Data is cached to reduce repeat downloads and can be refreshed explicitly.

**Important limitation:** Yahoo Finance is a free third-party source and is not exchange-certified. Source revision, missing sessions, symbol mapping, and historical values must be cross-checked against official Nifty Indices/NSE data before strong conclusions. This daily study does not establish intraday or expiry-specific validity.

## 3. Target and predictors

At the close of session (t), the target is the sign of (Close_{t+1}/Close_t - 1). Exact zero returns are mapped to the DOWN class for the binary metrics and separately counted in the report. Features use observations through session (t): lagged close returns, rolling return volatility, moving-average gaps, daily range percentage, opening gap, and close position within the daily range.

No random split is used. Rows with unavailable rolling features or next-session target are excluded. All models are scored on the same chronological test rows. The previous-session-direction baseline predicts the next direction using the sign of the latest completed session return.

## 4. Scientific methodology

1. Validate OHLC and date integrity before feature construction.
2. Split chronologically with an initial training period and a later test period.
3. Refit models on an expanding history every 20 test observations by default; each prediction uses only labels available before that prediction.
4. Compare naive baselines and three supervised classifiers.
5. Report accuracy, balanced accuracy, confusion matrices, per-class precision/recall/F1, log loss and Brier score when probabilities are available.
6. Estimate a 95% interval for balanced accuracy using a circular block bootstrap (default block length 10, 1,500 replicates). These intervals are approximate and do not eliminate model-selection or source uncertainty.
7. Keep optional volatility modeling and conformal uncertainty in separate analyses; neither should be described as directional skill without its own suitable evaluation.

## 5. Statistical analysis plan

Balanced accuracy is the primary metric because up/down class frequencies may differ. Accuracy and class-wise confusion metrics provide context. Log loss and Brier score evaluate probabilistic forecasts and are not directly comparable to classifiers without probabilities. The block bootstrap resamples paired observed labels and predictions in circular blocks to partially preserve local dependence.

The protocol avoids random shuffling and tuning against the final test period. A later robustness phase should predeclare regimes from lagged information and report all variants to reduce cherry-picking and multiple-comparison risk. A statistically favorable direction score would not by itself imply economic value, causal predictability, or options-market profitability.

## 6. Results

### Preliminary historical diagnostic (not final benchmark)

A reproducible custom Node.js diagnostic was run against a public third-party CSV mirror covering 2000-01-03 through 2019-12-02. After feature construction, 4,893 observations remained. The chronological 75/25 split used 3,669 training rows and 1,224 test rows, covering 2014-12-16 through 2019-11-29. The test-set up rate was 53.02%, with two exact zero-return labels mapped to DOWN.

| Model | Accuracy | Balanced accuracy | 95% circular block-bootstrap interval for balanced accuracy |
|---|---:|---:|---:|
| Majority-class baseline | 53.02% | 50.00% | [50.00%, 50.00%] |
| Previous-session direction | 52.78% | 52.60% | [49.72%, 55.56%] |
| Zero-return forecast (DOWN tie convention) | 46.98% | 50.00% | [50.00%, 50.00%] |
| Custom expanding logistic regression | 52.86% | 52.78% | [50.11%, 55.36%] |

The custom logistic diagnostic's Brier score was 0.2494 and log loss was 0.6919. A comparison chart is available at [preliminary_balanced_accuracy.svg](../../reports/nifty-prediction/preliminary_balanced_accuracy.svg), and the full diagnostic report is [here](../../reports/nifty-prediction/preliminary_historical_diagnostic.md). Its balanced accuracy was only about 0.18 percentage points above the previous-session-direction baseline; their approximate intervals overlap substantially. The majority baseline has higher raw accuracy due to the test-set class imbalance.

**Evidence boundary:** These are preliminary historical results, not the production scikit-learn benchmark. The custom logistic implementation differs from scikit-learn, random forest and gradient boosting were not evaluated here, and the data ends in 2019. No robust predictive advantage is established. The main benchmark workflow and source-parity audit were executed successfully in Actions run #34. The exact match across the two public sources is not independent confirmation; they may share upstream provenance.

## 7. Inferences and discussion

The preliminary diagnostic does not demonstrate a reliable predictive edge: the custom logistic model's balanced-accuracy estimate is close to the previous-direction baseline and uncertainty intervals overlap. A successful script run is not evidence of generalization to current markets. Any future apparent improvement must be interpreted alongside class balance, uncertainty intervals, source quality, regime variation, and the number of model variants attempted.

## 8. Strengths

- Explicit source manifest and file hash.
- Chronological walk-forward evaluation rather than random splitting.
- Naive baselines scored on the same test dates as machine-learning models.
- Automated OHLC validation and unit tests.
- Primary metric, uncertainty method, and key limitations specified before results.
- Clear separation between daily prediction, volatility forecasting, and future trading research.

## 9. Limitations

- Free daily Yahoo data is not exchange-certified.
- The benchmark is for next-session spot-index direction, not intraday or weekly-expiry direction.
- The initial feature set is intentionally modest and omits global markets, FII/DII flows, options chain, news, corporate actions, and broader regime data.
- The bootstrap interval is approximate; its block length is fixed initially and requires sensitivity analysis.
- Optional libraries and external repositories have not all been integrated or executed.
- No trading costs, slippage, brokerage, option payoff, or out-of-sample P&L is evaluated.

## 10. Conclusion

A preliminary historical diagnostic has been completed, and it does not show a robust improvement over naive direction forecasts. The main empirical gate remains open because the production scikit-learn workflow and its artifacts have not been verified, and the dataset ends in 2019. The study does not name a best model or recommend a trading strategy. If the current-market benchmark similarly fails to improve robustly on naive baselines, the correct conclusion will be that this feature/model set has not demonstrated useful predictive skill.

## 11. Future research

1. Verify historical spot data against official Nifty Indices/NSE sources and document discrepancies.
2. Add lagged global index returns, volatility proxies, gold, currency, and market-regime features where reliable aligned data is available.
3. Incorporate FII/DII flows, options data, corporate actions, and news only after point-in-time availability and provenance are established.
4. Add ARCH/GARCH volatility forecasts with suitable volatility loss functions.
5. Evaluate MAPIE only with a time-series-valid calibration design.
6. Explore PySR/Quantevolve only with nested chronological validation and an untouched final holdout.
7. Review TradingAgents and astra-quant-agent for evidence synthesis and connector patterns, not as substitutes for benchmark labels.
8. If prediction evidence is robust, design a separate options/trading study that includes Paytm Money brokerage, taxes/fees, bid-ask spread, slippage, liquidity, and realistic execution timing.

## Appendix A. Reproducibility

- Plan: [RESEARCH_PLAN.md](RESEARCH_PLAN.md)
- Phase status: [PHASE_STATUS.md](PHASE_STATUS.md)
- Source acquisition: [acquire_daily_data.py](acquire_daily_data.py)
- Cross-source audit: [audit_source_parity.py](audit_source_parity.py)
- Evaluation: [evaluate_daily_models.py](evaluate_daily_models.py)
- Unit tests: [test_nifty_prediction_benchmark.py](../../tests/test_nifty_prediction_benchmark.py)
- Workflow: [nifty-prediction-benchmark.yml](../../.github/workflows/nifty-prediction-benchmark.yml)
- Error log: [ERROR_LOG.md](ERROR_LOG.md)
- Integration plan: [REPOSITORY_INTEGRATION.md](REPOSITORY_INTEGRATION.md)

Run locally after installing pandas, numpy, scikit-learn, and yfinance:

```bash
python -m unittest discover -s tests -p "test_nifty_prediction_benchmark.py" -v
python research/nifty-prediction/acquire_daily_data.py
python research/nifty-prediction/evaluate_daily_models.py
```

## Appendix B. Decision gate

A model can be considered for further study only after the workflow and data artifacts are verified, data-source quality is documented, and the out-of-sample advantage over naive baselines is stable enough to warrant a preregistered robustness phase. This manuscript is not a financial recommendation.


## 12. Verified production benchmark update (2026-10-25)

GitHub Actions run [#34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710) completed successfully. The main job's unit tests, data acquisition, second-source OHLC audit, chronological benchmark, result persistence, and artifact upload all passed. The optional ARCH/MAPIE environment audit also passed.

### Data and evaluation

The primary dataset was acquired from Yahoo Finance via `yfinance` for `^NSEI`: 4,686 rows from 2007-09-17 to 2026-10-23, with no invalid OHLC rows or duplicate dates reported by the loader. SHA-256: `8d73f2b98d2109a5ccf6bfc6e85927de9f5c59ced889c188f6aa59a340079ab0`. It is a third-party source and is not exchange-certified. The chronological holdout has 1,157 observations from 2022-02-14 to 2026-10-22; predictions use daily OHLC-derived lagged/rolling features and expanding walk-forward refits every 20 test rows.

### Results

| Model | Accuracy | Balanced accuracy | 95% circular block-bootstrap interval for balanced accuracy | Brier | Log loss |
|---|---:|---:|---:|---:|---:|
| Majority-class baseline | 52.20% | 50.00% | 50.00–50.00% | — | — |
| Previous-session direction | 54.19% | 54.10% | 51.30–56.81% | — | — |
| Zero-return forecast (DOWN convention) | 47.80% | 50.00% | 50.00–50.00% | — | — |
| Logistic regression | 52.46% | 52.53% | 49.75–55.34% | 0.2495 | 0.6923 |
| Random forest | 50.56% | 50.44% | 47.67–53.03% | 0.2518 | 0.6971 |
| Histogram gradient boosting | 53.15% | 52.82% | 50.12–55.58% | 0.2554 | 0.7055 |

The naive previous-session direction baseline has the highest balanced accuracy (54.10%). All three learned models are lower. The intervals overlap and the bootstrap intervals are approximate; no paired, preregistered test of model-vs-baseline differences was performed. Thus this experiment does **not** establish a reliable advantage from the tested learned models. The baseline's modest direction signal is not evidence of stable, actionable predictability and does not establish trading profitability.

### Cross-source audit

The public parquet mirror and Yahoo series were exactly identical for Open, High, Low, and Close across 4,686 dates (all reported absolute-error summaries zero). This is a parity result, not independent validation: the sources may share an upstream data provider or one may mirror the other. Official exchange/index confirmation remains outstanding.

### Updated conclusion

The fixed baseline experiment is operational and reproducible, but its current result is **no demonstrated predictive edge from the tested machine-learning models over the naive previous-direction baseline**. Stop model complexity escalation at this planned benchmark gate. Further research within the plan should prioritize source independence, statistical paired comparisons and regime stability, not unconstrained tuning. Do not develop a trading strategy from these results. No slippage, brokerage, taxes, option payoff, or P&L was assessed because this phase is prediction-only.


## Candidate-rule experiment update — 2026-10-25

The automated workflow now runs six predeclared candidates on the same chronological holdout: 3-session momentum, 5-session momentum, 1-session reversal, 3-session reversal, a 20-session trend filter, and a lagged-volatility-conditioned momentum/reversal rule. The report is `reports/nifty-prediction/candidate_rules.json`. Candidate metrics are pending the new workflow run and are not guessed here.

The existing benchmark result is verified: on 1,157 observations from 2022-02-14 through 2026-10-22, previous-session direction achieved 54.19% accuracy and 54.10% balanced accuracy; logistic regression achieved 52.46% and 52.53%, random forest 50.56% and 50.44%, and histogram gradient boosting 53.15% and 52.82%, respectively. None of the learned models establishes a reliable improvement over the simple baseline.

Any reported long/short index-return proxy from the candidate script is gross and illustrative only. It excludes implementable instrument selection, basis, leverage, brokerage, taxes/charges, slippage, liquidity, margin and execution timing. A candidate is not a usable strategy until these costs are included with sourced assumptions.


## Preliminary candidate-rule results

A preliminary calculation over the same 1,157 sessions (2022-02-14 through 2026-10-22) compared six fixed rules. The previous-session-direction baseline scored 54.10% balanced accuracy; 3-session momentum scored 53.18%, 5-session momentum 51.42%, 1-session reversal 45.99%, 3-session reversal 46.82%, a 20-session trend filter 53.90%, and the lagged-volatility-conditioned rule 51.22%. Thus, no new candidate beats the baseline on balanced accuracy in this diagnostic. The trend filter is the strongest new candidate but does not clear the baseline.

The diagnostic report is [candidate_rules_preliminary.json](../../reports/nifty-prediction/candidate_rules_preliminary.json). These numbers are marked preliminary until the automated Python run confirms them. Gross long/short index-proxy returns in the report are not executable net returns and exclude instrument selection, brokerage, taxes/charges, slippage, margin, basis, liquidity and execution timing. No usable strategy or profitability claim is established.
