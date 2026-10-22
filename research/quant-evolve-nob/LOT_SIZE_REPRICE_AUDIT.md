# QE-NOB-1.0 — dated lot-size reprice audit

**Audit date:** 2026-10-22  
**Audit type:** bounded post-hoc revaluation of the saved 600-candidate trade ledger; not a fresh evolutionary run.  
**Source artifact:** [Actions run #39741806754 artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754/artifacts/12417631602)  
**Corrected full rerun:** [Actions run #39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025), in progress at the time of this report.

## Why this audit was needed

The earlier lot-size proxy mistakenly used 25 units across dates before 2024-11-20. That distorted premium turnover, fees and rupee P&L. I re-priced all **483,706 trade rows** in the saved ledger by scaling raw premium turnover from the old lot proxy to the corrected date/family proxy, then reapplying the same primary/stress slippage and fee formulae. The source did not contain stable contract IDs or the full session calendar, so this is a **frozen-candidate revaluation**, not an exact-contract or full corrected re-evolution result.

The corrected proxy references the official NSE changes: [FAOP47854 — 75 to 50 from 2021](https://archives.nseindia.com/content/circulars/FAOP47854.pdf), [FAOP61415 — 50 to 25 in 2024](https://nsearchives.nseindia.com/content/circulars/FAOP61415.pdf), [FAOP64672 — phased 25 to 75 transition](https://nsearchives.nseindia.com/content/circulars/FAOP64672.pdf), and [FAOP70616 — 75 to 65 for 2025/26 expiries](https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf). Because Dhan's rolling endpoint does not expose a stable expiry identifier, the effective date is a WEEK1/MONTH1 proxy, not an exact instrument-master join.

## Cost assumptions

- Primary: next-bar OHLC trade simulation, 50 bps adverse slippage per side, ₹10 brokerage per executed order, plus the existing date-effective STT/exchange/SEBI/GST/stamp model. Paytm Money's published F&O FAQ lists ₹10 per executed order; user-account legacy tariff cohorts may differ.
- Stress: 100 bps and 200 bps adverse slippage per side, ₹20 brokerage per order.
- No historical bid/ask/depth is invented. The analysis proceeds on available OHLC, but remains unsuitable for claims of guaranteed or executable fills.

## Reprice results

All values below are corrected **exploratory** per-day averages from the frozen pre-correction candidate set. A candidate was only a possible statistical winner if it passed every preregistered condition; positive average P&L alone is not enough.

| Candidate | Strategy description | OOS trades | Validation mean/day | OOS mean/day | OOS median/day | 100-bps + ₹20/order mean/day | 200-bps + ₹20/order mean/day | Disposition |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 86 | Monthly gap continuation, 0.15% gap, 120-minute hold, one-step OTM | 151 | ₹121.73 | ₹6.14 | ₹0.00 | −₹104.19 | −₹296.25 | Fails daily-median and cost-stress gates |
| 558 | Weekly gap continuation, 0.15% gap, 15-minute hold, one-step OTM | 159 | ₹53.28 | ₹70.37 | ₹0.00 | ₹10.02 | −₹80.53 | Fails daily-median and 200-bps stress gates |
| 501 | Weekly opening-range breakout, zero buffer, 30-minute hold, one-step OTM | 244 | −₹13.99 | ₹44.06 | ₹41.40 | −₹43.99 | −₹173.83 | Fails validation and both cost-stress gates |
| 588 | Monthly opening-range breakout, zero buffer, 30-minute hold, one-step OTM | 244 | −₹25.94 | ₹23.81 | ₹69.30 | −₹147.26 | −₹443.16 | Fails validation and both cost-stress gates |
| 264 | Weekly EMA pullback, 8/21, 120-minute hold, one-step OTM | 137 | ₹0.00 | ₹126.11 | ₹0.00 | ₹76.99 | ₹4.74 | Fails minimum OOS trade count, validation and daily-median gates |

### Necessary-gate screening

- 600 candidates were re-priced, including 536 strategy-family candidates (excluding simple controls).
- Only **two** candidates had both at least 150 OOS trades and a positive OOS daily median; both had negative corrected validation means and negative stress P&L at 100 bps / ₹20 per order.
- No candidate met the joint daily-median, validation and stress prerequisites. Consequently, no candidate can pass the full promotion gate from this frozen candidate set.
- Approximate reconstructed daily HAC/Holm screening also produced no multiplicity-adjusted OOS pass. This specific p-value screen is diagnostic, not the final inference: the trade ledger omitted seven zero-trade session dates, so the local diagnostic inserted those zero days evenly for autocorrelation calculations. The current full workflow uses the underlying session grid and remains the source for final exact inference.

## Conclusion

**No-go for strategy approval from the re-priced saved candidate set.** The lot-size defect has been accounted for in this audit; the previously published P&L figures should not be used. There is no reliable, cost-robust strategy supported by these results. This is not proof that every conceivable NIFTY option strategy is unprofitable. It means that none of the tested candidates in this saved set met the predeclared statistical/robustness gates after the corrected lot-size revaluation.

The available OHLC data were sufficient to conduct the bounded statistical revaluation. Missing bid/ask/depth and stable exact contract identity remain execution-readiness limitations only. The corrected full evolutionary rerun is a single supplementary confirmation, not a reason to wait for unavailable quote data.

## Developer / tester handoff

**Developer:** close the bounded work on this evidence unless the already-running corrected workflow produces materially different metrics; if so, reconcile the result and update the README/manuscript once. Do not restart unbounded discovery.

**Tester:** the user explicitly declined an independent tester; no tester branch/report is requested or claimed.
