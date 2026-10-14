# Independent tester report — expanded NIFTY prediction run #60

**Tester branch:** `research/pdf-audit-tester-final`  
**Audited developer commit:** `e93fe35d8bb11df65d1c466434d5401298c077ed`  
**Workflow:** [run #60](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38593936036) — completed successfully  
**Artifact:** `nifty-prediction-reports-38593936036.zip`  
**Artifact SHA-256:** `b601320f64ab8ec0c62f0a07e458287cba781eca73107f1b2c38beda140a8151`

## Disposition

**FAIL FOR FINAL SCIENTIFIC SIGN-OFF; workflow execution PASS.** The results are acquired and broadly interpretable, but one data-integrity defect and several inferential/reporting gates need correction before final closure. This is not a request to expand the model catalogue.

## Checks performed

1. **Workflow integrity — PASS.** The data acquisition, target validation, feature matrix, technical and global model catalogue, ARIMA benchmark, merge, summary and artifact-upload steps all completed successfully.
2. **Data provenance — PASS WITH LIMITATIONS.** Manifest identifies 4,901 Dhan NIFTY daily observations, 2007-01-02 through 2026-10-13, SHA-256 `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050`. Twenty weekend-dated observations are flagged, not independently verified as special sessions.
3. **Selected regression arithmetic — PASS on spot checks.** Recomputed from matching `feature_set` prediction rows: CNN technical return h=1 RMSE 0.00793967 and MSE skill +0.0008746; XGBoost technical return h=5 RMSE 0.01735158 and MSE skill +0.0200225; global Gradient Boosting return h=20 RMSE 0.03310045 and MSE skill +0.0333034. These agree with the exported headline metrics to displayed precision.
4. **QLIKE score-difference direction — PASS on spot check.** Global XGBoost volatility h=1 has QLIKE -8.767421 vs baseline -8.431197, so baseline-minus-model improvement is +0.336225. The corrected additive score-difference field has the expected sign.
5. **Paired-loss interpretation — PASS AS DOCUMENTED, NOT CONFIRMATORY.** The code computes model loss minus baseline loss. Negative means model loss is lower; positive means baseline is better. A two-sided p-value by itself is not an improvement claim. Example: global MLP direction h=1 has log loss 0.791031 vs baseline 0.691277, with positive mean loss difference 0.099754; its small p-value indicates worse performance, not an edge.
6. **Sequence configuration — PASS.** Run metadata and configured estimators indicate three epochs. Sequence target/horizon exclusions are explicitly marked compute-budget blocked.

## Blocking findings

### T-01 — Missing target dates in exported predictions (HIGH)

The merged `predictions.csv` has **1,260 null target_date values**. They occur in volatility and volatility-expansion long horizons (notably h=5 and h=20) across feature sets. These rows have numeric actuals/predictions, so the artifact does not prove which future session each outcome corresponds to. The manuscript and result summary must not claim complete target-date/horizon alignment until fixed.

**Required developer action:** inspect target-date construction in the feature-matrix/target builder; ensure each non-null target label has a matching future trading-session date; add a hard test that every OOS prediction with a non-null target has a non-null target date and target_date is strictly after origin_date at the correct 1/5/20-session offset. Rerun the bounded workflow and verify zero null target dates for evaluated rows. If the date cannot be reconstructed reliably, exclude affected rows and recompute all affected metrics, counts, tests and manuscript tables.

### T-02 — Direction / volatility-expansion classification outputs are not reliable enough for winner claims (HIGH)

Some classification rows have log loss far above the prevalence baseline and negative Brier skill, while accuracy can look attractive due to threshold/class prevalence. Example: global MLP direction h=1 log loss 0.7910 vs baseline 0.6913. This is a valid warning signal, not evidence of prediction. Do not label classification candidates as winners based on accuracy or small p-values.

**Required developer action:** ensure the results tables state proper-score and baseline comparisons and avoid a universal classifier winner. For volatility expansion, audit the target-date defect first, then recompute balanced accuracy, Brier, log loss and baseline metrics on valid rows. Any calibration analysis must be out-of-sample and reported as diagnostic.

### T-03 — Full significance-family reproduction still required (MEDIUM)

The code applies Holm within task/horizon groups over rows carrying OOS metrics. A few spot checks support arithmetic, but I did not independently reproduce every HAC p-value, moving-block interval and Holm family from all 485 evaluated rows. The study should call these results screening-level, not definitive statistical proof. Also verify that overlapping 5-/20-session targets are reflected in dependence assumptions.

**Required developer action:** add a reproducible independent validation script or a compact validation output that recomputes all metric rows with raw predictions and checks p-value direction, confidence intervals, family size and Holm-adjusted values. Do not tune models from this check.

### T-04 — Scope and source-timing limitations (MEDIUM)

Global daily series pass the configured schema validator, but that does not establish point-in-time availability relative to the NIFTY close. The twenty weekend-dated NIFTY observations remain unresolved. Options/PCR, FII/DII, breadth, point-in-time news and corporate actions are not acquired/verified.

**Required developer action:** retain these as limitations; do not claim comprehensive global-market or India microstructure coverage. No trading strategy is in scope.

## Conclusion supported at this gate

The available results support **no robust return/direction winner established**. Return headline rows have negligible or statistically unsupported skill. Some volatility metrics improve descriptively, but ranking depends on scoring rule and target-date integrity must be corrected before final reliance. Volatility-expansion is exploratory. No trading strategy is approved.

## Developer instructions

1. Fix T-01 first and add the target-date integrity assertion.
2. Recompute affected predictions, metrics, CIs, HAC p-values and Holm adjustments if any rows change.
3. Update the run results, manuscript, README, phase status, experiment log and error log with the new workflow/artifact hashes and exact row counts.
4. Resubmit a new artifact for independent review. Do not widen the scope or begin options-strategy work.
