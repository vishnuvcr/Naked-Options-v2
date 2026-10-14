# OPT-BUY-3.0 — Entry × exit criteria research protocol

**Version:** OPT-BUY-3.0  
**Created:** 2026-10-14 (Asia/Kolkata)  
**Developer branch:** `research/option-entry-exit-developer`  
**Status:** protocol frozen; empirical result pending workflow execution  
**Scope:** NIFTY 50 long-option entry and exit testing only. No index prediction model selection, no short-option strategy, no live orders.

## 1. Why this is a separate study

NIFTY-PRED-1.0 remains closed and unchanged. OPT-BUY-1.0 and OPT-BUY-2.0 tested a small, different set of implementations and both ended NO-GO for the candidates tested. OPT-BUY-3.0 is a separately versioned finite screen because the user explicitly changed scope to study option-buying entries and exits. Earlier negative findings remain valid and cannot be overwritten. The new screen is not allowed to relax old data-quality standards or use prediction-model scores as entries.

## 2. Primary research question

Among a frozen catalogue of random/control, time-based, gap, breakout, momentum, trend, mean-reversion, implied-volatility, premium-breakout and OI/spot-alignment entries, paired with compatible prespecified exits, is any NIFTY 50 intraday long option rule associated with positive and reproducible **after-cost net rupee expectancy** on out-of-sample dates, relative to random and simple controls?

### Secondary questions

1. How much do entry rules and exit rules each change net P&L, trade frequency, win rate, profit factor and maximum rupee drawdown?
2. Does any positive result survive 100-basis-point adverse slippage per premium side and both chronological halves?
3. Are measured results concentrated in particular prior-known volatility/trend regimes?
4. How much of each result is lost to missing/ambiguous quotes, option contract assumptions, transaction costs and multiple-comparison correction?

## 3. Aim and objectives

**Aim:** perform a bounded, auditable comparison of prespecified long-option entry/exit rules after realistic costs.

**Objectives**
- Reuse the existing private Dhan rolling-option cache where its manifest and schema validate; otherwise attempt documented API acquisition via the configured GitHub Actions secret.
- Inventory usable dates, five-minute quote bars, strike identity, missing bars, conflicting duplicate groups and candidate-specific coverage.
- Implement fixed-seed random controls alongside rules that use only data already available at the signal time.
- Enter on the next five-minute bar after a bar-close signal; fixed-time controls are explicitly identified and enter at the named bar open.
- Evaluate a finite catalogue of compatible exits without using future bars at entry time.
- Model brokerage, STT, stamp duty, SEBI fee, an explicitly estimated exchange fee, GST and adverse slippage.
- Use chronological reporting, block-bootstrap uncertainty, one-sided positive-expectancy tests and Holm family-wise adjustment.
- Create machine-readable ledgers, cost-sensitivity tables, coverage diagnostics, charts and a manuscript based on observed results.
- Run automated regression, data-integrity, trade-matching, cost, statistical, and robustness checks within the same research workflow; fix defects and rerun affected checks before accepting results.

## 4. Research hypotheses

- **H0 (primary):** mean net P&L per scheduled eligible session for a candidate is at most zero after modeled costs.
- **H1 (primary alternative):** a candidate's mean net P&L per scheduled eligible session is greater than zero after modeled costs.
- **H2 (robustness):** an accepted candidate remains positive under 100 bps adverse slippage per premium side.
- **H3 (stability):** both chronological halves have positive mean net P&L, with adequate trade count and quote coverage.
- **H4 (relative control):** a candidate improves on the matched random/simple-control baseline, but relative improvement alone is never evidence of profitability.

All candidate-entry × compatible-exit combinations form the registered primary screening family. Holm correction applies to every available primary one-sided positive-expectancy p-value in that family. Family size, skipped/incompatible cells and missing p-values must be reported. Do not choose a winner using unadjusted p-values, win rate alone, or a positive comparison with a loss-making baseline.

## 5. Data and information cut-off

**Primary option data:** DhanHQ v2 historical rolling-option endpoint (`POST /charts/rollingoption`), five-minute OHLC, implied volatility, volume, open interest, strike and spot fields. Existing helper uses MONTH / expiryCode=1; results must be described as monthly rolling relative-strike data, not as a weekly-option backtest or a stable expiry/contract history. Dhan documentation: https://dhanhq.co/docs/v2/expired-options-data/

