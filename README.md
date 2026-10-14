# Fresh NIFTY 50 Prediction Research

**Research version:** NIFTY-PRED-1.0  
**Scope:** Prediction only. No trading strategy design, optimization, or recommendation in this study.  
**Started:** 2026-10-14  
**Status:** Phase 5 is running under a bounded, auditable execution plan; first full model fits completed, but the results merge is being repaired.

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

- Repository bootstrap and protocol: complete for NIFTY-PRED-1.0; original repository was empty at audit.
- Daily target data: Dhan cache verified with 4,901 rows (2007-01-02 to 2026-10-13), SHA-256 b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050. Weekend-dated bars are now warnings, not automatically removed.
- Data-quality tests and feature matrix: passed on the latest inspected workflow steps; feature/test build is verified.
- Model experiments: Actions run [#41](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38526229786) completed technical and global model fitting (278 technical and 210 global experiment records) but failed while merging because an empty error CSV was parsed. Per-run CSVs were not included in its artifact, so no model ranking is accepted. The corrected run [#45](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38527508857) includes safe empty-file handling, per-run artifact uploads, and a QLIKE correction; it is pending.
- Known defect correction: benchmark-relative out-of-sample R-squared has been fixed on the phase-5 branch; that branch's corrected run must be the canonical result.
- External inputs: seven public daily series were validated in run #41 (S&P 500, Nasdaq, Nikkei 225, Hang Seng, CBOE VIX, India VIX proxy, U.S. 10-year yield proxy). USD/INR, gold and WTI failed OHLC checks and were not used. Historical options, FII/DII, breadth, point-in-time constituents and news/sentiment data are not verified as acquired.
- Independent tester report is available on `research/independent-tester`; it identified the partial-forward-window volatility-label defect. Phase 5/7 remain open until the developer fix passes CI and a corrected model run is independently rechecked.
- Provisional ARIMA(1,0,0) metrics did not show statistically significant improvement over zero-return forecasts at 1/5/20 sessions (raw p = 0.492/0.935/0.842; loss-difference intervals include zero). These are not final until the corrected merge rerun reproduces the outputs and Holm-adjusted comparisons are available. No best model is declared yet.

See [phase status](research/PHASE_STATUS.md) for the authoritative gate state.

- [Run 45 results and evidence register](research/RESULTS.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md)
- [Developer correction branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/developer-review)


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


The static research status page has been deployed successfully through [Pages publish workflow #2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38535940026). Future updates to the README, results, phase status, manuscript, figure or docs trigger the lightweight publishing workflow without rerunning the model catalogue.

<!-- OPTION_VALIDATION_README_START -->
## Follow-on study: option-buying validation — OPT-BUY-1.0

The original nine-phase NIFTY-PRED-1.0 prediction-only study remains closed and unchanged. This separate user-approved validation tests next-session intraday ATM straddles and one-step OTM strangles filtered by development-only 5/20-session technical Logistic volatility-expansion probabilities. It is not a live-trading workflow.

**Latest status:** INCONCLUSIVE_PARTIAL_OR_INCOMPLETE_DATA. **Git SHA:** b5f78b27b7f6f020d39f9507dfead79d65b9bff0. **Workflow:** https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38544279448.

- [Validation plan](research/OPTION_BUYING_VALIDATION_PLAN.md)
- [Option validation results](research/option-validation/RESULTS.md)
- [Primary comparisons CSV](reports/option_validation/primary_comparisons.csv)
- [Option validation workflow](.github/workflows/option-buying-validation.yml)

Raw option quotes are kept out of the public repository/artifacts. Do not call a strategy validated unless the cost, statistical, robustness and independent-review gates pass.
<!-- OPTION_VALIDATION_README_END -->
