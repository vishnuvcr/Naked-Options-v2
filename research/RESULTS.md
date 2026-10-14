# Results and evidence register

Version: NIFTY-PRED-1.0  
Last updated: 2026-10-14  
Status: NO EMPIRICAL RESULTS YET.

## Research design status

Repository bootstrap and first-pass literature review are documented. The target repository was empty at initialization. Data collection, baseline fitting, systematic model experiments, and the final out-of-sample test have not yet been verified as run.

## Result table (to be populated only from machine-generated artifacts)

| Target | Horizon | Candidate / benchmark | OOS n | Baseline metric | Candidate metric | Difference + CI | Raw p | Adjusted p | Regime stability | Gate |
|---|---:|---|---:|---:|---:|---|---:|---:|---|---|
| Future log return | 1 session | pending | — | — | — | — | — | — | — | BLOCKED |
| Direction | 1 session | pending | — | — | — | — | — | — | — | BLOCKED |
| Future realized volatility | 5 sessions | pending | — | — | — | — | — | — | — | BLOCKED |
| Price level | 1 session | persistence | — | — | — | — | — | — | — | BLOCKED |
| Return / direction / volatility | 5 / 20 sessions | pending | — | — | — | — | — | — | — | BLOCKED |

## Rules for result statements

- A result is empirical only if its data hash, experiment code, validation split and generated metrics can be reproduced.
- An OOS model with lower error but no corrected significance / stability is described as exploratory or inconclusive, not successful.
- A high level R² without gain over persistence is not a discovery of predictable market movement.
- No model is named the overall winner without a specific target, horizon, metric, uncertainty and comparison.
- Previous manuscripts' results are literature, not results of this fresh experiment. They will not be copied into this table.

## Current conclusion

No model can yet be ranked because no experiment output has been verified. This is a deliberate evidence status, not an empirical finding that all prediction is impossible.

## Latest run status — 2026-10-14

