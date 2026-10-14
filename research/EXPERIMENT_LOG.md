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


## OPT-BUY-1.0 final gate and independent review — 2026-10-14

- Final workflow: [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384), commit `0d33e2e046a26e017f0100f75e28243753177cb7`; 13 tests passed pre- and post-analysis. Artifact SHA-256 `86e9d03c6c55c17d46348a8dc40b9a02f247f2f9bca38703110c74c030be889`.
- Final cached request status: 686 cached windows, 0 new requests, 0 failed windows. Quote data: 1,062,082 raw rows, 1,029,545 usable rows.
- Data gate: straddle coverage 83.98% (pass); strangle coverage 69.18% (fail against ≥80%); conflicting quote groups 452/32,085=1.409% (fail against ≤1%).
- Primary-cost net daily P&L: −₹315.71, −₹349.35, −₹327.64 and −₹369.43 for 5-session straddle, 5-session strangle, 20-session straddle and 20-session strangle. All 95% intervals lie below zero; all 100-bps and both-half profitability gates fail.
- Independent tester reproduced the 48,032-row ledger arithmetic and four primary means, bootstrap intervals, raw p-values and Holm adjustments. Positive paired differences vs always-buy are not proof of profitability.
- Final disposition: close OPT-BUY-1.0 as NO-GO for tested implementations and INCONCLUSIVE for the broader hypothesis. No paper/live candidate approved. See research/option-validation/TESTER_REPORT.md and DEVELOPER_DISPOSITION.md.

## OPT-BUY-2.0 — 2026-10-14 strike-grid implementation attempt

- Frozen protocol: [research/STRIKE_SELECTION_PLAN.md](STRIKE_SELECTION_PLAN.md); code branch `research/option-strike-selection`.
- Run #1: 13 pre-existing regression tests passed; acquisition step completed but strike grid exited with `BLOCKED: no usable option quote rows`. [Evidence](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551789841).
- Developer correction: emit sanitized diagnostics and empty result tables on data block, and add the prespecified 16-candidate × 2-horizon block-bootstrap/Holm inference family. Follow-up runs #2 and #3 are pending/in progress at the time of this entry.
- No result values are claimed. If data remain unavailable, close as data-blocked; do not loosen gates or rank candidates.


## OPT-BUY-2.0 — run #4 live checkpoint (2026-10-14 17:34 IST)

- Workflow: [run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097), branch `research/option-strike-selection`, commit `29182fbf7e49fed42d4271c4bb41ad4f7dadd4e4`.
- Status at check: running. Daily-target acquisition and validation completed, and the existing regression suite passed (13 tests). “Acquire/reuse options cache” remains in progress; strike grid, sanitized result upload and final tests remain pending.
- No result artifact is currently available. This checkpoint is operational only; there are no strike ranks, candidate P&Ls, p-values, or strategy conclusions to report. User waived independent tester sign-off for this run, but the frozen data-quality and inference gates remain in force.


### Run #4 progress checkpoint — 2026-10-14 — subsequent live poll

- A subsequent live poll shows the options-cache step completed and the frozen strike grid is now running. Daily target validation and the pre-analysis regression suite (13 tests) passed.
- The options step's workflow-level success is not interpreted as proof that option data passed the data gate because the step uses `continue-on-error: true`. No result artifact or strike-grid conclusion is available at this checkpoint.


## OPT-BUY-2.0 run #4 — results and disposition (2026-10-14)

- [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) completed successfully at workflow level; 13 pre-analysis and 13 final regression tests passed, and sanitized artifact `option-strike-selection-38552144097` was uploaded (SHA-256 `7fae1922403e398f040ee8ca3a80f607e07e0d6569c98eb35b3ae0c6f168d285`).
- Data: 1,055,699 raw rows; 1,023,541 usable rows; 452 conflicting duplicate groups out of 31,706 duplicate groups (1.4256%); no parse failures; quote dates 2022-11-01 through 2026-10-14.
- Coverage across the 980 test dates ranged from 83.27% for ATM/ATM (C0_P0) down to 16.94% for C3_P-3. Only C0_P0 cleared the 80% coverage gate. The conflict rate exceeded the 1% gate. Overall confirmatory gate failed; all candidate ranking is exploratory.
- At primary costs (50 bps adverse slippage per premium side and ₹10 per order), all 32 model-filtered candidate × horizon means were negative, with 95% block-bootstrap interval upper bounds below zero. Examples: ATM/ATM horizon 5 mean −₹315.02 per eligible date (95% CI −₹406.69 to −₹232.69; 223 alert trades); ATM/ATM horizon 20 mean −₹330.45 (95% CI −₹416.51 to −₹244.30; 259 alert trades). Across the full grid, chronological half means were negative in both halves for all model-filtered cells. Higher slippage further worsened outcomes. These are exploratory descriptive outcomes because the data gate failed.
- Defect found in run #4 artifact: all 32 primary raw/Holm p-values were blank/NaN despite nonempty ledgers. Do not treat multiplicity-adjusted inference as complete. Developer added an explicit null-centered circular block-bootstrap p-value implementation in commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9; [corrective rerun #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress. No parameter search is being expanded; this is a bounded inference correction.
- Additional scope limitation: the frozen plan calls for a common-date sensitivity, but run #4 artifact does not contain one. Do not claim cross-candidate superiority; record this as not completed under the failed quality gate.
- Decision: **NO-GO / no strike candidate approved**. The study is non-confirmatory due conflict rate and coverage failures, all measured primary model-filtered means are negative, and the p-value output defect requires the single corrective rerun. No paper or live deployment.


