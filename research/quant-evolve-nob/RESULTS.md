# QE-NOB-1.0 — fresh QuantEvolve-style naked option buying

**Run status:** PASS_ANALYZED — corrected duplicate identity passed; workflow #39741806754 completed successfully  
**Date range:** 2021-10-25 to 2026-10-21  
**Candidates tested:** 600  
**Candidates meeting statistical gate:** 0  
**Candidates meeting strict execution/promotion gate:** 0  
**Basic data quality gate:** PASS on duplicate/grid checks (contract identity still unverified)  
**Execution data gate:** FAIL  
**Decision:** DATA_LIMITED — no profitability conclusion; no strategy approved.

## Run and dataset

Corrected workflow [#39741806754](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754) analyzed 1,241 sessions, 92,510 underlying rows, and 2,600,975 option rows. After including rolling ATM offset in the duplicate key, there were 0 duplicate groups, 0 conflicting groups, and 0 rows dropped. Timestamp coverage was 99.772%; row-grid coverage was 100%. Automated tests passed (11 tests). Four islands evaluated 600 unique candidates over nine generations. Pre-run and post-run automated tests each passed (11 tests).

## Main finding

The best candidate selected on validation was a 0.15% opening-gap continuation rule. Its OOS mean daily net was ₹10.68, with a 95% block-bootstrap interval of -₹188.62 to ₹237.43/day, OOS Sharpe 0.097, profit factor 1.021, and Holm-adjusted p=1.0. The first OOS half averaged ₹109.76/day, while the second averaged -₹87.60/day, indicating instability. The modeled 100-bps slippage / ₹20-per-order stress case averaged -₹98.54/day; the 200-bps / ₹20-per-order case averaged -₹288.37/day. The candidate also failed the paired baseline significance test.

These are exploratory simulated results based on rolling option OHLC, not verified executable fills. They do not establish a profitable strategy.

## Data and execution limitations

- Corrected duplicate identity includes the source ATM offset; this reduced the detected duplicate groups from 471 (453 conflicting) to zero. This resolves the prior duplicate-key diagnostic but does not validate exact exchange contract identity.
- Dhan rolling ATM-relative option OHLC does not provide historical best bid/ask/depth for execution validation.
- Exact historical expiry, stable strike/contract identity and lot-size mapping have not been reconciled to dated instrument-master evidence.
- Cost assumptions are provisional and must be reconciled to the actual Paytm Money tariff effective on each date.
- Failed Dhan requests are preserved in the source failure report.

## Final disposition

**DATA-LIMITED / NO-GO for strategy approval.** Do not paper trade or deploy any candidate from this run. Resolve duplicate identity semantics, validate exact contract continuity and dated lot sizes, obtain or defensibly reconstruct executable quotes, freeze the actual cost schedule, and rerun the frozen gates before considering prospective paper testing.

## Artifacts

- [Workflow run and downloadable report artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501)
- [Research phase status](PHASE_STATUS.md)
- [Error log](ERROR_LOG.md)
- [Research plan](PLAN.md)
- [Source and literature notes](LITERATURE_REVIEW.md)
- [Run summary JSON](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v1-developer/reports/quant_evolve_nob_v1)

The corrected report artifact and bounded report files were committed by workflow #39741806754. A follow-up workflow #39741823249 was queued by the test change and is being monitored.
