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