The canonical bounded workflow candidate is [Actions run #34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38525308372) at commit d654d8f825ba19dc8dfc08f9f2e7b8f26779e7d3. Its data validation, feature construction and unit tests were progressing successfully at the last inspection. The experiment stage has not yet emitted a completed metric table; all result cells above remain BLOCKED until that run and artifact review complete.

No best model, final out-of-sample accuracy, statistical significance or calibration claim is made from a pending run.

## Compute-budget amendment

The model grid has been bounded before accepting any out-of-sample result. Full algorithm comparisons are made for next-session return and direction; a core set covers remaining target/horizon cells. This choice is documented in RESEARCH_PLAN.md and all omitted family cells are explicitly blocked. It constrains the scope of conclusions: no cross-family winner is inferred for a target/horizon with only a core screen. No empirical performance figure is available from the superseded runs.

## Observed outputs from Actions run #41 — provisional, merge gate failed

GitHub Actions run #41 successfully completed data validation, feature construction, unit tests, technical model fitting, global-augmented model fitting, and ARIMA fitting. Its JSON run manifests report 278 technical experiment rows / 72,253 OOS prediction rows and 210 global-augmented experiment rows / 64,413 OOS prediction rows. However, the merge stage failed and per-model CSVs were not included in the run artifact. Therefore, no tabular/sequence model ranking from that run can be reported yet.

The retained ARIMA CSV provides the following preliminary single-model results. Forecasts are cumulative log returns, compared against a zero-return forecast. Positive loss differential means ARIMA had higher squared loss than zero-return; CIs/p-values are raw and not yet Holm-adjusted.

| Horizon | n | MAE | RMSE | OOS R² vs zero return | Skill vs training mean | Loss difference vs zero | 95% block CI | HAC p |
|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 1 session | 980 | 0.005775 | 0.007957 | -0.003482 | -0.004050 | 2.197e-7 | [-3.097e-7, 8.047e-7] | 0.4917 |
| 5 sessions | 976 | 0.013654 | 0.017518 | 0.001095 | -0.000965 | -3.365e-7 | [-7.705e-6, 8.115e-6] | 0.9351 |
| 20 sessions | 961 | 0.025702 | 0.033486 | 0.010657 | -0.001352 | -1.208e-5 | [-1.284e-4, 1.027e-4] | 0.8420 |

**Interpretation:** this preliminary ARIMA benchmark has no statistically significant predictive gain on the tested holdout: all p-values are large and the loss-difference confidence intervals cross zero. The slightly positive R² at 5 and 20 sessions does not override that uncertainty. These figures are transcribed from the machine-generated ARIMA artifact and remain provisional until run #45 reproduces and merges the outputs.

No model winner is declared. The corrected merge run must return per-candidate metrics/predictions, corrected QLIKE scores, Holm adjustments and source/run manifests. Final results must distinguish level prediction from return/direction prediction and identify any blocked family.

## Verified outputs — bounded run #45 (2026-10-14)

Source: [GitHub Actions run #45](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38527508857), commit `c11ee9b408473cb2279e76a7e8a2b98a8a88b011`, artifact `nifty-prediction-reports-38527508857` (SHA-256 `674824d1f5ba18a2fa453338c013a9e4de7aadec97ad6b278391e97df2db2479`). The artifact includes data/source manifests, per-model predictions, metrics, errors, feature ablation and run manifests. Technical run reports 278 rows / 72,253 predictions; global-feature run reports 210 rows / 64,413 predictions; merged metrics CSV has 491 rows (including blocked and development-only rows), with 143 OOS-evaluated model/target/horizon rows. There are 208 explicit compute-budget-blocked rows. Do not interpret every CSV row as an OOS score.

### Preliminary holdout signals (not strategy results)

| Feature set | Target / horizon | Candidate with best listed metric | Metric | Benchmark | Raw p | Holm p | Interpretation |
|---|---|---|---:|---:|---:|---:|---|
| Technical | Return, 1 session | XGBoost | MSE skill +0.13% | Zero return | 0.737 | 1.000 | Negligible, not significant |
| Global-augmented | Return, 1 session | CatBoost | MSE skill +0.17% | Zero return | 0.579 | 1.000 | Negligible, not significant |
| Technical | Direction, 1 session | CatBoost | Accuracy 54.1% | Compare to prevalence/baseline; calibration skill +0.43% Brier | 0.382 | 1.000 | No corrected evidence of useful directional skill |
| Global-augmented | Direction, 1 session | CatBoost | Accuracy 54.1% | Brier skill +0.75% | 0.0288 | 0.193 | Not significant after correction |
| Technical | Volatility, 1 session | Random Forest | QLIKE 1.606; skill +13.8% | Historical-volatility baseline QLIKE 1.862 | 0.00935 | 0.0374 | Promising variance forecast signal in this family; requires target/formula audit and independent replication |
| Global-augmented | Volatility, 1 session | Random Forest | QLIKE 1.541; skill +17.3% | Historical-volatility baseline QLIKE 1.862 | reported 0.000 | 0.000 | Strong provisional signal, but treat displayed p=0 as numerical underflow, not literal zero; independent recomputation required |
| Technical | Volatility, 5 sessions | HistGradientBoosting | QLIKE 0.520; skill +11.0% | Baseline QLIKE 0.585 | 0.0331 | 0.132 | Not significant after correction |
| Global-augmented | Volatility, 5 sessions | Random Forest | QLIKE 0.479; skill +18.1% | Baseline QLIKE 0.585 | 0.0785 | 0.314 | Not significant |
| Technical | Volatility, 20 sessions | HistGradientBoosting | QLIKE 0.322; skill +20.6% | Baseline QLIKE 0.405 | 0.282 | 0.702 | Not significant |
| Global-augmented | Volatility, 20 sessions | ElasticNet | QLIKE 0.267; skill +34.0% | Baseline QLIKE 0.405 | 0.0219 | 0.0875 | Not significant after correction |
| Global-augmented | Return, 5 sessions | ElasticNet | MSE skill -3.1% | Zero return | 0.155 | 0.255 | Worse than benchmark; no gain |
| Global-augmented | Return, 20 sessions | Ridge | MSE skill -12.4% | Zero return | 0.0418 | 0.0758 | Worse than benchmark; not significant after correction |

The model family is screened on the development folds; all test values above are descriptive until the tester independently recomputes them from `predictions.csv`. Candidate rankings are per metric/target/horizon and not a single global winner. The full family is tested only for 1-session return and direction; other cells are core-screen only.

### Data/source status from the same artifact

- NIFTY daily: 4,901 rows, 2007-01-02 to 2026-10-13, Dhan cache SHA `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050`. Yahoo overlap check: 4,679 dates, median absolute close difference 0.0001953 and max 0.0007813 (likely source precision/rounding; retain manifest).
- Passed global/volatility proxy series: S&P 500, Nasdaq Composite, Nikkei 225, Hang Seng, CBOE VIX, India VIX and US 10-year yield. USD/INR, gold and WTI were rejected by strict validation and are not features.
- NSE historical API attempt returned no recognized rows. No historical options chain, FII/DII flow, NSE breadth, PCR or timestamped news/sentiment stream was successfully acquired. The feature-ablation result therefore tests technical-only versus the available global-market/volatility proxies, not the complete requested feature universe.

### Mandatory audit caveat

The artifact's `level` predictions are in NIFTY index-point units (holdout actual mean about 22,519), while the current source `build_feature_matrix.py` defines `target_log_close_h = log(close.shift(-h))` and the runner references that field. This source/target/unit mismatch must be resolved against the exact run commit before any level-model result is accepted. The independent tester must also verify the baseline used for each target, probability baseline construction, Holm family boundaries, target-date alignment for overlapping horizons, and the use of QLIKE variance versus standard-deviation targets. Level rows and any dependent claims are BLOCKED until reconciled.
