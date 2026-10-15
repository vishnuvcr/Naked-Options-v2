# Independent tester report — expanded NIFTY prediction run #62

**Review date:** 2026-10-15 (Asia/Kolkata)  
**Tester branch:** `research/pdf-audit-tester-final`  
**Developer run:** [GitHub Actions #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792)  
**Artifact:** `nifty-prediction-reports-38604064792.zip`  
**Artifact SHA-256 (GitHub metadata):** `14c9d6fc1bcb0f00ff28e708cb10c6cab9b378e5e60ff31f6e66aaa5e977172b`

## Disposition

**PASS FOR TARGET-DATE INTEGRITY AND CORE METRIC REPRODUCTION; FINAL STATISTICAL SIGN-OFF WITHHELD.**

This report directly inspects the run #62 artifact, rather than carrying forward the earlier run #60 findings unchanged. Run #60's failure remains part of the historical record. The run #62 artifact resolves the reported null-target-date defect. However, some volatility-score outputs are pathological and the complete HAC / block-bootstrap inferential pipeline has not been independently recomputed from raw predictions. Do not claim unqualified scientific sign-off.

## Checks performed on run #62 artifact

1. **Workflow / artifact provenance — PASS.** GitHub reports the research job completed successfully. The artifact exists and its SHA-256 is `14c9d6fc1bcb0f00ff28e708cb10c6cab9b378e5e60ff31f6e66aaa5e977172b`. The job completed data acquisition, target validation, target/scoring tests, feature-matrix construction, technical/global model catalogues, ARIMA, report merge, status summary, and report upload.
2. **Prediction table integrity — PASS.** `predictions.csv` contains 471,735 rows and 11 columns. There are **zero null target_date values** and zero null origin_date, actual, baseline, prediction, task, horizon, model, or feature_set values. Missing `probability_positive` values are expected for regression tasks; the field is not applicable to all rows.
3. **Target horizon alignment — PASS for exported origins/targets.** For all 471,735 prediction rows, mapping the sorted unique observed origin/target dates to session indices gives target offsets exactly equal to the recorded 1-, 5-, or 20-session horizon. This directly resolves T-01's run #60 finding for this artifact. Calendar/session verification of the 20 weekend-dated source observations remains outstanding.
4. **Regression metric reproduction — PASS.** Recomputed MAE and RMSE from raw prediction rows for all 485 `OOS_EVALUATED` metric records. All counts matched exactly; maximum absolute MAE discrepancy was (4.66\times10^{-10}) and maximum RMSE discrepancy was (7.45\times10^{-9}). Recomputed MSE skill relative to the exported baseline matched almost all rows to numerical precision; a small number of price-level MLP rows showed discrepancies up to 0.0078125 in skill despite baseline-MSE absolute differences around (10^{-10}), consistent with floating-point cancellation at large level magnitudes. Those level rows should not be used for a headline claim without stable higher-precision calculation.
5. **Multiplicity adjustment — PASS for the exported family definition.** Independently recomputed Holm-adjusted p-values from the exported raw p-values within each task × horizon family. The maximum absolute discrepancy from `p_holm` was (1.11\times10^{-16}). This verifies the adjustment arithmetic and family grouping as encoded in the artifact; it does **not** independently validate the underlying HAC p-values.
6. **QLIKE sign convention — PASS for arithmetic direction, with output warnings.** For global XGBoost volatility h=1, QLIKE is -8.767421 versus baseline -8.431197 and the exported improvement is +0.336225, consistent with baseline-minus-model score. The corresponding exported Holm value is approximately (1.96\times10^{-9}). This is a metric-specific result, not a universal model winner or a trading signal.
7. **Volatility score quality — WARNING / INFERENCE BLOCKER.** Some OOS volatility rows emit extremely large positive QLIKE values (for example elastic-net at h=5 has QLIKE around (1.31\times10^9), with a correspondingly huge negative improvement). The artifact does not establish whether this reflects an edge-case target, a clipping convention, or an implementation issue. Recompute QLIKE directly from actual/predicted volatility with explicit positivity/zero handling and document the formula before using volatility rankings or claims. There are 34 zero actual volatility labels in the exported prediction rows; this edge case must be handled transparently.
8. **Classification interpretation — PASS WITH LIMITATION.** Accuracy is not sufficient to establish superiority; the export contains rows where balanced accuracy is near chance and log loss is worse than baseline. Report baseline-relative proper scores and class balance. Do not select a winner solely from accuracy.
9. **Independent inference scope — NOT COMPLETE.** The raw HAC p-values and moving-block confidence intervals have not all been independently recomputed from raw predictions in this check. Overlapping 5-/20-session targets and global close-time/holiday alignment remain limitations. Do not call the results confirmatory.

## Scientific conclusion supported

- No robust return/direction winner is established by the exported results.
- The one-session global XGBoost volatility row shows a favourable QLIKE score difference and a small exported Holm-adjusted p-value, but this remains metric-specific and provisional until QLIKE edge cases and the inferential pipeline are independently reproduced.
- The experiment is a bounded model screen, not exhaustive replication of every uploaded paper or feature family.
- The dataset lacks verified historical options/PCR, FII/DII, breadth, point-in-time news, corporate actions/constituent history, and fully audited global close-time alignment.
- No trading strategy or live execution conclusion is in scope.

## Required bounded follow-up

1. Recompute QLIKE from raw predictions for every volatility row, define treatment of zero actuals and floors, and add tests for finite/meaningful scores.
2. Independently recompute HAC p-values and block-bootstrap intervals for the declared primary rows/families, or explicitly label them unverified and remove confirmatory language.
3. Stabilize large price-level skill calculations or keep them descriptive only.
4. Update the manuscript and README only after those results are reconciled; do not expand the model catalogue or tune models during audit.

## Developer instructions

Resolve the QLIKE edge-case implementation, add deterministic regression tests, produce a defect-only rerun if needed, and submit the updated artifact for independent re-review. Preserve the run #60 report and this run #62 audit trail. Do not proceed to a new research question or any strategy development under NIFTY-PRED-1.0.
