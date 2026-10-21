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


## Uploaded-PDF method comparison — bounded run initiated 2026-10-14

| Run | Branch / commit | Status | Scope |
|---|---|---|---|
| PDF-METHOD-AUDIT-001 | [research/pdf-method-audit](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/pdf-method-audit), latest code commit `5cd571a013b6ba218ff2ea868edb571a5864b725` | Workflow [#55](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562973443) pending/queued at log time | Expanded classic regressors/classifiers and sequence candidates. New model outcomes pending; no result inferred from code presence. |

Changes: added Linear Regression, Lasso, SGD, KNN, Decision Tree, Gradient Boosting and AdaBoost to classical registries; added vanilla RNN, CNN and LSTM+GRU, CNN+RNN, CNN+TCN, LSTM+TCN compact sequence candidates. The frozen runner uses chronological splits and existing scoring/uncertainty routines; sequence models are restricted to one-session return/direction for a bounded CPU budget.

Uncovered method families are explicit: BERT/news fusion (requires timestamped news), self-organizing fuzzy neural networks, DBN, wavelet preprocessing, Granger feature screening and backward-elimination LSTM are not yet empirically tested. Three options-strategy PDFs remain outside the prediction-only question. The final artifact must classify each family as tested, failed, blocked or not implemented.


## VOL-REGIME-OPT-1.0 — protocol freeze and source-gate probe (2026-10-15)

A separate user-approved study was opened for a weekly volatility-regime switch. Frozen protocol: 5-session volatility-expansion classifier is primary; 20-session signal is secondary; high regime buys ATM weekly straddle; low regime sells OTM weekly call/put near absolute delta 0.07; middle probability band is no-trade. Positions are held to the same week's expiry close. Costs, slippage, exact contract identity, expiry calendar, lot size, coverage and tail risk are hard gates.

The first automated step is a Dhan weekly/monthly schema control probe on a fixed five-day historical window. Do not infer P&L from source-schema success. The prior option studies had failing data-quality/profitability gates and do not validate this new strategy. No threshold tuning or live deployment.


### VOL-REGIME-OPT-1.0 source-gate correction — 2026-10-15

Initial workflow failure was an infrastructure configuration error (setup-python pip cache path); fixed by explicitly naming requirements-research.txt. The subsequent Dhan probe passed the MONTH schema control (375 rows per option type in 2025-01-06 through 2025-01-10) but WEEK / expiryCode=0 returned HTTP 400 / DH-905 “expiryCode is required”. A single bounded correction now tests weekly codes 0, 1 and 2. No option P&L has been calculated and monthly rows are not treated as weekly contracts.


### QE-NIFTY-1.0 — safe adapter implementation (2026-10-22)

- Pinned upstream QuantEvolve to 2df1e85758620e8ac0ca88ffc428b379d6cb9620.
- Added a literal-only candidate schema and a trusted evaluator using daily NIFTY data, past-only feature normalization, three chronological development folds and a one-time final 20% holdout evaluation.
- Added an updated Gemini provider patch using the google-genai SDK, with a single model, maximum four iterations, fixed seed, no retries and a separate publisher that only receives sanitized JSON.
- Added automated checks for source parsing (not execution), feature causality, holdout isolation, metric interval generation and explicit options source/contract gates.
- Regression workflow [39662185936](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39662185936) exposed an exact-phrase assertion mismatch (2 pass, 1 fail), before any candidate ran. The correction is included in this implementation batch. Verify the next workflow run before considering the integration shell passed.
- Options contract/quality status remains blocked by the previous cancelled HF contract audit [38807375042](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38807375042). No option P&L was run, and none is permitted until the new source gate passes.
- No OOS performance finding exists at this implementation checkpoint.

### QE-DELIVERY-39665389015 — 2026-10-21T19:53:08.803176+00:00
- Prediction run status: **BLOCKED_AUTOMATED_TESTS**; sanitized reason: integration test gate did not pass.
- No valid QuantEvolve prediction holdout result is claimed.


### QE-NIFTY-1.0 bounded controller run — 2026-10-22

- [Run 39665689785](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39665689785): all 10 tests passed; Dhan daily data validated (4,905 rows, 2007-01-02 to 2026-10-19; SHA-256 66e06c7fd4affcf8753e68046b311b8cfe27cb292af93691d2ee63787381629c); pinned QuantEvolve checkout and bounded controller job completed.
- The selected declarative specification had all weights and intercept equal to zero. Final holdout n=981, 2022-11-04 to 2026-10-19. MAE 0.0058034626, same as zero-return baseline; skill 0.0; MAE-improvement 95% circular block-bootstrap interval [0, 0]. This is no improvement for this selected candidate; no strategy profitability inference.
- Directional accuracy is undefined because the selected model issued only zero forecasts; directional coverage is 0%. This corrects the initial inaccurate direction metric label.
- A runner validator defect rejected holdout status PREDICTION_HOLDOUT_EVALUATED because it expected PASS for every stage. The metrics were validated against saved spec/hash/arithmetic and the run manifest has been reconciled. The runner's expected status and artifact workspace are fixed for subsequent runs.
- The options contract gate remains BLOCKED_NO_VERIFIED_CONTRACT_DATA; no options strategy P&L has been run.

### QE-DELIVERY-39666799180 — 2026-10-21T20:03:03.004060+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39667156299 — 2026-10-21T20:07:02.694500+00:00
- Prediction run status: **PREDICTION_HOLDOUT_EVALUATED**. Candidate source was never executed; only a validated declarative spec was retained.
- Final chronological holdout: n=981; target dates 2022-11-04 to 2026-10-19.
- MAE skill vs zero-return baseline: 0.000000; directional accuracy: not available; MAE-improvement 95% circular block-bootstrap interval: [0.000000, 0.000000].
- Interpretation: one selected candidate evaluated once against a zero-return forecast; not proof of a profitable trading strategy or universal superiority.
- Published reports: reports/quantevolve/prediction/run-39667156299/best_strategy_spec.json, reports/quantevolve/prediction/run-39667156299/run_manifest.json, reports/quantevolve/prediction/run-39667156299/development_metrics.json, reports/quantevolve/prediction/run-39667156299/holdout_metrics.json


### QE-NIFTY-1.0 two-run bounded prediction outcome — 2026-10-22

- Runs [39665689785](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39665689785) and [39667156299](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39667156299) completed bounded four-iteration controller workflows. Both selected the declarative zero-return forecast; both held-out MAE was 0.00580346256399, identical to the zero-return baseline, for MAE skill 0 and block-bootstrap MAE-improvement CI [0,0] (second run report verified directly).
- Holdout was 981 targets from 2022-11-04 to 2026-10-19; final holdout was not used for selection. Directional accuracy is undefined and coverage is 0 for the zero forecast.
- Provider-call telemetry was absent, so do not imply that the LLM returned a successful mutation. Sanitized attempt/success/failure counters and a success gate are added now. Future expensive runs must be explicitly requested via manual workflow_dispatch; automatic request is false.
- Options P&L remains blocked pending source/contract mapping and lot-size provenance.

### QE-DELIVERY-39667767456 — 2026-10-21T20:09:34.577276+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39667889681 — 2026-10-21T20:10:29.755713+00:00
- Prediction run status: **BLOCKED_AUTOMATED_TESTS**; sanitized reason: integration test gate did not pass.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39668093032 — 2026-10-21T20:12:02.681024+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39668183031 — 2026-10-21T20:16:51.439416+00:00
- Prediction run status: **EVOLUTION_NO_SUCCESSFUL_LLM_RESPONSES**; sanitized reason: controller returned without a verified successful Gemini generation response.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39669107291 — 2026-10-21T20:19:04.095512+00:00
- Prediction run status: **EVOLUTION_NO_SUCCESSFUL_LLM_RESPONSES**; sanitized reason: controller returned without a verified successful Gemini generation response.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39669141475 — 2026-10-21T20:19:45.272070+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.


### QE-NIFTY-1.0 API diagnostic disposition — 2026-10-22

- [Run 39668183031](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39668183031): 4 Gemini attempts, 0 successful responses (3 TimeoutError, 1 ServerError); candidate generation gate correctly blocked scoring.
- [Run 39669107291](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39669107291): one fallback request to gemini-3.6-flash, 0 successful responses (1 ServerError). No forecast metrics exist for either failed-generation run.
- API diagnostic closed under the finite protocol. No further automatic API retries; repository run request is offline by default. This is an integration/API availability outcome, not evidence about prediction skill.

### QE-DELIVERY-39669633087 — 2026-10-21T20:22:22.795946+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39669708490 — 2026-10-21T20:23:18.221112+00:00
- Prediction run status: **NO_RUN_MANIFEST**; sanitized reason: no successful holdout report.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39670001128 — 2026-10-21T20:25:04.924319+00:00
- Prediction run status: **NO_RUN_MANIFEST**; sanitized reason: no successful holdout report.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39670041315 — 2026-10-21T20:25:42.699029+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.


### QE-NIFTY-1.0 options source audit and final disposition — 2026-10-22

- Workflow [39670001128](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39670001128) sampled three public HF NIFTY expiry files: 986,041 rows, 8,822,294 bytes; each schema had timestamp/expiry/strike/type/OHLCV/OI but no lot_size field. Per-file hashes and license metadata are in [options_source_audit.json](../reports/quantevolve/options_source_audit.json).
- Source license is CC-BY-NC-4.0; raw files remain in cache and are not committed. Timestamp type was timestamp[ns, tz=+05:30].
- Official expiry reconciliation, historical lot-size mapping, full coverage, duplicate conflict rate and executable prices remain unverified. Options gate remains blocked; no P&L was run.
- Prediction API diagnostic: [39668183031](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39668183031) recorded 4 failed Gemini requests; [39669107291](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39669107291) recorded one failed fallback request. Zero successful generation responses, no candidate scored. Stop API retries under finite protocol.
- Final manuscript: [QUANTEvolve_NIFTY_INTEGRATION_MANUSCRIPT.md](manuscripts/QUANTEvolve_NIFTY_INTEGRATION_MANUSCRIPT.md). Final disposition: INCONCLUSIVE/BLOCKED; no strategy approved.

### QE-DELIVERY-39670494972 — 2026-10-21T20:28:30.360971+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39671741090 — 2026-10-21T20:36:59.137048+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39671900967 — 2026-10-21T20:38:06.559428+00:00
- Options source audit status: **BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED**; sampled files=3; sample rows=986041.
- License: CC-BY-NC-4.0; lot-size field present in all samples=False.
- Options P&L permitted=False. Official expiry reconciliation, historical lot size, full coverage and executable pricing remain mandatory gates.
- Published source report: reports/quantevolve/options_source_audit.json.


### QE-DELIVERY-39671900967 — row-level audit not valid
- The bounded HF sample acquisition completed (3 files, 986,041 rows), and source/schema metadata was published.
- Official circular lot mappings were recorded for the three expiry cohorts, but all row-level reconciliation checks failed with `NameError` because the source audit omitted `import pandas as pd`.
- Do not treat sample expiry identity as verified from this run; correction and one bounded validation retry pending. Options P&L remains forbidden.

### QE-DELIVERY-39672382046 — 2026-10-21T20:41:43.644443+00:00
- Options source audit status: **BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED**; sampled files=3; sample rows=986041.
- License: CC-BY-NC-4.0; lot-size field present in all samples=False.
- Options P&L permitted=False. Official expiry reconciliation, historical lot size, full coverage and executable pricing remain mandatory gates.
- Published source report: reports/quantevolve/options_source_audit.json.

### QE-DELIVERY-39672476827 — 2026-10-21T20:42:28.121600+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39672831979 — 2026-10-21T20:44:37.099025+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39672923539 — 2026-10-21T20:45:29.129229+00:00
- Prediction run status: **BLOCKED_AUTOMATED_TESTS**; sanitized reason: integration test gate did not pass.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39673276814 — 2026-10-21T20:47:45.092701+00:00
- Prediction run status: **BLOCKED_AUTOMATED_TESTS**; sanitized reason: integration test gate did not pass.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39673437932 — 2026-10-21T20:48:49.402937+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39673574590 — 2026-10-21T20:49:48.425703+00:00
- Options source audit status: **BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED**; sampled files=3; sample rows=986041.
- License: CC-BY-NC-4.0; lot-size field present in all samples=False.
- Options P&L permitted=False. Official expiry reconciliation, historical lot size, full coverage and executable pricing remain mandatory gates.
- Published source report: reports/quantevolve/options_source_audit.json.

### QE-DELIVERY-39673603711 — 2026-10-21T20:50:43.641117+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39673809637 — 2026-10-21T20:51:31.557623+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39673874887 — 2026-10-21T20:53:28.339543+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39674271641 — 2026-10-21T20:54:50.087688+00:00
- Options source audit status: **BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED**; sampled files=3; sample rows=986041.
- License: CC-BY-NC-4.0; lot-size field present in all samples=False.
- Options P&L permitted=False. Official expiry reconciliation, historical lot size, full coverage and executable pricing remain mandatory gates.
- Published source report: reports/quantevolve/options_source_audit.json.

### QE-DELIVERY-39674310202 — 2026-10-21T20:55:31.163470+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39674503245 — 2026-10-21T20:56:14.835215+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39674646848 — 2026-10-21T20:57:19.486917+00:00
- Options source audit status: **BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED**; sampled files=3; sample rows=986041.
- License: CC-BY-NC-4.0; lot-size field present in all samples=False.
- Options P&L permitted=False. Official expiry reconciliation, historical lot size, full coverage and executable pricing remain mandatory gates.
- Published source report: reports/quantevolve/options_source_audit.json.

### QE-DELIVERY-39674682536 — 2026-10-21T20:58:08.010459+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39674850493 — 2026-10-21T20:58:51.053248+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39675010446 — 2026-10-21T20:59:58.207970+00:00
- Options source audit status: **BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED**; sampled files=3; sample rows=986041.
- License: CC-BY-NC-4.0; lot-size field present in all samples=False.
- Options P&L permitted=False. Official expiry reconciliation, historical lot size, full coverage and executable pricing remain mandatory gates.
- Published source report: reports/quantevolve/options_source_audit.json.

### QE-DELIVERY-39675047713 — 2026-10-21T21:00:44.121812+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39675217418 — 2026-10-21T21:01:38.477111+00:00
- Prediction run status: **LLM_EVOLUTION_NOT_REQUESTED**; sanitized reason: automatic workflow ran offline gate only; no model-generation API call was requested.
- No valid QuantEvolve prediction holdout result is claimed.

### QE-DELIVERY-39675422599 — 2026-10-21T21:02:57.742297+00:00
- Options source audit status: **BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED**; sampled files=3; sample rows=986041.
- License: CC-BY-NC-4.0; lot-size field present in all samples=False.
- Options P&L permitted=False. Official expiry reconciliation, historical lot size, full coverage and executable pricing remain mandatory gates.
- Published source report: reports/quantevolve/options_source_audit.json.
