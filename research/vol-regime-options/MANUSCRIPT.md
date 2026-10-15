# VOL-REGIME-OPT-1.0: Feasibility of a Weekly NIFTY Options Volatility-Regime Switch

**Research status:** CLOSED — BLOCKED AT SOURCE/CONTRACT-IDENTITY GATE  
**Version:** 1.0  
**Cut-off date:** 2026-10-15  
**Developer branch:** `research/vol-regime-options-developer`  
**Independent review:** [Tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-tester/research/vol-regime-options/TESTER_REPORT.md)

## Abstract

This bounded feasibility study asked whether an out-of-sample NIFTY 50 volatility-regime forecast could select between a long ATM weekly straddle in forecast high-volatility conditions and a short approximately 0.07-absolute-delta weekly strangle in forecast low-volatility conditions. The frozen protocol required verified historical expiry mapping, fixed-contract entry-to-expiry continuity, at least 80% eligible-date coverage, duplicate-conflict control, historical lot sizes for rupee results, dated statutory charges, brokerage and adverse slippage, paired statistical comparisons, and tail-risk analysis.

Dhan's expired rolling-option endpoint returned structurally valid arrays for candidate weekly expiry codes 1, 2 and 3 in a five-day January 2025 probe. Code 3 returned 357 CALL rows and 349 PUT rows; codes 1 and 2 returned 375 rows per side. Code 0 returned HTTP 400 with `DH-905: expiryCode is required`. These schema checks do not establish which actual expiry date each code represents or whether the same numeric strike and expiry can be followed from entry to exit. A Hugging Face fallback probe was canceled by a runner shutdown before producing an auditable result. The independent tester therefore confirmed BLOCKED. No full historical dataset, P&L, cost simulation, statistical inference or profitability result was produced. This is a data-feasibility blocker, not evidence that the hypothesis wins or loses.

## 1. Introduction

Volatility forecasts can be statistically informative without being economically useful for options. A regime-switching option structure also faces asymmetric payoff and execution challenges: long straddles pay premium and require sufficient movement; short strangles collect premium but carry substantial tail risk. Rolling ATM-relative historical data can create false continuity if it is mistaken for a fixed contract. The present study therefore placed contract identity and data feasibility before P&L analysis.

The parent prediction study (NIFTY-PRED-1.0) found no robust return/direction edge and treated volatility-expansion classification as exploratory. The separate option-buying studies were not approvals and were not reused as evidence for this hypothesis.

## 2. Research question, aim and objectives

**Question:** Can a point-in-time volatility-regime forecast select weekly NIFTY options structures with positive net performance after realistic costs and controlled tail risk?

**Aim:** evaluate the economic value of a volatility-regime switch, conditional on a verified historical contract-level dataset.

Objectives:
1. Verify weekly options history, expiry mapping, strike identity and coverage.
2. Freeze a signal using only information available by the prior NIFTY close.
3. Compare a long ATM weekly straddle in the high regime with a short weekly strangle near 0.07 absolute delta in the low regime.
4. Reconstruct same-expiry entry-to-exit P&L using exact contracts.
5. Include brokerage, historical statutory charges, and 0/25/50/100 bps adverse-slippage sensitivity.
6. Evaluate common-date comparisons, uncertainty, multiple testing and tail risk.
7. Publish reproducible artifacts and independent gate disposition.

## 3. Frozen hypotheses and protocol

- Primary signal: existing technical Logistic 5-session volatility-expansion classifier; high/low thresholds from the 75th/25th percentiles of development-only out-of-fold probabilities. Middle regime means no trade.
- Secondary signal: 20-session classifier, explicitly secondary and horizon-mismatched.
- High regime: buy ATM weekly call and put, same expiry.
- Low regime: sell call and put each nearest to absolute delta 0.07 within ±0.02; skip if no acceptable leg.
- Entry: next eligible session at the first available 5-minute bar starting 09:20 IST.
- Exit: same weekly expiry session, final valid bar no later than 15:25 IST.
- Exact numeric strike and expiry must match; missing-contract exits count against coverage.
- Minimum coverage: 80%; conflicting duplicate groups ≤1%; no forward-fill.
- Primary costs: ₹10 brokerage per order plus date-appropriate documented charges and 50 bps adverse slippage per premium side; sensitivity includes ₹20/order and 0/25/50/100 bps.
- Confirmatory comparisons: regime switch versus always-buy straddle, always-sell strangle, no-trade, and a non-forecast historical-regime baseline. Paired common dates, block bootstrap intervals, suitable paired-loss tests, and Holm correction were prespecified.
- No parameter relaxation, monthly substitution, or strategy tuning to rescue a failed source gate.

## 4. Scientific methodology

### 4.1 Data acquisition and source validation

A bounded Dhan request matrix probed WEEK codes 0–3 and a MONTH code 1 control for 2025-01-06 through 2025-01-10 at 5-minute resolution. The schema check required timestamp, open, close, strike, spot and IV arrays of matching lengths and monotonic timestamps. Workflow logs were inspected after the full workflow was canceled during the fallback probe. The available Dhan evidence was persisted to [source audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/source_audit.json).

### 4.2 Contract identity gate

