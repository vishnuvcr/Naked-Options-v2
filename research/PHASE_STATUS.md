# Phase status and gate decisions

Last updated: 2026-10-14  
Research version: NIFTY-PRED-1.0

| Phase | Branch | Status | Gate / evidence | Next action |
|---|---|---|---|---|
| 1. Repository audit and design | research/phase-1-audit | COMPLETE FOR CURRENT SCOPE | Repository initialization and execution policy are documented. | Reopen only if scope changes. |
| 2. Literature review | research/phase-2-literature | PARTIAL | Initial literature/source review exists; no exhaustive source-family review is claimed. | Complete the final reference matrix and research-gap mapping before manuscript approval. |
| 3. Data collection/validation/cache | research/phase-3-data | PASS WITH LIMITATIONS | Run #49 passed acquisition/validation using cached NIFTY daily data and seven external series. Rejected series and unavailable options/FII-DII/PCR/breadth/news inputs are documented. | Independent audit of global timing/holiday alignment and source coverage. |
| 4. Baselines | research/phase-4-baselines | COMPLETE FOR CURRENT DATA | Zero-return, persistence, historical-prevalence and ARIMA benchmark artifacts generated. | Tester to verify ARIMA artifact separately. |
| 5. Model experiments | research/phase-5-models | RUN COMPLETE; TESTER GATE OPEN | Run #49 passed tests, feature construction, technical/global catalogues, ARIMA, merge and report steps. 491 metric rows; 143 OOS-evaluated rows; 208 budget-blocked rows. | Tester validates model outputs and experiment-scope compliance. |
| 6. Feature/horizon/regime analysis | research/phase-6-features-regimes | PARTIAL | Technical/global comparison and horizon cells exist; market-regime segmentation and important data families (options, FII/DII, PCR, breadth, news) remain untested. | Keep untested feature families explicit; do not claim full regime analysis. |
| 7. Statistical validation | research/phase-7-validation | PARTIAL; FINAL GATE OPEN | Recomputed 91 regression skill metrics (max discrepancy ~2.04e-9), 140 non-ARIMA block-CIs (max discrepancy <8e-9), and target-date/horizon alignment. HAC p-values differ by at most ~1.24e-5 in independent reconstruction; multiplicity/ARIMA review remains. | Tester signs off on HAC/Holm families, ARIMA artifact, probability calibration and dependence handling. |
| 8. Independent tester | research/independent-tester | IN PROGRESS | Run #45 report failed on a confirmed tail-window label defect. Developer fix and corrected workflow #49 now pass CI and contain zero null target dates in OOS predictions. | Update tester report against run #49 and give explicit PASS/FAIL. |
| 9. Manuscript and conclusion | research/phase-9-manuscript | PROVISIONAL | Results register now has a corrected-run evidence table and explicit limitations. No trading strategy has been validated. | Finalize manuscript only after tester report and statistical gate are closed. |

## Corrected workflow evidence — 2026-10-14

- [Run #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) completed successfully on commit `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`.
- The corrected target-window regression test passed. All OOS prediction rows have non-null target dates later than their origin dates; declared horizon offsets were verified as 1/5/20 sessions where both dates were present in the OOS origin calendar.
- Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`.
- Model results are now available, but final research acceptance remains conditional on independent tester review. No strategy approval is implied.
