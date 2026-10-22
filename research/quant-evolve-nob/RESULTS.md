# QE-NOB-1.0 — fresh QuantEvolve-style naked option buying

**Run status:** CORRECTED RERUN COMPLETE — NO_STATISTICAL_CANDIDATE. Workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) completed successfully.  
**Date range:** 2021-10-25 to 2026-10-21  
**Candidates tested:** 600  
**Previous-run result (superseded):** 0/600 candidates passed the statistical gate; do not carry forward its P&L values after correcting lot sizing.  
**Data integrity:** offset-aware duplicate/grid checks pass; exact contract IDs remain unavailable.  
**Execution readiness:** quotes/depth not available; exploratory OHLC analysis proceeds with adverse-slippage and cost assumptions, but this is not a claim of executable fills.  
**Interim decision:** no strategy approved; the frozen-candidate reprice audit found zero gate pass. The corrected full evolutionary rerun remains a single supplementary check.

## Run and dataset

Corrected workflow [#39741806754](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754) analyzed 1,241 sessions, 92,510 underlying rows, and 2,600,975 option rows. After including rolling ATM offset in the duplicate key, there were 0 duplicate groups, 0 conflicting groups, and 0 rows dropped. Timestamp coverage was 99.772%; row-grid coverage was 100%. Automated tests passed (11 tests). Four islands evaluated 600 unique candidates over nine generations. Pre-run and post-run automated tests each passed (11 tests).

## Main finding

Those candidate statistics were computed using an invalid date-based lot proxy that assigned 25 units to the entire period before November 2024. They are retained only as a record of the superseded run and must not be used as the current P&L result. The corrected run applies dated lot proxies by WEEK1 versus MONTH1 and will recompute candidate ranking, net P&L, uncertainty intervals and stress results.

The study proceeds using next-bar option OHLC, modeled adverse slippage, and disclosed fee assumptions. Missing historic best bid/ask/depth limits execution realism, not whether the planned statistical analysis may be run.

## Data and execution limitations

- Corrected duplicate identity includes the source ATM offset; this reduced the detected duplicate groups from 471 (453 conflicting) to zero. This resolves the prior duplicate-key diagnostic but does not validate exact exchange contract identity.
- Dhan rolling ATM-relative option OHLC does not provide historical best bid/ask/depth for execution validation.
- Exact historical expiry and stable exchange contract identity are not returned by the rolling endpoint. A dated WEEK1/MONTH1 lot-size proxy now uses NSE circular transition dates; it is a defensible approximation, not an exact instrument-master join.
- Primary brokerage uses ₹10 per executed order per Paytm Money's currently published F&O FAQ; ₹20 per order remains the conservative stress scenario because account-specific legacy tariffs can differ. Statutory/exchange fees are date-based approximations and slippage is modeled rather than observed.
- Failed Dhan requests are preserved in the source failure report.

## Final disposition

**No strategy is approved.** The statistical research does not wait for unavailable bid/ask/depth: the revised methodology proceeds with OHLC and modeled slippage. Exact contract identity and executable fills remain unproven, so even a positive corrected result would remain exploratory and could not authorize paper/live deployment. The current pre-correction metrics are superseded until the dated-lot rerun finishes.

## Artifacts

- [Workflow run and downloadable report artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501)
- [Research phase status](PHASE_STATUS.md)
- [Error log](ERROR_LOG.md)
- [Research plan](PLAN.md)
- [Source and literature notes](LITERATURE_REVIEW.md)
- [Run summary JSON](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v1-developer/reports/quant_evolve_nob_v1)

The corrected report artifact and bounded report files were committed by workflow #39741806754. A follow-up workflow #39741823249 was queued by the test change and is being monitored.


## Dated lot-size correction — 2026-10-22

The prior proxy was defective: it applied 25 units to every date before 2024-11-20, despite NSE's 2021 change from 75 to 50 and the 2024 change from 50 to 25. The corrected proxy is family-aware:

| Rolling series | Period | Proxy lot size | Grounding |
|---|---|---:|---|
| WEEK1 / MONTH1 | 2021-10-25 to 2024-04-25 | 50 | [NSE circular FAOP47854 (2021)](https://archives.nseindia.com/content/circulars/FAOP47854.pdf) |
| WEEK1 / MONTH1 | From 2024-04-26; revised weekly and monthly expiries begin May 2 / May 30 | 25 | [NSE circular FAOP61415 (2024)](https://nsearchives.nseindia.com/content/circulars/FAOP61415.pdf) |
| WEEK1 | 2024-12-20 to 2025-12-23 | 75 | [NSE corrigendum FAOP64672 (2024)](https://nsearchives.nseindia.com/content/circulars/FAOP64672.pdf) |
| MONTH1 | 2024-12-20 to 2025-01-30 | 25 | [NSE corrigendum FAOP64672 (2024)](https://nsearchives.nseindia.com/content/circulars/FAOP64672.pdf) |
| MONTH1 | 2025-01-31 to 2025-12-30 | 75 | [NSE circular FAOP64672 (2024)](https://nsearchives.nseindia.com/content/circulars/FAOP64672.pdf) |
| WEEK1 | 2025-12-24 onward | 65 | [NSE circular FAOP70616 (2025)](https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf) |
| MONTH1 | 2025-12-31 onward | 65 | [NSE circular FAOP70616 (2025)](https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf) |

This uses last-old/first-new expiry dates as trade-date cutoffs because individual expiry IDs are absent in the Dhan rolling series. The additional regression test checks all proxy transitions. Corrected P&L and inference remain pending workflow #39774033025.



## Latest reprice audit

See [LOT_SIZE_REPRICE_AUDIT.md](LOT_SIZE_REPRICE_AUDIT.md). All 483,706 rows from the saved ledger were repriced using the corrected date/family lot schedule. No candidate from this frozen 600-candidate set met the joint median/validation/stress gates. The prior P&L result remains superseded; the corrected full re-evolution workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) completed successfully and its final metrics are summarized above.


## Corrected full evolutionary rerun — completed 2026-10-22

The corrected run [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) completed successfully. It reran the bounded search after the dated WEEK1/MONTH1 lot-size proxy correction. The run summary reports 1,241 sessions (2021-10-25–2026-10-21), 92,510 underlying rows, 2,600,975 rolling-option rows, 600 unique candidates, four islands and nine generations. All 1,708 acquisition requests were satisfied from the preserved cache; source failures in this corrected run: zero. Pre-run and post-run mathematical/test steps passed, and the sanitized report artifact was uploaded and bounded report files committed.

**Final corrected disposition: NO_STATISTICAL_CANDIDATE.** Zero of 600 candidates passed the statistical gate; zero passed the strict execution/promotion gate. The basic OHLC data-quality gate passed, but the execution data gate did not. Validation-selected candidate 86 had validation mean daily net P&L about ₹116.80; its OOS mean daily net was about ₹6.14, the 95% block-bootstrap lower bound was about −₹195.69, and Holm-adjusted p=1.0. It did not pass the gate. These figures supersede the earlier incorrect lot-size run; they do not establish profitability.

The corrected run summary is [run_summary.json](../../reports/quant_evolve_nob_v1/run_summary.json); its top-candidate table is in [the bounded run report](../../reports/quant_evolve_nob_v1/RESULTS.md), with the full downloadable files in [workflow artifact #39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025). The frozen-ledger reprice audit remains a separate sensitivity check, not a substitute for the corrected evolution.

Execution limitations remain: rolling ATM-relative OHLC does not provide historical bid/ask/depth or stable exact exchange contract identity. Lot sizes are date/family proxies, not an exact instrument-master join. Costs/slippage are modeled. Therefore no paper/live deployment or executable-fill claim is approved. No independent tester was performed, per user's explicit instruction.
