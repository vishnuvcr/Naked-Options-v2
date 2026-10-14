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

The preregistered protocol freezes model families and acceptance criteria before experiments. Chronological development and validation precede an untouched final holdout. Hyperparameters are selected through expanding-window time-series folds. Preprocessing is fitted within each training fold and targets use strictly future returns. Level forecasts are benchmarked against persistence; returns against zero, historical mean and autoregressive baselines. Forecast scores are target-specific and uncertainty is quantified.

## 6. Statistical analysis

Planned metrics include MAE, RMSE, benchmark-relative out-of-sample R-squared, direction accuracy / balanced accuracy / precision / recall / F1 / ROC-AUC / Brier / log loss, volatility MAE/RMSE/QLIKE, moving-block bootstrap confidence intervals, appropriate DM/HAC or Clark-West tests and Holm-adjusted p-values. The executable analysis and metric definitions must be linked to the supplement.

## 7. Results

See [RESULTS.md](RESULTS.md) for the run #49 evidence table. Return/direction models show no robust edge; selected global 5-/20-session return models are worse than zero return. Selected volatility models do not pass adjusted QLIKE comparisons. Some volatility-expansion classifiers improve log loss at 5/20 sessions, but these are exploratory single-holdout results.

## 8. Discussion

The one-session return improvement is negligible and statistically unsupported; direction results are close to chance and fail Holm correction. Level models do not beat persistence. Volatility metrics are mixed, and volatility-expansion results are exploratory, with poor one-session probability calibration.

## 9. Strengths and limitations

Protocol strengths include target-specific benchmarks, chronological holdout, feature availability rules, preregistered experiments, failure logs, fixed random seeds and a separate tester gate. Limitations remain unresolved: data depth and API access are not verified; historical options, point-in-time constituent, FII/DII and timestamped news data may not be freely available; newer regimes may be underpowered; and deep models may be infeasible on modest compute.

## 10. Conclusion

For the bounded data and model universe tested, there is no robust evidence that complex models improve return or direction forecasts over simple benchmarks. This does not show prediction is impossible; it shows this feature set and holdout did not establish a robust return/direction edge. The independent tester passed the prediction-only study with scope limitations.

## 11. Future research

Future work should prioritize timestamp-aligned historical option data, validated FII/DII and breadth series, point-in-time corporate actions and news features, separate-period calibration/regime stability, and a new untouched-period replication. A separate trading study would need realistic spread, brokerage, taxes, slippage, margin, liquidity and broker-specific execution assumptions.

## References

See [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md) for the source register and bibliographic links. The final version will format all citations and supplement metadata.

## Supplementary material

- Source manifest and retrieval hashes: included in [run #49 artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128).
- Frozen split boundaries and row hashes: pending.
- Experiment configurations, seeds and package versions: pending.
- Out-of-sample predictions, metrics and tests: included in the run #49 artifact; summary in [RESULTS.md](RESULTS.md).
- Charts, model diagnostics and regime results: pending.
- Tester report and defect-closure evidence: pending.


## Final scope note

Historical option chains, FII/DII, PCR, breadth, timestamped news, and corporate-action features were not verified as acquired. No brokerage/slippage simulation, Paytm Money execution analysis, options backtest, or live strategy is included. See the [independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md).
