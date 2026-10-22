# Results and evidence register

Version: NIFTY-PRED-1.0  
Last updated: 2026-10-22  
Status: Earlier results retained as history; latest run #39699761966 held for target-label correction and independent review.

## Latest audit and corrective status — 2026-10-22

- [Prior workflow #39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966) completed at workflow level; artifact SHA-256 `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`.
- Its 291,886-row `predictions.csv` contained 798 rows with missing `target_date` but populated numeric forecast values: volatility h5=60, h20=360; volatility expansion h5=54, h20=324. Cause: the h5/h20 forward standard deviation skipped missing returns at the dataset boundary.
- Affected h5/h20 volatility and volatility-expansion results from the prior run are not accepted for final inference. The code fix is in [commit e8133a5](https://github.com/vishnuvcr/Naked-Options-v2/commit/e8133a582cbe6c06ce46514f871d1393fc142f6f); [corrective run #39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) was in progress at last check.
- The one-session global ExtraTrees volatility result was independently reproduced from the prior artifact: n=981, QLIKE loss difference −0.31559705, HAC p=1.74758e−9, 95% block CI [−0.42298094, −0.21014542], Holm p=4.26410e−7 across 299 comparisons. No missing target dates occur in that h1 cell. It remains a replication candidate only, not a trading signal.
- Return/direction forecasts have not established a robust edge. Truly untouched future-period replication is not available from the short current data extension. See [audit record](FRESH_PREDICTION_AUDIT_2026-10-22.md) and [tester branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-independent-tester).

**Current gate: HOLD** pending corrected workflow output and independent review. No strategy approved.

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


## Exploratory within-holdout sensitivity and score distribution — 2026-10-22

The selected global ExtraTrees h1 volatility-proxy model was evaluated in four equal-count consecutive slices of the same final holdout. This is retrospective sensitivity analysis, not independent-period replication.

| Slice | Origin dates | n | Mean model-minus-baseline QLIKE | 95% moving-block CI | HAC p | Holm p across four slices |
|---|---|---:|---:|---:|---:|---:|
| 1 | 2022-11-04 to 2023-11-01 | 246 | −0.2640 | [−0.4370, −0.1046] | 0.001492 | 0.003871 |
| 2 | 2023-11-02 to 2024-10-25 | 245 | −0.3516 | [−0.5893, −0.0959] | 0.006660 | 0.006660 |
| 3 | 2024-10-28 to 2025-10-21 | 245 | −0.2770 | [−0.4582, −0.1261] | 0.000793 | 0.003174 |
| 4 | 2025-10-23 to 2026-10-19 | 245 | −0.3700 | [−0.6041, −0.1589] | 0.001290 | 0.003871 |

All four mean differences are negative in this diagnostic. However, the daily loss differential is skewed: its median is +0.00662 and 50.97% of days have positive model-minus-baseline loss (worse model score), despite the mean of −0.31560. The 10% winsorized mean remains negative (−0.10137). Therefore the selected average QLIKE result is not consistent daily superiority; it is sensitive to the magnitude of tail outcomes. The within-holdout splits do not replace a future untouched-period replication.

These checks were calculated from run #39699761966's saved predictions, before the corrected artifact was available. The artifact-level reproduction utility is [`research/audits/audit_nifty_predictions.py`](audits/audit_nifty_predictions.py).


Supplemental figure: [`volatility_qlike_subperiod_sensitivity.svg`](figures/volatility_qlike_subperiod_sensitivity.svg).


## QLIKE interpretation caveat — 2026-10-22

The pipeline trains the h1 volatility model on absolute next-session log return and then squares the target, forecast and baseline before applying QLIKE. This makes the scored realized quantity (r_{t+1}^2), but the model forecast is the square of a fitted absolute-return estimate, not a separately trained conditional-variance estimate. Therefore the reported improvement is metric-specific evidence for a variance-scaled volatility proxy; it should not be described as a fully calibrated conditional-variance forecast without additional validation.


## Corrected run #39704420478 — results reconciliation (2026-10-22)

The corrective GitHub Actions workflow completed successfully on `research/fresh-prediction-developer` at commit `e8133a582cbe6c06ce46514f871d1393fc142f6f`. The downloaded artifact reports 277,633 prediction rows, 647 metric rows, 299 OOS-evaluated model/task/horizon comparisons, and **zero missing target dates**. Data quality validation passed for 4,683 NIFTY daily rows (2007-09-17 to 2026-10-19); one weekend-dated observation (2025-02-01) is preserved and flagged for calendar/source cross-check.

### Forecast conclusions from the corrected artifact

- **Returns:** No statistically robust selected return edge. Selected CatBoost 5- and 20-session MSE skill versus baseline was +1.12% and +4.57%, respectively, but raw p-values were 0.361 and 0.275 and Holm-adjusted p-values were 1.0. The selected 1-session Transformer had negative MSE skill (−1.78%) and Holm p=0.556.
- **Direction:** Selected accuracy was 52.99% at one session (balanced accuracy 50.0%), 53.86% at five sessions (balanced accuracy 50.0%), and 57.91% at 20 sessions (balanced accuracy 50.03%). Holm-adjusted p-values were 1.0 across these selected rows; no useful directional edge is established.
- **Level:** Selected Elastic Net forecast RMSE was 190.97, 422.23 and 857.03 index points at horizons 1, 5 and 20. MSE skill versus the historical-mean baseline was negative (−7.97%, −7.86%, −22.34%). Statistical loss-difference tests were significant after correction for some horizons, but they indicate the model is worse than the baseline (positive model-minus-baseline loss difference); they are not evidence of predictive benefit.
- **Volatility proxy:** Best global h1 comparison by adjusted p-value was CatBoost, n=936, MAE=0.004048, RMSE=0.005375, MSE skill +7.45%, mean model-minus-baseline loss difference −0.33325, 95% CI [−0.46212, −0.23389], raw p=1.66e−9, Holm p=3.33e−8 across the 299 OOS comparisons. Global ExtraTrees was also positive in this artifact (MSE skill +7.34%, Holm p=4.87e−8). These are model-selection comparisons within the screened catalogue, not independent-period replication. The scored QLIKE transformation squares an absolute-return forecast; interpret as a variance-scaled volatility-proxy score, not a fully calibrated conditional variance estimate.
- **Model diagnostics:** Some volatility MLP/Ridge rows have extreme loss-difference magnitudes, suggesting near-zero or otherwise unstable predicted scales under the QLIKE transformation. These rows must be investigated before generalizing from the overall candidate family. The selected Elastic Net h1 volatility row itself does not show the strongest result; selection-by-validation and best OOS score must not be conflated.
- **Data scope:** This run used the cached NIFTY close/volume series and global index sources in the manifest. The manifest's cross-source checks are empty; this run does not establish official NSE/BSE reconciliation, complete DII/FII/news/corporate-action coverage, or option-contract data sufficiency.

### Decision

The missing-target-date defect is fixed for this artifact and the pipeline completed. The prediction research has **not** established a robust return/direction edge. The volatility-proxy result is promising within the screened historical holdout but requires a genuinely untouched future-period replication and calibration/robustness checks. No trading strategy or options P&L is approved. User requested developer-only continuation; no tester branch/report is required.
