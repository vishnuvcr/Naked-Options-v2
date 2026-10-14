# Option-buying validation plan — OPT-BUY-1.0

**Created:** 2026-10-14  
**Branch:** research/option-buying-validation  
**Status:** protocol frozen before option-P&L inspection; data acquisition and empirical analysis pending  
**Relationship to NIFTY-PRED-1.0:** separate, user-approved scope amendment. The original nine-phase prediction-only study remains closed and unchanged.

## 1. Research question

Does the existing NIFTY volatility-expansion classifier provide incremental, positive after-cost value when used as an alert to enter a same-session long straddle or long strangle on the next NSE session, relative to buying the same structure on every eligible session?

This is a study of option-premium outcomes, not a claim that volatility-classification accuracy implies profits. Directional Calls/Puts are excluded because the prior study did not establish reliable direction skill after multiple-testing correction.

## 2. Background evidence from the completed prediction study

The prior out-of-sample study reported 5-session volatility-expansion accuracy of 61.99% and Brier skill of +6.9% (Holm-adjusted log-loss p=.0233), and 20-session accuracy of 65.76% and Brier skill of +13.0% (adjusted p=.0109). Both were exploratory single-holdout classifier findings. The study did not test option prices, bid/ask spreads, theta, brokerage, STT, or execution costs. It did not establish an options edge. The 1-session classifier had negative Brier skill and poor calibration. These statistics motivate, but do not validate, this separate test.

## 3. Aim and objectives

**Aim:** determine whether the prespecified volatility-expansion alert produces a reproducible, economically positive option-buying result under conservative transaction-cost assumptions.

**Objectives**
1. Acquire point-in-time NIFTY index-option intraday bars from DhanHQ historical rolling-options API, subject to authentication, schema, coverage and licensing checks.
2. Rebuild the prior technical Logistic volatility-expansion classifier using only features available at the close of signal session t.
3. Fix alert thresholds from chronological development-period out-of-fold scores; do not tune a threshold using the option test period.
4. Compare same-session next-day ATM long straddles and one-step OTM long strangles with an always-buy-the-same-structure benchmark.
5. Recompute P&L after Paytm Money brokerage and exchange/statutory charges; stress adverse slippage at 0, 25, 50 and 100 basis points per option-premium side and brokerage at ₹10 or ₹20 per executed order.
6. Calculate effect sizes, moving-block uncertainty intervals and a four-comparison Holm correction for the primary comparison family.
7. Record missing data and failed requests; never forward-fill option prices or fabricate a trade.
8. Produce machine-readable reports, an auditable results manuscript and a post-acquisition developer/tester review.

## 4. Hypotheses

- H1: At the primary cost setting (₹10 per executed order and 50 bps adverse slippage per premium side), alert-filtered straddle/strangle trades have higher mean daily net return on option premium deployed than buying the same structure every eligible day.
- H2: Alert-filtered daily net returns are positive after all modeled costs at the primary setting.
- H3: Any apparent advantage remains positive under 100 bps adverse slippage and in both chronological halves of eligible evaluation dates.

All four combinations (5-session alert × straddle, 5-session × strangle, 20-session × straddle, 20-session × strangle) are prespecified as the primary family. H1 is not confirmed by raw p-values alone: confidence intervals, Holm-adjusted p-values, sample counts, costs and stability all matter. H2/H3 are robustness gates, not extra chances to choose a winner after seeing results.

## 5. Data scope and source hierarchy

**Primary target/features:** validated Dhan daily NIFTY-50 cache already used by NIFTY-PRED-1.0. External/global features are excluded for reproducing the original technical classifier.

**Primary option source:** DhanHQ API v2 POST /charts/rollingoption. Its documentation describes rolling expired-option history up to five years, at most 30 calendar days per request, 5-minute candles and ATM-relative strikes with OHLC, IV, volume, OI and spot. Source: https://dhanhq.co/docs/v2/expired-options-data/

