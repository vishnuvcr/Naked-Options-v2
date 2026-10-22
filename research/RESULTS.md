# Results and evidence register

Version: NIFTY-PRED-1.0  
Last updated: 2026-10-22  
Status: Prior bounded study results remain historical; latest run #39699761966 is under a defect-driven correction hold pending independent review.

## Latest audit and corrective status — 2026-10-22

- Prior run: [Actions #39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966), commit `cecac3a63878d3a189c94b143f875bcb9be33983`, artifact SHA-256 `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`.
- Artifact reviewed locally: `predictions.csv`, 291,886 rows. 798 rows had missing `target_date` with otherwise populated forecast fields: volatility h5=60, volatility h20=360, volatility-expansion h5=54, volatility-expansion h20=324.
- Root cause: h5/h20 forward-return standard deviation skipped NaNs, permitting partial boundary windows. The prior run's successful workflow did not detect this label-integrity issue. Multi-session volatility and volatility-expansion results from that run must not be accepted as final.
- Code correction: commit `e8133a582cbe6c06ce46514f871d1393fc142f6f`, adding `skipna=False` and tail-window regression assertions. [Corrective run #39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) was in progress at the last status check. Its final status and artifact are not yet claimed.
- The previously reported one-session global ExtraTrees volatility-proxy result (MAE 0.0039515 versus baseline 0.0039671; QLIKE −8.7402 versus −8.4246; mean loss difference −0.3156; block-bootstrap 95% CI approximately [−0.4230, −0.2101]) is not in the subset of rows with missing target dates. Still, the previous result is not promoted beyond a replication candidate until its corrected artifact arithmetic and Holm family are independently checked.
- Return/direction forecasts continue to show no robust edge in the reported holdout. The one-session volatility result is not a trading signal. No options P&L, brokerage/slippage simulation, or strategy approval is implied.
- A genuinely independent future-period replication is not yet available from the current data horizon. Historical folds have already participated in screening; using them again must be labeled retrospective sensitivity analysis, not untouched replication.

**Current gate:** HOLD final sign-off pending run #39704420478 and [independent tester review](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-independent-tester). See [audit detail](FRESH_PREDICTION_AUDIT_2026-10-22.md) and [error log](ERROR_LOG.md).

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

Phase 5: PASS. Phase 7: PASS for bounded prediction-only scope. Phase 8: tester PASS WITH SCOPE LIMITATIONS. Phase 9: manuscript complete. Phase 2 literature depth and Phase 6 source/regime coverage remain partial and are explicitly accepted limitations. No options strategy is approved.


## Final tester disposition — 2026-10-14

The independent tester now reports **PASS WITH SCOPE LIMITATIONS** for the bounded prediction-only study: [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md). Holm corrections were independently reproduced within 1e-16. ARIMA(1,0,0) benchmark skill, HAC p-values and block confidence intervals reproduced from the separate ARIMA predictions file. The selected 1-session global direction model has ECE 0.016; the selected technical volatility-expansion model has descriptive ECE 0.184/0.053/0.040 at 1/5/20 sessions, so its 1-session probabilities are poorly calibrated.

Scoped conclusion: no robust return/direction edge was demonstrated. Volatility-expansion findings remain exploratory. This is not a trading strategy; options chains, broker fees/slippage, Paytm Money execution and live deployment were not tested.


## Closure record

The nine-phase study is closed for the bounded prediction-only scope. The tested model/data set did not establish a robust return/direction edge. Unavailable options/FII-DII/PCR/breadth/news inputs and lack of brokerage/slippage/execution tests prohibit strategy-level claims.
