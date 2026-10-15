# Independent tester report — expanded NIFTY prediction run #62

**Review date:** 2026-10-15 (Asia/Kolkata)  
**Tester branch:** `research/pdf-audit-tester-final`  
**Developer run:** [GitHub Actions #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792)  
**Artifact:** `nifty-prediction-reports-38604064792.zip`  
**Artifact SHA-256 (GitHub metadata):** `14c9d6fc1bcb0f00ff28e708cb10c6cab9b378e5e60ff31f6e66aaa5e977172b`

## Disposition

**PASS WITH SCOPE LIMITATIONS.** The run #62 artifact resolves the target-date defect from run #60. The tester independently reproduced the primary arithmetic and inferential outputs from the artifact. This is a bounded forecasting-method screen, not exhaustive literature replication and not evidence that a model is a profitable trading signal.

## Checks performed on run #62 artifact

1. **Workflow / artifact provenance — PASS.** GitHub reports the research job completed successfully. The artifact exists and its SHA-256 is `14c9d6fc1bcb0f00ff28e708cb10c6cab9b378e5e60ff31f6e66aaa5e977172b`. Data acquisition, validation, target/scoring tests, feature matrix, technical/global model catalogues, ARIMA, report merge, status summary, and artifact upload completed.
2. **Prediction table integrity — PASS.** `predictions.csv` contains 471,735 rows and 11 columns. There are zero null target_date values and zero null origin_date, actual, baseline, prediction, task, horizon, model, or feature_set values. Missing `probability_positive` values are expected for regression tasks.
3. **Target horizon alignment — PASS for exported origins/targets.** For all 471,735 rows, the sorted union of observed origin/target dates yields target offsets exactly equal to each row's recorded 1-, 5-, or 20-session horizon. This resolves T-01 from run #60 for the current artifact. The 20 weekend-dated source observations still need exchange-calendar/source verification.
4. **Regression metric reproduction — PASS.** Recomputed MAE and RMSE from raw prediction rows for all 485 `OOS_EVALUATED` metric records. All observation counts matched exactly; maximum absolute MAE discrepancy was (4.66\times10^{-10}), and maximum RMSE discrepancy was (7.45\times10^{-9}). MSE skill matched to numerical precision for nearly all rows. A few large price-level MLP rows show up to 0.0078125 absolute skill discrepancy despite baseline-MSE absolute differences around (10^{-10}), consistent with floating-point cancellation at large level magnitudes; do not use these rows for headline claims without stable higher-precision calculation.
5. **HAC p-values and block-bootstrap intervals — PASS.** Recomputed paired-loss definitions from the saved predictions for all 485 OOS-evaluated rows, then reproduced the repository's HAC test and 300-replicate circular block bootstrap with the frozen seeds/block lengths. Maximum absolute p-value discrepancy was (3.17\times10^{-5}); maximum relative interval-bound discrepancy was (3.67\times10^{-6}) for the lower bound and (5.85\times10^{-7}) for the upper bound. The small differences are limited to floating-point/CSV precision; the sign and inferential interpretation agree.
6. **Holm multiplicity correction — PASS.** Independently recomputed Holm-adjusted p-values from the raw p-values within each task × horizon family. Maximum discrepancy from the exported `p_holm` was (1.11\times10^{-16}). Recomputing Holm from independently reconstructed raw p-values also agreed within (3.43\times10^{-8}).
7. **QLIKE formula and sign — PASS WITH INTERPRETATION NOTE.** Independently recomputed QLIKE for all 102 volatility metric rows using the repository's documented variance-form formula and (10^{-8}) lower floor. Maximum absolute differences from exported model QLIKE and improvement were (3.06\times10^{-5}); baseline QLIKE difference was (2.14\times10^{-14}). The extreme elastic-net h=5 score (about (1.31\times10^9)) is explained by near-floor predictions paired with non-negligible realized volatility, which incurs a very large penalty under the formula; it is not by itself evidence of an arithmetic defect. There are 34 zero actual volatility labels; the floor treatment is implemented and must remain documented. For global XGBoost h=1, QLIKE is -8.767421 versus baseline -8.431197, giving improvement +0.336225 and exported Holm p approximately (1.96\times10^{-9}). This remains a narrow, metric-specific forecasting result, not a universal winner.
8. **Classification interpretation — PASS WITH LIMITATION.** Some classification rows have weak balanced accuracy and/or worse proper scores than prevalence baselines. Accuracy alone is not sufficient; report class balance, log loss and Brier skill. Do not claim a classifier winner from accuracy or a small two-sided p-value alone.
9. **Data/source scope — LIMITATION ACCEPTED.** The 20 weekend-dated target observations remain flagged for source/calendar verification. Global daily series passed schema checks, but strict point-in-time availability relative to the NIFTY close is not fully established. Historical options/PCR, FII/DII, breadth, point-in-time news, corporate actions and point-in-time constituent history are not verified in the current dataset. Some PDF methods are only inventoried or blocked, not replicated.

## Scientific conclusion supported

- **No robust return/direction winner is established** by this bounded model comparison.
- The one-session global XGBoost volatility row shows favourable QLIKE score difference and adjusted significance under the configured family; it is a narrow volatility forecast result and should not be generalized to other targets, horizons, regimes, or trading profitability.
- A large price-level fit does not imply return predictability.
- The work is a bounded screening comparison, not exact replication of every uploaded paper or an exhaustive feature-source study.
- No trading strategy, options execution, transaction-cost, slippage, brokerage, or live deployment conclusion is in scope.

## Closure and developer instructions

**NIFTY-PRED-1.0 expanded model audit: PASS WITH SCOPE LIMITATIONS.** No further model-catalogue expansion or parameter tuning is warranted under the frozen plan. Preserve the source-timing, weekend-calendar, and missing-feature-family limitations in the manuscript and status page. Any follow-on research must have a separately versioned, preregistered question; this prediction study does not authorize strategy development.