**Free-source checks:** official NSE derivatives reports: https://www.nseindia.com/all-reports-derivatives. The existing data catalog lists public Hugging Face collections; one has a CC-BY-NC licence and another has an unverified “other” licence. They are not substituted into this test unless licence, provenance, timestamp integrity and redistribution rights are verified. Dhan credentials are accessed only through GitHub Actions secret DHAN_ACCESS_TOKEN, never committed or logged.

**Historical interval:** only origins in the prior study's final chronological 20% holdout are included. Options are requested for the next NSE session after each origin. Effective dates are the common intersection of the original holdout and valid options records. If the common window falls outside Dhan's rolling history, that gap is reported and not synthetically filled.

**Contract identity limitation:** the API exposes relative strike series rather than a stable contract ID/expiry in each row. Therefore this first test holds positions intraday only. It matches the actual numeric strike at entry and exit and never treats a rolling ATM-relative series as the same contract across days. Multi-day option holding is out of scope unless stable contract identity, expiry and lot-size history are independently established.

## 6. Fixed strategy definitions

- Signal time: after the NIFTY cash-session close at origin t, using only features available by that close.
- Entry session: the next observed NIFTY session, t+1.
- Entry: 5-minute bar timestamped 09:20 IST and its open premium.
- Exit: same-session 5-minute bar timestamped 15:25 IST and its close premium, intended to exit before the session ends. If either exact timestamp or a required quote is missing, skip and count the date; do not select a convenient alternate bar.
- Structure A, long ATM straddle: buy one call and one put at the same available numeric strike closest to entry-time spot.
- Structure B, long one-step OTM strangle: buy one call at the next available strike above ATM and one put at the next available strike below ATM.
- Alert models: Technical Logistic regression for volatility expansion at horizons 5 and 20 sessions, with the same technical feature family, median imputation/scaling pipeline, class weighting and seed as the original experiment. Development labels must mature before the 80% chronological cutoff.
- Threshold: 75th percentile of development-only, purged chronological out-of-fold probabilities. Thresholds are calculated independently per horizon. The test period never changes them.
- Benchmark: buy the identical structure on every test date for which entry and exit premiums are valid. Model-filtered variants make no trade on non-alert dates; return contribution is zero on those dates.
- No overnight position, no short options, no compounding and no live orders. This avoids multi-day rolling-contract identity errors and limits trade risk to premium debit plus modeled charges.

## 7. Quote quality and trade matching

Only rows with positive numeric strike, spot, entry open and exit close are eligible. Unix timestamps are converted to Asia/Kolkata. Quote identity is session date + timestamp + option type + actual numeric strike, not a relative label such as ATM+1. At exit, the selected entry strike must exist for the same option type on the same date. Duplicate rows are deduplicated only after consistency checks; disagreements are counted as a warning. Missing data are not interpolated. API raw responses stay in the workflow cache and are excluded from public repository commits and artifacts.

## 8. Costs and execution sensitivity

Primary brokerage: ₹10 per executed unique order per the current Paytm Money F&O FAQ (https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web); ₹20/order is a sensitivity case. A two-leg entry and two-leg exit equals four executed orders.

Modeled charges:
- STT on option-premium sell turnover: 0.10% up to 2026-03-31 and 0.15% from 2026-04-01, per official NSE schedule: https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax
- Options stamp duty on buyer turnover: 0.003%.
- SEBI turnover fee: ₹10/crore (0.0001%).
- NSE option-premium transaction charge: current 0.0355201% approximation applied consistently over the historical sample as a standardized cost assumption. Historical exchange tariffs varied, so this is not exact historical contract-note reconstruction. Source catalogue: https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies and https://nsearchives.nseindia.com/content/circulars/FA73061.pdf
- GST: 18% on brokerage, exchange transaction and SEBI fees.
- Adverse slippage: entry premium is increased and exit premium decreased by each of 0, 25, 50 and 100 bps per side. The Dhan rolling endpoint does not provide historical bid/ask here, so this is sensitivity, not observed spread.
- Lot sizing: premium-point returns are primary. Currency outputs use a clearly labelled date-based NIFTY lot-size proxy: 50 before 2024-04-26; 25 from 2024-04-26 to 2024-11-19; 75 from 2024-11-20 onward. The API's missing contract expiry/introduction metadata means this proxy may be wrong around lot-size transitions and is not verified contract-master lot sizing.

