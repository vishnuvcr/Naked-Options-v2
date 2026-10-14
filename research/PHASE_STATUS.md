# Phase status and gate decisions

Last updated: 2026-10-14  
Research version: NIFTY-PRED-1.0

| Phase | Branch | Status | Evidence / next action |
|---|---|---|---|
| 1. Repository audit and design | research/phase-1-audit | COMPLETE FOR CURRENT SCOPE | Repository initialization and execution policy are documented. Reopen only if scope changes. |
| 2. Literature review | research/phase-2-literature | PARTIAL, ACCEPTED LIMITATION | First-pass review and source register are included; exhaustive review across all media/source families was not completed and is stated as a limitation. |
| 3. Data collection/validation/cache | research/phase-3-data | PASS WITH LIMITATIONS | Run #49 validated cached NIFTY data and seven external series. Rejected series and unavailable options/FII-DII/PCR/breadth/news inputs are documented. Global timing/holiday alignment still needs audit. |
| 4. Baselines | research/phase-4-baselines | COMPLETE FOR CURRENT DATA | Zero-return, persistence, historical-prevalence and ARIMA benchmark artifacts generated. Tester must review ARIMA artifact separately. |
| 5. Model experiments | research/phase-5-models | RUN COMPLETE; TESTER PASS WITH SCOPE LIMITATIONS | Run #49 passed tests, feature construction, technical/global catalogues, ARIMA, merge and report steps. 491 metric rows, 143 OOS-evaluated rows, 208 budget-blocked rows. |
| 6. Feature/horizon/regime analysis | research/phase-6-features-regimes | PARTIAL, ACCEPTED LIMITATION | Technical/global and horizon comparisons are complete within acquired data; full regime segmentation and option/FII-DII/PCR/breadth/news families remain untested. |
| 7. Statistical validation | research/phase-7-validation | PASS FOR BOUNDED PREDICTION SCOPE | 91 regression skill metrics independently reproduced (max discrepancy ~2.04e-9); 140 non-ARIMA block CIs reproduced (max discrepancy <8e-9); HAC p-values within ~1.24e-5. Tester to review p-value/Holm families, ARIMA, probability calibration and dependence handling. |
| 8. Independent tester | research/independent-tester | PASS WITH SCOPE LIMITATIONS | Tester report on run #49 confirms target-window correction, arithmetic, CIs, HAC/Holm and ARIMA checks. Calibration and unavailable data families are limitations. |
| 9. Manuscript and conclusion | research/phase-9-manuscript | COMPLETE WITH SCOPE LIMITATIONS | Tester-reviewed manuscript and selected-results figure committed. The study is closed as prediction-only; unacquired data families and missing execution analysis are documented. No trading strategy is approved. |

## Corrected workflow evidence