**Primary date universe:** option-cache quote dates overlapping the helper's available historical evaluation windows. The helper's acquisition code builds its date window from the previous holdout schedule; OPT-BUY-3.0 will **not** use, read or rank prediction probabilities as entry signals. Reports must state actual first/last quote date and valid date counts. If option rows cannot be loaded, the analysis is BLOCKED and produces no P&L claim.

**Data privacy:** raw provider response files remain under the runner's private `data/cache/options_rolling` cache and must not be committed or uploaded. Only sanitized metadata, aggregated results and a ledger without raw OHLC/quotes may be committed or artifacted. Tokens are read from `DHAN_ACCESS_TOKEN` and never logged.

**Bar identity:** all timestamps are converted to Asia/Kolkata. No forward-filling, no synthetic option prices, no nearest-strike substitution, no use of a different strike to exit a position, and no overnight holdings. A signal based on bar t executes no earlier than bar t+1. Fixed-time baselines explicitly use the open of their named bar.

**Spot caveat:** the endpoint's per-bar spot value is sampled provider data, not an independently verified official cash-index OHLC stream. Spot breakouts/technical indicators are therefore proxies and this limitation must be disclosed. All technical signals use only observed bars known at the signal time.

## 6. Frozen entry catalogue

| ID | Rule | Entry definition |
|---|---|---|
| E01 | Random direction/time CALL/PUT | Date-seeded random eligible entry time; random CALL or PUT; one trade maximum per date |
| E02 | Random-time ATM straddle | Date-seeded random eligible time; buy matched ATM CALL + PUT |
| E03 | Always CALL 09:20 | Buy ATM CALL at the 09:20 bar open |
| E04 | Always PUT 09:20 | Buy ATM PUT at the 09:20 bar open |
| E05 | ATM straddle 09:20 | Buy ATM CALL + PUT at the 09:20 bar open |
| E06 | Random-direction at 10:00 | Random CALL/PUT at fixed 10:00 bar open |
| E07 | Random-direction at 12:00 | Random CALL/PUT at fixed 12:00 bar open |
| E08 | Opening-gap continuation | If absolute first observed spot gap from previous observed session close is at least 0.25%, choose the gap direction at 09:20 |
| E09 | Opening-range breakout | After the first three observed spot samples, trigger at least 0.05% beyond their high/low; execute at next bar open |
| E10 | Three-bar momentum | If three-bar spot move is at least +0.15% buy CALL; at most −0.15% buy PUT; next bar open |
| E11 | EMA(5/15) cross | Bullish EMA5/EMA15 cross buys CALL; bearish cross buys PUT; next bar open |
| E12 | RSI(14) mean-reversion re-entry | RSI crosses back above 30 after oversold => CALL; crosses back below 70 after overbought => PUT; next bar open |
| E13 | RSI(14) momentum | Cross into RSI above 55 => CALL; cross into RSI below 45 => PUT; next bar open |
| E14 | Range expansion with direction | Three-bar range exceeds 1.5× its prior 12-bar median and three-bar spot direction exceeds ±0.10%; next bar open |
| E15 | Trend pullback resumption | EMA15 trend direction, with spot/EMA5 pullback and recross in that direction; next bar open |
| E16 | Low-IV straddle | At an ATM bar, mean ATM CALL/PUT IV is below the prior 12 valid-bar 25th percentile; enter straddle next bar |
| E17 | ATM premium breakout | ATM relative-offset CALL/PUT close exceeds its prior 12-bar high; enter the matching single leg next bar |
| E18 | OI surge plus spot momentum | ATM-side OI increases at least 10% over three bars and three-bar spot move aligns; next bar open. Exploratory only because OI is not intrinsically directional |

Random numbers are generated deterministically from `SEED=20261014` and date/rule ID. A signal rule may have zero trades on some days; zero P&L is included for genuinely no-signal days, but missing/ambiguous quote outcomes are NA and trigger coverage checks instead of being silently turned into zeroes.

## 7. Frozen exit catalogue

