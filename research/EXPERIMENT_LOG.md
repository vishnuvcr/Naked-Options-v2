# Experiment log

Version: NIFTY-PRED-1.0  
Rule: append outcomes; do not delete failed, negative or blocked experiments.

## Run-level ledger

| Run ID | Date UTC | Phase | Commit / workflow run | Data hash | Status | Result / failure |
|---|---|---|---|---|---|---|
| INIT-20261014 | 2026-10-14 | 1 | README bootstrap commit e0b634fdb98da9a2ed136320a24afb7fdda8afb9 | none | COMPLETE | Target repository was empty; no history to audit or overwrite. |
| LIT-20261014 | 2026-10-14 | 2 | Literature review documented in NIFTY-PRED-1.0 | none | PARTIAL | Reviewed available project PDF and source pages; literature review is preliminary until all references are corroborated. |
| DATA-001 | pending | 3 | pending | pending | NOT RUN | No dataset downloaded or data API call made at initialization. |
| BASE-001 | pending | 4 | pending | pending | BLOCKED | Requires validated target data. |
| MODEL-001 | pending | 5 | pending | pending | BLOCKED | Requires validated target data and training environment. |
| VALID-001 | pending | 7 | pending | pending | BLOCKED | Requires a locked holdout and predictions. |

## Predefined experiment catalogue

Catalogue is frozen by research plan v1.0. Run status is not inferred from inclusion here.

| Experiment family | ID prefix | Methods / comparisons | Status |
|---|---|---|---|
| Source/schema validation | E0 | Source access, row schema, hash, missingness, date/price/OHLC quality, time cut-offs, leakage assertions | NOT RUN |
| Level forecasting | E1 | Persistence, drift/trend, ridge / linear regression, tree regressors | NOT RUN |
| Return regression | E2 | Zero/mean forecasts, AR(1)/ARIMA, Ridge/ElasticNet, SVR, Random Forest, gradient boosting, optional XGBoost/LightGBM/CatBoost | NOT RUN |
| Direction classification | E3 | Base-rate/majority, logistic regression, SVM, Random Forest, boosting, MLP | NOT RUN |
| Sequence forecasting | E4 | LSTM, GRU, TCN, Transformer; fixed short sequence length and bounded epochs; only after data and compute gate | NOT RUN |
| Forecast ensembles | E5 | Simple mean and validation-selected weighting; only trained/fitted using development period | NOT RUN |
| Feature ablation | E6 | NIFTY lags/returns/volatility; India VIX; global proxies/FX/commodity/rates; options/F&O; breadth; FII/DII; news, each only if verified | NOT RUN |
| Horizons/regimes | E7 | 1/5/20 session targets; volatility regimes determined from training-only thresholds | NOT RUN |
| Statistical validation | E8 | OOS metrics, moving-block bootstrap, DM/HAC or Clark-West when appropriate, Holm corrections, calibration, subperiod stability | NOT RUN |
| Final tester review | E9 | Independent tests of source/schema, target horizon, metric signs, split boundaries, leakage and conclusion claims | NOT RUN |

## Required per-experiment fields

Each concrete run should record: experiment ID; timestamp; git commit; workflow URL/run ID if observed; source/data hash; dates and row count; target and forecast origin; feature-family list; training/validation/test boundaries; model class/version; parameters; random seed; fit/runtime status; metrics; benchmark metrics; CIs and p-values; adjusted p-value family; regime results; artifact links; error/warning; and decision. If not run, state why.

## Executed workflow evidence

| Run ID | Date UTC | Phase | Commit / workflow | Data hash / split | Status | Outcome |
|---|---|---|---|---|---|---|
| RUN-29 | 2026-10-14 | 3–5 | [GitHub Actions #29](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38523126078), commit bd601089029614a7b0ff3a9e4e29f6fefab847a1 | Cached target SHA b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050 | CANCELLED / SUPERSEDED | Dependency install passed; target had 4,901 rows (2007-01-02–2026-10-13). Original validator flagged 20 weekend-dated records as a failure; no model scores taken from the run. |
| RUN-30 | 2026-10-14 | 3–5 | [GitHub Actions #30](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38523958559), commit 1c5e32f12bb9b01212b54002fb98796f2f54c46c | Same cached target SHA; chronological cut is 80% | IN PROGRESS at last inspection | Data validation and feature matrix passed, tests passed; technical-only experiment step was active. This run's metric code had an OOS R² label that was subsequently corrected on the phase-5 branch, so its R² field is not the canonical result. |
| RUN-31 | 2026-10-14 | 3–5 | [GitHub Actions #31](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38524465651), phase-5 branch commit e9e75c17fd8c57c0825b18cf47075931f02b91f9 | Same cached target SHA; chronological cut is 80% | SUPERSEDED BY METRIC FIX | Passed data validation and feature construction; technical-only catalogue was active. A benchmark-relative OOS R² fix was committed while this run was active; do not use its output as canonical. |
| RUN-32+ | 2026-10-14 | 5 | Phase-5 branch after correction commit 470d7444a95af0fe3c3fbdc319bbe55ee874de14 | Expected same hash unless source refresh changes it | QUEUED / NOT YET VERIFIED | Re-run must verify tests, full experiment run, ARIMA, merge and artifacts before any result is adopted. |

All experiment results remain unranked until a completed run emits machine-generated predictions and metrics. Do not treat a pending workflow as a completed experiment.

| #49 | 2026-10-14 | 5/7 | 9b655da8d72667a6d2f15e4dad5df55a1bec2e84 | 97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7 | SUCCESS | Tests, target validation, feature matrix, technical/global catalogues, ARIMA, merge and report generation passed. Zero null target dates in OOS predictions. Independent skill metrics and block-CI checks reproduced; final statistical tester gate remains open. |

<!-- OPTION_VALIDATION_EXPERIMENT_START -->
## Follow-on option-buying validation — OPT-BUY-1.0

- Last stage: ACQUISITION; decision: PARTIAL; workflow: https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621701520; commit: 0d9eb96d36316bf009f88e828d37812b2cd286cd.
- Options requests planned: 686; completed/empty: 673; failed: 13.
- Primary comparisons written: 0; result file: research/option-validation/RESULTS.md.
- Raw data were not committed or uploaded. Missing/failed requests remain visible in the sanitized acquisition summary/error log.
<!-- OPTION_VALIDATION_EXPERIMENT_END -->

- OPT-BUY-3.0 Actions run 38617943823; branch research/option-entry-exit-developer; commit 53029f81971b7adb395ac76a8b936830bbd6be7a. See research/option-entry-exit/RESULTS.md.

- OPT-BUY-3.0 Actions run 38620992395; branch research/option-entry-exit-developer; commit aa379a8099a3146ae6cde79886606b765d1fda01. See research/option-entry-exit/RESULTS.md.

- OPT-BUY-3.0 Actions run 38621480232; branch research/option-entry-exit-developer; commit 6c4f94e28c2dd88744071e5c7156a2397e55f4c1. See research/option-entry-exit/RESULTS.md.

- OPT-BUY-3.0 Actions run 38621701520; branch research/option-entry-exit-developer; commit 0d9eb96d36316bf009f88e828d37812b2cd286cd. See research/option-entry-exit/RESULTS.md.
