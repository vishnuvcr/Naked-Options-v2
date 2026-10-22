# Predicting NIFTY 50: A preregistered comparison of statistical, machine-learning and sequence models

**Manuscript status:** Updated with completed rerun #39699761966 on 22 October 2026. Earlier run #49 was independently tester-reviewed; this rerun has automated gates plus a separate familywise statistical audit, but no new tester branch was created in accordance with the project instruction.  
**Version:** NIFTY-PRED-1.0. **Study start:** 14 October 2026.

## Abstract

This prediction-only study evaluated NIFTY 50 level, log-return, direction, volatility-proxy and volatility-expansion forecasts at 1-, 5- and 20-session horizons. The completed rerun used 4,906 Dhan daily observations from 2007-01-02 to 2026-10-21 and compared technical-only with prior-date global-market features. It produced 299 out-of-sample candidate comparisons and 33 validation-selected primary outcomes including ARIMA benchmarks. No robust selected-model improvement in return or direction forecasting was established. The selected global CatBoost return model had MSE skill of -0.26%, +0.85% and -1.70% versus zero return at 1, 5 and 20 sessions, respectively; none was statistically supported after correction. One selected global ExtraTrees model improved one-session volatility-proxy QLIKE loss by 0.3156 (95% moving-block bootstrap CI for model-minus-baseline loss: -0.4230 to -0.2101; HAC p=1.75e-9; Holm p=4.26e-7 across all 299 candidate comparisons). This is a promising forecasting result requiring independent-period replication, not a trading edge. Selected global level models were significantly worse than persistence. No options strategy was tested or recommended.

## 1. Introduction

NIFTY 50 forecasts describe India's large-cap equity market, but price persistence makes raw level fit different from predicting returns or direction. This study tests whether model complexity and additional features improve forecasts beyond transparent benchmarks using information available at the forecast origin.

## 2. Literature review and gap

See [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md). NIFTY-specific work compares linear regressors, tree ensembles, SVMs, CNN/LSTM sequence models and technical indicators. General forecasting research emphasizes appropriate benchmarks, time-dependent evaluation, and data-snooping control. Reported results from external studies are not this study's empirical findings.

## 3. Questions, aims and hypotheses

See [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md). The primary aim is to estimate out-of-sample predictive skill for price levels, log returns, direction and forward volatility at 1-, 5- and 20-session horizons, conditional on valid data access.

## 4. Data and provenance

Actual source status and field definitions are recorded in [DATA_CATALOG.md](DATA_CATALOG.md). No series may be described as acquired until a run produces a manifest with row count, coverage, missingness and SHA-256. Feature availability is aligned by timestamp; global-market closes are not joined as if available before their actual close.

## 5. Scientific methodology

The first 80% of the 4,901-row daily series was used for development and the final 20% for holdout evaluation. Candidate selection used four expanding chronological folds for tabular models and two for sequence models, with a horizon gap to prevent overlapping-target leakage. Sequence models were fitted for three epochs under the compute budget. The catalogue included linear methods, SVM/SVR, tree ensembles, boosting, MLP and compact LSTM/GRU/TCN/Transformer models. Full catalogue comparison was limited to one-session return/direction; other target/horizon cells used a prespecified core set and excluded cells were explicitly marked BLOCKED_COMPUTE_BUDGET. Level forecasts were benchmarked against persistence, returns against zero, and classification against development-sample prevalence.

## 6. Statistical analysis

Regression metrics include MAE, RMSE, benchmark-relative MSE skill and, for volatility proxies, QLIKE. Classification metrics include accuracy, balanced accuracy, Brier score/skill, log loss and ROC-AUC. Paired loss differences were tested with HAC standard errors; moving-block bootstrap confidence intervals used 300 resamples and a minimum block length of five observations. The original pipeline applied Holm correction within each target/horizon group. A supplementary familywise audit was also performed after result acquisition across (a) the 33 validation-selected primary outcomes (30 selected feature-set/target/horizon outcomes plus three ARIMA return benchmarks) and (b) all 299 OOS candidate comparisons with valid p-values. This broader correction is reported as a conservative sensitivity analysis. Statistical significance does not imply economic value or tradability.

## 7. Results

