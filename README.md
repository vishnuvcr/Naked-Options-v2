# Fresh NIFTY 50 Prediction Research

**Research version:** NIFTY-PRED-1.0  
**Scope:** Prediction only. No trading strategy design, optimization, or recommendation in this study.  
**Started:** 2026-10-14  
**Status:** NIFTY-PRED-1.0 is closed with accepted limitations. Follow-on OPT-BUY-1.0 is also closed: no tested option-buying candidate passed the data-quality and profitability gates.

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

- **Original prediction study (NIFTY-PRED-1.0): CLOSED WITH SCOPE LIMITATIONS.** Its corrected canonical run is [#49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128); see [results](research/RESULTS.md), [phase status](research/PHASE_STATUS.md), and [scientific manuscript](research/MANUSCRIPT.md).
- **Follow-on option-buying validation (OPT-BUY-1.0): CLOSED — NO-GO for tested candidates; broader hypothesis inconclusive.** The completed [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) and independent review found strangle quote coverage of 69.18% (<80%), conflicting duplicate groups at 1.409% (>1%), and negative net daily P&L confidence intervals for all four candidates. No paper/live strategy is approved; details are in [the option-validation results](research/option-validation/RESULTS.md) and [tester report](research/option-validation/TESTER_REPORT.md).
- Daily NIFTY data: 4,901 rows from 2007-01-02 to 2026-10-13; SHA-256 `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050`.
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


## Latest expanded PDF-method audit — 2026-10-14

- Corrected [workflow run #56](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38585954777) completed successfully on `research/pdf-method-audit` after a bounded fix for empty CSV merging.
- [Method inventory](research/PDF_METHOD_AUDIT.md) and [run 56 results](research/PDF_METHOD_AUDIT_RESULTS.md) document the expanded screening of uploaded-paper method families. Data: 4,901 Dhan daily rows through 2026-10-13; seven external market series passed the configured validator; USD/INR, gold and WTI were rejected, and the NSE endpoint returned no recognized rows.
- **No best model is approved yet.** Return-model differences are small and the inspected return rows do not survive Holm correction. Some direction/volatility-expansion p-values are below .05 but require independent verification of hypothesis families and test calculations.
- Two explicit audit issues remain open: (1) exported `qlike_skill_vs_baseline` is NaN with finite QLIKE values; (2) sequence metadata says eight epochs despite the documented three-epoch budget. See [error log](research/ERROR_LOG.md) and [phase status](research/PHASE_STATUS.md).
- The expanded audit remains prediction-only. It does not include option P&L, Paytm Money costs, slippage, or an approved trading strategy. Blocked/unreplicated PDF methods and missing data families are documented, not silently treated as tested.
