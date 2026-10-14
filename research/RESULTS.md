# Results and evidence register

Version: NIFTY-PRED-1.0  
Last updated: 2026-10-14  
Status: Corrected run #49 completed; preliminary empirical results independently checked; tester gate remains open.

## Canonical run

- Workflow: [run #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128)
- Commit: `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`
- Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`
- Data: 4,901 NIFTY daily rows, 2007-01-02 to 2026-10-13. Seven global series passed validation (S&P 500, Nasdaq, Nikkei 225, Hang Seng, CBOE VIX, India VIX proxy, US 10-year yield proxy). USD/INR, gold and WTI were rejected; NSE endpoint returned no recognized rows. Historical options, FII/DII, PCR, breadth and timestamped news sentiment were not acquired.
- Output: 491 merged metric rows; 143 OOS-evaluated rows; 208 compute-budget-blocked rows; 139,289 prediction rows.
- Target-window check: zero null target dates in OOS predictions; zero target dates on/before origin; where both dates occur in the OOS origin calendar, offsets match the declared 1/5/20-session horizon.
- Independent arithmetic: 91 regression skill metrics reproduced with max absolute discrepancy ~2.04e-9. 140 non-ARIMA block confidence intervals reproduced with max discrepancy <8e-9. HAC p-values independently reconstructed within ~1.24e-5; this did not alter interpretation of selected return/direction results. ARIMA predictions are in a separate artifact and were not included in the merged prediction arithmetic check.

## Selected model results

| Target | Horizon | Selected feature set/model | OOS n | Result | Adjusted inference |
|---|---:|---|---:|---|---|
| Log return | 1 | Global CatBoost | 980 | MSE skill +0.17% vs zero-return | p=.579; Holm p=1.000; no gain shown |
| Log return | 5 | Global HistGradientBoosting | 976 | MSE skill -25.8% | Holm p=.0256; worse than baseline |
| Log return | 20 | Global HistGradientBoosting | 961 | MSE skill -157.0% | Holm p=.000054; worse than baseline |
| Direction | 1 | Global CatBoost | 980 | Accuracy 54.08%; balanced accuracy 51.96% | raw p=.0288; Holm p=.5478; not significant |
| Direction | 5 | Global Random Forest | 976 | Accuracy 50.20% | Holm p=.8206 |
| Direction | 20 | Global Random Forest | 961 | Accuracy 49.12% | Holm p=.3061 |
| Volatility | 1 | Global ElasticNet | 980 | MSE skill +10.8%; QLIKE skill -19.8% | Holm p=.3165 |
| Volatility | 5 | Global ElasticNet | 976 | MSE skill +33.1%; QLIKE skill +6.3% | Holm p=1.000 |
| Volatility | 20 | Global ElasticNet | 961 | MSE skill +38.3%; QLIKE skill +29.9% | raw p=.0355; Holm p=.2843 |
| Volatility expansion | 1 | Technical Logistic | 980 | Accuracy 55.31%; Brier skill -12.1% | Holm log-loss p=.000487; calibration/Brier concern |
| Volatility expansion | 5 | Technical Logistic | 976 | Accuracy 61.99%; Brier skill +6.9% | Holm log-loss p=.0233; exploratory |
| Volatility expansion | 20 | Technical Logistic | 961 | Accuracy 65.76%; Brier skill +13.0% | Holm log-loss p=.0109; exploratory |

## Interpretation and limitations

Return forecasting does not show robust useful skill; the 1-session direction result does not survive multiplicity correction. Volatility MSE gains do not translate into accepted QLIKE gains after correction. Volatility-expansion classification has encouraging log-loss comparisons in some horizons, but is not a validated trading signal. The run uses one chronological 80/20 holdout and two expanding CV folds. Global timing/holiday alignment remains to be reviewed. Options chains, FII/DII, PCR, breadth, timestamped news and corporate-action features were not verified as acquired. No transaction-cost/slippage or broker execution simulation was conducted.

## Gate

Phase 5: run complete, tester gate open. Phase 7: arithmetic checks passed; remaining multiplicity/ARIMA/calibration review. Phase 8: tester must issue explicit PASS/FAIL. Phase 9: manuscript remains provisional. No model or options strategy is approved.


## Additional validation and calibration

- Independent tester disposition: [PASS WITH SCOPE LIMITATIONS](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md).
- Holm adjustment was independently recomputed for each task/horizon family; maximum absolute difference was below 1e-16.
- ARIMA(1,0,0) return benchmark checks from its separate prediction artifact reproduced skill and HAC p-values to numerical precision. MSE skill vs zero-return was -0.35% at 1 session (p=.492), +0.11% at 5 sessions (p=.935), and +1.07% at 20 sessions (p=.842); confidence intervals include zero at all horizons.
- Supplemental decile ECE (descriptive, not preregistered): selected global CatBoost 1-session direction ECE 0.016; selected technical Logistic volatility-expansion ECE 0.184 / 0.053 / 0.040 at 1/5/20 sessions. The 1-session expansion probabilities are poorly calibrated. Single-holdout results do not establish regime stability.
- Auxiliary global features use backward as-of joins with same-date matches excluded. This reduces same-date look-ahead risk, but source coverage and market-calendar alignment remain limitations.

## Final scoped conclusion

The bounded prediction-only study passes the independent tester gate with scope limitations. No robust return/direction advantage is demonstrated. Some volatility-expansion log-loss comparisons are promising but exploratory. No options trading strategy, Paytm Money fee/slippage model, option-chain backtest or live deployment was evaluated.