Before P&L, the study required an independently verifiable mapping from rolling expiry code to actual expiry date, including historical holiday/weekday changes, and proof that the same numeric strike and expiry were observed at entry and exit. The returned schema did not contain an explicit expiry-date field. A short-window ATM-relative response is not itself a fixed-contract ledger.

### 4.3 Planned statistical and economic analysis

No analysis in this subsection was executed. If a verifiable source becomes available in a new preregistered study, the planned tests include net premium-point P&L, rupee P&L only with date-specific lot sizes, common-date paired comparisons, circular moving-block bootstrap confidence intervals, adjusted p-values, drawdown, expected shortfall, worst week, turnover, coverage and cost/slippage sensitivity. Naked short-strangle tail exposure would be reported explicitly.

## 5. Results

### 5.1 Source schema probe

| Request | Result | Rows | Interpretation |
|---|---:|---:|---|
| WEEK code 0 CALL/PUT | HTTP 400 | 0 | Provider rejected with `DH-905: expiryCode is required` |
| WEEK code 1 CALL/PUT | PASS | 375 each | Basic schema pass only |
| WEEK code 2 CALL/PUT | PASS | 375 each | Basic schema pass only |
| WEEK code 3 CALL | PASS | 357 | Basic schema pass only |
| WEEK code 3 PUT | PASS | 349 | Basic schema pass only |
| MONTH code 1 CALL/PUT | PASS | 375 each | Control only; not substituted for weekly data |

The sample is a short five-day window. Different row counts for code 3 also show that per-side response counts are not automatically interchangeable. The probe is not a coverage test over the intended historical period.

### 5.2 Workflow and fallback

Workflow [#10](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667) was marked failed after the runner received a shutdown signal during the Hugging Face fallback probe. Cache-save, audit-commit and artifact-upload steps were skipped in that run. The Dhan request evidence was recovered from logs and persisted separately. The HF fallback remains unverified; no dataset license or coverage pass is claimed.

### 5.3 P&L and inference

**Not run.** No full-window option data, exact contract ledger, matched-date coverage report, historical lot-size mapping, cost ledger, P&L series, confidence interval, p-value, Holm adjustment, drawdown or tail-risk statistic exists. No profitability result can be inferred from schema validation.

## 6. Discussion

The source endpoint is responsive for several candidate weekly codes, so the narrow finding is not “weekly data are unavailable.” The critical unresolved issue is whether the rolling codes can be mapped to actual expiry dates and stable numeric strike/expiry contracts at the exact timestamps needed by the frozen strategy. Without that evidence, any backtest could pair prices from different contracts and produce misleading returns. The canceled HF fallback also means no independent source has yet resolved this identity problem.

## 7. Strengths

- Frozen protocol and acceptance gates were established before P&L.
- Weekly and monthly requests were distinguished; monthly results were not substituted.
- Code 3 was checked using actual workflow logs rather than assuming the previous saved audit covered it.
- Workflow cancellation and incomplete fallback were logged explicitly.
- The independent tester issued a separate blocked disposition.
- No unsupported performance claim or strategy approval was made.

## 8. Limitations

- The source probe covers only five calendar days in January 2025.
- No verified mapping of Dhan expiry codes to actual expiry dates was obtained.
- No fixed-contract entry-to-expiry ledger or historical coverage audit exists.
- Historical bid/ask, contract lot sizes, historical charges and executed-side prices were not established.
- The Hugging Face fallback was canceled; license and data quality remain unresolved.
- No model, economic, statistical or tail-risk analysis was performed for this study.
- Consequently, this manuscript reports a feasibility result only, not a trading result.

## 9. Conclusion

**VOL-REGIME-OPT-1.0 is closed as BLOCKED at the source/contract-identity gate.** Candidate weekly codes 1, 2 and 3 pass a short schema check, but exact expiry mapping and fixed-contract continuity remain unproven. No P&L was calculated; the hypothesis is neither accepted nor rejected on profitability. No paper or live strategy is approved.

## 10. Future research

A future version should begin only after obtaining a source or documented reconstruction that provides verifiable expiry dates and exact contract identifiers at each timestamp. The next protocol should then validate historical contract master/lot sizes, date-specific fee schedules, quote quality and coverage on a small preregistered pilot before any full acquisition. Any new study must have its own version, branch, frozen gates and independent tester review.

## Appendix A. Provenance

- Frozen plan: [VOL_REGIME_OPTIONS_PLAN.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/research/VOL_REGIME_OPTIONS_PLAN.md)
- Source-gate disposition: [SOURCE_GATE_DISPOSITION.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/SOURCE_GATE_DISPOSITION.md)
- Sanitized source audit: [source_audit.json](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/source_audit.json)
- Independent tester: [TESTER_REPORT.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-tester/research/vol-regime-options/TESTER_REPORT.md)
- Workflow evidence: [run #10](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667)

## Appendix B. Machine-readable output status

| Artifact | Status |
|---|---|
| Sanitized source audit | Available |
| Full options dataset / contract ledger | Not produced |
| P&L ledger | Not produced |
| Cost and slippage ledger | Not produced |
| Statistical inference outputs | Not produced |
| Strategy comparison charts | Not produced because no valid P&L series exists |
| Independent tester report | Available; BLOCKED |
