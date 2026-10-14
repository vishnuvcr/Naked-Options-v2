# Predicting NIFTY 50: A preregistered comparison of statistical, machine-learning and sequence models

**Manuscript status:** Protocol/results shell; empirical sections intentionally incomplete.  
**Version:** NIFTY-PRED-1.0. **Study start:** 14 October 2026.

## Abstract

To be completed after all prespecified phases and independent review. No accuracy, winner, p-value or predictive conclusion is claimed at protocol initialization.

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

**Pending verified data acquisition and experiments.** No out-of-sample sample size, performance estimate, confidence interval, statistical significance or best-performing model is available at protocol initialization. Generate this section from saved predictions and result files; do not type guessed numbers.

## 8. Discussion

To be written after experiments and tester review. Interpretation will distinguish level forecasting from movement prediction, aggregate gains from stable gains, and association from causal explanations.

## 9. Strengths and limitations

Protocol strengths include target-specific benchmarks, chronological holdout, feature availability rules, preregistered experiments, failure logs, fixed random seeds and a separate tester gate. Limitations remain unresolved: data depth and API access are not verified; historical options, point-in-time constituent, FII/DII and timestamped news data may not be freely available; newer regimes may be underpowered; and deep models may be infeasible on modest compute.

## 10. Conclusion

Pending results. This manuscript currently makes no empirical claim that any model can or cannot predict NIFTY 50.

## 11. Future research

To be finalized only after the nine fixed phases. New ideas discovered after examining the holdout will not be added to this study's catalogue.

## References

See [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md) for the source register and bibliographic links. The final version will format all citations and supplement metadata.

## Supplementary material

- Source manifest and retrieval hashes: pending.
- Frozen split boundaries and row hashes: pending.
- Experiment configurations, seeds and package versions: pending.
- Out-of-sample predictions, metrics and tests: pending.
- Charts, model diagnostics and regime results: pending.
- Tester report and defect-closure evidence: pending.
