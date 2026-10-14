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


## Follow-on option-buying validation — 2026-10-14

| Run ID | Branch | Status | Scope / gate |
|---|---|---|---|
| OPT-INIT-001 | research/option-buying-validation | INITIALIZED; NO RESULTS | Test next-session intraday ATM straddle and one-step OTM strangle after a prespecified technical Logistic volatility-expansion alert. Dhan historical options are preferred if auth and schemas validate. Include Paytm Money brokerage, current statutory/exchange charges, and 0/25/50/100 bps adverse-slippage scenarios. Results must be acquired before developer/tester branches are created. |

This is a user-approved scope amendment after NIFTY-PRED-1.0 closure. It does not replace or rewrite the original study. No option P&L result is available or asserted in this initialization entry.


## OPT-BUY-1.0 — source acquisition attempts

| Run | Commit | Result | Evidence |
|---|---|---|---|
| [Option validation #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38542434374) | 944ec84c8047d31dce66165bd8db0a094133dc23 | BLOCKED_REQUEST_AUTH_OR_SCHEMA | First Dhan request (WEEK, expiryCode=0, ATM CALL, 2022-11-01 to 2022-12-01) returned HTTP 400. Zero successful/empty requests; one failed request; no P&L. Unit tests passed. |
| [Option validation #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38542754673) | 8a3d9a3c7f47628501c60229c5802653a637b1e5 | BLOCKED_REQUEST_AUTH_OR_SCHEMA | Same first-request 400 after adopting official NSE fee assumptions; no quotes or P&L; unit tests passed. |
| [Option validation #6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38543046923) | 29aa17d29794ac7ef9368a90f56d9d20582b9ef1 | IN PROGRESS AT LOG UPDATE | Uses Dhan's documented MONTH/expiryCode=1 request example and includes redacted provider error details. Empirical results pending; no inference until run completes. |

The earlier attempts are retained as failed runs. The protocol is not considered data-complete until the provider request succeeds and quote-quality gates pass.

## OPT-BUY-1.0 — first pilot outcome and corrected run

| Run | Status | Outcome |
|---|---|---|
| [#6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38543046923) | SUCCESS technically; pilot data gate FAIL | Dhan monthly option calls: 196 planned, 196 valid/empty, 0 failed. 303,548 raw rows; 294,419 usable; 45 conflicting duplicate groups / 9,084 duplicate groups. Only 171/980 (17.45%) dates had valid fixed-strike entry/exit for both structures. Four candidate average premium-normalized daily returns were negative. Results are preliminary and not accepted. |
| [#7](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38544279448) | FAILED TEST GATE | Eight tests passed; one redaction-fixture assertion failed because expected error fields were missing from the fake response. Acquisition was skipped. Failure and correction are documented in ERROR_LOG.md. |
| [#8](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38545312929) | CANCELLED / SUPERSEDED | Started from the pre-correction test fixture; do not treat its output as final. |
| [#9](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38545503819) | RUNNING | Fixes cache filename and test fixture; expands request grid to monthly ATM−3…ATM+3 for calls and puts. Primary comparison is daily net rupee P&L; premium returns are secondary. |

The first pilot data gate failed because quote coverage was only 17.45% (<80% threshold). Its paired percentage-return p-values do not qualify as evidence under this protocol; the wider-strike corrected run is required.
