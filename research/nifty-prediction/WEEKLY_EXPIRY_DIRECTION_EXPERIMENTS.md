# Weekly-expiry NIFTY 50 direction research

**Purpose:** Investigate whether NIFTY 50 spot direction into the upcoming weekly index-options expiry can be predicted better than simple baselines. This is a focused extension of the existing daily prediction work; it does not change the existing research plan retroactively.

**Target definition (must be frozen before training):**
- At a predeclared forecast cutoff, predict whether the NIFTY 50 spot close on the actual upcoming NIFTY weekly index-options expiry session will be above or below the spot close at the forecast cutoff.
- Forecast cutoff is a model input, not a free choice: evaluate separate fixed cutoffs (e.g. previous session close, expiry-day open, and a fixed intraday timestamp) as distinct tasks.
- If an exchange holiday shifts expiry, use the official expiry calendar and the actual expiry session.
- Label: UP if expiry close > cutoff reference price; DOWN if expiry close < reference price; FLAT if equal at available precision. Report FLAT separately and predeclare handling.
- Never mix spot target labels with futures or option premium outcomes.

## Candidate hypotheses

1. **Regime specialist ensemble:** train separate calibrated classifiers for trending, range-bound, high-volatility, and transition regimes, with regimes computed from past-only data.
2. **Global-to-India lead-lag:** use only global index, currency, crude, and gold data that had actually arrived by the forecast cutoff; compare against NIFTY-only features.
3. **Breadth divergence:** add point-in-time constituent breadth, sector returns, advance/decline, and equal-weighted index proxies where historical constituents and timestamps are available.
4. **Options-implied expectation:** use point-in-time NIFTY option-chain IV, skew, term structure, ATM straddle-implied move, and changes in OI/volume. OI is not assigned a simplistic directional sign.
5. **Change-point and transition risk:** estimate shifts in return/volatility/correlation using past-only features; test whether lowering confidence during transitions improves calibration.
6. **Multi-horizon agreement:** combine next-session, three-session, and expiry-horizon probabilities only after each has been calibrated on earlier chronological data.
7. **Baseline residual correction:** fit a second-stage model to baseline errors using training data only; retain it only if rolling out-of-sample gains are stable.
8. **Intraday opening pressure:** for intraday cutoffs only, add opening gap, first 15/30-minute returns, range, volume and acceptance/rejection of key levels. Never use these inputs for a prior-close forecast.
9. **Event-aware calendar:** encode known-at-the-time macro/RBI events, expiry proximity, and scheduled corporate events; do not use retrospective event classifications.
10. **Selective calibrated forecast:** calibrate probabilities on a chronological calibration window; evaluate coverage and accuracy among predeclared confidence bands and allow an explicit UNCERTAIN output.

## Experimental protocol

1. **Data inventory first:** inspect cached repository data and workflows. Inventory target dates, expiry calendar, spot bars, point-in-time global features, breadth, options-chain snapshots, and event timestamps. Mark every unavailable feature as unavailable; do not synthesize historical snapshots.
2. **Freeze forecast cutoffs and labels:** build separate datasets per cutoff, each with a timestamped feature-availability contract and an explicit expiry-session label.
3. **Baselines:** majority class, unconditional historical UP rate, previous available direction, NIFTY-only regularized logistic regression, and a simple tree-based model. All models share identical eligible dates per comparison.
4. **Chronological validation:** expanding/rolling walk-forward evaluation; keep expiry weeks together when splitting. Reserve the most recent eligible block as untouched final evaluation. Use nested validation for tuning and avoid random shuffles.
5. **Ablation:** test each new feature family alone and then in the combined model. Compare to NIFTY-only baselines to measure incremental value.
6. **Metrics:** balanced accuracy, accuracy, Matthews correlation, confusion matrix, Brier score, log loss, calibration, confidence intervals using dependence-aware resampling, and performance by regime/year/cutoff. Report the sample count and class balance.
7. **Multiple testing:** disclose the full candidate count and use a predeclared correction or nested model-selection approach. Do not promote the best of many candidates solely on the final test block.
8. **Go/no-go:** keep a candidate only if its gain is repeatable across walk-forward folds, uncertainty is compatible with a real improvement, calibration is acceptable, and no leakage is found. Otherwise report no demonstrated edge.
9. **Artifacts:** save the dataset schema/provenance, cutoff/label definitions, feature availability matrix, per-fold predictions, metrics JSON/CSV, plots, tests, and manuscript updates in the repository.
10. **Execution is out of scope for this prediction phase.** A prediction edge does not establish an options-buying or selling edge; option premiums, expiry payoff, slippage, taxes, brokerage, liquidity, and Paytm Money costs require a separate later evaluation.

## Critical limitations

- Daily OHLC data alone cannot validate an intraday cutoff or point-in-time options-chain hypotheses.
- Historical options-chain data must include timestamps and contract metadata. Current chain snapshots cannot be backfilled as historical evidence.
- If weekly expiry history or schedule changes are not documented from an authoritative source, mark affected labels uncertain and exclude them from primary results.
- The previously reported daily next-session benchmark is not evidence of weekly-expiry prediction skill.
- No result or strategy should be described as successful until the experiment actually runs and its outputs are inspected.

## Completion rule

Run this as a bounded set of ten hypothesis families, with feature-availability gates. Stop after each family has a documented result or a documented blocker, then provide a combined conclusion. Do not loop indefinitely or silently skip failed experiments.
