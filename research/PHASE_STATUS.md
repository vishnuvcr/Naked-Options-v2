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
## Separate follow-on study — option-buying validation (does not reopen NIFTY-PRED-1.0)

| Track | Branch | Status | Evidence / gate |
|---|---|---|---|
| Intraday option-buying validation | research/option-buying-validation | BLOCKED_NO_VALID_DAILY_DATA | Workflow: https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38617943823; commit: 53029f81971b7adb395ac76a8b936830bbd6be7a; acquisition: BLOCKED_NO_VALID_DAILY_DATA; requests failed: 0. Independent post-result developer/tester gate required. |

No live strategy is approved. The first experiment is intraday-only because rolling strike-relative option series do not establish stable multi-day contract identity.
<!-- OPTION_VALIDATION_PHASE_END -->