Primary setting is ₹10/order and 50 bps; sensitivities use both brokerage values and all four slippage values. All rates are recorded in the run manifest.

## 9. Chronological model and statistical methods

- Reuse the fixed 80/20 chronological origin cutoff of NIFTY-PRED-1.0. Train only on development observations whose forward-volatility-expansion labels are fully known before test cutoff; retain the original horizon gap.
- For each horizon, fit median imputation, StandardScaler and LogisticRegression(C=0.1, class_weight='balanced', max_iter=1500, random_state=20261014), matching the existing technical model.
- Thresholds use 4-fold TimeSeriesSplit predictions with origin-time purge; no holdout labels choose them.
- Primary metric: mean daily net return on option premium deployed, zero on no-trade dates; compare alert strategy against always-buy benchmark on paired valid dates. Secondary metrics: per-trade return, counts, trade frequency, win rate, mean/median net P&L per lot proxy, profit factor and drawdown.
- Use moving-block bootstrap for 95% confidence intervals of means and paired alert-minus-benchmark difference, preserving time dependence. Generate a two-sided null-centred moving-block-bootstrap p-value. Use a 5-session block for 5-session alerts and a 20-session block for 20-session alerts.
- Apply Holm correction across the four primary comparisons at primary cost setting. Sensitivity settings are robustness tests, not extra candidate-selection opportunities.
- Compare first and second chronological halves of eligible option dates without retuning.
- Minimum of 100 executed alert trades per candidate is required for a positive gate; otherwise candidate is INCONCLUSIVE.

## 10. Acceptance gates and stop rule

Finite stages: (A) source/credential/schema gate, (B) target/options date and quote coverage gate, (C) strategy computation and formula tests, (D) cost/statistical robustness, (E) independent developer/tester gate, then stop.

A candidate can be described as a research-supported paper-trading candidate only if (a) at least 100 signal trades occur, (b) mean net daily return is positive and its 95% block-bootstrap CI lower bound is above zero, (c) paired outperformance versus always-buy survives Holm correction at p<.05, (d) net performance stays positive at 100 bps slippage and in both predeclared time halves, and (e) independent tests find no critical data, math or leakage defect. Missing data means BLOCKED; low power means INCONCLUSIVE. A passing backtest still does not authorize live deployment: a separate prospective paper-trading period, broker contract-note verification and risk approval would be required.

If the API is unavailable, data are sparse, or costs overwhelm any edge, stop with a reproducible blocked/negative conclusion. Do not expand strategies, retune thresholds or loop beyond these gates.

## 11. Required outputs

- This frozen protocol.
- Sanitized acquisition manifest with requested windows, request counts, success/failure summaries and hashes; no tokens/raw quotes.
- Alert signal file with origin/trade date, horizon, probability, development-only threshold and alert decision.
- Per-trade outcome ledger without raw quotes or strike IDs; aggregate costs/results, sensitivity, block-bootstrap intervals, raw/adjusted p-values.
- Results, phase status, README, experiment log, error log and interaction log.
- Unit tests for quote identity, no-lookahead purging, fee/sign formulae, missing-bar skip, bootstrap determinism and Holm adjustment.
- Separate developer and tester branches only after empirical acquisition attempts complete. The tester must independently recompute key quantities and pass, request corrections or block.

## 12. Reproducibility and provenance

Record Git SHA, Actions run ID, original daily-data hash, classifier horizons/cutoff/threshold source, options request window and schema status, coverage, strategy rules, costs, slippage, package versions, seeds and result hashes. Dhan tokens are read only from DHAN_ACCESS_TOKEN. Errors log status/error class without credentials. Raw response JSON remains in workflow cache and is never explicitly staged, committed or uploaded. Aggregate reports are versioned.
