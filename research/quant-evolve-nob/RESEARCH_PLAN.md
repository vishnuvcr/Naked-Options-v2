# QuantEvolve Fresh Research: Naked NIFTY Option Buying (QE-NOB-1.0)

**Research ID:** QE-NOB-1.0  
**Initiated:** 2026-10-22  
**Active phase:** Phase 1 — protocol and data-source qualification  
**Operating mode:** developer-led; user explicitly said no tester  
**Repository:** https://github.com/vishnuvcr/Naked-Options-v2

## Fresh-start declaration

This is a new study. Existing prediction-study and prior option-buying findings are not training labels, priors, performance benchmarks, seed strategies, or evidence for this study. Old artifacts remain in repository history for auditability only. This study has its own source cache, strategy catalogue, run IDs, reports, preregistration and error log. Any reused software utility must be independently tested against this protocol. No prior strategy result is presumed positive or negative.

## Aim

Discover whether any predeclared, evolvable long-premium NIFTY options strategy produces positive, reproducible, risk-adjusted net returns after realistic Paytm Money brokerage, statutory/exchange charges, slippage and execution constraints.

The study considers standalone long calls, standalone long puts, and—only as a distinct long-volatility family—long ATM straddles/one-step OTM strangles. No short-option leg, credit spread, hedge-sale, martingale, averaging-down, unbounded compounding or discretionary intervention is permitted.

## Core research questions

1. Do directional NIFTY signals have enough next-bar/next-session edge to overcome option premium, theta, implied volatility, spread and fees?
2. Which bounded signal families—opening-range breakout, trend/VWAP continuation, gap follow-through/reversal, pullback-reclaim, and implied-versus-forecast-move filters—survive chronological out-of-sample testing?
3. Does an evolutionary search improve out-of-sample net P&L over fixed simple baselines, or merely overfit its search universe?
4. Which expiry/moneyness/time-to-expiry combinations provide a reasonable trade-off between cost, delta exposure, theta decay and liquidity?
5. Do volume, open interest, IV, India VIX, realized volatility, global leads, DII/FII activity, market breadth and scheduled event features add incremental out-of-sample value when timestamps and coverage permit?
6. Can any candidate remain profitable under conservative fill/slippage and fee stress tests, across separate chronological periods, and with uncertainty quantified?
7. If licensed, time-aligned bid/ask/order-book evidence is absent, can a candidate only be classed as exploratory rather than executable/profitable?

## Study boundary and fixed phases

This study has eight phases and will stop at Phase 8; no endless discovery loop or unplanned parameter fishing.

### Phase 1 — Protocol, source and implementation qualification
Freeze hypotheses, candidate families, data schema, transaction-cost schedule, chronological partitions, search budget and pass/fail gates. Check official contract specifications and Paytm Money charges; build audit files before backtesting.

### Phase 2 — Data acquisition, cache and integrity
Use DhanHQ Data API expired-option/rolling data as the primary paid source because the user has a subscription/token. Retrieve fresh data into data/cache/quant_evolve_nob_v1/, isolated from all earlier caches. The documented rolling endpoint has minute OHLC, spot, IV, volume and OI and supports at most 30 days per call over a rolling historical window; verify actual returned fields, timeframe and coverage at runtime. Acquire NIFTY underlying intraday/daily candles and India VIX where available. Try free official NSE/NSE Indices/BSE/RBI/FRED/public sources and openly licensed Kaggle/Hugging Face/Zenodo/GitHub datasets to extend or cross-check. Composite data only after timestamp, instrument, units, contract identity and overlap consistency pass. Cache manifests, checksums, source/licence notes and every failed call. Never make up prices, interpolate option fills, silently substitute contracts or publish restricted raw quotes.

### Phase 3 — Point-in-time feature panel and executable contract map
Align on Asia/Kolkata timestamps and NSE sessions. Point-in-time features only: underlying candles, range/breakout, gap, returns/momentum, VWAP if intraday volume supports it, moving averages, realized volatility, India VIX, IV, OI/volume changes, put-call/ATM-relative measures and pre-open global-market leads with conservative release/close-time lags. Use exact option identity where the source exposes contract details; rolling ATM-relative data may only be used if fixed-strike continuity within a trade is demonstrably reconstructable. Record expiry calendar and lot size effective on each date. Missing/ambiguous strike or expiry means no trade, never a guessed match.

### Phase 4 — Benchmarks and cost/execution accounting
Implement zero-signal/no-trade, always-buy eligible single-leg, fixed-time ATM call/put baselines, simple underlying-direction rules, and long-volatility always-buy controls. All trades simulate entry at the next executable bar, never the signal bar's close. Use one contract lot with historical contract-master lot size. Model entry and exit slippage, Paytm Money brokerage, exchange transaction charges, GST, SEBI/IPFT fees, stamp duty, date-effective STT, and any expiry/exercise costs. Primary cost assumption must be verified against the current broker tariff before numerical execution. Fixed tests stress 0/25/50/100/200 bps adverse slippage and ₹10/₹20 brokerage per executed order unless official tariff calls for a revised pre-result freeze. Never label OHLC midpoint/close as a guaranteed executable price; if historic spread/depth is absent, report limitations and fail the executable-quote gate.

