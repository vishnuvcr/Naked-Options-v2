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

## Model-run execution trace (Phase 5 branch)

| Run | SHA | Status | Evidence / disposition |
|---|---|---|---|
| #30 | 1c5e32f12bb9b01212b54002fb98796f2f54c46c | In progress at last observation on main | Data gate, feature matrix and tests passed, but uses 4 walk-forward folds for tabular models and its OOS-R² field is not canonical. |
| #31 | e9e75c17fd8c57c0825b18cf47075931f02b91f9 | Cancelled | Bound sequence tasks/3 epochs was applied, but no model result retained. |
| #32 | 470d7444a95af0fe3c3fbdc319bbe55ee874de14 | Cancelled | Added benchmark-relative OOS-R² formula; rerun was superseded before result acquisition. |
| #33 | 09a92967d9a6634a96b8bfccab14ce2b3e9066c5 | Cancelled | Added unit test for benchmark-relative OOS-R²; queued run was superseded to apply the final two-fold compute bound. |
| #34 | d654d8f825ba19dc8dfc08f9f2e7b8f26779e7d3 | In progress | Canonical bounded run candidate: two chronological development folds; sequence models limited to three epochs and next-session return/direction; latest 20% remains untouched. Accept results only after the workflow completes and artifacts/tests are inspected. |

## Resource-bounded screening update — 2026-10-14

The dated amendment in RESEARCH_PLAN.md is now part of the branch history. It preserves all five targets, 1/5/20-session horizons, two chronological folds, and the locked latest 20% holdout, but restricts the full algorithm catalogue to 1-session return/direction. Other target/horizon combinations use a fixed core set; all excluded model cells must be emitted as BLOCKED_COMPUTE_BUDGET.

| Run | Commit | Workflow status at last check | Result / disposition |
|---|---|---|---|
| #34 | d654d8f825ba19dc8dfc08f9f2e7b8f26779e7d3 | Stayed in progress at technical-only model catalogue; no artifact observed | Superseded operationally by the bounded candidate grid. No result retained. |
| #35 | cafb2d56c523cde020ebc9bc7d7d0c57c2f30b51 | Cancelled by later push | Added explicit per-task core budget and exclusion rows. |
| #36 | 4e1b872f2a415499192e2ed19d70c096deed0247 | Cancelled by later push | Lowered tree/MLP iteration caps. |
| #37 | 41df4ac5f14b750d7c8e01b621b0e6f1ea289a61 | Cancelled by later push | Added testable budget selector. |
| #38 | 11bb7c107907c110d2d62ecabd3f0f7b43c502e4 | Cancelled by later push | Wired the budget selector into experiment runner and wrote explicit BLOCKED_COMPUTE_BUDGET statuses. |
| #39 | 7799b070975dfbe7d3f3bb50888ecc38fc8c0e18 | Pending at last check | Added unit tests proving full catalogue vs core-screen selection. |
| #40+ | 2ea446b3afa42e4283ab7e26964c08d2e2659821 | Expected after plan amendment; must be verified | Candidate canonical run using final policy. No final model metric is accepted until tests, completed job, artifact output and code SHA are verified. |

The model pool and estimator caps are configuration choices fixed before inspecting out-of-sample performance. The locked holdout remains a one-time comparison source and is not used for selection.
