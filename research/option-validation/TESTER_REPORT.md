# Independent Tester Report — OPT-BUY-1.0

**Review date:** 2026-10-14  
**Reviewed branch/commit:** `research/option-buying-independent-tester`, based on result commit `fd64fd970f8abb185b97b7a9452fc7b50f26d2bc`  
**Source run:** [GitHub Actions #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384)  
**Artifact:** `option-validation-results-38548437384.zip`  
**Artifact SHA-256:** `86e9d03c6c55c17d46348a8dc40b9a02f247f2f9bca38703110c74c030be889`

## Tester disposition

**Overall decision: FAIL — DO NOT APPROVE AN OPTION-BUYING CANDIDATE.**

The calculations in the saved trade ledger and primary comparison table independently reproduce within rounding tolerance, and the workflow's 13 unit tests pass. The research acceptance gates do not pass: strangle quote coverage is 69.18% (<80%), conflicting quote groups are 1.409% (>1%), and all four alert-filtered candidates have negative average net P&L with negative 95% block-bootstrap intervals. The positive paired differences against always-buy describe a reduction in losses versus a worse baseline; they do not make the filtered strategies profitable.

The result is **inconclusive as to a general market inefficiency**, but is negative for the current tested implementations. No paper-trading or live-trading recommendation is justified.

## 1. Reproducibility and arithmetic audit

I independently extracted the sanitized artifact rather than relying only on the Markdown summary. The ledger contains **48,032 rows**: 24,016 always-buy rows and 24,016 model-filtered rows.

Independent audit results:

| Check | Independent result |
|---|---:|
| `net_pnl_rupees = gross_pnl_rupees − total_cost_rupees` maximum absolute error | < (2\times10^{-12}) rupees |
| `total_cost_rupees = slippage_cost_rupees + explicit fees` maximum absolute error | < (5\times10^{-13}) rupees |
| Negative-cost rows | 0 |
| Rows with net P&L greater than gross P&L | 0 |
| Nonpositive-debit rows | 17,048; all were non-trades with zero P&L and zero cost |

For all four primary cases, I rebuilt the paired daily P&L series from the trade ledger and independently reran the circular block bootstrap with the declared horizon block length, 2,000 replicates, and seeds. The means, 95% block intervals and p-values reproduced the stored values to floating-point rounding. Holm-adjusted p-values also match the four-comparison family ((p_{Holm}=0.0020) for each comparison).

This validates the saved arithmetic and primary summary computations; it does **not** validate the historical lot-size proxy, missing bid/ask spread assumptions, or the source data's completeness.

## 2. Frozen data-quality gates

Evidence from [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384):

| Data gate | Observed | Required | Verdict |
|---|---:|---:|---|
| Acquisition requests failed | 0; 686 saved request windows reused from cache | 0 | PASS |
| Straddle fixed-strike eligible-date coverage | 83.98% | ≥80% | PASS |
| Strangle fixed-strike eligible-date coverage | 69.18% | ≥80% | **FAIL** |
| Conflicting duplicate groups / duplicate groups | 452 / 32,085 = 1.409% | ≤1% | **FAIL** |
| Parse failures | 0 | 0 | PASS |

The code drops conflicting `(date,time,type,strike)` keys before pricing, which is safer than picking an arbitrary conflicting quote. However, dropping the rows does not make the source-quality gate pass: the conflict rate still exceeds its frozen ceiling. The missing same-strike exit bars and inconsistent relative offsets also reduce strangle eligibility. Because the data gate fails, the run is correctly marked `INCONCLUSIVE_PARTIAL_OR_INCOMPLETE_DATA`.

## 3. Net results at the primary cost setting

Primary setting: ₹10 brokerage per executed order and 50 bps adverse slippage on each option-premium side. Rupee values use the declared date-based lot-size proxy. Both candidate and benchmark are computed over the same eligible dates, with zero candidate P&L on non-alert dates.

| Horizon | Structure | Alert trades | Alert-filtered net P&L/date | 95% block CI | Always-buy net P&L/date | Paired improvement/date | Holm p | Candidate gate |
|---:|---|---:|---:|---|---:|---:|---:|---|
| 5 sessions | Straddle | 224 | −₹315.71 | −₹405.17 to −₹230.81 | −₹1,097.15 | +₹781.44 | 0.0020 | FAIL |
| 5 sessions | Strangle | 178 | −₹349.35 | −₹449.83 to −₹258.22 | −₹1,265.49 | +₹916.14 | 0.0020 | FAIL |
| 20 sessions | Straddle | 259 | −₹327.64 | −₹414.94 to −₹244.21 | −₹1,097.15 | +₹769.50 | 0.0020 | FAIL |
| 20 sessions | Strangle | 210 | −₹369.43 | −₹473.19 to −₹268.35 | −₹1,265.49 | +₹896.05 | 0.0020 | FAIL |

All candidates fail the positive-P&L confidence-bound requirement. Each candidate also has negative average P&L in both chronological halves and negative P&L under 100-bps adverse slippage. Therefore the positive paired comparison only means the alert filter lost less than buying every eligible day; it does not establish profitable option buying. The candidate gates correctly remain false.

## 4. Method and limitations that remain

1. **Quote-quality gate failure:** the current run cannot support a confirmed result because the prespecified coverage and conflicting-duplicate ceilings are not met. Do not relax those cutoffs to rescue the study.
2. **Historical execution data:** Dhan's rolling endpoint supplies 5-minute OHLC but no historical bid/ask. The 0/25/50/100-bps scenarios are stress assumptions rather than measured spreads/market impact.
3. **Contract sizing:** rupee P&L depends on a date-based lot-size proxy, not a reconstructed expiry-specific contract master. Premium-point results are more directly grounded than exact historical rupee P&L.
4. **Scope:** this tests monthly rolling options with next-session 09:20 entry and 15:25 same-session exit. It does not test weekly options, longer-held option positions, directional calls/puts, or other strategies.
5. **Forecast/monetization horizon:** the classifier labels 5- or 20-session volatility expansion while the option position is exited that same day. This is the prespecified experiment, but it tests immediate monetization rather than holding for the target horizon.
6. **Generalization:** a single chronological historical sample does not establish live profitability or rule out other option-buying hypotheses.

## 5. Recommendation

Close OPT-BUY-1.0 as **NO-GO for the tested option-buying implementations**. Keep the numerical results, cost sensitivities, manuscript, two SVG charts and failed quality gates as the reproducible outcome. Do not ship a paper-trading recommendation. The most defensible actionable conclusion is that the tested volatility-expansion alert, when converted into the specified intraday long straddle/strangle trades, did not demonstrate positive net option P&L after the modeled costs.

A future study should be a new, separately versioned protocol, not a threshold change inside OPT-BUY-1.0. It would need better validated quote coverage/contract metadata and a newly preregistered monetization hypothesis before fresh performance testing.

## Instruction to developer

Accept this independent no-go disposition, update README/phase status/error and interaction logs on main, mark this bounded follow-on complete with scope limitations, and preserve the artifact SHA above. Do not loosen the data gates or run further variants to search for a positive result. No live orders or deployment.
