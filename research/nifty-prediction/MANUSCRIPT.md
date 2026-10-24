# NIFTY 50 Next-Session Direction Prediction — Research Manuscript (Living Draft)

**Version/date:** 2026-10-25  
**Status:** Protocol and implementation draft; empirical results pending verified workflow artifacts.  
**Scope:** Prediction only. No trading strategy, option profitability, or execution recommendation is evaluated.

## Abstract

This study is designed to test whether daily NIFTY 50 spot-index observations available through session close can support reliable prediction of the next session's direction. A free Yahoo Finance daily series is used as an initial, explicitly non-exchange-certified data source. Naive directional benchmarks are compared with logistic regression, random forest, and histogram gradient boosting using chronological expanding walk-forward evaluation. Balanced accuracy is the primary metric; accuracy, class-wise metrics, probabilistic scores, and block-bootstrap uncertainty are secondary. The code and workflow are committed, but the real data acquisition, unit-test run, and benchmark artifact have not yet been independently verified. Therefore, this draft makes no performance claim and names no winning model.

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

**Evidence boundary:** These are preliminary historical results, not the production scikit-learn benchmark. The custom logistic implementation differs from scikit-learn, random forest and gradient boosting were not evaluated here, and the data ends in 2019. No robust predictive advantage is established. The main benchmark workflow, source-parity audit, and their artifacts still need execution verification.

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