| ID | Rule | Exit |
|---|---|---|
| X01 | EOD | Exact 15:25 bar close at the same numeric strike |
| X02 | Hold 30 minutes | Close after six consecutive five-minute bars |
| X03 | Hold 60 minutes | Close after 12 consecutive five-minute bars |
| X04 | Hold 120 minutes | Close after 24 consecutive five-minute bars |
| X05 | Hold 240 minutes | Close after 48 consecutive five-minute bars |
| X06 | Premium TP +20% / SL −20% | Single-leg premium barrier; first stop/target touch, otherwise EOD |
| X07 | Premium TP +40% / SL −25% | Single-leg premium barrier; first stop/target touch, otherwise EOD |
| X08 | Premium TP +60% / SL −30% | Single-leg premium barrier; first stop/target touch, otherwise EOD |
| X09 | Trailing stop −25% | Single-leg trailing premium stop, thereafter EOD |
| X10 | Underlying stop/target | Directional signal only: adverse underlying move −0.35% or favourable +0.50%; exit at next bar open after observed crossing |
| X11 | Spot reversal | Directional signal only: a subsequent three-bar spot move at least 0.10% against the position; exit at next bar open |

A two-leg straddle is compatible only with time/EOD exits because summing leg OHLC highs/lows would create an invented path. Premium barriers/trailing stops are single-leg only. Underlying barrier/reversal exits are directional only. Incompatible combinations must be marked `INCOMPATIBLE`, not substituted. Intrabar ambiguity is handled conservatively: if a bar touches both the premium stop and target, assume the stop occurred first. If a required next bar, monitoring bar, entry quote or exact-strike exit quote is missing, the trade outcome is NA and is excluded from P&L estimation but counted against the completion/coverage gates.

## 8. Costs and execution assumptions

**Primary case:** ₹10 brokerage per executed order and 50 bps adverse slippage on every premium-side execution. Sensitivities: slippage = 0, 25, 50, 100 bps per premium side; brokerage = ₹10 or ₹20 per executed order.

- Brokerage: apply per executed order, not per strategy; a round trip is two executed orders per single leg, four for a two-leg straddle.
- STT on option sales: 0.10% through 2026-03-31; 0.15% from 2026-04-01 onward. Verify against official NSE rules before release: https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax
- Buyer stamp duty: 0.003% of premium turnover.
- SEBI fee: ₹10/crore turnover.
- Exchange transaction fee: use the prior project's 0.03553% turnover estimate only as a documented approximation; mark for independent verification rather than asserting a permanent rate.
- GST: 18% on brokerage + SEBI + exchange transaction fees per the frozen proxy model.
- P&L is one-lot-proxy ₹ P&L. The provider rolling endpoint does not expose exact stable contract/expiry identity; dated lot sizes inherited from the prior project are a limitation. Never claim capital-normalized returns or percentage drawdown without an explicit position-sizing/capital denominator.
- Premium-side slippage worsens each purchase price and reduces each sale price; higher slippage cannot improve net P&L.

Brokerage source: Paytm Money's official F&O FAQ says ₹10 per unique executed order: https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web

## 9. Statistical analysis and prespecified gates

**Primary outcome:** mean net rupee P&L per scheduled eligible session. A no-signal date contributes zero. A signal with missing/incomplete exact-strike quotes is NA, recorded and coverage-gated; it must not be imputed.

**Intervals/inference:** circular moving-block bootstrap, 2,000 replications, block length 5 sessions; one-sided, null-centered bootstrap test for mean candidate P&L > 0; Holm correction across every eligible primary entry × compatible exit family. Report raw and adjusted p-values, sample count, and all failures. Report mean/median P&L per executed trade, win rate, profit factor, cumulative and maximum rupee drawdown, quote coverage, signal count, completion rate, both chronological-half means, and full cost sensitivity.

**Data/coverage gates (frozen):**
- zero schema/parse failures in rows used for a result;
- conflicting quote groups / all duplicated keys no more than 1%;
- at least 80% date coverage for the matched baseline leg universe;
- at least 80% eligible quote outcomes for a candidate;
- at least 90% completion among generated signals;
- at least 100 completed trades for a candidate to be considered for any acceptance.

