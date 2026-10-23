# Fresh NIFTY 50 Prediction Research

## Latest prediction audit — 2026-10-22

The prior workflow completed operationally, but its artifact contains Historical defect in run #39699761966: 798 multi-session forecasts had missing target dates due to partial forward windows. Corrective run #39704420478 completed with zero missing target dates. The pipeline is operationally corrected; scientific conclusions remain limited pending future-period replication and numerical stability checks.

- [Audit record](research/FRESH_PREDICTION_AUDIT_2026-10-22.md) · [Artifact audit utility](research/audits/audit_nifty_predictions.py) · [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-developer) · [Corrective workflow #39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478)
- Return/direction forecasts have no robust selected edge. The one-session ExtraTrees volatility-proxy result was numerically reproduced from the prior artifact, but remains a replication candidate and not a trading signal. Options P&L and strategy development remain blocked.

**Research version:** NIFTY-PRED-1.0  
**Scope:** Prediction only. No trading strategy design, optimization, or recommendation in this study.  
**Started:** 2026-10-14  
**Status:** Corrective workflow [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) completed; 277,633 prediction rows have zero missing target dates. Return/direction edge not established; volatility-proxy result requires untouched future replication. Developer-only process per user request; no tester gate. Artifact audit found 798 invalid missing-target-date rows in h5/h20 volatility and volatility-expansion outputs. Correction commit [e8133a5](https://github.com/vishnuvcr/Naked-Options-v2/commit/e8133a582cbe6c06ce46514f871d1393fc142f6f) is running through workflow [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478). No strategy is approved.

## Repository audit

The repository was empty at project start: no readable README, files, branches, commits, datasets, experiment logs, or workflows. This project therefore starts a new research record without overwriting prior repository work. Relevant prior literature available in the ChatGPT Project library is cited in `research/LITERATURE_REVIEW.md`; it is not treated as this project's validated experimental output.

## Research navigation

- [Research plan](research/RESEARCH_PLAN.md)
- [Research questions and hypotheses](research/RESEARCH_QUESTIONS.md)
- [Literature review](research/LITERATURE_REVIEW.md)
- [Data catalog](research/DATA_CATALOG.md)
- [Experiment log](research/EXPERIMENT_LOG.md)
- [Results](research/RESULTS.md)
- [Phase status and gates](research/PHASE_STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Independent tester report](research/TESTER_REPORT.md)
- [Scientific manuscript](research/MANUSCRIPT.md)
- [Reproducibility guide](research/REPRODUCIBILITY.md)
- [Execution policy and phase-branch rules](research/EXECUTION_POLICY.md)

## Phase branches

Historical checkpoint branches for completed setup phases and the active model branch are available: [Phase 1](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-1-audit), [Phase 2](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-2-literature), [Phase 3](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-3-data), [Phase 4](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-4-baselines), and [Phase 5](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-5-models). The resource-bounded execution branch is [research/phase-5-bounded](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-5-bounded). Future phase branches will be created only after their predecessor gate passes.

## Scientific integrity

No model will be declared best from training fit, shuffled validation, price-level R² alone, or a reused test set. Return, directional, volatility, and level targets will be evaluated separately with chronological walk-forward evaluation, simple benchmarks, uncertainty estimates, and multiplicity control. Results unavailable because of data, credentials, compute, or workflow restrictions will be marked **blocked/not run**, never imputed or fabricated.

## Current summary

### Active follow-on: VOL-REGIME-OPT-1.0

A separate weekly-options volatility-regime hypothesis is in protocol/source-gate work on [the developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-developer). A bounded Dhan probe has returned structurally valid weekly CALL/PUT arrays for candidate expiry codes 1 and 2 in a five-day January 2025 sample. Exact expiry mapping, stable contract identity, full coverage and P&L remain unverified. See the [frozen plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/research/VOL_REGIME_OPTIONS_PLAN.md) and [sanitized source audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/source_audit.json). No strategy is approved.

- **Original prediction study (NIFTY-PRED-1.0): CLOSED WITH SCOPE LIMITATIONS.** Its corrected canonical run is [#49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128); see [results](research/RESULTS.md), [phase status](research/PHASE_STATUS.md), and [scientific manuscript](research/MANUSCRIPT.md).
- **Follow-on option-buying validation (OPT-BUY-1.0): CLOSED — NO-GO for tested candidates; broader hypothesis inconclusive.** The completed [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) and independent review found strangle quote coverage of 69.18% (<80%), conflicting duplicate groups at 1.409% (>1%), and negative net daily P&L confidence intervals for all four candidates. No paper/live strategy is approved; details are in [the option-validation results](research/option-validation/RESULTS.md) and [tester report](research/option-validation/TESTER_REPORT.md).
- Latest validated NIFTY data: 4,906 Dhan daily rows from 2007-01-02 to 2026-10-21; SHA-256 `2a76714665754ec6371e92d8b9b56565606c0d1a4a2fc9cc9013291e233b2158` (the earlier 4,901-row run remains historical).
- Data gaps remain documented: historical options features, FII/DII, PCR, breadth, point-in-time constituents/corporate actions, and timestamped news were not comprehensively verified for the original prediction study. These gaps limit the scope of inference.
- Statistical integrity: the original study found no robust return/direction edge after multiple-testing correction. The option-buying follow-on did not demonstrate profitable net option P&L after modeled costs.
- Audit trail: [error log](research/ERROR_LOG.md), [experiment log](research/EXPERIMENT_LOG.md), [interaction log](research/INTERACTION_LOG.md), [frozen option validation plan](research/OPTION_BUYING_VALIDATION_PLAN.md), [independent tester](research/option-validation/TESTER_REPORT.md), and [developer disposition](research/option-validation/DEVELOPER_DISPOSITION.md).

The original prediction study and follow-on option-buying study are both closed for their stated protocols. Any further work should start a separately versioned research question and preregistered protocol rather than reopen failed gates or repeat parameter loops.


## Latest correction checkpoint — 2026-10-14

The independent audit found that forward-volatility targets near the sample tail could be calculated from partial future windows. The developer branch now requires all horizon returns to be present before assigning the 5-/20-session volatility target. Workflow [#48](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38532904979) stopped at a regression-test assertion (a scalar `.notna()` call), before feature construction or model fitting. That test was corrected to `pd.notna` in commit `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`; workflow [#49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) is the retest and corrected-run gate.

Until #49 completes, the run #45 model scores remain preliminary. No strategy or model is approved. Phase 5/7 remain open pending successful tests, corrected OOS predictions with complete target windows, and an independent tester report. See the [developer error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/developer-review/research/ERROR_LOG.md) and [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/developer-review/research/PHASE_STATUS.md).


## Corrected run #49 — 2026-10-14

The forward-volatility target defect has been fixed and regression-tested. [Workflow #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) completed successfully. Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`.

- [Results and evidence register](research/RESULTS.md)
- [Phase status and gate decisions](research/PHASE_STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Developer correction branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/developer-review)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md)

Preliminary results: no robust return/direction edge has been demonstrated; selected 5-/20-session global return models are worse than the zero-return baseline; volatility models do not pass adjusted QLIKE comparisons. Some volatility-expansion classifiers improve log loss, but are exploratory and not trading signals. The independent tester passed the bounded prediction-only study with scope limitations; Phase 2 literature depth and Phase 6 data/regime coverage remain partial and are documented. This is prediction research only: no options-chain strategy, transaction-cost/slippage simulation, or Paytm Money execution analysis has been completed.


## Independent review outcome — 2026-10-14

The independent tester has issued **PASS WITH SCOPE LIMITATIONS** for the bounded prediction-only research. See the [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md), [results register](research/RESULTS.md), and [phase gates](research/PHASE_STATUS.md).

Conclusion: no robust return/direction edge is demonstrated. Volatility-expansion results are exploratory, and one-session probabilities are poorly calibrated. No trading strategy is approved or tested. Historical option chains, FII/DII, PCR, breadth, timestamped news, transaction costs/slippage and Paytm Money execution remain outside the verified dataset and experiments.


**Closure status:** The nine-phase research is closed for the bounded prediction-only scope, with accepted limitations. The conclusion is that this tested model/data set did not establish a robust return/direction edge. No options strategy or live execution plan is approved.


The static research status page is published through the lightweight [Pages publish workflow](https://github.com/vishnuvcr/Naked-Options-v2/actions/workflows/publish-research-status.yml). The final option-buying plan, results, manuscript, figures and independent review are now in main; this README update triggers a fresh status-page deployment.


## Follow-on study: option-buying validation — OPT-BUY-1.0

The original nine-phase NIFTY-PRED-1.0 prediction-only study remains closed and unchanged. The separate test of next-session intraday monthly-option straddles/strangles is now closed for its frozen scope.

**Final disposition: NO-GO for the tested implementations; broader hypothesis INCONCLUSIVE because the data-quality gate failed.** Final workflow [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) completed successfully; 13 unit tests passed before and after analysis.

- [Frozen validation plan](research/OPTION_BUYING_VALIDATION_PLAN.md)
- [Results](research/option-validation/RESULTS.md)
- [Structured manuscript](research/option-validation/MANUSCRIPT.md)
- [Net P&L comparison chart](research/option-validation/figures/net_pnl_comparison.svg)
- [Slippage sensitivity chart](research/option-validation/figures/slippage_sensitivity.svg)
- [Primary comparisons CSV](reports/option_validation/primary_comparisons.csv)
- [Results summary JSON](reports/option_validation/results_summary.json)
- [Independent tester report](research/option-validation/TESTER_REPORT.md)
- [Developer disposition](research/option-validation/DEVELOPER_DISPOSITION.md)
- [Workflow run/artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-buying-developer)
- [Independent tester branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-buying-independent-tester)

At ₹10 brokerage/order and 50 bps adverse slippage per premium side, all four alert-filtered candidates had mean net daily P&L between −₹315.71 and −₹369.43 per one-lot-proxy eligible-day slot; all 95% intervals were negative. Positive paired differences versus always-buy (Holm-adjusted p=0.002) only show loss reduction relative to a worse baseline.

Frozen gates failed: strangle quote coverage 69.18% (minimum 80%) and conflicting duplicate groups 1.409% (maximum 1%). All candidates failed the 100-bps and both-half profitability gates. No paper-trading or live deployment is approved. Do not relax gates or continue optimization loops.

## OPT-BUY-2.0 — Strike-selection research (in progress)

- Protocol: [strike-selection plan](research/STRIKE_SELECTION_PLAN.md); implementation: [strike-grid code](research/option-strike-selection/strike_grid.py).
- Automated run #1 failed at the data stage: the existing 13 regression tests passed, but no usable historical option quote rows were loaded. This is a data blocker, not a profitability finding. [Run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551789841).
- Diagnostic-output fix and inference-family correction are being tested in [run #2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551939491) and [run #3](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552000337). No strike winner or strategy is approved.
- Separate review branches: [developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-strike-selection-developer) and [independent tester](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-strike-selection-independent-tester). The tester's current report is blocked pending usable quotes.




## OPT-BUY-2.0 run #4 — results and disposition (2026-10-14)

- [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) completed successfully at workflow level; 13 pre-analysis and 13 final regression tests passed, and sanitized artifact `option-strike-selection-38552144097` was uploaded (SHA-256 `7fae1922403e398f040ee8ca3a80f607e07e0d6569c98eb35b3ae0c6f168d285`).
- Data: 1,055,699 raw rows; 1,023,541 usable rows; 452 conflicting duplicate groups out of 31,706 duplicate groups (1.4256%); no parse failures; quote dates 2022-11-01 through 2026-10-14.
- Coverage across the 980 test dates ranged from 83.27% for ATM/ATM (C0_P0) down to 16.94% for C3_P-3. Only C0_P0 cleared the 80% coverage gate. The conflict rate exceeded the 1% gate. Overall confirmatory gate failed; all candidate ranking is exploratory.
- At primary costs (50 bps adverse slippage per premium side and ₹10 per order), all 32 model-filtered candidate × horizon means were negative, with 95% block-bootstrap interval upper bounds below zero. Examples: ATM/ATM horizon 5 mean −₹315.02 per eligible date (95% CI −₹406.69 to −₹232.69; 223 alert trades); ATM/ATM horizon 20 mean −₹330.45 (95% CI −₹416.51 to −₹244.30; 259 alert trades). Across the full grid, chronological half means were negative in both halves for all model-filtered cells. Higher slippage further worsened outcomes. These are exploratory descriptive outcomes because the data gate failed.
- Defect found in run #4 artifact: all 32 primary raw/Holm p-values were blank/NaN despite nonempty ledgers. Do not treat multiplicity-adjusted inference as complete. Developer added an explicit null-centered circular block-bootstrap p-value implementation in commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9; [corrective rerun #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress. No parameter search is being expanded; this is a bounded inference correction.
- Additional scope limitation: the frozen plan calls for a common-date sensitivity, but run #4 artifact does not contain one. Do not claim cross-candidate superiority; record this as not completed under the failed quality gate.
- Decision: **NO-GO / no strike candidate approved**. The study is non-confirmatory due conflict rate and coverage failures, all measured primary model-filtered means are negative, and the p-value output defect requires the single corrective rerun. No paper or live deployment.


### Latest status

Corrective [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress on commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9 to fix missing primary p-values. The run #4 result remains exploratory and no strategy is approved.


## Uploaded-PDF method audit — expanded comparison initiated

On 2026-10-14, all 13 uploaded PDFs were materialized and text-extracted for method inventory. The bounded forecasting-model comparison is running on [research/pdf-method-audit](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/pdf-method-audit). See [PDF method audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-method-audit/research/PDF_METHOD_AUDIT.md) for source-by-source methods, implemented candidates, scope exclusions, and data-dependent blockers.

- Expanded the classical registry to include Linear Regression, Lasso, SGD, KNN, Decision Tree, Gradient Boosting and AdaBoost in addition to the existing baselines, SVR, forests, MLP and optional XGBoost/LightGBM/CatBoost.
- Expanded compact CPU sequence candidates to LSTM, GRU, vanilla RNN, CNN, TCN, Transformer and four hybrids (LSTM+GRU, CNN+RNN, CNN+TCN, LSTM+TCN). These remain **pending empirical validation** until the workflow completes and artifacts are checked.
- BERT/news sentiment, fuzzy neural networks, Deep Belief Networks, wavelet preprocessing, Granger screening, and backward-elimination variants are explicitly not yet validated; some require point-in-time data or additional implementation. The three options-strategy PDFs remain outside the prediction-only scope.
- The run is a bounded screening comparison, not an exhaustive recreation of every paper's private dataset, preprocessing, or hyperparameter search. No method will be called tested without completed out-of-sample evidence.


## NIFTY prediction research — final status (2026-10-14)

The bounded prediction-only study completed on research branch `research/pdf-audit-developer` and received independent tester disposition **PASS WITH SCOPE LIMITATIONS** on `research/pdf-audit-tester-final`.

- [Final workflow #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792) — success; artifact SHA-256 `14c9d6fc1bcb0f00ff28e708cb10a6cab9b378e5e60ff31f6e66aaa5e977172b`.
- [Final research results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/PDF_METHOD_AUDIT_RESULTS.md)
- [Scientific manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/MANUSCRIPT.md)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/PHASE_STATUS.md)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/ERROR_LOG.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md)

Final artifact: 471,735 out-of-sample predictions; zero missing target dates; target-date defect resolved. Conclusion: no robust return/direction winner was established. One-session global XGBoost volatility QLIKE improvement survives the configured Holm correction; other volatility findings are metric-specific and volatility-expansion results remain exploratory. Twenty weekend-dated observations, global-market close-time alignment, and missing/unverified options/PCR, FII/DII, breadth, news and corporate-action inputs remain limitations. This is prediction-only research; no trading strategy is approved.


## OPT-BUY-2.0 strike-selection grid — final status (2026-10-14)

**Disposition: NO-GO for all tested candidates.** Frozen workflow [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) succeeded; artifact SHA-256 `e727095479b645703252832956a99a2924a5b5f68c507d68ec38b66ec9bd61e5`.

- [Strike-grid results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/option-strike-selection/RESULTS.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-independent-tester-final/research/option-strike-selection/TESTER_REPORT.md)
- [Developer error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/ERROR_LOG.md)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/PHASE_STATUS.md)

At ₹10/order and 50 bps adverse slippage per premium side, all 32 model-filtered strike-pair × horizon cells have negative mean net P&L and 95% intervals entirely below zero; both chronological halves are negative. Mean daily net P&L ranges from −₹316.87 to −₹622.96 per eligible-date slot. Quote conflict rate is 1.4154% (frozen ceiling 1%), and only ATM/ATM clears 80% coverage. The artifact's 32 primary p-value rows are blank with zero observations; no multiplicity-adjusted significance claims are valid. Independent tester disposition: FAIL / NO-GO. Do not paper-trade or live-trade these candidates; do not relax gates or extend this grid. The original prediction-only study remains closed, and the OPT-BUY-1.0 result remains unchanged.


## OPT-BUY-3.0 — entry/exit research (in progress)

The user shifted the follow-on work from prediction to NIFTY 50 long-option entry/exit testing. Prior OPT-BUY-1.0 and OPT-BUY-2.0 no-go conclusions remain unchanged.

- [Frozen protocol and phases](research/OPTION_ENTRY_EXIT_PLAN.md)
- [Research questions](research/OPTION_ENTRY_EXIT_QUESTIONS.md)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-entry-exit-developer)
- [Implementation](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/entry_exit_backtest.py)
- [Regression tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/test_entry_exit.py)
- [Workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/.github/workflows/option-entry-exit.yml)

The first executable is only a partial time-based CALL/PUT screen with fixed-duration/EOD exits. It does not yet implement the entire registered random, rule-based, premium-barrier or trailing-stop catalogue. No empirical result or strategy is approved until the workflow output and cost formulas are independently checked. The existing 1% duplicate-conflict and 80% coverage gates remain fixed.


## OPT-BUY-3.0 — Entry/exit research (active)

The user has paused prediction research and requested a bounded NIFTY 50 long-option buying study, from random/control entries to targeted entries and varied exits. The user explicitly rejected independent reviews; **no separate tester role, tester branch, or tester-report gate will be created**. Automated tests, data checks, cost calculations, statistical corrections and robustness checks remain mandatory.

- [OPT-BUY-3.0 protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/OPTION_ENTRY_EXIT_PLAN.md)
- [Entry/exit implementation (partial)](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/entry_exit_backtest.py)
- [Entry/exit regression tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/test_entry_exit.py)
- [Automated workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/.github/workflows/option-entry-exit.yml)
- [Current entry/exit results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/RESULTS.md)

**Current limitation:** the committed screen only covers fixed-time CALL/PUT entries and fixed holding/EOD exits; it does not yet implement the full registered entry/exit catalogue. Current branch results say BLOCKED_NO_VALID_QUOTES; no strategy result or approval is claimed. Research continues only through the predefined finite phases, and the existing failed gates from OPT-BUY-1.0/2.0 remain unchanged.


### OPT-BUY-3.0 execution update (2026-10-15)

Actions run [#3](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38620992395) completed technically and 16 tests passed, but quote acquisition yielded zero usable rows and zero candidates. A stale-manifest skip and a single-leg cost-helper mismatch were identified. Workflow/cache retry, single-leg cost accounting, expanded entries/exits, sensitivity scenarios and regression tests have been committed on the active research branch; runs [#4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621390693) and [#5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621455619) were triggered and are pending verification. No strategy conclusion is available yet.


**Data acquisition correction:** [Run #6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621480232) passed tests but had no daily NIFTY cache, so the rolling-options manifest planned zero requests and no empirical result was possible. The workflow now acquires daily data before option history when the cache is missing. [Run #7](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621701520) is pending; do not interpret the earlier blocked output as strategy performance.


### OPT-BUY-4.0 — 1,000+ unique naked-option strategy algorithms (2026-10-15)

The new study explicitly distinguishes **unique decision algorithms** from execution configurations. Strike, exit, holding-period, and cost variants do not increase the strategy count. The development branch now contains a deterministic catalogue generator, signature-based duplicate audit, registry tests, and an Actions workflow. The catalogue audit is a prerequisite only; it does not establish trading performance. Empirical option testing remains pending until the strategy catalogue is audited and usable point-in-time option data passes quality gates.

- [Research protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/OPTION_BUYING_1000_PLAN.md)
- [Research questions](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/OPTION_BUYING_1000_QUESTIONS.md)
- [Unique-strategy catalogue generator](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/option-buying-1000/strategy_catalogue.py)
- [Registry integrity tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/option-buying-1000/test_strategy_catalogue.py)
- [Automated catalogue workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/.github/workflows/option-buying-1000.yml)

**Status:** implementation is underway; no new backtest results or profitable strategy are claimed. The next gates are catalogue generation/deduplication, data audit, causal backtest implementation, cost accounting, chronological holdout, multiplicity correction, and manuscript closure.


## Fresh prediction continuation audit — 2026-10-15

A continuation audit was added at [research/FRESH_PREDICTION_CONTINUATION_AUDIT.md](research/FRESH_PREDICTION_CONTINUATION_AUDIT.md). The existing bounded prediction research and expanded model workflow are already recorded as completed, but the tester branch report currently available still reports run #60 as FAIL FOR FINAL SCIENTIFIC SIGN-OFF, while this README refers to run #62 and a pass. That evidence mismatch is now logged and must be reconciled before claiming final scientific sign-off. No strategy development is included in this prediction-only continuation.


### Run #62 independent artifact review — 2026-10-15

The independent tester has now inspected [run #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792). Target-date integrity and core MAE/RMSE/Holm arithmetic pass: 471,735 prediction rows have non-null target dates and all recorded targets align with their 1/5/20-session horizons. **Final scientific sign-off remains withheld** because some volatility QLIKE outputs are pathological (including elastic-net at horizon 5) and full HAC/block-bootstrap inference has not been independently reproduced. See the [current tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md), [ERR-019](research/ERROR_LOG.md), and [phase status](research/PHASE_STATUS.md). Only a bounded defect correction is warranted; no model-catalogue expansion or strategy development is authorized by the prediction-only scope.


### Final independent audit — run #62 (2026-10-15)

The tester has completed direct artifact review and reports **PASS WITH SCOPE LIMITATIONS**: [run #62 tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md). All 471,735 exported prediction rows have non-null target dates with offsets matching their 1/5/20-session horizons. MAE/RMSE, all 485 HAC p-values and block-bootstrap intervals, Holm corrections, and all 102 volatility QLIKE rows were independently reproduced within numerical precision. Extreme QLIKE values for some models are a large penalty for near-floor forecasts, not a confirmed calculation defect. The conclusion remains **no robust return/direction winner established**; a narrow one-session global XGBoost volatility QLIKE improvement is metric-specific, not a trading signal. Weekend-date verification and missing options/PCR, FII/DII, breadth, point-in-time news/corporate-action inputs and strict global timing remain limitations. The bounded NIFTY prediction model screen is closed; do not expand the catalogue or infer trading profitability.


## Volatility-regime weekly options hypothesis — VOL-REGIME-OPT-1.0 (2026-10-15)

A new, separate validation study was opened after user approval to test: buy an ATM NIFTY weekly straddle in a predicted high-volatility regime, and sell a weekly OTM strangle with each leg near absolute delta 0.07 in a predicted low-volatility regime. This is a hypothesis, not an approved strategy. The prior prediction-only study and prior monthly/intraday option tests remain closed and unchanged.

- [Frozen protocol and nine-phase plan](research/VOL_REGIME_OPTIONS_PLAN.md)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-developer)
- [Source-gate workflow](.github/workflows/vol-regime-options.yml)
- [Source probe](research/vol-regime-options/source_probe.py)
- [Source audit results](reports/vol_regime_options/source_audit.json) (created by Actions when the source probe completes)

Primary signal is the 5-session technical volatility-expansion classifier; the 20-session signal is secondary only. The protocol explicitly requires weekly-expiry and exact-contract validation, historical expiry/lot-size provenance, ≥80% quote coverage, ≤1% conflicting duplicate groups, realistic Paytm Money/statutory charges and slippage stress, risk/tail metrics, and independent tester approval. If weekly history or contract identity cannot be verified, the study stops as blocked/inconclusive. No live trading or deployment is authorized.


**Source-gate checkpoint (2026-10-15):** the first probe [run #38676211935](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676211935) exposed a workflow cache configuration issue, which was fixed. The corrected run confirmed the monthly schema control but Dhan rejected WEEK / expiryCode=0 with “expiryCode is required”. A single bounded diagnostic now tests WEEK codes 0, 1 and 2; weekly availability and expiry mapping are still unverified. No strategy results are claimed.

### VOL-REGIME-OPT-1.0 checkpoint — 2026-10-15

**Status: BLOCKED at expiry mapping / exact-contract identity; no P&L run.** Saved Dhan evidence shows schema responses for candidate weekly expiry codes 1 and 2 in a short sample, but does not establish actual expiry dates or same-contract entry/exit continuity. The saved audit predates the code-3 probe edit. The fallback dataset audit was not found and its script flags license review as required. The frozen hypothesis remains unchanged. No strategy is approved. See `research/PHASE_STATUS.md`, `research/ERROR_LOG.md`, and the source-gate disposition and independent tester report on the research branches.


## VOL-REGIME-OPT-1.0 latest source-gate checkpoint — 2026-10-15

The latest bounded Dhan probe completed its weekly schema requests in [workflow run #10](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667): candidate WEEK codes 1, 2 and 3 returned structurally valid CALL/PUT arrays in the five-day 2025-01-06 to 2025-01-10 sample (code 3 returned 357 CALL rows and 349 PUT rows). WEEK code 0 still fails. The workflow was ultimately marked failed because the runner received a shutdown signal during the Hugging Face fallback probe; the audit and later steps were skipped by that run, so the completed Dhan result has now been persisted separately. The HF fallback remains unverified.

**Decision remains BLOCKED:** schema success does not identify the actual expiry dates represented by each code or prove same-strike/same-expiry entry-to-exit continuity. No P&L, statistical strategy comparison, or profitability claim is allowed. The independent tester's report is at [tester branch](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-tester/research/vol-regime-options/TESTER_REPORT.md); see the [developer source-gate disposition](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/SOURCE_GATE_DISPOSITION.md) and [sanitized audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/source_audit.json).

**Developer instruction:** do not proceed to P&L unless a verifiable source establishes expiry-code/date mapping and fixed-contract continuity. **Tester instruction:** independently check the persisted code-3 evidence and confirm the blocked disposition; do not infer profitability or loss from this data gate.

Feasibility manuscript for the closed weekly-options follow-on: [VOL-REGIME-OPT-1.0 manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/research/vol-regime-options/MANUSCRIPT.md). Independent source-gate disposition: [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-tester/research/vol-regime-options/TESTER_REPORT.md).


## Option-buying continuation — 2026-10-16

User requested continued bounded research toward the best evidence-supported option-buying strategy. The prior NIFTY prediction study and OPT-BUY-1.0/2.0 no-go decisions remain unchanged. A continuation branch and finite protocol were created: [VOL_REGIME_OPTIONS_CONTINUATION.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-continuation/research/VOL_REGIME_OPTIONS_CONTINUATION.md). The current weekly-regime hypothesis remains **BLOCKED at expiry-code/date mapping and exact-contract continuity** until a verified source establishes both. Short-window Dhan schema success is not evidence of valid historical weekly contracts or profitability. Frozen data gates remain >=80% coverage and <=1% conflicting duplicate groups; costs, taxes, slippage, chronological holdout, risk metrics and multiplicity correction are mandatory. No strategy is approved and no P&L is claimed.


### Source audit retry — 2026-10-16

The failed source-audit job has been retried as [run #38676451667, attempt 2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667). The last status check showed it in progress. This is only an acquisition/metadata retry: until the job finishes and the saved artifacts are checked, no Hugging Face data availability, license clearance, coverage, or strategy P&L is claimed. Expiry mapping and exact-contract continuity remain the blocking gates.


### Reusing the existing NIFTY options archive — 2026-10-16

Repository inspection found that [`vishnuvcr/Nifty`](https://github.com/vishnuvcr/Nifty) already uses the Hugging Face dataset [`thetrademarkk/india-index-options-1m`](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m), caching `options/NIFTY/*.parquet` and index bars for expiry-exit analysis. Its dataset card lists minute OHLCV/OI, explicit expiry/strike/option-type fields, and a **CC-BY-NC-4.0** license; this is suitable only for non-commercial research with attribution and not for commercial redistribution. A new cached, sanitized source-audit workflow was added on [the continuation branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-continuation); [run #38807375042](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38807375042) was in progress at the last check. No data-quality pass or P&L is claimed until its report is inspected and sample contracts are reconciled against official NSE evidence. The dataset contains OHLC bars, not executable bid/ask quotes.


The free-source audit also records official NSE expiry-rule changes across 2025; see the [continuation source audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-continuation/research/VOL_REGIME_OPTIONS_FREE_SOURCE_AUDIT.md). These changes mean the research must use dated contract-file evidence rather than a weekday-only expiry heuristic. The HF audit run's download step completed, but its data-quality step remained in progress at the latest check; all strategy/P&L gates remain closed pending its report and official contract reconciliation.


## Latest NIFTY prediction rerun — 2026-10-22

- [Workflow #39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966) completed successfully. Artifact SHA-256: `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`.
- [Sanitized aggregate run summary](reports/nifty_prediction_run_39699761966_summary.json) · [research results](research/RESULTS.md) · [structured manuscript](research/MANUSCRIPT.md) · [phase status](research/PHASE_STATUS.md).
- Output: 647 metric rows, 299 OOS candidate comparisons, 296 CV-pass rows, 52 compute-budget-blocked rows.
- No robust selected return/direction edge was established. One selected global ExtraTrees model improved the one-session volatility-proxy QLIKE loss; Holm p=4.26e-7 across all 299 candidate comparisons. This requires independent-period replication and is not a trading signal.
- Options research remains **BLOCKED_NO_VERIFIED_CONTRACT_DATA**. No options P&L, trading recommendation, or live deployment is authorized.


## QE-NOB-1.0 — fresh QuantEvolve-inspired naked option buying (2026-10-22)

**Decision: DATA-LIMITED / NO strategy approved.** [Workflow #39712854501](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501) completed 600 candidates across 9 generations, but 0 passed the statistical gate and 0 passed the execution/promotion gate. The run acquired 92,510 underlying rows and 2,588,918 option rows from 2021-10-25 through 2026-10-21. Data quality failed because 453 of 471 duplicate groups conflicted; historical executable bid/ask/depth and exact expiry/lot-size mapping remain unverified. The strongest validation-selected opening-gap candidate's OOS mean daily net was ₹10.68 with a 95% block-bootstrap interval of -₹188.62 to ₹237.43; Holm-adjusted p=1.0, and stressed costs turned its mean daily net negative. These results do not establish profitability.

- [Fresh study branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v1-developer) · [Results report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/RESULTS.md) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/ERROR_LOG.md) · [Workflow artifact and logs](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501)
- User explicitly declined a tester; this is a developer-led analysis with automated unit checks, not an independently audited result. The workflow's final repository commit failed on a documentation rebase conflict and is being corrected; the run artifact uploaded successfully.

- [Structured research manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/MANUSCRIPT.md) · [Workflow correction](https://github.com/vishnuvcr/Naked-Options-v2/commit/4191d5a0cbbbd703867d5b0f5e7474d8b13f825e)


## QE-NOB-1.0 latest status — 2026-10-22

The corrected duplicate-key diagnostic is valid (0 duplicate groups; 2,600,975 option rows; 99.772% timestamp coverage and 100% row-grid coverage), but the previously reported P&L is superseded: a lot-size proxy bug used 25 units across all dates before 2024-11-20. The source now uses a sourced, expiry-family/date-based NIFTY proxy (WEEK1 vs MONTH1), adding the official 2021 75→50, 2024 50→25, phased 25→75, and 2025/26 75→65 revisions. Revised metrics are pending the corrected bounded workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025).

The study proceeds with available rolling option OHLC, modeled adverse slippage and a disclosed fee model; missing bid/ask/depth does not stop statistical analysis. It does prevent a claim of executable fills. No strategy is approved. [Research plan](research/quant-evolve-nob/RESEARCH_PLAN.md) · [Results](research/quant-evolve-nob/RESULTS.md) · [Phase status](research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](research/quant-evolve-nob/ERROR_LOG.md) · [Manuscript](research/quant-evolve-nob/MANUSCRIPT.md) · [Activity log](research/quant-evolve-nob/INTERACTION_LOG.md)

User explicitly declined an independent tester; no tester branch/report is awaited.

## QE-NOB-1.0 final corrected result — 2026-10-22

**Final disposition: NO_STATISTICAL_CANDIDATE / NO-GO for strategy approval.** Corrected full workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) completed successfully. It evaluated 600 unique candidates over 4 islands and 9 generations using 1,241 sessions (2021-10-25 to 2026-10-21), 92,510 underlying rows and 2,600,975 rolling option rows. All 1,708 acquisition requests were cache hits, zero acquisition failures were recorded, and pre-run/post-run automated tests passed. Zero of 600 candidates passed the statistical gate; zero passed the execution/promotion gate. Candidate 86's corrected OOS mean daily net was about ₹6.14, with a 95% block-bootstrap lower bound about −₹195.69 and Holm p=1.0. The OHLC quality gate passed, but historical bid/ask/depth and exact exchange contract identity remain unverified, so executable profitability is not established.

- [Final results](research/quant-evolve-nob/RESULTS.md) · [Phase status](research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](research/quant-evolve-nob/ERROR_LOG.md) · [Corrected manuscript](research/quant-evolve-nob/MANUSCRIPT.md) · [Dated lot-size reprice audit](research/quant-evolve-nob/LOT_SIZE_REPRICE_AUDIT.md) · [Activity log](research/quant-evolve-nob/INTERACTION_LOG.md)
- [Sanitized run report](reports/quant_evolve_nob_v1/RESULTS.md) · [Run summary JSON](reports/quant_evolve_nob_v1/run_summary.json) · [Workflow artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025)

The frozen-ledger reprice audit is a separate sensitivity check, not the final evolutionary run. No strategy is approved. User explicitly declined independent testing; no tester branch/report is claimed. The bounded study is closed; do not repeat unbounded search without materially better contract/execution data.


## Follow-on: QE-NOB-2.0 open structural strategy discovery

QE-NOB-1.0 is closed **NO-GO** for its tested restricted grammar. The follow-on protocol explicitly addresses the limitation that the earlier search mainly combined predefined signal families and fixed-time exits, rather than evolving structurally distinct entry/exit programs.

- [QE-NOB-2.0 developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v2-discovery-developer)
- [Open strategy discovery plan](research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md)
- [Phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Feature/source feasibility audit](research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md)
- [Activity log](research/quant-evolve-nob/INTERACTION_LOG_V2.md)

**Current status:** Phase 1 protocol amendment complete; Phase 2 data/feature feasibility is pending runtime coverage checks. The plan caps the new study at 1,500 unique structurally distinct candidates and 20 generations, with novelty-aware multi-objective search, evolvable exit state machines, frozen chronological OOS, Holm correction, block bootstrap and after-cost stress tests. The budget is fixed; this is not an endless search. No new strategy has yet been implemented, run, or shown profitable. No tester branch/report will be created, per the user's explicit instruction.


### QE-NOB-2.0 implementation checkpoint — 2026-10-22

Phase 1 protocol and static Phase 2 feasibility audit are documented. A typed structural grammar, novelty metric, mutation/crossover and regression tests are committed. Automated grammar CI is configured but its successful result has not yet been verified; the grammar is not integrated with the backtester and no new strategy results exist.

- [Feature feasibility](research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md)
- [Grammar implementation](research/quant-evolve-nob/strategy_grammar_v2.py)
- [Grammar tests](research/quant-evolve-nob/test_strategy_grammar_v2.py)
- [Implementation error log](research/quant-evolve-nob/ERROR_LOG_V2.md)


### QE-NOB-2.0 checkpoint — feature audit tooling added

A local-cache audit utility and tests are now committed, along with a second automatic/manual GitHub Actions test workflow. The audit reports schema fields, null counts, timestamp ranges and hashes, while explicitly refusing to claim exact contract identity or historical bid/ask/depth.

- [Feature audit utility](research/quant-evolve-nob/feature_audit_v2.py)
- [Feature audit tests](research/quant-evolve-nob/test_feature_audit_v2.py)
- [Feature audit workflow](.github/workflows/qe-nob-v2-feature-audit-tests.yml)
- [Updated phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Updated error log](research/quant-evolve-nob/ERROR_LOG_V2.md)

**Status:** workflows are configured but their results have not been verified; the cache audit has not been run on the research cache. Simulator integration and discovery remain pending. No strategy result is claimed.


### QE-NOB-2.0 — bounded structural candidate generator added

The candidate proposal generator now creates typed, structurally distinct strategy candidates using deterministic mutations/crossover, parent lineage and novelty-based selection. Hard limits are 1,500 candidates and 20 generations. It deliberately does not calculate fitness or P&L until a validated simulator is integrated.

- [Candidate generator](research/quant-evolve-nob/evolve_candidates_v2.py)
- [Generator tests](research/quant-evolve-nob/test_evolve_candidates_v2.py)
- [Generator test workflow](.github/workflows/qe-nob-v2-candidate-generator-tests.yml)
- [Updated phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Updated error log](research/quant-evolve-nob/ERROR_LOG_V2.md)

Automated test results have not been verified yet. This is a candidate-generation component, not evidence of a profitable strategy.


### QE-NOB-2.0 — signal evaluator checkpoint

A leakage-aware predicate evaluator now converts strategy conditions into signal timestamps and maps entry to the next actual market bar. A sparse-signal timing defect in the first draft was caught, corrected and recorded in the error log. Regression tests and a manual/automatic workflow are committed; CI is not yet verified.

- [Signal evaluator](research/quant-evolve-nob/signal_evaluator_v2.py)
- [Signal evaluator tests](research/quant-evolve-nob/test_signal_evaluator_v2.py)
- [Signal evaluator workflow](.github/workflows/qe-nob-v2-signal-evaluator-tests.yml)
- [Updated error log](research/quant-evolve-nob/ERROR_LOG_V2.md)

This component does not simulate option fills, transaction costs or P&L. The study must not progress to profitability conclusions until the option simulator and cost fixtures are implemented and tested.


### QE-NOB-2.0 — OHLC option simulator added

The research branch now includes an indicative long-option OHLC simulator with next-bar entries, same-strike exits, one-position-at-a-time enforcement per candidate, dated lot-size proxies, modeled fees and slippage. The execution gate remains hard-coded **FAIL** because rolling OHLC does not prove exact contract identity or executable quotes.

- [Option simulator](research/quant-evolve-nob/option_simulator_v2.py)
- [Simulator tests](research/quant-evolve-nob/test_option_simulator_v2.py)
- [Simulator test workflow](.github/workflows/qe-nob-v2-option-simulator-tests.yml)
- [Updated phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Error log](research/quant-evolve-nob/ERROR_LOG_V2.md)

CI results are not yet verified. The simulator has not been run against the historical cache; no strategy profitability is claimed.

### QE-NOB-2.0 implementation and CI checkpoint — 2026-10-22

**Status: software regression checks passing; empirical discovery still blocked pending Phase 2 runtime cache/source acquisition. No new strategy result is claimed.**

- [Bounded open structural discovery plan](research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md) · [Phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md) · [Feature/source feasibility](research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md) · [Error log](research/quant-evolve-nob/ERROR_LOG_V2.md) · [Activity log](research/quant-evolve-nob/INTERACTION_LOG_V2.md)
- Implemented typed predicate validation, deterministic structural mutation/crossover, and a candidate generator capped at 1,500 unique candidates / 20 generations. Only implemented signal-entry and time/premium-stop/premium-target semantics are generated; candidate generator still does not calculate fitness or P&L.
- Automated checks passed: [grammar + feature audit #39802894371](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802894371) (15 tests); [standalone feature audit #39802894311](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802894311); [signal evaluator #39801804759](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801804759); [option simulator #39801813009](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801813009); [candidate generator #39802753682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802753682).
- The option simulator includes cost/slippage assumptions and conservative premium stop/target handling, but its execution gate intentionally remains FAIL because rolling OHLC does not confirm exact exchange contract identity, historical bid/ask/depth or actual broker fills.
- Initial runtime audit [#39803204747](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803204747) returned `BLOCKED_NO_LOCAL_CACHE` (zero files). This does not prove Dhan or any free source is unavailable; the sibling branch's Actions cache was not present in the v2 runner.
- A bounded cache-first/source-acquisition-only workflow was added: [.github/workflows/qe-nob-v2-data-audit.yml](.github/workflows/qe-nob-v2-data-audit.yml). Run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) was automatically triggered; inspect its sanitized artifact before changing Phase 2 status. Raw market payloads are kept in the runner cache and are not uploaded as artifacts.
- QE-NOB-1.0 remains NO-GO and unchanged. No QE-NOB-2.0 candidate has yet been backtested for fitness or shown profitable; no tester branch/report is created, per the user's explicit instruction.


### QE-NOB-2.0 acquisition result — 2026-10-23

**Status: BLOCKED at data acquisition; no new candidate or profitability result.** Eligible weekly-only workflow [#39838508682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838508682) passed pre-acquisition regression gates but failed the source gate. Its [fresh sanitized artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838508682/artifacts/12451299405) reports Dhan HTTP 401 DH-901 (access token invalid or expired), incomplete weekly option history, and no verified 5-minute underlying series. The final cache audit counted 745 parseable JSON files, including 744 option-folder files and one underlying probe; parseability does not establish historical coverage. Exact contract identity and historical bid/ask/depth remain unverified. The cache was preserved and empirical discovery was skipped.

- [Phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md) · [Error log](research/quant-evolve-nob/ERROR_LOG_V2.md) · [Activity log](research/quant-evolve-nob/INTERACTION_LOG_V2.md) · [Source catalogue](research/quant-evolve-nob/SOURCE_CATALOG_V2.md)

**Next gate:** renew the Dhan token in GitHub Actions secrets or verify and integrate a legally usable alternate source with explicit expiry/contract mapping and historical underlying bars. Do not repeat acquisition with the same invalid credential. Phase 5 remains blocked; Phases 6–7 are not started; execution remains FAIL.


### Dhan token renewal automation — 2026-10-23

The QE-NOB-2.0 acquisition workflow now has a TOTP-based token bootstrap using Dhan's documented token-generation endpoint. Before source acquisition, it generates a fresh 24-hour access token, validates it with the Dhan profile endpoint, and places it only in the current GitHub Actions job environment. It does **not** print or commit the token.

**Required one-time setup:** enable TOTP in Dhan Web → My Profile → Access DhanHQ APIs, then add these repository Actions secrets: `DHAN_CLIENT_ID`, `DHAN_PIN`, and `DHAN_TOTP_SECRET` (the authenticator's base32 secret). Do not paste them into chat or commit them. The existing `DHAN_ACCESS_TOKEN` is not sufficient for reliable unattended renewal after it expires.

Implementation: [token helper](research/quant-evolve-nob/dhan_auth.py) · [RFC regression tests](research/quant-evolve-nob/test_dhan_auth.py) · [acquisition workflow](.github/workflows/qe-nob-v2-data-audit.yml) · [phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md) · [error log](research/quant-evolve-nob/ERROR_LOG_V2.md).

**Verification state:** implementation committed; live authentication is pending the three secrets and a successful workflow run. Research Phase 2 remains blocked until token/profile validation and the historical data acquisition/cache gate pass.**Candidate rules, source audit and artifact integrity (2026-10-23):** [Exact finalist rules](research/quant-evolve-nob/EXACT_FINALIST_RULES.md) records all 12 statistical-gate candidates. [Simulator/feature audit](research/quant-evolve-nob/SIMULATOR_FEATURE_AUDIT.md) documents signed opening-gap semantics, point-in-time features and stop-first behavior. [Artifact integrity and decision](research/quant-evolve-nob/ARTIFACT_INTEGRITY_DECISION.md) confirms 1,185 unique archive signatures, 20/20 finalist signature joins, 200/200 cost-stress rows, 12/20 statistical-gate passes and 0/20 execution-gate passes. No paper/live approval; overall status remains DATA-LIMITED.

## Latest prediction audit — 2026-10-22

The prior workflow completed operationally, but its artifact contains Historical defect in run #39699761966: 798 multi-session forecasts had missing target dates due to partial forward windows. Corrective run #39704420478 completed with zero missing target dates. The pipeline is operationally corrected; scientific conclusions remain limited pending future-period replication and numerical stability checks.

- [Audit record](research/FRESH_PREDICTION_AUDIT_2026-10-22.md) · [Artifact audit utility](research/audits/audit_nifty_predictions.py) · [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-developer) · [Corrective workflow #39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478)
- Return/direction forecasts have no robust selected edge. The one-session ExtraTrees volatility-proxy result was numerically reproduced from the prior artifact, but remains a replication candidate and not a trading signal. Options P&L and strategy development remain blocked.

**Research version:** NIFTY-PRED-1.0  
**Scope:** Prediction only. No trading strategy design, optimization, or recommendation in this study.  
**Started:** 2026-10-14  
**Status:** Corrective workflow [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) completed; 277,633 prediction rows have zero missing target dates. Return/direction edge not established; volatility-proxy result requires untouched future replication. Developer-only process per user request; no tester gate. Artifact audit found 798 invalid missing-target-date rows in h5/h20 volatility and volatility-expansion outputs. Correction commit [e8133a5](https://github.com/vishnuvcr/Naked-Options-v2/commit/e8133a582cbe6c06ce46514f871d1393fc142f6f) is running through workflow [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478). No strategy is approved.

## Repository audit

The repository was empty at project start: no readable README, files, branches, commits, datasets, experiment logs, or workflows. This project therefore starts a new research record without overwriting prior repository work. Relevant prior literature available in the ChatGPT Project library is cited in `research/LITERATURE_REVIEW.md`; it is not treated as this project's validated experimental output.

## Research navigation

- [Research plan](research/RESEARCH_PLAN.md)
- [Research questions and hypotheses](research/RESEARCH_QUESTIONS.md)
- [Literature review](research/LITERATURE_REVIEW.md)
- [Data catalog](research/DATA_CATALOG.md)
- [Experiment log](research/EXPERIMENT_LOG.md)
- [Results](research/RESULTS.md)
- [Phase status and gates](research/PHASE_STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Independent tester report](research/TESTER_REPORT.md)
- [Scientific manuscript](research/MANUSCRIPT.md)
- [Reproducibility guide](research/REPRODUCIBILITY.md)
- [Execution policy and phase-branch rules](research/EXECUTION_POLICY.md)

## Phase branches

Historical checkpoint branches for completed setup phases and the active model branch are available: [Phase 1](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-1-audit), [Phase 2](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-2-literature), [Phase 3](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-3-data), [Phase 4](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-4-baselines), and [Phase 5](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-5-models). The resource-bounded execution branch is [research/phase-5-bounded](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-5-bounded). Future phase branches will be created only after their predecessor gate passes.

## Scientific integrity

No model will be declared best from training fit, shuffled validation, price-level R² alone, or a reused test set. Return, directional, volatility, and level targets will be evaluated separately with chronological walk-forward evaluation, simple benchmarks, uncertainty estimates, and multiplicity control. Results unavailable because of data, credentials, compute, or workflow restrictions will be marked **blocked/not run**, never imputed or fabricated.

## Current summary

### Active follow-on: VOL-REGIME-OPT-1.0

A separate weekly-options volatility-regime hypothesis is in protocol/source-gate work on [the developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-developer). A bounded Dhan probe has returned structurally valid weekly CALL/PUT arrays for candidate expiry codes 1 and 2 in a five-day January 2025 sample. Exact expiry mapping, stable contract identity, full coverage and P&L remain unverified. See the [frozen plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/research/VOL_REGIME_OPTIONS_PLAN.md) and [sanitized source audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/source_audit.json). No strategy is approved.

- **Original prediction study (NIFTY-PRED-1.0): CLOSED WITH SCOPE LIMITATIONS.** Its corrected canonical run is [#49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128); see [results](research/RESULTS.md), [phase status](research/PHASE_STATUS.md), and [scientific manuscript](research/MANUSCRIPT.md).
- **Follow-on option-buying validation (OPT-BUY-1.0): CLOSED — NO-GO for tested candidates; broader hypothesis inconclusive.** The completed [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) and independent review found strangle quote coverage of 69.18% (<80%), conflicting duplicate groups at 1.409% (>1%), and negative net daily P&L confidence intervals for all four candidates. No paper/live strategy is approved; details are in [the option-validation results](research/option-validation/RESULTS.md) and [tester report](research/option-validation/TESTER_REPORT.md).
- Latest validated NIFTY data: 4,906 Dhan daily rows from 2007-01-02 to 2026-10-21; SHA-256 `2a76714665754ec6371e92d8b9b56565606c0d1a4a2fc9cc9013291e233b2158` (the earlier 4,901-row run remains historical).
- Data gaps remain documented: historical options features, FII/DII, PCR, breadth, point-in-time constituents/corporate actions, and timestamped news were not comprehensively verified for the original prediction study. These gaps limit the scope of inference.
- Statistical integrity: the original study found no robust return/direction edge after multiple-testing correction. The option-buying follow-on did not demonstrate profitable net option P&L after modeled costs.
- Audit trail: [error log](research/ERROR_LOG.md), [experiment log](research/EXPERIMENT_LOG.md), [interaction log](research/INTERACTION_LOG.md), [frozen option validation plan](research/OPTION_BUYING_VALIDATION_PLAN.md), [independent tester](research/option-validation/TESTER_REPORT.md), and [developer disposition](research/option-validation/DEVELOPER_DISPOSITION.md).

The original prediction study and follow-on option-buying study are both closed for their stated protocols. Any further work should start a separately versioned research question and preregistered protocol rather than reopen failed gates or repeat parameter loops.


## Latest correction checkpoint — 2026-10-14

The independent audit found that forward-volatility targets near the sample tail could be calculated from partial future windows. The developer branch now requires all horizon returns to be present before assigning the 5-/20-session volatility target. Workflow [#48](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38532904979) stopped at a regression-test assertion (a scalar `.notna()` call), before feature construction or model fitting. That test was corrected to `pd.notna` in commit `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`; workflow [#49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) is the retest and corrected-run gate.

Until #49 completes, the run #45 model scores remain preliminary. No strategy or model is approved. Phase 5/7 remain open pending successful tests, corrected OOS predictions with complete target windows, and an independent tester report. See the [developer error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/developer-review/research/ERROR_LOG.md) and [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/developer-review/research/PHASE_STATUS.md).


## Corrected run #49 — 2026-10-14

The forward-volatility target defect has been fixed and regression-tested. [Workflow #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) completed successfully. Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`.

- [Results and evidence register](research/RESULTS.md)
- [Phase status and gate decisions](research/PHASE_STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Developer correction branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/developer-review)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md)

Preliminary results: no robust return/direction edge has been demonstrated; selected 5-/20-session global return models are worse than the zero-return baseline; volatility models do not pass adjusted QLIKE comparisons. Some volatility-expansion classifiers improve log loss, but are exploratory and not trading signals. The independent tester passed the bounded prediction-only study with scope limitations; Phase 2 literature depth and Phase 6 data/regime coverage remain partial and are documented. This is prediction research only: no options-chain strategy, transaction-cost/slippage simulation, or Paytm Money execution analysis has been completed.


## Independent review outcome — 2026-10-14

The independent tester has issued **PASS WITH SCOPE LIMITATIONS** for the bounded prediction-only research. See the [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md), [results register](research/RESULTS.md), and [phase gates](research/PHASE_STATUS.md).

Conclusion: no robust return/direction edge is demonstrated. Volatility-expansion results are exploratory, and one-session probabilities are poorly calibrated. No trading strategy is approved or tested. Historical option chains, FII/DII, PCR, breadth, timestamped news, transaction costs/slippage and Paytm Money execution remain outside the verified dataset and experiments.


**Closure status:** The nine-phase research is closed for the bounded prediction-only scope, with accepted limitations. The conclusion is that this tested model/data set did not establish a robust return/direction edge. No options strategy or live execution plan is approved.


The static research status page is published through the lightweight [Pages publish workflow](https://github.com/vishnuvcr/Naked-Options-v2/actions/workflows/publish-research-status.yml). The final option-buying plan, results, manuscript, figures and independent review are now in main; this README update triggers a fresh status-page deployment.


## Follow-on study: option-buying validation — OPT-BUY-1.0

The original nine-phase NIFTY-PRED-1.0 prediction-only study remains closed and unchanged. The separate test of next-session intraday monthly-option straddles/strangles is now closed for its frozen scope.

**Final disposition: NO-GO for the tested implementations; broader hypothesis INCONCLUSIVE because the data-quality gate failed.** Final workflow [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) completed successfully; 13 unit tests passed before and after analysis.

- [Frozen validation plan](research/OPTION_BUYING_VALIDATION_PLAN.md)
- [Results](research/option-validation/RESULTS.md)
- [Structured manuscript](research/option-validation/MANUSCRIPT.md)
- [Net P&L comparison chart](research/option-validation/figures/net_pnl_comparison.svg)
- [Slippage sensitivity chart](research/option-validation/figures/slippage_sensitivity.svg)
- [Primary comparisons CSV](reports/option_validation/primary_comparisons.csv)
- [Results summary JSON](reports/option_validation/results_summary.json)
- [Independent tester report](research/option-validation/TESTER_REPORT.md)
- [Developer disposition](research/option-validation/DEVELOPER_DISPOSITION.md)
- [Workflow run/artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-buying-developer)
- [Independent tester branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-buying-independent-tester)

At ₹10 brokerage/order and 50 bps adverse slippage per premium side, all four alert-filtered candidates had mean net daily P&L between −₹315.71 and −₹369.43 per one-lot-proxy eligible-day slot; all 95% intervals were negative. Positive paired differences versus always-buy (Holm-adjusted p=0.002) only show loss reduction relative to a worse baseline.

Frozen gates failed: strangle quote coverage 69.18% (minimum 80%) and conflicting duplicate groups 1.409% (maximum 1%). All candidates failed the 100-bps and both-half profitability gates. No paper-trading or live deployment is approved. Do not relax gates or continue optimization loops.

## OPT-BUY-2.0 — Strike-selection research (in progress)

- Protocol: [strike-selection plan](research/STRIKE_SELECTION_PLAN.md); implementation: [strike-grid code](research/option-strike-selection/strike_grid.py).
- Automated run #1 failed at the data stage: the existing 13 regression tests passed, but no usable historical option quote rows were loaded. This is a data blocker, not a profitability finding. [Run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551789841).
- Diagnostic-output fix and inference-family correction are being tested in [run #2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551939491) and [run #3](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552000337). No strike winner or strategy is approved.
- Separate review branches: [developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-strike-selection-developer) and [independent tester](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-strike-selection-independent-tester). The tester's current report is blocked pending usable quotes.




## OPT-BUY-2.0 run #4 — results and disposition (2026-10-14)

- [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) completed successfully at workflow level; 13 pre-analysis and 13 final regression tests passed, and sanitized artifact `option-strike-selection-38552144097` was uploaded (SHA-256 `7fae1922403e398f040ee8ca3a80f607e07e0d6569c98eb35b3ae0c6f168d285`).
- Data: 1,055,699 raw rows; 1,023,541 usable rows; 452 conflicting duplicate groups out of 31,706 duplicate groups (1.4256%); no parse failures; quote dates 2022-11-01 through 2026-10-14.
- Coverage across the 980 test dates ranged from 83.27% for ATM/ATM (C0_P0) down to 16.94% for C3_P-3. Only C0_P0 cleared the 80% coverage gate. The conflict rate exceeded the 1% gate. Overall confirmatory gate failed; all candidate ranking is exploratory.
- At primary costs (50 bps adverse slippage per premium side and ₹10 per order), all 32 model-filtered candidate × horizon means were negative, with 95% block-bootstrap interval upper bounds below zero. Examples: ATM/ATM horizon 5 mean −₹315.02 per eligible date (95% CI −₹406.69 to −₹232.69; 223 alert trades); ATM/ATM horizon 20 mean −₹330.45 (95% CI −₹416.51 to −₹244.30; 259 alert trades). Across the full grid, chronological half means were negative in both halves for all model-filtered cells. Higher slippage further worsened outcomes. These are exploratory descriptive outcomes because the data gate failed.
- Defect found in run #4 artifact: all 32 primary raw/Holm p-values were blank/NaN despite nonempty ledgers. Do not treat multiplicity-adjusted inference as complete. Developer added an explicit null-centered circular block-bootstrap p-value implementation in commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9; [corrective rerun #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress. No parameter search is being expanded; this is a bounded inference correction.
- Additional scope limitation: the frozen plan calls for a common-date sensitivity, but run #4 artifact does not contain one. Do not claim cross-candidate superiority; record this as not completed under the failed quality gate.
- Decision: **NO-GO / no strike candidate approved**. The study is non-confirmatory due conflict rate and coverage failures, all measured primary model-filtered means are negative, and the p-value output defect requires the single corrective rerun. No paper or live deployment.


### Latest status

Corrective [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress on commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9 to fix missing primary p-values. The run #4 result remains exploratory and no strategy is approved.


## Uploaded-PDF method audit — expanded comparison initiated

On 2026-10-14, all 13 uploaded PDFs were materialized and text-extracted for method inventory. The bounded forecasting-model comparison is running on [research/pdf-method-audit](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/pdf-method-audit). See [PDF method audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-method-audit/research/PDF_METHOD_AUDIT.md) for source-by-source methods, implemented candidates, scope exclusions, and data-dependent blockers.

- Expanded the classical registry to include Linear Regression, Lasso, SGD, KNN, Decision Tree, Gradient Boosting and AdaBoost in addition to the existing baselines, SVR, forests, MLP and optional XGBoost/LightGBM/CatBoost.
- Expanded compact CPU sequence candidates to LSTM, GRU, vanilla RNN, CNN, TCN, Transformer and four hybrids (LSTM+GRU, CNN+RNN, CNN+TCN, LSTM+TCN). These remain **pending empirical validation** until the workflow completes and artifacts are checked.
- BERT/news sentiment, fuzzy neural networks, Deep Belief Networks, wavelet preprocessing, Granger screening, and backward-elimination variants are explicitly not yet validated; some require point-in-time data or additional implementation. The three options-strategy PDFs remain outside the prediction-only scope.
- The run is a bounded screening comparison, not an exhaustive recreation of every paper's private dataset, preprocessing, or hyperparameter search. No method will be called tested without completed out-of-sample evidence.


## NIFTY prediction research — final status (2026-10-14)

The bounded prediction-only study completed on research branch `research/pdf-audit-developer` and received independent tester disposition **PASS WITH SCOPE LIMITATIONS** on `research/pdf-audit-tester-final`.

- [Final workflow #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792) — success; artifact SHA-256 `14c9d6fc1bcb0f00ff28e708cb10a6cab9b378e5e60ff31f6e66aaa5e977172b`.
- [Final research results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/PDF_METHOD_AUDIT_RESULTS.md)
- [Scientific manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/MANUSCRIPT.md)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/PHASE_STATUS.md)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/ERROR_LOG.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md)

Final artifact: 471,735 out-of-sample predictions; zero missing target dates; target-date defect resolved. Conclusion: no robust return/direction winner was established. One-session global XGBoost volatility QLIKE improvement survives the configured Holm correction; other volatility findings are metric-specific and volatility-expansion results remain exploratory. Twenty weekend-dated observations, global-market close-time alignment, and missing/unverified options/PCR, FII/DII, breadth, news and corporate-action inputs remain limitations. This is prediction-only research; no trading strategy is approved.


## OPT-BUY-2.0 strike-selection grid — final status (2026-10-14)

**Disposition: NO-GO for all tested candidates.** Frozen workflow [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) succeeded; artifact SHA-256 `e727095479b645703252832956a99a2924a5b5f68c507d68ec38b66ec9bd61e5`.

- [Strike-grid results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/option-strike-selection/RESULTS.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-independent-tester-final/research/option-strike-selection/TESTER_REPORT.md)
- [Developer error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/ERROR_LOG.md)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/PHASE_STATUS.md)

At ₹10/order and 50 bps adverse slippage per premium side, all 32 model-filtered strike-pair × horizon cells have negative mean net P&L and 95% intervals entirely below zero; both chronological halves are negative. Mean daily net P&L ranges from −₹316.87 to −₹622.96 per eligible-date slot. Quote conflict rate is 1.4154% (frozen ceiling 1%), and only ATM/ATM clears 80% coverage. The artifact's 32 primary p-value rows are blank with zero observations; no multiplicity-adjusted significance claims are valid. Independent tester disposition: FAIL / NO-GO. Do not paper-trade or live-trade these candidates; do not relax gates or extend this grid. The original prediction-only study remains closed, and the OPT-BUY-1.0 result remains unchanged.


## OPT-BUY-3.0 — entry/exit research (in progress)

The user shifted the follow-on work from prediction to NIFTY 50 long-option entry/exit testing. Prior OPT-BUY-1.0 and OPT-BUY-2.0 no-go conclusions remain unchanged.

- [Frozen protocol and phases](research/OPTION_ENTRY_EXIT_PLAN.md)
- [Research questions](research/OPTION_ENTRY_EXIT_QUESTIONS.md)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-entry-exit-developer)
- [Implementation](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/entry_exit_backtest.py)
- [Regression tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/test_entry_exit.py)
- [Workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/.github/workflows/option-entry-exit.yml)

The first executable is only a partial time-based CALL/PUT screen with fixed-duration/EOD exits. It does not yet implement the entire registered random, rule-based, premium-barrier or trailing-stop catalogue. No empirical result or strategy is approved until the workflow output and cost formulas are independently checked. The existing 1% duplicate-conflict and 80% coverage gates remain fixed.


## OPT-BUY-3.0 — Entry/exit research (active)

The user has paused prediction research and requested a bounded NIFTY 50 long-option buying study, from random/control entries to targeted entries and varied exits. The user explicitly rejected independent reviews; **no separate tester role, tester branch, or tester-report gate will be created**. Automated tests, data checks, cost calculations, statistical corrections and robustness checks remain mandatory.

- [OPT-BUY-3.0 protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/OPTION_ENTRY_EXIT_PLAN.md)
- [Entry/exit implementation (partial)](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/entry_exit_backtest.py)
- [Entry/exit regression tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/test_entry_exit.py)
- [Automated workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/.github/workflows/option-entry-exit.yml)
- [Current entry/exit results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/RESULTS.md)

**Current limitation:** the committed screen only covers fixed-time CALL/PUT entries and fixed holding/EOD exits; it does not yet implement the full registered entry/exit catalogue. Current branch results say BLOCKED_NO_VALID_QUOTES; no strategy result or approval is claimed. Research continues only through the predefined finite phases, and the existing failed gates from OPT-BUY-1.0/2.0 remain unchanged.


### OPT-BUY-3.0 execution update (2026-10-15)

Actions run [#3](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38620992395) completed technically and 16 tests passed, but quote acquisition yielded zero usable rows and zero candidates. A stale-manifest skip and a single-leg cost-helper mismatch were identified. Workflow/cache retry, single-leg cost accounting, expanded entries/exits, sensitivity scenarios and regression tests have been committed on the active research branch; runs [#4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621390693) and [#5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621455619) were triggered and are pending verification. No strategy conclusion is available yet.


**Data acquisition correction:** [Run #6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621480232) passed tests but had no daily NIFTY cache, so the rolling-options manifest planned zero requests and no empirical result was possible. The workflow now acquires daily data before option history when the cache is missing. [Run #7](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621701520) is pending; do not interpret the earlier blocked output as strategy performance.


### OPT-BUY-4.0 — 1,000+ unique naked-option strategy algorithms (2026-10-15)

The new study explicitly distinguishes **unique decision algorithms** from execution configurations. Strike, exit, holding-period, and cost variants do not increase the strategy count. The development branch now contains a deterministic catalogue generator, signature-based duplicate audit, registry tests, and an Actions workflow. The catalogue audit is a prerequisite only; it does not establish trading performance. Empirical option testing remains pending until the strategy catalogue is audited and usable point-in-time option data passes quality gates.

- [Research protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/OPTION_BUYING_1000_PLAN.md)
- [Research questions](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/OPTION_BUYING_1000_QUESTIONS.md)
- [Unique-strategy catalogue generator](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/option-buying-1000/strategy_catalogue.py)
- [Registry integrity tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/option-buying-1000/test_strategy_catalogue.py)
- [Automated catalogue workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/.github/workflows/option-buying-1000.yml)

**Status:** implementation is underway; no new backtest results or profitable strategy are claimed. The next gates are catalogue generation/deduplication, data audit, causal backtest implementation, cost accounting, chronological holdout, multiplicity correction, and manuscript closure.


## Fresh prediction continuation audit — 2026-10-15

A continuation audit was added at [research/FRESH_PREDICTION_CONTINUATION_AUDIT.md](research/FRESH_PREDICTION_CONTINUATION_AUDIT.md). The existing bounded prediction research and expanded model workflow are already recorded as completed, but the tester branch report currently available still reports run #60 as FAIL FOR FINAL SCIENTIFIC SIGN-OFF, while this README refers to run #62 and a pass. That evidence mismatch is now logged and must be reconciled before claiming final scientific sign-off. No strategy development is included in this prediction-only continuation.


### Run #62 independent artifact review — 2026-10-15

The independent tester has now inspected [run #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792). Target-date integrity and core MAE/RMSE/Holm arithmetic pass: 471,735 prediction rows have non-null target dates and all recorded targets align with their 1/5/20-session horizons. **Final scientific sign-off remains withheld** because some volatility QLIKE outputs are pathological (including elastic-net at horizon 5) and full HAC/block-bootstrap inference has not been independently reproduced. See the [current tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md), [ERR-019](research/ERROR_LOG.md), and [phase status](research/PHASE_STATUS.md). Only a bounded defect correction is warranted; no model-catalogue expansion or strategy development is authorized by the prediction-only scope.


### Final independent audit — run #62 (2026-10-15)

The tester has completed direct artifact review and reports **PASS WITH SCOPE LIMITATIONS**: [run #62 tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md). All 471,735 exported prediction rows have non-null target dates with offsets matching their 1/5/20-session horizons. MAE/RMSE, all 485 HAC p-values and block-bootstrap intervals, Holm corrections, and all 102 volatility QLIKE rows were independently reproduced within numerical precision. Extreme QLIKE values for some models are a large penalty for near-floor forecasts, not a confirmed calculation defect. The conclusion remains **no robust return/direction winner established**; a narrow one-session global XGBoost volatility QLIKE improvement is metric-specific, not a trading signal. Weekend-date verification and missing options/PCR, FII/DII, breadth, point-in-time news/corporate-action inputs and strict global timing remain limitations. The bounded NIFTY prediction model screen is closed; do not expand the catalogue or infer trading profitability.


## Volatility-regime weekly options hypothesis — VOL-REGIME-OPT-1.0 (2026-10-15)

A new, separate validation study was opened after user approval to test: buy an ATM NIFTY weekly straddle in a predicted high-volatility regime, and sell a weekly OTM strangle with each leg near absolute delta 0.07 in a predicted low-volatility regime. This is a hypothesis, not an approved strategy. The prior prediction-only study and prior monthly/intraday option tests remain closed and unchanged.

- [Frozen protocol and nine-phase plan](research/VOL_REGIME_OPTIONS_PLAN.md)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-developer)
- [Source-gate workflow](.github/workflows/vol-regime-options.yml)
- [Source probe](research/vol-regime-options/source_probe.py)
- [Source audit results](reports/vol_regime_options/source_audit.json) (created by Actions when the source probe completes)

Primary signal is the 5-session technical volatility-expansion classifier; the 20-session signal is secondary only. The protocol explicitly requires weekly-expiry and exact-contract validation, historical expiry/lot-size provenance, ≥80% quote coverage, ≤1% conflicting duplicate groups, realistic Paytm Money/statutory charges and slippage stress, risk/tail metrics, and independent tester approval. If weekly history or contract identity cannot be verified, the study stops as blocked/inconclusive. No live trading or deployment is authorized.


**Source-gate checkpoint (2026-10-15):** the first probe [run #38676211935](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676211935) exposed a workflow cache configuration issue, which was fixed. The corrected run confirmed the monthly schema control but Dhan rejected WEEK / expiryCode=0 with “expiryCode is required”. A single bounded diagnostic now tests WEEK codes 0, 1 and 2; weekly availability and expiry mapping are still unverified. No strategy results are claimed.

### VOL-REGIME-OPT-1.0 checkpoint — 2026-10-15

**Status: BLOCKED at expiry mapping / exact-contract identity; no P&L run.** Saved Dhan evidence shows schema responses for candidate weekly expiry codes 1 and 2 in a short sample, but does not establish actual expiry dates or same-contract entry/exit continuity. The saved audit predates the code-3 probe edit. The fallback dataset audit was not found and its script flags license review as required. The frozen hypothesis remains unchanged. No strategy is approved. See `research/PHASE_STATUS.md`, `research/ERROR_LOG.md`, and the source-gate disposition and independent tester report on the research branches.


## VOL-REGIME-OPT-1.0 latest source-gate checkpoint — 2026-10-15

The latest bounded Dhan probe completed its weekly schema requests in [workflow run #10](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667): candidate WEEK codes 1, 2 and 3 returned structurally valid CALL/PUT arrays in the five-day 2025-01-06 to 2025-01-10 sample (code 3 returned 357 CALL rows and 349 PUT rows). WEEK code 0 still fails. The workflow was ultimately marked failed because the runner received a shutdown signal during the Hugging Face fallback probe; the audit and later steps were skipped by that run, so the completed Dhan result has now been persisted separately. The HF fallback remains unverified.

**Decision remains BLOCKED:** schema success does not identify the actual expiry dates represented by each code or prove same-strike/same-expiry entry-to-exit continuity. No P&L, statistical strategy comparison, or profitability claim is allowed. The independent tester's report is at [tester branch](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-tester/research/vol-regime-options/TESTER_REPORT.md); see the [developer source-gate disposition](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/SOURCE_GATE_DISPOSITION.md) and [sanitized audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/source_audit.json).

**Developer instruction:** do not proceed to P&L unless a verifiable source establishes expiry-code/date mapping and fixed-contract continuity. **Tester instruction:** independently check the persisted code-3 evidence and confirm the blocked disposition; do not infer profitability or loss from this data gate.

Feasibility manuscript for the closed weekly-options follow-on: [VOL-REGIME-OPT-1.0 manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/research/vol-regime-options/MANUSCRIPT.md). Independent source-gate disposition: [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-tester/research/vol-regime-options/TESTER_REPORT.md).


## Option-buying continuation — 2026-10-16

User requested continued bounded research toward the best evidence-supported option-buying strategy. The prior NIFTY prediction study and OPT-BUY-1.0/2.0 no-go decisions remain unchanged. A continuation branch and finite protocol were created: [VOL_REGIME_OPTIONS_CONTINUATION.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-continuation/research/VOL_REGIME_OPTIONS_CONTINUATION.md). The current weekly-regime hypothesis remains **BLOCKED at expiry-code/date mapping and exact-contract continuity** until a verified source establishes both. Short-window Dhan schema success is not evidence of valid historical weekly contracts or profitability. Frozen data gates remain >=80% coverage and <=1% conflicting duplicate groups; costs, taxes, slippage, chronological holdout, risk metrics and multiplicity correction are mandatory. No strategy is approved and no P&L is claimed.


### Source audit retry — 2026-10-16

The failed source-audit job has been retried as [run #38676451667, attempt 2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667). The last status check showed it in progress. This is only an acquisition/metadata retry: until the job finishes and the saved artifacts are checked, no Hugging Face data availability, license clearance, coverage, or strategy P&L is claimed. Expiry mapping and exact-contract continuity remain the blocking gates.


### Reusing the existing NIFTY options archive — 2026-10-16

Repository inspection found that [`vishnuvcr/Nifty`](https://github.com/vishnuvcr/Nifty) already uses the Hugging Face dataset [`thetrademarkk/india-index-options-1m`](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m), caching `options/NIFTY/*.parquet` and index bars for expiry-exit analysis. Its dataset card lists minute OHLCV/OI, explicit expiry/strike/option-type fields, and a **CC-BY-NC-4.0** license; this is suitable only for non-commercial research with attribution and not for commercial redistribution. A new cached, sanitized source-audit workflow was added on [the continuation branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-continuation); [run #38807375042](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38807375042) was in progress at the last check. No data-quality pass or P&L is claimed until its report is inspected and sample contracts are reconciled against official NSE evidence. The dataset contains OHLC bars, not executable bid/ask quotes.


The free-source audit also records official NSE expiry-rule changes across 2025; see the [continuation source audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-continuation/research/VOL_REGIME_OPTIONS_FREE_SOURCE_AUDIT.md). These changes mean the research must use dated contract-file evidence rather than a weekday-only expiry heuristic. The HF audit run's download step completed, but its data-quality step remained in progress at the latest check; all strategy/P&L gates remain closed pending its report and official contract reconciliation.


## Latest NIFTY prediction rerun — 2026-10-22

- [Workflow #39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966) completed successfully. Artifact SHA-256: `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`.
- [Sanitized aggregate run summary](reports/nifty_prediction_run_39699761966_summary.json) · [research results](research/RESULTS.md) · [structured manuscript](research/MANUSCRIPT.md) · [phase status](research/PHASE_STATUS.md).
- Output: 647 metric rows, 299 OOS candidate comparisons, 296 CV-pass rows, 52 compute-budget-blocked rows.
- No robust selected return/direction edge was established. One selected global ExtraTrees model improved the one-session volatility-proxy QLIKE loss; Holm p=4.26e-7 across all 299 candidate comparisons. This requires independent-period replication and is not a trading signal.
- Options research remains **BLOCKED_NO_VERIFIED_CONTRACT_DATA**. No options P&L, trading recommendation, or live deployment is authorized.


## QE-NOB-1.0 — fresh QuantEvolve-inspired naked option buying (2026-10-22)

**Decision: DATA-LIMITED / NO strategy approved.** [Workflow #39712854501](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501) completed 600 candidates across 9 generations, but 0 passed the statistical gate and 0 passed the execution/promotion gate. The run acquired 92,510 underlying rows and 2,588,918 option rows from 2021-10-25 through 2026-10-21. Data quality failed because 453 of 471 duplicate groups conflicted; historical executable bid/ask/depth and exact expiry/lot-size mapping remain unverified. The strongest validation-selected opening-gap candidate's OOS mean daily net was ₹10.68 with a 95% block-bootstrap interval of -₹188.62 to ₹237.43; Holm-adjusted p=1.0, and stressed costs turned its mean daily net negative. These results do not establish profitability.

- [Fresh study branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v1-developer) · [Results report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/RESULTS.md) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/ERROR_LOG.md) · [Workflow artifact and logs](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501)
- User explicitly declined a tester; this is a developer-led analysis with automated unit checks, not an independently audited result. The workflow's final repository commit failed on a documentation rebase conflict and is being corrected; the run artifact uploaded successfully.

- [Structured research manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/MANUSCRIPT.md) · [Workflow correction](https://github.com/vishnuvcr/Naked-Options-v2/commit/4191d5a0cbbbd703867d5b0f5e7474d8b13f825e)


## QE-NOB-1.0 latest status — 2026-10-22

The corrected duplicate-key diagnostic is valid (0 duplicate groups; 2,600,975 option rows; 99.772% timestamp coverage and 100% row-grid coverage), but the previously reported P&L is superseded: a lot-size proxy bug used 25 units across all dates before 2024-11-20. The source now uses a sourced, expiry-family/date-based NIFTY proxy (WEEK1 vs MONTH1), adding the official 2021 75→50, 2024 50→25, phased 25→75, and 2025/26 75→65 revisions. Revised metrics are pending the corrected bounded workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025).

The study proceeds with available rolling option OHLC, modeled adverse slippage and a disclosed fee model; missing bid/ask/depth does not stop statistical analysis. It does prevent a claim of executable fills. No strategy is approved. [Research plan](research/quant-evolve-nob/RESEARCH_PLAN.md) · [Results](research/quant-evolve-nob/RESULTS.md) · [Phase status](research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](research/quant-evolve-nob/ERROR_LOG.md) · [Manuscript](research/quant-evolve-nob/MANUSCRIPT.md) · [Activity log](research/quant-evolve-nob/INTERACTION_LOG.md)

User explicitly declined an independent tester; no tester branch/report is awaited.

## QE-NOB-1.0 final corrected result — 2026-10-22

**Final disposition: NO_STATISTICAL_CANDIDATE / NO-GO for strategy approval.** Corrected full workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) completed successfully. It evaluated 600 unique candidates over 4 islands and 9 generations using 1,241 sessions (2021-10-25 to 2026-10-21), 92,510 underlying rows and 2,600,975 rolling option rows. All 1,708 acquisition requests were cache hits, zero acquisition failures were recorded, and pre-run/post-run automated tests passed. Zero of 600 candidates passed the statistical gate; zero passed the execution/promotion gate. Candidate 86's corrected OOS mean daily net was about ₹6.14, with a 95% block-bootstrap lower bound about −₹195.69 and Holm p=1.0. The OHLC quality gate passed, but historical bid/ask/depth and exact exchange contract identity remain unverified, so executable profitability is not established.

- [Final results](research/quant-evolve-nob/RESULTS.md) · [Phase status](research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](research/quant-evolve-nob/ERROR_LOG.md) · [Corrected manuscript](research/quant-evolve-nob/MANUSCRIPT.md) · [Dated lot-size reprice audit](research/quant-evolve-nob/LOT_SIZE_REPRICE_AUDIT.md) · [Activity log](research/quant-evolve-nob/INTERACTION_LOG.md)
- [Sanitized run report](reports/quant_evolve_nob_v1/RESULTS.md) · [Run summary JSON](reports/quant_evolve_nob_v1/run_summary.json) · [Workflow artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025)

The frozen-ledger reprice audit is a separate sensitivity check, not the final evolutionary run. No strategy is approved. User explicitly declined independent testing; no tester branch/report is claimed. The bounded study is closed; do not repeat unbounded search without materially better contract/execution data.


## Follow-on: QE-NOB-2.0 open structural strategy discovery

QE-NOB-1.0 is closed **NO-GO** for its tested restricted grammar. The follow-on protocol explicitly addresses the limitation that the earlier search mainly combined predefined signal families and fixed-time exits, rather than evolving structurally distinct entry/exit programs.

- [QE-NOB-2.0 developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v2-discovery-developer)
- [Open strategy discovery plan](research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md)
- [Phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Feature/source feasibility audit](research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md)
- [Activity log](research/quant-evolve-nob/INTERACTION_LOG_V2.md)

**Current status:** Phase 1 protocol amendment complete; Phase 2 data/feature feasibility is pending runtime coverage checks. The plan caps the new study at 1,500 unique structurally distinct candidates and 20 generations, with novelty-aware multi-objective search, evolvable exit state machines, frozen chronological OOS, Holm correction, block bootstrap and after-cost stress tests. The budget is fixed; this is not an endless search. No new strategy has yet been implemented, run, or shown profitable. No tester branch/report will be created, per the user's explicit instruction.


### QE-NOB-2.0 implementation checkpoint — 2026-10-22

Phase 1 protocol and static Phase 2 feasibility audit are documented. A typed structural grammar, novelty metric, mutation/crossover and regression tests are committed. Automated grammar CI is configured but its successful result has not yet been verified; the grammar is not integrated with the backtester and no new strategy results exist.

- [Feature feasibility](research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md)
- [Grammar implementation](research/quant-evolve-nob/strategy_grammar_v2.py)
- [Grammar tests](research/quant-evolve-nob/test_strategy_grammar_v2.py)
- [Implementation error log](research/quant-evolve-nob/ERROR_LOG_V2.md)


### QE-NOB-2.0 checkpoint — feature audit tooling added

A local-cache audit utility and tests are now committed, along with a second automatic/manual GitHub Actions test workflow. The audit reports schema fields, null counts, timestamp ranges and hashes, while explicitly refusing to claim exact contract identity or historical bid/ask/depth.

- [Feature audit utility](research/quant-evolve-nob/feature_audit_v2.py)
- [Feature audit tests](research/quant-evolve-nob/test_feature_audit_v2.py)
- [Feature audit workflow](.github/workflows/qe-nob-v2-feature-audit-tests.yml)
- [Updated phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Updated error log](research/quant-evolve-nob/ERROR_LOG_V2.md)

**Status:** workflows are configured but their results have not been verified; the cache audit has not been run on the research cache. Simulator integration and discovery remain pending. No strategy result is claimed.


### QE-NOB-2.0 — bounded structural candidate generator added

The candidate proposal generator now creates typed, structurally distinct strategy candidates using deterministic mutations/crossover, parent lineage and novelty-based selection. Hard limits are 1,500 candidates and 20 generations. It deliberately does not calculate fitness or P&L until a validated simulator is integrated.

- [Candidate generator](research/quant-evolve-nob/evolve_candidates_v2.py)
- [Generator tests](research/quant-evolve-nob/test_evolve_candidates_v2.py)
- [Generator test workflow](.github/workflows/qe-nob-v2-candidate-generator-tests.yml)
- [Updated phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Updated error log](research/quant-evolve-nob/ERROR_LOG_V2.md)

Automated test results have not been verified yet. This is a candidate-generation component, not evidence of a profitable strategy.


### QE-NOB-2.0 — signal evaluator checkpoint

A leakage-aware predicate evaluator now converts strategy conditions into signal timestamps and maps entry to the next actual market bar. A sparse-signal timing defect in the first draft was caught, corrected and recorded in the error log. Regression tests and a manual/automatic workflow are committed; CI is not yet verified.

- [Signal evaluator](research/quant-evolve-nob/signal_evaluator_v2.py)
- [Signal evaluator tests](research/quant-evolve-nob/test_signal_evaluator_v2.py)
- [Signal evaluator workflow](.github/workflows/qe-nob-v2-signal-evaluator-tests.yml)
- [Updated error log](research/quant-evolve-nob/ERROR_LOG_V2.md)

This component does not simulate option fills, transaction costs or P&L. The study must not progress to profitability conclusions until the option simulator and cost fixtures are implemented and tested.


### QE-NOB-2.0 — OHLC option simulator added

The research branch now includes an indicative long-option OHLC simulator with next-bar entries, same-strike exits, one-position-at-a-time enforcement per candidate, dated lot-size proxies, modeled fees and slippage. The execution gate remains hard-coded **FAIL** because rolling OHLC does not prove exact contract identity or executable quotes.

- [Option simulator](research/quant-evolve-nob/option_simulator_v2.py)
- [Simulator tests](research/quant-evolve-nob/test_option_simulator_v2.py)
- [Simulator test workflow](.github/workflows/qe-nob-v2-option-simulator-tests.yml)
- [Updated phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Error log](research/quant-evolve-nob/ERROR_LOG_V2.md)

CI results are not yet verified. The simulator has not been run against the historical cache; no strategy profitability is claimed.

### QE-NOB-2.0 implementation and CI checkpoint — 2026-10-22

**Status: software regression checks passing; empirical discovery still blocked pending Phase 2 runtime cache/source acquisition. No new strategy result is claimed.**

- [Bounded open structural discovery plan](research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md) · [Phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md) · [Feature/source feasibility](research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md) · [Error log](research/quant-evolve-nob/ERROR_LOG_V2.md) · [Activity log](research/quant-evolve-nob/INTERACTION_LOG_V2.md)
- Implemented typed predicate validation, deterministic structural mutation/crossover, and a candidate generator capped at 1,500 unique candidates / 20 generations. Only implemented signal-entry and time/premium-stop/premium-target semantics are generated; candidate generator still does not calculate fitness or P&L.
- Automated checks passed: [grammar + feature audit #39802894371](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802894371) (15 tests); [standalone feature audit #39802894311](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802894311); [signal evaluator #39801804759](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801804759); [option simulator #39801813009](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801813009); [candidate generator #39802753682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802753682).
- The option simulator includes cost/slippage assumptions and conservative premium stop/target handling, but its execution gate intentionally remains FAIL because rolling OHLC does not confirm exact exchange contract identity, historical bid/ask/depth or actual broker fills.
- Initial runtime audit [#39803204747](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803204747) returned `BLOCKED_NO_LOCAL_CACHE` (zero files). This does not prove Dhan or any free source is unavailable; the sibling branch's Actions cache was not present in the v2 runner.
- A bounded cache-first/source-acquisition-only workflow was added: [.github/workflows/qe-nob-v2-data-audit.yml](.github/workflows/qe-nob-v2-data-audit.yml). Run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) was automatically triggered; inspect its sanitized artifact before changing Phase 2 status. Raw market payloads are kept in the runner cache and are not uploaded as artifacts.
- QE-NOB-1.0 remains NO-GO and unchanged. No QE-NOB-2.0 candidate has yet been backtested for fitness or shown profitable; no tester branch/report is created, per the user's explicit instruction.


### QE-NOB-2.0 acquisition result — 2026-10-23

**Status: BLOCKED at data acquisition; no new candidate or profitability result.** Eligible weekly-only workflow [#39838508682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838508682) passed pre-acquisition regression gates but failed the source gate. Its [fresh sanitized artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838508682/artifacts/12451299405) reports Dhan HTTP 401 DH-901 (access token invalid or expired), incomplete weekly option history, and no verified 5-minute underlying series. The final cache audit counted 745 parseable JSON files, including 744 option-folder files and one underlying probe; parseability does not establish historical coverage. Exact contract identity and historical bid/ask/depth remain unverified. The cache was preserved and empirical discovery was skipped.

- [Phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md) · [Error log](research/quant-evolve-nob/ERROR_LOG_V2.md) · [Activity log](research/quant-evolve-nob/INTERACTION_LOG_V2.md) · [Source catalogue](research/quant-evolve-nob/SOURCE_CATALOG_V2.md)

**Next gate:** renew the Dhan token in GitHub Actions secrets or verify and integrate a legally usable alternate source with explicit expiry/contract mapping and historical underlying bars. Do not repeat acquisition with the same invalid credential. Phase 5 remains blocked; Phases 6–7 are not started; execution remains FAIL.


### Dhan token renewal automation — 2026-10-23

The QE-NOB-2.0 acquisition workflow now has a TOTP-based token bootstrap using Dhan's documented token-generation endpoint. Before source acquisition, it generates a fresh 24-hour access token, validates it with the Dhan profile endpoint, and places it only in the current GitHub Actions job environment. It does **not** print or commit the token.

**Required one-time setup:** enable TOTP in Dhan Web → My Profile → Access DhanHQ APIs, then add these repository Actions secrets: `DHAN_CLIENT_ID`, `DHAN_PIN`, and `DHAN_TOTP_SECRET` (the authenticator's base32 secret). Do not paste them into chat or commit them. The existing `DHAN_ACCESS_TOKEN` is not sufficient for reliable unattended renewal after it expires.

Implementation: [token helper](research/quant-evolve-nob/dhan_auth.py) · [RFC regression tests](research/quant-evolve-nob/test_dhan_auth.py) · [acquisition workflow](.github/workflows/qe-nob-v2-data-audit.yml) · [phase status](research/quant-evolve-nob/PHASE_STATUS_V2.md) · [error log](research/quant-evolve-nob/ERROR_LOG_V2.md).

**Verification state:** implementation committed; live authentication is pending the three secrets and a successful workflow run. Research Phase 2 remains blocked until token/profile validation and the historical data acquisition/cache gate pass.


## QE-NOB-2.0 final manuscript — 2026-10-23

The bounded evolutionary discovery run is now documented in the [final research manuscript](research/quant-evolve-nob/FINAL_RESEARCH_MANUSCRIPT.md). The report includes research questions, aims/objectives, chronological methodology, feature definitions, cost assumptions, statistical methods, OOS results, cost sensitivity table/chart, discussion, strengths, limitations, conclusion, future directions and appendices.

**Final disposition: DATA-LIMITED.** Of 20 frozen finalists, 12 passed the statistical gate after Holm correction and 0 passed the execution gate. Historical rolling option bars do not establish stable dated contract identity or executable bid/ask/depth/fills. No paper/live trading is approved. See [artifact integrity decision](research/quant-evolve-nob/ARTIFACT_INTEGRITY_DECISION.md), [simulator/feature audit](research/quant-evolve-nob/SIMULATOR_FEATURE_AUDIT.md), [phase status](research/quant-evolve-nob/PHASE_STATUS.md), and [error log](research/quant-evolve-nob/ERROR_LOG.md).


## QE-NOB-3.0 strategy hypothesis lab

A new bounded research branch proposes six falsifiable strategy families, with a strict fresh-data gate and no reuse of QE-NOB-2.0's examined OOS period. See [hypothesis plan](research/quant-evolve-nob/STRATEGY_HYPOTHESIS_LAB_V3.md), [phase status](research/quant-evolve-nob/PHASE_STATUS_V3.md), and [v3 error log](research/quant-evolve-nob/ERROR_LOG_V3.md). Regression workflow: [.github/workflows/qe-nob-v3-hypothesis-tests.yml](.github/workflows/qe-nob-v3-hypothesis-tests.yml). Empirical testing remains blocked until authentication, fresh-data coverage and stable dated contract identity pass. No new strategy has been tested or approved for trading.

- [Fresh-data eligibility probe workflow](.github/workflows/qe-nob-v3-data-probe.yml): bounded manual/push probe using repository secrets, sanitized artifact only, no bulk acquisition. Its execution has not yet been verified.


### Latest QE-NOB-3.0 verification (2026-10-23)

- [Regression workflow](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39913031868): **SUCCESS** after fixing a brittle plan-text assertion.
- [Fresh-data probe](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39912434371): **SUCCESS**; sanitized artifact uploaded. Probe reports weekly source availability and a small underlying schema sample.
- This probe is **not** full historical data validation: stable dated option-contract identity, complete coverage and quote-level execution data are not yet verified. Strategy discovery remains blocked pending those checks.
- Details: [QE-NOB-3.0 phase status](research/quant-evolve-nob/PHASE_STATUS_V3.md) and [error log](research/quant-evolve-nob/ERROR_LOG_V3.md).


### Strict data-gate result (2026-10-23)

The latest [data-probe workflow](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39933612441) completed successfully as a workflow, but the research gate correctly returned **BLOCKED_DATA_LIMITED**: 746 underlying probe rows and 765 rolling option rows were available in the small probe, but stable dated contract identity and executable bid/ask fields were absent. This is not a complete historical data validation and no strategy discovery has started. See [QE-NOB-3.0 phase status](research/quant-evolve-nob/PHASE_STATUS_V3.md) and [error log](research/quant-evolve-nob/ERROR_LOG_V3.md).
