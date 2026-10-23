# QE-NOB-2.0 — Artifact integrity and bounded decision checkpoint

**Date:** 2026-10-23  
**Source artifact:** [Workflow #39865627143](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143), sanitized artifact ID 12464009881.  
**No independent tester role**, as instructed.

## Mechanical artifact checks

Re-read the actual artifact files locally and verified:

- Candidate archive records: 1,185; declared count: 1,185.
- Candidate signatures unique: 1,185.
- Finalist rows: 20; all 20 signatures resolve to exactly one candidate definition.
- Statistical-gate passes: 12 of 20.
- Execution-gate passes: 0 of 20.
- Cost-stress rows: 200, exactly 10 scenarios for each of 20 finalists.
- All 20 finalists have exactly one 100-bps-per-side / ₹20-per-order stress row.
- No finalist signatures are missing from the stress grid.

The previous archive-truncation concern was a false alarm due to joining on a non-unique island-local candidate ID; join by signature. It is closed in the error log.

## Source-code findings

- `opening_gap_pct` is signed; it is not an absolute gap.
- `nifty_return_1/3/6` are within-session close-to-close percentage changes.
- Opening-range position uses the first three bars and becomes available from the fourth bar.
- EMA feature is sign(EMA-8 minus EMA-21), with values -1, 0, +1.
- Signal rows map to the next bar, restricted to the same IST session.
- Simulator stop takes priority over target if both are touched in the same bar.
- Repeated exit rules are reduced by the minimum threshold for that kind; duplicate identical rules do not change that threshold.

These are code/artifact integrity checks, not a full independent statistical reimplementation and not proof of real-world execution.

## Decision

**DATA-LIMITED; no strategy approved for paper or live trading.**

The 12 statistical-gate candidates remain modeled research candidates. The simulator operates on rolling ATM-relative OHLC proxies; exact dated contract identity and historical executable bid/ask/depth/fill evidence are not verified. Costs and slippage are modeled, not observed Paytm Money fills. Stress-positive simulated means cannot repair these execution-data gaps.

## Bounded next action and stopping rule

The source/formula and artifact identity audit is complete for the available output. One final bounded feasibility action may be taken only if the repository's existing source gates can supply stable dated contracts and credible executable prices from already available free/paid sources. If those requirements cannot be met without changing the data product or scope, close QE-NOB-2.0 as DATA-LIMITED, publish the final manuscript and evidence tables, and propose any new research question separately. Do not continue parameter search or tune the existing OOS block.

No live orders, no paper-trading approval, and no claim of executable profitability.
