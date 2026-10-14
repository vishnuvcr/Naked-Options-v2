# Results and evidence register

Version: NIFTY-PRED-1.0  
Last updated: 2026-10-14  
Status: **Corrected run #49 completed; preliminary empirical results verified; independent gate remains open.**

## Canonical corrected run

- Workflow: [run #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128)
- Branch / commit: `research/developer-review` / `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`
- Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`
- Artifact: 6.47 MB ZIP; contains 23 report/log files.
- Experiment rows: 491 merged metric rows; 143 OOS-evaluated rows; 208 explicitly blocked by compute budget; 139,289 prediction rows across tasks and feature sets.
- Input NIFTY daily data: 4,901 rows, 2007-01-02 through 2026-10-13. External validated series: S&P 500, Nasdaq, Nikkei 225, Hang Seng, CBOE VIX, India VIX proxy, and US 10-year yield proxy. USD/INR, gold and WTI were rejected by validation; NSE endpoint returned no recognized rows. Historical option chains, FII/DII, PCR, breadth and timestamped news sentiment were not acquired.
- Corrected target-window check: zero null target dates among OOS prediction rows; zero target dates on/before origin date; for target dates represented in the OOS origin calendar, session offsets match declared horizon (1/5/20). The corrected builder and boundary regression test passed in run #49.
- Independent metric arithmetic: recomputed benchmark-relative MSE skill and variance-scale QLIKE skill across 91 regression model/task/horizon/feature-set entries; maximum absolute discrepancy from stored skill metrics was approximately 2.04e-9. Recomputed moving-block confidence intervals across 140 non-ARIMA OOS rows; maximum absolute discrepancy was below 8e-9. HAC p-values were numerically close, with maximum difference about 1.24e-5; differences were concentrated in small probability-loss means and did not alter the interpretation of the selected return/direction results. ARIMA predictions are stored in a separate artifact and were not included in the merged prediction CSV arithmetic check.

## Selected-by-validation results (holdout is not used for selection)

| Target | Horizon | Feature set / selected model | OOS n | Main result | Multiplicity-adjusted inference |
|---|---:|---|---:|---|---|
| Log return | 1 session | Global / CatBoost | 980 | MSE skill vs zero-return baseline +0.17% | p=0.579; Holm p=1.000; no evidence of gain |
| Log return | 5 sessions | Global / HistGradientBoosting | 976 | MSE skill -25.8% | Holm p=0.0256; significantly worse than baseline under the recorded within-task/horizon family |
| Log return | 20 sessions | Global / HistGradientBoosting | 961 | MSE skill -157.0% | Holm p=0.000054; significantly worse than baseline under the recorded family |
| Direction | 1 session | Global / CatBoost | 980 | Accuracy 54.08%; balanced accuracy 51.96% | raw p=0.0288; Holm p=0.5478; not significant after correction |
| Direction | 5 sessions | Global / Random Forest | 976 | Accuracy 50.20% | Holm p=0.8206; no useful evidence |
| Direction | 20 sessions | Global / Random Forest | 961 | Accuracy 49.12% | Holm p=0.3061; no useful evidence |
| Volatility | 1 session | Global / ElasticNet | 980 | MSE skill +10.8%; QLIKE skill -19.8% | Holm p=0.3165; not accepted |
| Volatility | 5 sessions | Global / ElasticNet | 976 | MSE skill +33.1%; QLIKE skill +6.3% | Holm p=1.000; not accepted |
| Volatility | 20 sessions | Global / ElasticNet | 961 | MSE skill +38.3%; QLIKE skill +29.9% | raw p=0.0355; Holm p=0.2843; not significant after correction |
| Volatility expansion | 1 session | Technical / Logistic | 980 | Accuracy 55.31%; Brier skill -12.1% | Holm p=0.000487 for paired log-loss difference, but Brier skill is negative; calibration/probability quality needs further audit |
| Volatility expansion | 5 sessions | Technical / Logistic | 976 | Accuracy 61.99%; Brier skill +6.9% | Holm p=0.0233 for paired log-loss improvement within the recorded family; exploratory, not a trading signal |
| Volatility expansion | 20 sessions | Technical / Logistic | 961 | Accuracy 65.76%; Brier skill +13.0% | Holm p=0.0109 for paired log-loss improvement within the recorded family; exploratory, not a trading signal |

**Important interpretation:** the correction resolves the partial-forward-window defect; it does not prove the research is finished. Return forecasts show no robust useful skill; the global direction result does not survive multiplicity correction. Volatility results depend on the metric: MSE improvements do not translate into statistically accepted QLIKE improvements after correction. Volatility-expansion classification has promising log-loss comparisons, but is not yet validated as a stable, calibrated or tradable signal.

## Scope limitations

- The run uses a single chronological 80/20 development/holdout split; model selection uses two expanding chronological CV folds. The holdout is used for evaluation, not model selection.
- Full model catalogue is evaluated for 1-session return/direction; other target/horizon cells use the predeclared core screen. 208 excluded model/task cells are explicitly labelled `BLOCKED_COMPUTE_BUDGET`.
- Global data timing/holiday alignment needs more review. No historical option-chain, FII/DII, PCR, market breadth, point-in-time constituent, corporate-action event or timestamped news features were verified as acquired.
- No option strategy, transaction-cost/slippage simulation or broker-specific execution analysis was conducted. This is prediction research only, not a deployable strategy.
- Results are from a single OOS period and should not be presented as proof of future performance.

## Gate decision

- Phase 5: corrected bounded experiments completed; **awaiting independent tester approval**.
- Phase 7: arithmetic and window checks independently reproduced; remaining statistical family and robustness review required before final pass.
- Phase 8: tester must review run #49 artifacts and return an explicit pass/fail.
- Phase 9: manuscript may be finalized only after tester disposition and limitations are incorporated.