**Profitability gates (all must pass):**
- mean net P&L per scheduled eligible date > 0;
- 95% block-bootstrap lower bound > 0 at primary costs;
- mean net P&L remains > 0 at 100 bps/side;
- both chronological halves have positive mean P&L;
- one-sided Holm-adjusted p < 0.05 for positive expectancy;
- candidate passes every data/coverage/sample-size gate;
- independent automated validation reports PASS or PASS WITH EXPLICIT LIMITATIONS and confirms computations.

The prior study's duplicate conflict rate exceeds 1%; do not relax the threshold to force confirmatory status. If the new shared cache has the same issue, candidates may be reported for diagnosis only as exploratory and all approval flags remain false even when descriptive metrics appear positive. A relative win over a worse/random baseline never substitutes for positive absolute expectancy.

## 10. Finite phases and stopping rules

| Phase | Branch/checkpoint | Work and exit condition |
|---|---|---|
| 1. Audit and freeze | `research/option-entry-exit-developer` | Verify inherited data/code/closed results; commit this protocol and catalogue |
| 2. Data validation | same developer branch | Use/reacquire cache; validate schema, timestamp, strike continuity, duplicates, gaps, coverage; block or proceed |
| 3. Candidate implementation | same branch | Implement frozen entries/exits and arithmetic; unit-test formulae, no-lookahead, exact-strike handling, bar ordering |
| 4. Bounded run and report | same branch | One full run plus defect-only rerun; save sanitized ledger, metrics, cost sensitivity, diagrams, manuscript, SHA/workflow link |
| 5. Independent review | create `research/option-entry-exit-independent-automated validation` only after results acquisition | Tester independently validates math/signs, quote matching, cost cases, multiplicity and gates; write report |
| 6. Developer disposition | `research/option-entry-exit-developer` | Fix only confirmed defects, at most one corrective rerun; respond to tester report; do not optimize to bypass gates |
| 7. Close | PR/status update to main after tester report | Update README, research status, errors, activity log; close as GO-TO-PAPER-VALIDATION, NO-GO or INCONCLUSIVE. No live deployment from a historical backtest |

**Stop immediately** if no valid quote data exist, the source response is invalid, cache cannot be safely parsed, or the frozen protocol cannot be implemented correctly. A data blocker is not evidence that a strategy is unprofitable. Stop after the final prescribed review; no unbounded parameter search. If no candidate passes, say so and recommend only what new data or a separately approved study would address the limitation.

## 11. Required deliverables

- This frozen protocol and its hash/commit.
- `research/option-entry-exit/entry_exit_backtest.py`, `test_entry_exit.py`, report renderer.
- Sanitized acquisition/quote quality manifest, strategy metrics, primary candidate ledger, cost sensitivity, regime summary, SVG plots and a structured research manuscript.
- Updated `README.md`, `research/PHASE_STATUS.md`, `research/EXPERIMENT_LOG.md`, `research/ERROR_LOG.md` and `research/INTERACTION_LOG.md`.
- Post-results automated validation branch/report and developer disposition.
- Manual `workflow_dispatch` plus bounded push-triggered workflow, cache re-use, pre/post unit tests, sanitized-only artifacts and no automatic live trades.

## 12. Limitations and future research

The rolling endpoint is not a stable point-in-time exchange contract/expiry archive. Historical bid/ask quotes and queue/market impact are not available in this cache, so adverse slippage is a stress assumption rather than measured spread. Some source conflicts have previously exceeded the frozen ceiling. Spot fields are provider-sampled. Lot-size proxy and transaction-fee estimates must be independently verified. FII/DII, PCR, market breadth, complete point-in-time corporate actions, timestamp-aligned news, and fully timestamp-aligned global data are not assured. Historical performance cannot establish live profitability.

Future research should first improve point-in-time contract identity, bid/ask and execution-cost evidence, then separately preregister market-regime/context features or portfolio/risk controls only if there is enough valid quote coverage. It must not continue parameter optimization under this protocol.


## User-approved process amendment — 2026-10-15

The user explicitly rejected independent reviews. This study therefore has no separate tester role, tester branch, or tester-report dependency. All validation is performed in the same bounded workflow through unit tests, data-integrity checks, arithmetic invariants, statistical checks, robustness reruns, and documented error correction. This amendment changes the process, not the statistical acceptance gates or the prohibition on unsupported strategy approval.