## Uploaded-PDF model audit — run #56

| Run | Branch / commit | Workflow | Data hash | Status | Outcome |
|---|---|---|---|---|---|
| PDF-AUDIT-056 | `research/pdf-method-audit` / `cdf8bab26d9234a6312b1ae00a3f35370574c792` | [GitHub Actions #56](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38585954777) | `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050` | WORKFLOW SUCCESS; TESTER GATE OPEN | Data validation, feature matrix, technical/global catalogues, ARIMA, merge and artifact upload completed. Artifact SHA-256 `02a222453c7ac4e21e82253f407893e1943da0d5e6fec874750a350ba11aceb2`. See [expanded results](PDF_METHOD_AUDIT_RESULTS.md). QLIKE skill export and sequence epoch metadata require review; rejected USD/INR, gold, WTI and NSE sources are logged. No best model declared. |

Run #56 reports 632 technical experiment cells and 244,839 out-of-sample prediction rows in its run metadata. Descriptive one-session return RMSE values are tightly grouped around 0.00794, with no adjusted-significant evidence in the inspected top return rows. Direction and volatility-expansion metrics vary by horizon and need independent statistical review. Some Holm-adjusted p-values are below .05, so exact families and loss definitions must be independently checked before confirmatory claims.


## Corrected expanded catalogue — run #60

| Run | Branch / commit | Workflow | Data hash | Status | Outcome |
|---|---|---|---|---|---|
| PDF-AUDIT-060 | `research/pdf-audit-developer` / `e93fe35d8bb11df65d1c466434d5401298c077ed` | [GitHub Actions #60](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38593936036) | `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050` | WORKFLOW SUCCESS; RESULTS ACQUIRED; INDEPENDENT AUDIT NEXT | 1,097 merged metric rows; 485 OOS-evaluated rows; 130 compute-budget-blocked rows; empty technical/global model-error CSVs; corrected QLIKE score-difference export and three-epoch metadata. Artifact SHA-256 `b601320f64ab8ec0c62f0a07e458287cba781eca73107f1b2c38beda140a8151`. See [run #60 results](PDF_METHOD_AUDIT_RESULTS.md). |

Result interpretation: return rows show no Holm-adjusted evidence of skill. Classification p-values are not evidence of improvement without the paired-loss sign; positive model-minus-baseline loss differences mean the model is worse. Volatility rankings differ between MAE/RMSE and QLIKE. The conclusion is “no robust return/direction winner established”; volatility-expansion is exploratory. The separate tester handoff is allowed now because result acquisition and developer documentation are complete.


## Corrected expanded catalogue — run #60

| Run | Branch / commit | Workflow | Data hash | Status | Outcome |
|---|---|---|---|---|---|
| PDF-AUDIT-060 | `research/pdf-audit-developer` / `e93fe35d8bb11df65d1c466434d5401298c077ed` | [GitHub Actions #60](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38593936036) | `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050` | WORKFLOW SUCCESS; RESULTS ACQUIRED; INDEPENDENT AUDIT NEXT | 1,097 merged metric rows; 485 OOS-evaluated rows; 130 compute-budget-blocked rows; empty technical/global model-error CSVs; corrected QLIKE score-difference export and three-epoch metadata. Artifact SHA-256 `b601320f64ab8ec0c62f0a07e458287cba781eca73107f1b2c38beda140a8151`. See [run #60 results](PDF_METHOD_AUDIT_RESULTS.md). |

Interpretation rule: negative mean paired loss difference (`model loss - baseline loss`) favors the model; positive favors baseline. Small p-values alone do not imply improvement. Return rows show no Holm-adjusted evidence of skill; volatility rankings differ by MAE/RMSE and QLIKE. No robust return/direction winner is established.


## Final corrected run #62

- Workflow: [run #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792), commit `be02efcb8fbd21f36fec826bdcc3ee923f75849a` — SUCCESS.
- Artifact SHA-256: `14c9d6fc1bcb0f00ff28e708cb10a6cab9b378e5e60ff31f6e66aaa5e977172b`.
- Final output: 471,735 predictions, zero null target dates. Tester disposition: PASS WITH SCOPE LIMITATIONS. Full final tables are in [PDF audit results](PDF_METHOD_AUDIT_RESULTS.md).
- Final inference: one-session volatility QLIKE improved after Holm correction; no robust return/direction winner. Close the bounded prediction-only scope; retain missing data and source-timing issues as limitations.
