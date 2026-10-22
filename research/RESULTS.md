# Results and evidence register

Version: NIFTY-PRED-1.0  
Last updated: 2026-10-22  
Status: Defect-driven rerun #39699761966 completed successfully; prediction-only scope remains closed with accepted limitations. Run #49 is retained as historical independent-tester evidence, not as the latest metrics.

## Latest completed run — 2026-10-22

- Workflow: [run #39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966) — **success**.
- Commit: `cecac3a63878d3a189c94b143f875bcb9be33983`.
- Artifact SHA-256: `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`.
- Sanitized aggregate report: [nifty_prediction_run_39699761966_summary.json](../reports/nifty_prediction_run_39699761966_summary.json).
- Data: 4,906 Dhan daily rows, 2007-01-02 to 2026-10-21; target validation PASS; 20 weekend-dated rows flagged. Seven external series passed (S&P 500, Nasdaq, Nikkei 225, Hang Seng, CBOE VIX, India VIX, US 10-year yield proxy). NSE official retrieval failed; USD/INR and gold failed OHLC checks; WTI had non-positive OHLC and was excluded.
- Output: 647 metric rows; 299 OOS candidate comparisons; 296 CV-pass rows; 52 explicitly compute-budget-blocked rows; 291,886 merged OOS prediction rows including ARIMA outputs.
- Holdout: final chronological 20%; return sample sizes 981 / 977 / 962 for 1 / 5 / 20 sessions. Four expanding folds for tabular models, two for sequence models, with horizon purging.
- Multiple testing: a supplementary Holm audit across all 299 OOS candidate comparisons found 85 significant differences: 77 significantly worse than benchmark and eight improvements. All eight improvements were one-session volatility-proxy QLIKE comparisons; the validation-selected global ExtraTrees model was among them.
- Strongest selected result: global ExtraTrees one-session volatility proxy, QLIKE loss difference model-minus-baseline = -0.315597, 95% moving-block bootstrap CI [-0.422981, -0.210145], HAC p=1.75e-9, Holm p=4.26e-7 across 299 comparisons. MAE was 0.003952 vs baseline 0.003967; RMSE 0.005305 vs 0.005550.
- Return/direction conclusion: no robust selected-model return or direction edge. Global CatBoost return MSE skill was -0.26%, +0.85%, -1.70% at 1 / 5 / 20 sessions; all adjusted p-values were 1.0. Global level forecasts were significantly worse than persistence at all three horizons after Holm correction across the 33 selected primary outcomes.
- Volatility-expansion h20 technical Logistic result (accuracy 66.43%, Brier skill +0.133) did not survive Holm correction across 33 selected primary outcomes (adjusted p=.0582); exploratory only.
- The sequence-model metadata initially said eight epochs, but estimator objects were set to three. Source metadata and a regression assertion are corrected; the actual predictions used three epochs. The empty/headerless CSV merge fix passed its regression test and the end-to-end merge succeeded in this run.
- Limits: one holdout only; no independent-period replication; no validated options/FII-DII/PCR/breadth/news/corporate-action inputs; no trading strategy, brokerage, spread, slippage or broker execution simulation. This is not a trading recommendation.

### Selected outcomes

| Target | Horizon | Selected model | OOS n | Key result | Adjusted inference |
|---|---:|---|---:|---|---|
| Return | 1 | Global CatBoost | 981 | MAE 0.005788 vs zero 0.005803; MSE skill -0.26% | Holm (33 primary) p=1.000 |
| Return | 5 | Global CatBoost | 977 | MAE 0.013623 vs zero 0.013730; MSE skill +0.85% | Holm p=1.000 |
| Return | 20 | Global CatBoost | 962 | MAE 0.027171 vs zero 0.026252; MSE skill -1.70% | Holm p=1.000 |
| Direction | 1 | Global CatBoost | 981 | Accuracy 53.01%; balanced accuracy 52.82%; Brier skill -0.0009 | Holm p=1.000 |
| Volatility proxy | 1 | Global ExtraTrees | 981 | QLIKE difference -0.3156; 95% CI [-0.4230, -0.2101] | Holm (299 candidate tests) p=4.26e-7 |
| Volatility expansion | 20 | Technical Logistic | 980 | Accuracy 66.43%; Brier skill +0.133 | Holm (33 primary) p=.0582 |
| Level | 1 / 5 / 20 | Global ElasticNet / ElasticNet / Ridge | 981 / 977 / 962 | MSE skill vs persistence -16.4% / -8.9% / -34.5% | Significantly worse after correction |

\n## Historical run #49 (superseded for current metrics by run #39699761966)

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


## Historical tester disposition for run #49 — 2026-10-14 (does not cover rerun #39699761966)

The independent tester now reports **PASS WITH SCOPE LIMITATIONS** for the bounded prediction-only study: [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md). Holm corrections were independently reproduced within 1e-16. ARIMA(1,0,0) benchmark skill, HAC p-values and block confidence intervals reproduced from the separate ARIMA predictions file. The selected 1-session global direction model has ECE 0.016; the selected technical volatility-expansion model has descriptive ECE 0.184/0.053/0.040 at 1/5/20 sessions, so its 1-session probabilities are poorly calibrated.

Scoped conclusion: no robust return/direction edge was demonstrated. Volatility-expansion findings remain exploratory. This is not a trading strategy; options chains, broker fees/slippage, Paytm Money execution and live deployment were not tested.


## Closure record

The nine-phase study is closed for the bounded prediction-only scope. The tested model/data set did not establish a robust return/direction edge. Unavailable options/FII-DII/PCR/breadth/news inputs and lack of brokerage/slippage/execution tests prohibit strategy-level claims.


## Latest closure record — 2026-10-22

The defect-driven rerun completed successfully and the empty-result CSV merge was verified end-to-end. The bounded prediction-only conclusion is: no robust return/direction edge; one selected one-session volatility-proxy result survives familywise Holm correction and is retained for independent replication. The latest rerun has not received a new independent tester-branch review, per the instruction not to create that branch. No options strategy is approved, and the options data gate remains `BLOCKED_NO_VERIFIED_CONTRACT_DATA`.
