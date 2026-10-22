# Predicting NIFTY 50: A preregistered comparison of statistical, machine-learning and sequence models

**Manuscript status:** Historical manuscript with a 2026-10-22 corrigendum; final sign-off for the latest rerun is on hold pending corrective artifact review.  
**Version:** NIFTY-PRED-1.0. **Study start:** 14 October 2026.

## Corrigendum — 2026-10-22: target-window audit

The later run [#39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966) completed successfully at workflow level, but a row-level audit found 798 emitted prediction rows with missing `target_date` values while their numeric actual/prediction/baseline fields were populated. These occur in h5/h20 volatility and volatility-expansion tasks. The prior implementation calculated standard deviation while skipping missing forward returns, allowing partial future windows near the sample boundary. Therefore the prior run cannot support final claims for those affected task/horizon cells, and the overall publication gate is reopened.

A defect-specific correction uses `skipna=False` and adds tail-window regression tests in developer commit `e8133a582cbe6c06ce46514f871d1393fc142f6f`; corrective workflow [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) must finish and be independently reviewed before the abstract/results are finalized. The previously reported one-session global ExtraTrees volatility-proxy result has no missing target-date rows in this particular defect family, but it remains a **replication candidate only** until the corrected artifact and multiple-testing calculation are checked. Return/direction results did not establish a robust edge. No trading strategy is approved.

A genuinely untouched future-period replication is unavailable in the current data window. Reusing historical folds that were involved in model screening would not constitute an independent-period replication. This is recorded as a future research gate rather than represented as completed evidence. Detailed evidence: [current audit](FRESH_PREDICTION_AUDIT_2026-10-22.md), [results register](RESULTS.md), and [tester report](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-independent-tester).

## Abstract (historical run #49; retain as prior result)

This study tested NIFTY 50 forecasts at 1-, 5- and 20-session horizons using a bounded catalogue of statistical, machine-learning and sequence models. The corrected run evaluated 139,289 out-of-sample prediction rows. The selected global one-session return model improved MSE by only 0.17% over zero return (p=.579; Holm p=1); one-session direction accuracy was 54.08% but did not survive multiplicity correction (Holm p=.548). Selected global 5- and 20-session return models performed worse than zero return. The independent tester passed the bounded prediction-only study with scope limitations. No options strategy was tested.

## 1. Introduction

NIFTY 50 forecasts describe India's large-cap equity market, but price persistence makes raw level fit different from predicting returns or direction. This study tests whether model complexity and additional features improve forecasts beyond transparent benchmarks using information available at the forecast origin.

## 2. Literature review and gap

See [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md). NIFTY-specific work compares linear regressors, tree ensembles, SVMs, CNN/LSTM sequence models and technical indicators. General forecasting research emphasizes appropriate benchmarks, time-dependent evaluation, and data-snooping control. Reported results from external studies are not this study's empirical findings.

## 3. Questions, aims and hypotheses

See [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md). The primary aim is to estimate out-of-sample predictive skill for price levels, log returns, direction and forward volatility at 1-, 5- and 20-session horizons, conditional on valid data access.

## 4. Data and provenance

Actual source status and field definitions are recorded in [DATA_CATALOG.md](DATA_CATALOG.md). No series may be described as acquired until a run produces a manifest with row count, coverage, missingness and SHA-256. Feature availability is aligned by timestamp; global-market closes are not joined as if available before their actual close.

## 5. Scientific methodology

The first 80% of the 4,901-row daily series was used for development and the final 20% for holdout evaluation. Candidate selection used two expanding chronological folds with a horizon gap. The catalogue included linear methods, SVM/SVR, tree ensembles, boosting, MLP and compact LSTM/GRU/TCN/Transformer models. Full catalogue comparison was limited to one-session return/direction; other target/horizon cells used a prespecified core set and excluded cells were explicitly marked BLOCKED_COMPUTE_BUDGET. Level forecasts were benchmarked against persistence, returns against zero, and classification against development-sample prevalence.

## 6. Statistical analysis

Planned metrics include MAE, RMSE, benchmark-relative out-of-sample R-squared, direction accuracy / balanced accuracy / precision / recall / F1 / ROC-AUC / Brier / log loss, volatility MAE/RMSE/QLIKE, moving-block bootstrap confidence intervals, appropriate DM/HAC or Clark-West tests and Holm-adjusted p-values. Metrics included MAE, RMSE, benchmark-relative MSE skill, classification accuracy/balanced accuracy/Brier/log loss, variance-scale QLIKE, HAC paired-loss tests, moving-block confidence intervals and Holm adjustment within task/horizon families. The independent tester reproduced 91 regression skill metrics, 140 non-ARIMA confidence intervals, Holm adjustments and ARIMA benchmark metrics.

## 7. Results

See [RESULTS.md](RESULTS.md) for the run #49 evidence table. Return/direction models show no robust edge; selected global 5-/20-session return models are worse than zero return. Selected volatility models do not pass adjusted QLIKE comparisons. Some volatility-expansion classifiers improve log loss at 5/20 sessions, but these are exploratory single-holdout results.

## 8. Discussion

The one-session return improvement is negligible and statistically unsupported; direction results are close to chance and fail Holm correction. Level models do not beat persistence. Volatility metrics are mixed, and volatility-expansion results are exploratory, with poor one-session probability calibration.

## 9. Strengths and limitations

Strengths include target-specific benchmarks, chronological holdout, conservative prior-date joins for external series, cached data hashes, fixed random seeds, explicit compute exclusions, error logs and independent review. Limitations include one holdout period; incomplete options/FII-DII/PCR/breadth/news/corporate-action data; limited regime analysis; a descriptive non-preregistered calibration diagnostic; and no transaction-cost or execution backtest.

## 10. Conclusion

For the bounded data and model universe tested, there is no robust evidence that complex models improve return or direction forecasts over simple benchmarks. This does not show prediction is impossible; it shows this feature set and holdout did not establish a robust return/direction edge. The independent tester passed the prediction-only study with scope limitations.

## 11. Future research

Future work should prioritize timestamp-aligned historical option data, validated FII/DII and breadth series, point-in-time corporate actions and news features, separate-period calibration/regime stability, and a new untouched-period replication. A separate trading study would need realistic spread, brokerage, taxes, slippage, margin, liquidity and broker-specific execution assumptions.

## References

See [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md) for the source register and bibliographic links. External literature is contextual, not empirical evidence from this run. The source register and bibliography are maintained in LITERATURE_REVIEW.md.

## Supplementary material

- Source manifest and retrieval hashes: included in [run #49 artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128).
- Frozen split: chronological 80/20 with two expanding CV folds; data/source hashes are in the run manifest.
- Experiment configurations, seeds and package versions: pending.
- Out-of-sample predictions, metrics and tests: included in the run #49 artifact; summary in [RESULTS.md](RESULTS.md).
- Selected results chart: [selected_model_results.svg](figures/selected_model_results.svg). Full regime analysis is not performed.
- Tester report and defect-closure evidence: [independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md).


## Final scope note

Historical option chains, FII/DII, PCR, breadth, timestamped news, and corporate-action features were not verified as acquired. No brokerage/slippage simulation, Paytm Money execution analysis, options backtest, or live strategy is included. See the [independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md).


## Additional corrigendum — volatility loss distribution and temporal sensitivity (2026-10-22)

A post hoc sensitivity diagnostic split the same 981-origin final holdout into four approximately equal-count consecutive slices. All four mean QLIKE loss differences were negative after within-four-slice Holm adjustment (adjusted p-values 0.003174–0.006660; moving-block 95% intervals below zero). These are slices of the same holdout, not independent-period replication.

The distribution is skewed: the median model-minus-baseline QLIKE loss difference is +0.00662, and the model has a higher loss than the baseline on 50.97% of days, despite the negative mean difference −0.31560. A 10% winsorized mean remains negative (−0.10137), so the mean result is not explained by one observation, but it should not be described as uniform day-by-day superiority. The one-session volatility result remains a narrow average-score replication candidate; it is not a trading signal.


Supplemental figure: [Four-window volatility-proxy QLIKE sensitivity](figures/volatility_qlike_subperiod_sensitivity.svg). This partitions the same holdout and is not an independent replication.


## QLIKE interpretation caveat — 2026-10-22

The pipeline trains the h1 volatility model on absolute next-session log return and then squares the target, forecast and baseline before applying QLIKE. This makes the scored realized quantity (r_{t+1}^2), but the model forecast is the square of a fitted absolute-return estimate, not a separately trained conditional-variance estimate. Therefore the reported improvement is metric-specific evidence for a variance-scaled volatility proxy; it should not be described as a fully calibrated conditional-variance forecast without additional validation.
