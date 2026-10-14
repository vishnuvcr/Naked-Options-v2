# Phase status and gate decisions

Last updated: 2026-10-14  
Research version: NIFTY-PRED-1.0

| Phase | Branch | Status | Evidence / next action |
|---|---|---|---|
| 1. Repository audit and design | research/phase-1-audit | COMPLETE FOR CURRENT SCOPE | Repository initialization and execution policy are documented. Reopen only if scope changes. |
| 2. Literature review | research/phase-2-literature | PARTIAL | Initial review exists; exhaustive reference matrix and research-gap mapping remain before manuscript approval. |
| 3. Data collection/validation/cache | research/phase-3-data | PASS WITH LIMITATIONS | Run #49 validated cached NIFTY data and seven external series. Rejected series and unavailable options/FII-DII/PCR/breadth/news inputs are documented. Global timing/holiday alignment still needs audit. |
| 4. Baselines | research/phase-4-baselines | COMPLETE FOR CURRENT DATA | Zero-return, persistence, historical-prevalence and ARIMA benchmark artifacts generated. Tester must review ARIMA artifact separately. |
| 5. Model experiments | research/phase-5-models | RUN COMPLETE; TESTER GATE OPEN | Run #49 passed tests, feature construction, technical/global catalogues, ARIMA, merge and report steps. 491 metric rows, 143 OOS-evaluated rows, 208 budget-blocked rows. |
| 6. Feature/horizon/regime analysis | research/phase-6-features-regimes | PARTIAL | Technical/global and horizon comparisons exist; full market-regime segmentation and option/FII-DII/PCR/breadth/news data families remain untested. |
| 7. Statistical validation | research/phase-7-validation | PARTIAL; FINAL GATE OPEN | 91 regression skill metrics independently reproduced (max discrepancy ~2.04e-9); 140 non-ARIMA block CIs reproduced (max discrepancy <8e-9); HAC p-values within ~1.24e-5. Tester to review p-value/Holm families, ARIMA, probability calibration and dependence handling. |
| 8. Independent tester | research/independent-tester | IN PROGRESS | Previous report failed due to partial forward-volatility windows. Developer fix passed workflow #49; no null target dates remain in OOS predictions. Tester must review corrected artifact and give explicit PASS/FAIL. |
| 9. Manuscript and conclusion | research/phase-9-manuscript | PROVISIONAL | Results register now contains corrected-run evidence. Final manuscript and conclusion require tester disposition and explicit limitations. |

## Corrected workflow evidence

- [Run #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) succeeded on commit `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`.
- Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`.
- Target-construction tests and feature matrix passed. OOS predictions have non-null target dates later than origin dates; available date pairs align with 1/5/20-session horizons.
- Preliminary interpretation: no robust return/direction edge; selected volatility forecasts are not statistically accepted after multiplicity correction; volatility-expansion classification is exploratory only.
- No strategy approval is implied. No options data or transaction-cost/slippage simulation was available.
