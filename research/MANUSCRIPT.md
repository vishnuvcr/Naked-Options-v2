# Predicting NIFTY 50: A preregistered comparison of statistical, machine-learning and sequence models

**Manuscript status:** Tester-reviewed prediction-only study; PASS WITH SCOPE LIMITATIONS.  
**Version:** NIFTY-PRED-1.0. **Study start:** 14 October 2026.

## Abstract

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


## Expanded PDF-method catalogue supplement (run #60, 14 October 2026)

This supplement records the later bounded method-screening run and does not replace the earlier run #49 evidence record. Workflow #60 completed successfully on `research/pdf-audit-developer` at commit `e93fe35d8bb11df65d1c466434d5401298c077ed`; the report artifact is [nifty-prediction-reports-38593936036](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38593936036). The validated target data hash and coverage remained unchanged: 4,901 Dhan daily rows from 2007-01-02 through 2026-10-13. The merged metric table contained 1,097 rows, including 485 OOS-evaluated metric rows and 130 explicitly compute-blocked rows. No model error rows were emitted by the technical or global run.

### Supplementary results

| Forecast target | Representative run #60 row | Finding |
|---|---|---|
| 1-session return | CNN sequence, technical; RMSE 0.007940; MSE skill +0.0875%; Holm p=1 | No supported return advantage. |
| 5-session return | XGBoost, technical; RMSE 0.017352; MSE skill +2.0023%; Holm p=1 | Small descriptive gain, statistically unsupported. |
| 20-session return | Gradient boosting, global; RMSE 0.033100; MSE skill +3.3303%; Holm p=1 | Descriptive gain, statistically unsupported. |
| Volatility | Best MAE and best QLIKE differ across horizons/models | Volatility ranking is metric-dependent; report both rather than selecting a universal winner. |
| Direction / volatility expansion | Accuracy can be inflated by class prevalence and decision threshold; several rows have poor balanced accuracy or proper scores | Accuracy-only rankings are not evidence of a robust predictive edge. |

### Inferential caution

For the implemented paired-loss tests, `mean_loss_diff = model loss - baseline loss`; negative favors the model and positive favors the baseline. A small two-sided p-value only establishes a loss difference, not improvement. Rows with p-values below .05 can therefore represent statistically worse forecasts. Interpret the sign, benchmark skill, confidence interval, proper score and multiplicity correction together. The model catalogue is a screening exercise on one chronological holdout; it is not exhaustive hyperparameter optimization or proof of out-of-sample stability.

### Revised conclusion

The expanded screen does not establish a robust return/direction winner. Certain volatility rows improve individual descriptive metrics, but the best model varies by scoring rule and needs independent reproduction. Volatility-expansion results remain exploratory. Unavailable point-in-time news, options/PCR, FII/DII, breadth and corporate-action features, rejected currency/commodity sources, calendar uncertainty and incomplete global close-time validation limit the conclusions. No trading strategy or options recommendation follows from these prediction results.
