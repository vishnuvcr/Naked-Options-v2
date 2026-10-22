# Research questions — QE-NOB-1.0

## Main question
Can a constrained QuantEvolve search identify a long-premium NIFTY 50 option-buying process that remains net profitable after Paytm Money charges, statutory fees, realistic slippage and chronological out-of-sample tests?

## Primary questions
1. Can underlying directional signals correctly time option premium moves enough to offset theta, delta, gamma, implied volatility and execution friction?
2. Which fixed signal families—opening-range breakout, trend/VWAP continuation, opening-gap continuation/fade, pullback-reclaim/reject and intraday volatility expansion—have positive net after-cost expectancy on identified NIFTY options?
3. Does a predicted underlying move exceed the option-implied premium breakeven after time decay and costs often enough to justify buying calls, puts, straddles or strangles?
4. Do IV percentile, India VIX, realized volatility, option volume and OI changes improve out-of-sample results beyond simple price/volume baselines?
5. Are any apparent benefits robust to chronological splits, Holm adjustment, block-bootstrap intervals, placebo controls, multiple slippage levels and different volatility regimes?
6. How much of gross return is consumed by brokerage, STT, GST, stamp duty, exchange/SEBI/IPFT charges and adverse fills?
7. What data-quality gates (historical bid/ask, exact contract mapping, missing candles, rolling ATM strike mapping, lot-size schedules) are required to support an executable rather than merely indicative backtest?

## Null hypotheses
- H0-A: every candidate's expected net P&L is non-positive under the primary after-cost specification.
- H0-B: evolution does not improve untouched OOS results over simple preregistered baselines.
- H0-C: apparent edge is explained by data/selection bias, costs, regime concentration or extreme-outcome dependence.

## Explicit exclusions
No short-premium strategies, spreads containing short legs, futures-only final strategy, arbitrary manually curated post-hoc rule, test-set parameter optimization or live order placement.
