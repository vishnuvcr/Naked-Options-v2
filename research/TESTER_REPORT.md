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

### HIGH-001 — Level target/unit mismatch (BLOCKING)

Artifact level predictions/actuals are in index-point units (mean actual around 22,519), but current build_feature_matrix.py defines target_log_close_h = log(close.shift(-h)) and run_experiments.py references target_log_close. A log-price target should be around 10, not 22,000. Exact run source must be identified. Do not accept level scores until run commit and target schema agree.

Required fix: include target schema/units in every manifest; assert target scale; use target_close with persistence close_t, or target_log_close with persistence log_close_t, consistently. Add tests and rerun level experiments.

### HIGH-002 — Volatility target and QLIKE semantics (BLOCKING)

target_future_vol is a standard deviation / absolute-return proxy, while QLIKE is described as a variance forecast loss. Confirm the squared transformation or use a loss appropriate to standard deviation. QLIKE results are not accepted until actual and forecast are both variance-scale, positive, and baseline uses same scale. Displayed p=0 is numeric underflow, not literal zero; format as p<1e-6.

### HIGH-003 — Recompute and multiplicity (BLOCKING for significance)

Independently recompute paired losses from predictions, check HAC lag against horizon overlap, verify Holm correction family against the plan, and compare adjusted p-values. Nominal significance remains exploratory until reproduced.

### MEDIUM-004 — Source/feature availability

Global features include S&P 500, Nasdaq, Nikkei, Hang Seng, India VIX, CBOE VIX and US 10-year yield. Same-date closes are excluded, but timing and holiday alignment need review. USD/INR, gold and WTI were rejected; historical options, FII/DII, PCR, breadth and timestamped news were not acquired.

### MEDIUM-005 — Classification baseline

Verify baseline probabilities use development data only and Brier/log-loss skill use the same valid observations. Report balanced accuracy and calibration alongside raw accuracy.

### LOW-006 — Calendar

Twenty weekend-dated rows are preserved and flagged. Cross-check special sessions; do not delete solely based on weekend dates.

## Preliminary, not accepted

- One-session return models show no useful gain over zero-return in this run.
- One-session direction results are close to chance and do not survive Holm adjustment.
- Some volatility models appear promising, but QLIKE target-scale mismatch blocks acceptance.
- Level results are blocked by target/unit mismatch.
- ARIMA(1,0,0) has no significant gain over zero-return in the reported 1/5/20-session results; recompute independently.

## Gate decision

**Phase 5: FAIL pending target reconciliation and independent metric reproduction.  
Phase 6: partial; global feature ablation ran, regime segmentation and source families remain incomplete.  
Phase 7: open; significance/QLIKE audit not passed.  
Phase 8: report submitted, not approved.  
Phase 9: manuscript remains provisional.**

## Developer instructions

1. Identify exact commit/code bundle that generated run #45. Resolve level target schema and units; add target-unit tests.
2. Ensure QLIKE uses realized variance and forecast variance, or replace it with a scale-appropriate loss. Correct p-value formatting.
3. Recompute candidate/baseline metrics from predictions, including paired losses, block confidence intervals, HAC tests and Holm correction.
4. Check global feature availability timing, overlapping target-date dependence and classification baselines.
5. Run tests and regenerate artifacts; update RESULTS.md, ERROR_LOG.md, PHASE_STATUS.md and README.md. Resubmit for tester review; do not progress to publication gate before passing.