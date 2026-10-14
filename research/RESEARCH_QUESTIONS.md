# Research questions and preregistered hypotheses

Version: NIFTY-PRED-1.0  
Freeze date: 2026-10-14

## Primary questions

RQ1. Do any prespecified predictors improve NIFTY 50 next-session, 5-session or 20-session return forecasts over zero-return and historical-mean / autoregressive benchmarks on the untouched chronological holdout?

RQ2. Which model families forecast closing index levels, returns, direction and forward volatility best, using metrics aligned to each target rather than one blended accuracy score?

RQ3. Do volatility, volume, India VIX, external markets, currencies, commodities, rates, market breadth, options/F&O positioning, FII/DII flows, news and sentiment add incremental predictive information beyond lagged NIFTY OHLCV, when availability and publication times are verifiable?

RQ4. How does predictive performance change by horizon and by regimes defined using training-only thresholds?

RQ5. Are any benchmark-relative gains practically material, statistically distinguishable from zero after dependence and multiple-testing adjustments, calibrated, stable, and reproducible on genuinely unseen observations?

## Hypotheses and decision criteria

- H1 (direction): a candidate improves final-holdout Brier/log loss and has statistically defensible benchmark-relative skill. Accuracy alone is insufficient. Null: no predictive improvement over majority/base-rate and logistic/zero-return benchmarks.
- H2 (returns): at least one candidate yields positive OOS R-squared versus the historical-mean forecast and lower MSE than benchmark, with confidence interval and dependence-aware test supporting an improvement after correction. Null: no incremental return-forecast skill.
- H3 (levels): models can reduce level MAE/RMSE versus price persistence, but this is only a level-prediction finding and is not evidence of return/direction predictability unless those separate tests pass.
- H4 (volatility): lagged realized volatility and India VIX may improve forward volatility and expansion forecasts versus historical-volatility baselines. Null: no gain in QLIKE / MAE or proper probability scores.
- H5 (feature augmentation): a family adds incremental value only if a prespecified ablation improves validation metrics and retains a gain on holdout. Availability and release-lag checks are mandatory.
- H6 (regime stability): a candidate's performance is not considered robust merely because the aggregate holdout is positive; direction and effect must not rely entirely on one small regime or one crisis subperiod.
- H7 (generalization): rankings remain reasonably stable across walk-forward folds and nearby calendar blocks. Large variance in ranks, sign reversals or holdout collapse count against promotion.

## Model-selection and significance safeguards

1. The latest 20% of eligible observations is held out before fitting; the boundary, sample count, and input hashes are saved.
2. Hyperparameters and ensemble weights use only the earlier development data and walk-forward folds.
3. Primary metrics are declared per target in RESEARCH_PLAN.md. There is no singular "accuracy" for a mixed set of regression/classification/volatility targets.
4. A family-wise Holm correction is applied to the predefined benchmark-comparison family per primary target/horizon; raw and adjusted p-values are retained.
5. Inference uses block bootstrap / HAC because financial observations and overlapping 5-/20-session targets are serially dependent.
6. All metrics must specify positive/negative orientation and target units. Index-level R² does not substitute for OOS return R².
7. Forecast availability is timestamped and only uses inputs known at the prediction cut-off.

## Acceptance gates

- Gate A — valid data: reproducible NIFTY index history, duplicate/missingness/timezone review, data hashes and source provenance.
- Gate B — valid comparison: benchmark metrics match hand-computed test cases; at least one baseline prediction is generated.
- Gate C — no leakage: all feature transformations fitted on train folds; targets strictly future; global close data lagged; no post-origin data.
- Gate D — robust evidence: holdout improvement, uncertainty, corrected significance and stability are jointly reported.
- Gate E — independent reproducibility: separate tester branch independently recomputes core metrics and checks result claims.

These are falsifiable hypotheses. If no candidate passes, the correct conclusion is "no robust predictive skill found under this protocol", not failure to complete research.
