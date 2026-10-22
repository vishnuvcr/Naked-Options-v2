# QE-NOB-1.0 — fresh QuantEvolve-style naked option buying

**Run status:** PASS_ANALYZED (GitHub Actions overall failure was in the final commit/rebase step)  
**Date range:** 2021-10-25 to 2026-10-21  
**Candidates tested:** 600  
**Candidates meeting statistical gate:** 0  
**Candidates meeting strict execution/promotion gate:** 0  
**Basic data quality gate:** FAIL  
**Execution data gate:** FAIL  
**Decision:** DATA_LIMITED — no profitability conclusion; no strategy approved.

## Run and dataset

Workflow [#39712854501](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501) analyzed 1,241 sessions, 92,510 underlying rows, and 2,588,918 option rows after conflict filtering. Four islands evaluated 600 unique candidates over nine generations. Pre-run and post-run automated tests each passed (11 tests).

## Main finding

The best candidate selected on validation was a 0.15% opening-gap continuation rule. Its OOS mean daily net was ₹10.68, with a 95% block-bootstrap interval of -₹188.62 to ₹237.43/day, OOS Sharpe 0.097, profit factor 1.021, and Holm-adjusted p=1.0. The first OOS half averaged ₹109.76/day, while the second averaged -₹87.60/day, indicating instability. The modeled 100-bps slippage / ₹20-per-order stress case averaged -₹98.54/day; the 200-bps / ₹20-per-order case averaged -₹288.37/day. The candidate also failed the paired baseline significance test.

These are exploratory simulated results based on rolling option OHLC, not verified executable fills. They do not establish a profitable strategy.

## Data and execution limitations

- 471 duplicate groups were detected, 453 of which conflicted (96.18% of duplicate groups); 906 rows were excluded. This caused the basic data-quality gate to fail despite row-grid coverage of 99.947%.
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

The workflow uploaded the complete reports as an artifact. Its commit step failed during a rebase conflict in `INTERACTION_LOG.md`; the workflow is being corrected to commit a bounded allowlist and keep the large trade ledger only in the downloadable artifact.
