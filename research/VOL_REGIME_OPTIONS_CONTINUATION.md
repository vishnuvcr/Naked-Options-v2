# VOL-REGIME-OPT-1.0 bounded continuation

**Started:** 2026-10-16  
**Branch:** `research/vol-regime-options-continuation`  
**Parent protocol:** [frozen protocol on developer branch](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/research/VOL_REGIME_OPTIONS_PLAN.md)  
**Status:** IN PROGRESS — source/contract identity gate first; no strategy is approved.

## User directive
Continue the option-buying research toward identifying the strongest evidence-supported candidate. Do not stop merely because early candidates fail. However, never fabricate data, bypass a preregistered data-quality gate, or call a candidate "best" without valid out-of-sample net results. A failed source gate is a data feasibility result, not evidence of strategy profitability.

## Current evidence inherited from the repository
- NIFTY-PRED-1.0 found no robust return/direction winner.
- OPT-BUY-1.0 and OPT-BUY-2.0 are closed no-go for tested implementations; their frozen quality gates must not be weakened.
- VOL-REGIME-OPT-1.0 proposes buying an ATM weekly straddle in a high predicted volatility-expansion regime and selling a delta-targeted weekly strangle in a low regime. The latest saved Dhan probe returned structurally valid weekly CALL/PUT arrays for candidate codes 1, 2, and 3 over a short sample, but did not prove expiry-date mapping, exact-contract continuity, broad coverage, or P&L.
- The original Dhan/HF source-gate workflow was interrupted during the Hugging Face fallback; that fallback is not considered verified. The related `vishnuvcr/Nifty` repository independently identifies `thetrademarkk/india-index-options-1m` and caches `options/NIFTY/*.parquet` with expiry-specific filenames. A new bounded audit workflow now reuses this same dataset source in the continuation branch, downloads only NIFTY options into the Actions cache, and records sanitized schema/expiry/duplicate/quality metadata. The dataset is labelled CC-BY-NC-4.0, so the work is restricted to non-commercial research with attribution.
- These prior results are constraints/context, not new performance evidence.

## Finite phases and gates

### C1 — Reconcile source audit and contract identity
1. Inspect current Dhan endpoint documentation and persisted sanitized probe evidence.
2. Reuse the exact HF dataset source already used in `vishnuvcr/Nifty`: `thetrademarkk/india-index-options-1m`, `options/NIFTY/*.parquet`. Its files are expiry-specific and contain explicit `expiry`, `strike`, `option_type`, `timestamp`, and OHLCV/OI fields according to its dataset card. Run the new cached audit before any P&L work. The dataset is CC-BY-NC-4.0; use only for non-commercial research with attribution.
3. Establish expiry-date validity using explicit dataset expiry fields and an independent official NSE expiry calendar/contract record; compare filename date to row expiry.
4. Prove stable instrument identity across entry and exit for the same expiry, numeric strike, and option type. Do not substitute rolling ATM-relative offsets for exact contracts.
5. Check free alternatives before any paid source: NSE historical derivatives/contract files and public licensed datasets. Record terms, retrieval dates, schemas, gaps, and hashes.
6. If the HF source fails schema, coverage, identity, or license gates, compare with official NSE contract files and Dhan data only as permitted; if no source proves expiry mapping and continuity within this bounded source phase, record BLOCKED and do not compute synthetic P&L.

### C2 — Full data quality and coverage
- Build cached point-in-time option records; preserve source provenance and license conditions.
- Required gates remain: >=80% eligible-date coverage for the tested candidate, <=1% conflicting duplicate groups, explicit missingness and timestamp audits, and valid expiry/lot-size history for rupee P&L.
- Compare exact-contract quote continuity and executable-side price proxies. OHLC data are not bid/ask quotes; explicitly state this limitation.
- If gates fail, fix source/parser defects once and rerun; do not lower thresholds.

### C3 — Frozen signal and baseline evaluation
- Primary signal stays the 5-session technical Logistic volatility-expansion classifier and development-only out-of-fold 75th/25th percentile thresholds from the parent protocol.
- Compare regime switch with no trade, always-buy ATM straddle, always-sell delta-targeted strangle, and a simple non-forecast regime baseline.
- Only information available by the prior NIFTY close may drive the next-session entry.

### C4 — Backtest and realistic costs
- Entry/exit, weekly expiry handling, exact contracts, lot sizes, and missing-exit behavior follow the frozen parent plan.
- Include Paytm Money brokerage assumptions, applicable historical statutory/exchange charges, and adverse slippage sensitivities 0/25/50/100 bps per premium side; use ₹10 and ₹20 per-order sensitivity.
- Include spread/impact caveats, margin/capital assumptions, max drawdown, tail loss, worst trade/week, turnover, and no-trade days.
- Never treat unfilled or missing quotes as a zero-cost fill.

### C5 — Statistical validation
- Chronological development/holdout split; purging/embargo for overlapping targets; thresholds and any model choices selected only in development data.
- Report net P&L distributions, mean/median, block-bootstrap confidence intervals, drawdown/tail risk, candidate sample sizes, and paired baseline differences.
- Correct the predefined comparison family for multiplicity (Holm at minimum). Report both chronological subperiods and cost sensitivities.
- No holdout reuse for candidate selection. No positive claim from gross P&L or a significant difference versus a worse baseline.

### C6 — Automated quality checks and disposition
- Unit/regression tests cover contract identity, expiry mapping, sign conventions, lot-size application, fees/taxes, slippage, missing data, P&L arithmetic, and bootstrap/Holm calculations.
- Record every failure and correction. Existing user instruction waives a separate independent tester role for the option-entry/exit track; therefore use reproducible automated checks and explicitly label absence of independent review rather than inventing a tester sign-off.
- If at least one candidate passes all frozen gates and demonstrates positive net expectancy with uncertainty/stability support, label it the best *within this tested universe*, not universally optimal. If none pass, state no validated best strategy found and explain the limiting gate.

### C7 — Manuscript and closure
Deliver structured methods/results/discussion, data dictionary, source manifest, tests, charts/tables, limitations, conclusion and future work. Update README, phase status, experiment/interaction log, error log, and published status only with verified facts.

## Stop conditions
Stop after C1-C7 once, including only bounded defect-driven reruns. Stop earlier only for a serious blocker such as unavailable lawful data, credentials requiring user intervention, or inability to establish contract identity. Do not continue endless parameter searches. Do not recommend paper/live deployment unless the data and net-performance gates pass.

## Immediate next action
Inspect the latest workflow audit and public/free historical data sources. Do not compute option P&L until expiry mapping and fixed-contract continuity are verified.