- [Run #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) succeeded on commit `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`.
- Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`.
- Target-construction tests and feature matrix passed. OOS predictions have non-null target dates later than origin dates; available date pairs align with 1/5/20-session horizons.
- Preliminary interpretation: no robust return/direction edge; selected volatility forecasts are not statistically accepted after multiplicity correction; volatility-expansion classification is exploratory only.
- No strategy approval is implied. No options data or transaction-cost/slippage simulation was available.


## Tester disposition

The independent tester branch reports PASS WITH SCOPE LIMITATIONS for the bounded prediction-only study. This closes the execution/target-window and prespecified statistical checks for the scoped study; it does not approve a trading strategy or substitute for unacquired options, FII/DII, PCR, breadth, news or transaction-cost data.


## Closure

The nine-phase work is closed for the bounded prediction-only scope with accepted limitations. Phases 2 and 6 are partial by design/scope, not falsely marked complete. The final conclusion is that this model/data set did not establish a robust return/direction edge. No options strategy was tested or approved.


## Separate follow-on study (does not reopen NIFTY-PRED-1.0)

A user-approved scope amendment on 2026-10-14 created OPT-BUY-1.0 as a separate, bounded test. It does not alter the closed nine-phase NIFTY-PRED-1.0 study.

| Track | Branch | Status | Evidence / final gate |
|---|---|---|---|
| Intraday option-buying validation | research/option-buying-validation | CLOSED — NO-GO FOR TESTED CANDIDATES; BROADER HYPOTHESIS INCONCLUSIVE | [Run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) completed with 13 tests passing before and after analysis. Independent review: [TESTER_REPORT.md](research/option-validation/TESTER_REPORT.md). |

Acquisition succeeded from cache; the quote universe has 1,062,082 raw and 1,029,545 usable rows. The frozen data gate fails: strangle eligible-date coverage 69.18% (<80%) and conflicting duplicate groups 1.409% (>1%). All four filtered candidates have negative mean net daily P&L and negative 95% intervals; 100-bps and both-half profitability checks also fail. Significant paired improvement versus always-buy is loss reduction, not profitability.

The developer accepted the independent tester's no-go. No strategy, paper-trading candidate or live deployment is approved. Do not relax the frozen gates or run further parameter loops.

## OPT-BUY-2.0 — strike-selection grid

| Phase | Status | Evidence / next gate |
|---|---|---|
| Protocol and branch setup | COMPLETE | [Frozen plan](STRIKE_SELECTION_PLAN.md); [research branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-strike-selection) |
| Daily target acquisition/validation and regression tests | PASS IN RUN #4 | Daily target validated; 13 pre-analysis and 13 final regression tests passed. [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) |
| Options data quality | FAIL FOR CONFIRMATORY USE | 1,023,541 usable rows; 452 conflict groups / 31,706 duplicate groups = 1.4256%, above the 1% gate. No parse failures. |
| Coverage | FAIL FOR GRID-WIDE CONFIRMATORY USE | Only ATM/ATM coverage clears 80%; coverage ranges from 83.27% to 16.94% over 980 dates. |
| Frozen grid outcomes | COMPLETE — EXPLORATORY ONLY | At primary costs (50 bps/side, ₹10/order), all 32 model-filtered candidate × horizon means are negative and their 95% block-bootstrap upper bounds are below zero. No candidate approved. |
| Primary p-values / Holm family | CORRECTIVE RETEST | Run #4 emitted NaN for all 32 p-values despite a nonempty ledger. Fixed with explicit null-centered circular block bootstrap in commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9; [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress. |
| Common-date sensitivity | NOT COMPLETED | Not present in run #4 artifact. Do not claim cross-candidate superiority; the failed quality gate already precludes confirmatory ranking. |
| Independent tester sign-off | WAIVED BY USER | User explicitly waived separate tester sign-off; data-quality and inference gates remain mandatory. |

**Disposition:** NO-GO for any strike-selection candidate. Keep OPT-BUY-1.0 no-go unchanged. The one bounded corrective rerun must confirm valid p-values; do not start further parameter loops or approve paper/live deployment.


## Uploaded-PDF model audit extension — 2026-10-14

| Gate | Status | Evidence / next action |
|---|---|---|
| PDF method inventory | COMPLETE FOR SCREENING | [Method audit](PDF_METHOD_AUDIT.md); all 13 uploaded PDFs inventoried with out-of-scope and blocked methods marked. |
| Expanded run execution | PASS | [Workflow #56](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38585954777) completed data validation, technical/global catalogue, ARIMA, report merge and artifact upload. |
| Empirical summary | PROVISIONAL | [Run #56 results](PDF_METHOD_AUDIT_RESULTS.md); no model winner declared. Return gains are small and inspected return rows are not adjusted-significant. |
| Independent statistical/code audit | OPEN | Verify QLIKE skill NaNs, sequence epoch mismatch, p-value/Holm families, horizon/target alignment, calendar flags and global timing. Create tester branch/report before final disposition. |
| Strategy work | OUT OF SCOPE | Prediction-only request; no option strategy or trading recommendation is made from these metrics. |


## Run #60 — 2026-10-14

- Expanded execution/result acquisition: COMPLETE. [Workflow #60](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38593936036) succeeded; artifact SHA-256 `b601320f64ab8ec0c62f0a07e458287cba781eca73107f1b2c38beda140a8151`.
- Results and manuscript consolidation: COMPLETE FOR BOUNDED SCREEN. See [results](PDF_METHOD_AUDIT_RESULTS.md), [manuscript](MANUSCRIPT.md), experiment log and error log.
- Independent review: NEXT, permitted now that results are acquired and documented. Audit paired-loss signs, QLIKE, horizon alignment, calibration, calendar dates and global timing; submit actionable findings.
- Scientific disposition pending review: no robust return/direction winner established; volatility-expansion remains exploratory.
- Trading strategy: OUT OF SCOPE; no option strategy or execution claim.


## Independent review of run #60 — gate did not pass

Tester report: [PDF method audit tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md). Disposition: FAIL FOR FINAL SCIENTIFIC SIGN-OFF, while workflow execution itself passed. Main blocker: 1,260 missing target dates caused by partial future windows for volatility labels. Developer fix committed to `scripts/build_feature_matrix.py` with a new assertion test. Workflow #61 is testing the code correction and #62 is queued with the test addition. Do not close the independent-review gate until the corrected artifact is checked and the tester submits an updated disposition.


## Final run #62 disposition

- Workflow #62 succeeded. Final artifact has 471,735 prediction rows, zero null target dates and no target date on/before origin.
- Independent tester: [PASS WITH SCOPE LIMITATIONS](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md). Headline metrics, non-ARIMA confidence intervals, ARIMA benchmark and Holm corrections were reproduced.
- Conclusion: no robust return/direction winner. One-session global XGBoost volatility QLIKE improvement survives Holm correction; other volatility results are metric-specific and volatility-expansion remains exploratory.
- Close bounded prediction-only research. Preserve calendar/global timing and unavailable feature families as limitations.