### Phase 5 — Bounded QuantEvolve discovery
Use a constrained, deterministic strategy grammar rather than arbitrary generated code. Search fixed predicates and parameters in a maximum 600 unique candidates / 25 generations / fixed seeds (seed values in config); each candidate is evaluated only on training/validation folds. Families: (A) 5/15/30-minute opening-range breakouts with fixed buffers; (B) trend/VWAP/EMA continuation; (C) opening-gap follow-through and fade; (D) pullback-reclaim/reject; (E) volatility expansion with realized-versus-implied movement filter; (F) intraday regime filter using India VIX/realized volatility; (G) OI/volume/IV confirmation only if verified. Directional candidates choose CALL or PUT from signal sign. A separate long-straddle/strangle family tests predicted move relative to cost-adjusted breakeven, not merely volatility-classification accuracy. Evolution objectives are constrained to net P&L, drawdown, profit factor, stability and turnover; no in-sample Sharpe-only ranking.

### Phase 6 — Nested chronological validation and statistical tests
Freeze chronology before search: earliest valid data for training, rolling/expanding walk-forward inner folds for evolution/model selection, then chronological validation. Reserve the latest fully covered block as untouched OOS; do not view its metrics while evolving. If source coverage cannot support this split, return DATA-LIMITED rather than backfill synthetic data. Report trade count, weekly/monthly net P&L, win rate, expectancy, profit factor, Sharpe/Sortino, drawdown, loss tails/CVaR, exposure, turnover, costs and result concentration. Use HAC uncertainty and moving-block bootstrap; adjust the complete prespecified comparison family with Holm. Correct for search/selection effects; run shuffled-label or time-block placebo controls and ablation tests. Never reuse the final OOS segment for tuning.

### Phase 7 — Robustness, execution and data sensitivity
Repeat only frozen leading candidates across 0/25/50/100/200 bps slippage; ₹10/₹20 per order brokerage (or frozen, verified alternative); stricter spreads if quotes permit; alternate but prespecified stop/target controls; separate time-of-day, trend/range, high/low IV and event/non-event regimes. Reject results dependent on a single day/month, very small trade count, look-ahead, quote substitution, one extreme winner, one expiry/lot regime, or one cost setting. An OOS result is not independent just because a single holdout is partitioned after the fact.

### Phase 8 — Manuscript and decision
Produce reproducible code/config, cached-data manifest/hashes, machine-readable ledgers, charts, tables, audit appendix, error log, source/citation register and a structured manuscript. Final statuses: (1) PASS for prospective paper testing only, if all preregistered profitability, data and stability gates pass; (2) NO-GO if valid data show candidates are unprofitable/unstable; (3) DATA-LIMITED / INCONCLUSIVE if quotes, contract identity, coverage or licensing prevent a test. Historical backtest profitability alone never authorizes live deployment. Only one bounded run/correction cycle per material defect; then accept limitation or stop.

## Primary hypotheses and promotion gates

- H1, net profitability: at least one frozen candidate has positive mean and median net P&L after costs, positive lower 95% block-bootstrap confidence bound on net expectancy, and Holm-adjusted primary-family p < 0.05.
- H2, consistency: positive net P&L in each of two untouched chronological OOS subperiods defined before viewing outcomes, with at least 150 eligible trades overall and at least 40 in each subperiod where coverage permits; fewer observations means insufficient evidence.
- H3, execution stress: candidate expectancy remains positive at the prespecified base and 100-bps adverse-slippage stress; 200 bps is reported as a tail stress. If spreads/depth are not historically available, candidate is not called execution-validated.
- H4, comparative value: net performance exceeds both no-trade and a simple buy-every-eligible equivalent strategy after costs, with the paired difference reported and multiple-tested correctly.
- H5, search integrity: walk-forward selection only, no final-OOS tuning, no feature leakage, no future contract/calendar information used before it was known.
- H6, drawdown/risk: report maximum drawdown and 95/99% expected shortfall; no promotion if a small subset of extreme gains accounts for most total profit or if drawdown exceeds a predeclared 25% of marked strategy equity.
- H7, data gate: at least 90% coverage of the prespecified eligible opportunity panel, at most 0.5% conflicting duplicate rate after explainable deduplication, no unknown-strike/expiry fill substitution, and a clear raw-source/hash trail. If bid/ask history cannot be obtained, execution-quality gate remains explicitly limited even if row coverage passes.

## Costs and contract conventions

Use Paytm Money, not Dhan brokerage, to estimate transaction costs. Start with the official public tariff and calculator plus the exchange circulars current at the study date; freeze the full formula and a unit-tested example before evaluating any strategy. The official NSE STT page lists 0.15% on sale of an option from 1 April 2026, calculated on premium, and 0.15% on exercise for the buyer where applicable; historical trades use rates effective on their transaction date. Include GST on applicable charges, exchange/SEBI/IPFT fees, stamp duty on buy turnover, brokerage per order and conservative spread/slippage. Do not double-count costs and do not assume a stop-loss fills at its trigger price.

## Source hierarchy

1. DhanHQ expired options, historical candles, option chain/depth and instrument metadata (licensed token secret, never log or publish it).
2. Official NSE/NSE Indices reports and circulars, BSE as relevant, SEBI, RBI and government statistical releases.
3. Free historical/open datasets (Kaggle, Hugging Face, Zenodo, GitHub) only after provenance, licence, timestamp, adjustments and source identity pass review.
4. Research papers/preprints and educational videos for candidate generation only; backtested performance claims from articles/videos are not treated as evidence without reproducible data/methods and independent recomputation.

## Current scope status

This commit creates the protocol only. No new option data has yet been acquired under QE-NOB-1.0, no strategy has been run, and no profitability finding exists. The protocol does not claim any previous finding was replicated or overturned.

## Change control

Any change to hypothesis, strategy universe, cost model, data period, split boundary, optimization budget or promotion thresholds requires a dated protocol amendment before inspecting new outcome metrics; the error/interaction log must record why. No hidden chain-of-thought is stored; repository logs record actionable decisions, operations, results and errors only.