The canonical rerun is [workflow #39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966). Its aggregate/report artifact SHA-256 is `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`; the sanitized aggregate summary is committed at [nifty_prediction_run_39699761966_summary.json](../reports/nifty_prediction_run_39699761966_summary.json). Raw prediction rows remain in the time-limited GitHub Actions artifact. The merged report contains 647 metric rows, of which 299 are OOS-evaluated model comparisons, 296 are CV-pass rows and 52 are explicitly compute-budget-blocked. The technical catalogue emitted 148,407 OOS predictions, the global-augmented catalogue 140,559, and ARIMA supplied three return benchmarks.

### Selected outcomes

| Target | Horizon | Validation-selected model | OOS n | Holdout result | Familywise inference |
|---|---:|---|---:|---|---|
| Log return | 1 | Global CatBoost | 981 | MAE 0.005788 vs zero-return 0.005803; MSE skill -0.26% | raw p=.588; Holm across 33 primary tests=1.000 |
| Log return | 5 | Global CatBoost | 977 | MAE 0.013623 vs zero-return 0.013730; MSE skill +0.85% | raw p=.587; Holm=1.000 |
| Log return | 20 | Global CatBoost | 962 | MAE 0.027171 vs zero-return 0.026252; MSE skill -1.70% | raw p=.858; Holm=1.000 |
| Direction | 1 | Global CatBoost | 981 | Accuracy 53.01%; balanced accuracy 52.82%; Brier skill -0.0009 | raw p=.879; Holm=1.000 |
| Volatility proxy | 1 | Global ExtraTrees | 981 | MAE 0.003952 vs baseline 0.003967; RMSE 0.005305 vs 0.005550 | QLIKE loss difference -0.3156; 95% block CI [-0.4230, -0.2101]; raw p=1.75e-9; Holm across 299 comparisons=4.26e-7 |
| Volatility proxy | 5 | Global ElasticNet | 980 | MAE 0.002372 vs baseline 0.002944 | QLIKE comparison not significant after familywise correction |
| Volatility proxy | 20 | Global ElasticNet | 980 | MAE 0.002044 vs baseline 0.002387 | QLIKE comparison not significant after familywise correction |
| Volatility expansion | 20 | Technical Logistic regression | 980 | Accuracy 66.43%; Brier skill +0.133 | raw p=.0020; Holm across 33 primary tests=.0582; exploratory, not significant at .05 |
| Level | 1 / 5 / 20 | Global ElasticNet / ElasticNet / Ridge | 981 / 977 / 962 | MSE skill vs persistence -16.4% / -8.9% / -34.5% | all three significantly worse after Holm across 33 primary outcomes |

The one-session volatility target is the absolute next-session log return, a daily-return-based volatility proxy rather than intraday realized volatility. QLIKE compares variance-scale forecasts; a negative model-minus-baseline QLIKE loss difference favors the model. The selected global ExtraTrees model's mean loss difference was -0.315597, with a 95% moving-block bootstrap interval [-0.422981, -0.210145]. Its two-sided HAC p-value was 1.75e-9; the Holm-adjusted p-value was 2.62e-8 within the task/horizon family, 5.77e-8 across the 33 selected primary outcomes, and 4.26e-7 across all 299 OOS candidate comparisons.

Across the 299 candidate comparisons, 85 differences survived Holm adjustment; 77 were significantly worse than the relevant baseline and eight were significant improvements. All eight improvements were one-session volatility-proxy QLIKE comparisons across tree/boosting candidates. The validation-selected global ExtraTrees model was one of these eight. This is the strongest new result, but it comes from one chronological holdout and requires a fresh untouched-period replication.

### Data and reproducibility summary

The target source is Dhan daily NIFTY 50: 4,906 rows from 2007-01-02 through 2026-10-21. Validation passed, with 20 weekend-dated observations preserved and flagged for exchange-calendar review. Seven auxiliary series passed: S&P 500, Nasdaq, Nikkei 225, Hang Seng, CBOE VIX, India VIX and a US 10-year yield proxy. The NSE official endpoint returned no recognized data rows; USD/INR and gold failed OHLC validation and WTI had non-positive OHLC, so those sources were excluded. Historical options, FII/DII, PCR, breadth, timestamped news and point-in-time corporate-action data were not verified as acquired. The detailed provenance and failed-source diagnostics are in [DATA_CATALOG.md](DATA_CATALOG.md), [the error log](ERROR_LOG.md), and [the sanitized run summary](../reports/nifty_prediction_run_39699761966_summary.json).

## 8. Discussion

Return and direction forecasts remain the principal no-go finding: selected return models did not beat zero-return robustly, direction performance was close to the development-sample prevalence baseline, and global level forecasts were worse than persistence. The supplementary familywise audit across all 299 candidate comparisons reinforces this: the only significant improvements were for the one-session volatility proxy, not return or direction. Global inputs were lagged to prior-date observations; however, the study did not acquire FX, gold, crude, FII/DII, PCR, breadth, timestamped news or corporate-action features, and no full regime-stratified replication was performed. The volatility result is therefore a research lead, not a deployable signal.

The sequence-model report initially labelled the run as eight epochs, while the fitted estimator objects were set to three epochs. This metadata-only defect was corrected in the source and a regression assertion was added; the actual run used three epochs, so the fitted predictions are unchanged. The empty/headerless CSV merge defect was also corrected; the regression test and end-to-end merge passed in run #39699761966.

## 9. Strengths and limitations

Strengths include a hashed Dhan target series, a Yahoo overlap diagnostic, strictly prior-date global joins, a chronological 80/20 holdout, horizon-purged expanding validation, target-specific baselines, explicit blocked compute-budget cells, HAC paired-loss tests, moving-block bootstrap intervals, Holm correction and a reproducible report artifact.

Limitations include one final holdout; the latest rerun was not separately reviewed on a tester branch (per the project instruction not to create one); no independent-period replication; no full regime analysis; source failures for NSE official data, USD/INR, gold and WTI; unacquired options/FII-DII/PCR/breadth/news/corporate-action features; and the use of a daily-return proxy rather than intraday realized volatility. The global feature set is a limited subset of possible market context. No brokerage, spread, slippage, margin, liquidity or broker-execution simulation was conducted because this study was frozen to prediction only.

## 10. Conclusion

The latest bounded run does not establish a robust NIFTY return or direction forecasting edge. Global level forecasts are significantly worse than persistence. One selected global ExtraTrees model provides strong statistical evidence of better one-session volatility-proxy forecasts under QLIKE, surviving Holm correction across all 299 candidate comparisons (p=4.26e-7), but this result needs replication on a new untouched period and must not be translated into a trading strategy without separate research. Options P&L remains prohibited because fixed-contract identity, full-history coverage and executable prices are not verified. The prediction-only research is closed for this bounded run with the volatility result retained as a future replication hypothesis.

## 11. Future research

Future work should prioritize timestamp-aligned historical option data, validated FII/DII and breadth series, point-in-time corporate actions and news features, separate-period calibration/regime stability, and a new untouched-period replication. A separate trading study would need realistic spread, brokerage, taxes, slippage, margin, liquidity and broker-specific execution assumptions.

## References

See [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md) for the source register and bibliographic links. External literature is contextual, not empirical evidence from this run. The source register and bibliography are maintained in LITERATURE_REVIEW.md.

## Supplementary material

- Latest source manifest and retrieval hashes: included in [run #39699761966 artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966); aggregate summary is committed at [nifty_prediction_run_39699761966_summary.json](../reports/nifty_prediction_run_39699761966_summary.json). The previous [run #49 artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) remains historical.
- Frozen split: chronological 80/20; four expanding folds for tabular models and two for sequence models, with a horizon gap; source hashes are in the run manifest.
- Experiment configurations, seeds and package versions: pending.
- Out-of-sample predictions, metrics and tests: included in the run #39699761966 artifact; summary in [RESULTS.md](RESULTS.md).
- Selected results chart: [selected_model_results.svg](figures/selected_model_results.svg). Full regime analysis is not performed.
- Tester report and defect-closure evidence: [independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md).


## Final scope note

Historical option chains, FII/DII, PCR, breadth, timestamped news, and corporate-action features were not verified as acquired. No brokerage/slippage simulation, Paytm Money execution analysis, options backtest, or live strategy is included. See the [independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md).
