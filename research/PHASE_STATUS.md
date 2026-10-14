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

<!-- OPTION_VALIDATION_PHASE_START -->
## Follow-on option-buying validation — OPT-BUY-1.0

| Track | Branch | Status | Evidence / decision |
|---|---|---|---|
| Intraday option-buying validation | research/option-buying-validation | CLOSED — NO-GO FOR TESTED CANDIDATES; DATA GATE FAILED | [Run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) completed; 13 unit tests passed before and after analysis. Independent review is in [TESTER_REPORT.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-independent-tester/research/option-validation/TESTER_REPORT.md). |

Acquisition succeeded from cache (686 windows reused; no new requests or failed windows in the last run). The frozen acceptance gates fail: strangle eligible-date coverage 69.18% versus ≥80% required; conflicting duplicate groups 1.409% versus ≤1% allowed. All four candidates' mean net P&L and 95% daily-P&L intervals are negative at the primary cost setting, every 100-bps stress result and both chronological-half profitability tests fail. Positive paired differences versus always-buy reflect loss reduction against a worse baseline, not profitable option buying.

The independent tester reproduced ledger arithmetic, four paired means, block-bootstrap intervals and p-values. Final decision: no tested strategy, paper-trading candidate or live deployment is approved. Do not relax gates or continue parameter loops. The original nine-phase NIFTY-PRED-1.0 remains closed and unchanged.
<!-- OPTION_VALIDATION_PHASE_END -->
