# Independent tester report — run #45

Date: 2026-10-14  
Artifact: [Actions run #45](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38527508857)  
Artifact SHA-256: 674824d1f5ba18a2fa453338c013a9e4de7aadec97ad6b278391e97df2db2479  
Reviewed commit: c11ee9b408473cb2279e76a7e8a2b98a8a88b011  
Status: **FAIL — do not pass the research gate yet.**

## Evidence inspected

- Downloaded and inspected the run artifact ZIP; it contains 23 files including prediction CSVs, metrics, source/data manifests, model manifests and error logs.
- Technical manifest: COMPLETE, 278 experiment rows, 72,253 predictions; global-feature manifest: COMPLETE, 210 experiment rows, 64,413 predictions. Merged metrics: 491 rows, 143 OOS-evaluated rows, 208 compute-budget-blocked rows.
- Dhan daily series has 4,901 rows (2007-01-02 to 2026-10-13). Seven external market series passed; USD/INR, gold and WTI were rejected. NSE query returned no recognized data rows.
- One-session return forecasts show negligible skill: technical XGBoost MSE skill +0.13%, p=.737, Holm p=1; global CatBoost +0.17%, p=.579, Holm p=1.
- One-session direction accuracy is about 54.1%; global CatBoost nominal p=.0288 becomes Holm p=.193.
- Global Random Forest reports 17.3% one-session QLIKE skill, but volatility target/loss semantics need correction before accepting it.

## Findings and gates

### HIGH-001 — Level target transform needs explicit test (REVIEW REQUIRED, not yet confirmed defect)

The artifact's level predictions/actuals are in index-point units (mean actual around 22,519), while build_feature_matrix.py stores target_log_close in log units. However, run_experiments.py explicitly exponentiates actual, prediction and baseline before calculating point-scale metrics, so the unit difference may be intentional. The remaining test is to independently confirm the artifact's level rows match exp(target_log_close) and that the persistence baseline equals the origin close. Do not label this a confirmed defect unless the exact row-level comparison fails.

Recommended safeguard: include a target schema/units map in each manifest and add a unit test proving point-scale predictions/actuals equal the exponentiated log-price values, with persistence baseline equal to close_t.

### HIGH-002 — Verify QLIKE target transformation (REVIEW REQUIRED, code appears to square values)

The target is a standard-deviation / absolute-return proxy, but run_experiments.py squares actual, forecast and baseline before applying qlike_loss, which appears scale-consistent. Independently recompute this from prediction rows to confirm. Displayed p=0 is numerical underflow, not literal zero; format as p<1e-6.

### HIGH-003 — Recompute and multiplicity (BLOCKING for significance)

Independently recompute paired losses from predictions, check HAC lag against horizon overlap, verify Holm correction family against the plan, and compare adjusted p-values. Nominal significance remains exploratory until reproduced.

### HIGH-004 — Partial forward-volatility windows (CONFIRMED, BLOCKING)

The prediction CSV contains null target dates for 3 observations at horizon 5 and 18 observations at horizon 20 for the volatility and volatility-expansion tasks. The feature builder uses `fr.std(axis=1, ddof=1)` which skips missing future returns, so the last rows can be labelled using fewer than the declared horizon. These are not valid 5-/20-session targets and must not be evaluated as such.

Developer fix required: make future volatility missing unless all h future returns exist; add a regression test for the last h rows; rebuild the feature matrix and rerun experiments. After rerun, assert every OOS prediction has a non-null target_date later than origin_date and all horizon targets have complete windows.

### MEDIUM-005 — Source/feature availability

Global features include S&P 500, Nasdaq, Nikkei, Hang Seng, India VIX, CBOE VIX and US 10-year yield. Same-date closes are excluded, but timing and holiday alignment need review. USD/INR, gold and WTI were rejected; historical options, FII/DII, PCR, breadth and timestamped news were not acquired.

### MEDIUM-006 — Classification baseline

Verify baseline probabilities use development data only and Brier/log-loss skill use the same valid observations. Report balanced accuracy and calibration alongside raw accuracy.

### LOW-007 — Calendar

Twenty weekend-dated rows are preserved and flagged. Cross-check special sessions; do not delete solely based on weekend dates.

## Preliminary, not accepted

- One-session return models show no useful gain over zero-return in this run.
- One-session direction results are close to chance and do not survive Holm adjustment.
- Some volatility models appear promising; QLIKE is squared to variance scale in the runner, but the tester must reproduce the result independently before acceptance.
- Level results are blocked by target/unit mismatch.
- ARIMA(1,0,0) has no significant gain over zero-return in the reported 1/5/20-session results; recompute independently.

## Gate decision

**Phase 5: FAIL pending full-window volatility label correction, tests, and rerun.  
Phase 6: partial; global feature ablation ran, regime segmentation and source families remain incomplete.  
Phase 7: open; significance/QLIKE audit not passed.  
Phase 8: report submitted, not approved.  
Phase 9: manuscript remains provisional.**

## Developer instructions

1. Verify exact commit/code bundle and independently compare exponentiated level predictions/actuals against source targets; add target-unit tests if absent.
2. Recompute QLIKE from squared realized/predicted volatility; correct p-value formatting so underflow is not presented as literal zero.
3. Correct the partial forward-volatility window defect and rerun. Independently recompute candidate/baseline metrics from predictions, including paired losses, block confidence intervals, HAC tests and Holm correction.
4. Check global feature availability timing, overlapping target-date dependence and classification baselines.
5. Run tests and regenerate artifacts; update RESULTS.md, ERROR_LOG.md, PHASE_STATUS.md and README.md. Resubmit for tester review; do not progress to publication gate before passing.

## Independent arithmetic check update — 2026-10-14

I independently recalculated benchmark-relative MSE skill for return and level predictions and variance-scale QLIKE skill from the saved merged predictions. Across 91 regression model/target/horizon/feature-set entries, the largest absolute discrepancy versus the artifact metrics was approximately 2.04e-9 after applying the same 1e-12 variance floor. This confirms the core reported loss-skill arithmetic for those entries, but does not validate p-values, confidence intervals, or model selection.

The confirmed tail-window defect remains: the artifact contains missing target_date values for horizon-5 and horizon-20 volatility/volatility-expansion observations while the labels themselves are present. This is consistent with the old feature builder's partial-window standard deviation. The developer branch now corrects the construction and tests the boundary; a successful CI run and regenerated artifact are still required before approving the gate.


---

# Independent tester report — corrected run #49

Date: 2026-10-14  
Artifact: [Actions run #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128)  
Reviewed commit: `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`  
Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`

## Gate checks

- Workflow completed successfully. Data validation, target construction/scoring tests, feature matrix, technical and global catalogues, ARIMA, merge and report steps passed.
- The corrected future-volatility builder now requires all horizon observations. The boundary test passed. Across 139,289 OOS prediction rows, target_date has zero missing values and zero dates on/before origin_date. For target dates represented in the OOS origin calendar, the offset matches the declared horizon (1, 5, or 20 sessions).
- Independently recalculated 91 regression benchmark-relative MSE/QLIKE skill values from the merged prediction file. Maximum absolute difference from the saved metrics was approximately 2.04e-9.
- Independently recalculated 140 non-ARIMA moving-block confidence intervals using the registered seed and horizon. Maximum absolute difference was below 8e-9.
- Independently recomputed HAC paired-loss p-values for 140 non-ARIMA evaluated models; maximum absolute difference was approximately 1.24e-5, concentrated in small probability-loss mean differences. This is small numerically but should be checked against full-precision predictions before the statistical gate is finally closed. ARIMA predictions are a separate CSV and were not included in that merged-prediction check.
- Selected one-session global CatBoost direction accuracy is 54.08%, but raw p=.0288 and Holm p=.5478; not statistically accepted. Selected one-session global CatBoost return MSE skill is +0.17%, p=.579 and Holm p=1. Selected global 5-/20-session return models have negative MSE skill (-25.8% and -157.0%) and are worse than the zero-return benchmark under the recorded Holm family.
- Volatility model MSE skill is positive for selected global ElasticNet, but QLIKE skill is negative at 1 session and its 5-/20-session QLIKE comparisons do not survive Holm adjustment. Do not promote volatility results based on MSE alone.
- Some technical Logistic volatility-expansion models show adjusted log-loss improvements at 5 and 20 sessions; the 1-session technical model has negative Brier skill. Treat this as exploratory and require probability calibration, regime stability and independent period validation.
- Data scope remains limited: options chains, FII/DII, PCR, breadth, point-in-time constituents, corporate-action events and timestamped news were not verified as acquired. Global series timing/holiday alignment needs further review.

## Decision

**Phase 5 corrected-run gate: PASS for execution and target-window correction.**  
**Phase 7 statistical gate: CONDITIONAL / NOT FULLY PASSED.** Arithmetic skill and block-CI checks reproduce, but the tester has not yet completed full-precision HAC/Holm family verification, ARIMA artifact review, probability calibration, and global-source timing checks.  
**Overall research: NOT APPROVED FOR TRADING OR FINAL MANUSCRIPT SIGN-OFF.**

No trading strategy is recommended. No option-chain backtest, Paytm Money fee/slippage model, or live execution analysis is included in this prediction-only study.

## Developer instructions

1. Preserve this report and close remaining Phase 7 checks: compare full-precision model output and predictions for probability-loss/HAC differences, independently validate Holm correction family, and audit ARIMA predictions/metrics.
2. Audit auxiliary-series timestamp availability and holiday alignment; keep unavailable data families explicitly marked as not acquired.
3. Update README, RESULTS.md, PHASE_STATUS.md and ERROR_LOG.md on main with corrected run #49 evidence.
4. Do not call the study complete or design a live options strategy until Phase 7 passes. If remaining data families cannot be acquired within the bounded plan, record the limitation and finalize a prediction-only conclusion.


## Supplemental independent checks — 2026-10-14

- Independently recomputed the saved Holm adjustments within each task/horizon family: maximum absolute difference was below 1e-16.
- Independently recomputed ARIMA(1,0,0) return benchmark skill, HAC p-values and moving-block CIs from `reports/arima_predictions.csv`. Skill differences were below 5e-16; p-value differences below 3e-14; CI endpoint differences below 5e-16.
- Confirmed auxiliary features are joined with `merge_asof(..., direction="backward", allow_exact_matches=False)`, so same-date global closes are not used as if available at the NIFTY origin.
- Rechecked selected models' HAC p-values from the merged predictions; differences are effectively zero for selected models except technical Transformer 1-session direction, where the difference is about 4.2e-7 and does not affect its non-significant conclusion. A larger discrepancy observed among unselected sequence-model probabilities is small in absolute terms but should remain recorded.

Updated gate decision: ARIMA, Holm and selected-model HAC checks pass. Phase 5 execution/target-window gate passes. Phase 7 remains **CONDITIONAL** pending explicit reviewer agreement on scope and probability-calibration limitations; overall manuscript is not yet approved as a trading study.


## Final scoped gate update — 2026-10-14

- Recomputed decile expected calibration error (ECE) descriptively from saved OOS probabilities. Selected global CatBoost 1-session direction: ECE 0.016, Brier 0.2472, accuracy 54.08%. Selected technical Logistic volatility-expansion ECE: 0.184 (1 session), 0.053 (5 sessions), 0.040 (20 sessions). This is supplemental, not a preregistered endpoint; 1-session expansion probabilities are poorly calibrated and all results remain single-holdout estimates.
- Auxiliary features use backward as-of joins with same-date matches excluded. ARIMA benchmark skill, HAC p-values and block CIs were independently reproduced from its separate prediction file. Holm adjustments reproduce within 1e-16. Selected-model HAC p-values reproduce to numerical precision except technical 1-session Transformer direction (difference ~4.2e-7), which is non-significant either way.

**Tester disposition for the bounded prediction-only study: PASS WITH SCOPE LIMITATIONS.** The target-window defect is resolved; loss metrics, block CIs, HAC tests, Holm corrections and ARIMA benchmark are reproducible. No robust return/direction edge is demonstrated. Volatility-expansion results remain exploratory. This does not approve a trading strategy, options backtest, live deployment, or claims about unacquired options/FII-DII/PCR/breadth/news data. The manuscript may be finalized as a prediction-only mixed/negative-results study with these limitations explicit.
