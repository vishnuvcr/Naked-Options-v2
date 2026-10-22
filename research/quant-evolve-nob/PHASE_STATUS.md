# Phase status — QE-NOB-1.0

Last updated: 2026-10-22

Governance note: User explicitly declined an independent tester. No tester branch/report is created or awaited. Developer-side automated tests and explicit scientific/execution gates remain required.

## Latest completed acquisition/discovery run

- Latest completed data-quality run: [#39741806754](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754). A lot-size defect was identified and fixed in code; corrected source/test run is in progress at [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025); its pre-run test step passed. Earlier stalled run [#39741823249](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741823249) is not final evidence.
- Run status: `PASS_ANALYZED`; workflow and bounded report commit succeeded. Offset-aware duplicate identity reduced duplicate/conflicting groups to zero; no rows were removed by conflict filtering.
- Data window: 2021-10-25 to 2026-10-21; 1,241 sessions; 92,510 underlying rows; 2,600,975 option rows. Timestamp coverage 99.772%; row-grid coverage 100%.
- Evolution: 600 unique candidates, 4 islands, 9 generations completed.
- Candidate gates: 0/600 met the statistical gate; 0 passed the strict execution/promotion gate.
- Duplicate/grid gate: PASS after adding ATM offset to the duplicate key (0 duplicate groups; 0 conflicting groups; 0 rows dropped). This is a request-identity check, not proof of stable exchange contract identity.
- Research execution policy: missing bid/ask/depth does not block OHLC-based statistical analysis. It remains a separate execution-readiness failure and bars executable/paper/live claims.
- Historical lot-size bug: the prior proxy wrongly used 25 lots before November 2024. Code now uses official NSE effective-date schedules by rolling family (WEEK1 vs MONTH1); corrected backtest/inference are pending the bounded rerun. Prior P&L metrics are superseded.
- Interim decision: no strategy is approved. Do not rely on pre-correction OOS values; read the updated `RESULTS.md` and `MANUSCRIPT.md` after workflow #39774033025 completes.

| Phase | Status | Evidence / required exit gate |
|---|---|---|
| 1. Fresh protocol, literature seed, source audit | COMPLETE WITH LIMITATIONS | Frozen protocol and source audit recorded; no prior study performance imported. |
| 2. Fresh data acquisition and cache | COMPLETE WITH LIMITATIONS | Dhan acquisition produced a multi-year rolling ATM-relative OHLC dataset; corrected duplicate key yields zero duplicate groups, but exact contract identity and failed source requests remain documented. |
| 3. Feature panel and option contract identity | COMPLETE WITH LIMITATIONS | Rolling ATM-relative data are used for exploratory OHLC tests; exact contract identity is unknown and lot sizing uses a sourced family/date proxy. |
| 4. Cost model and baseline tests | COMPLETE WITH LIMITATIONS | Uses published ₹10/order primary brokerage, ₹20/order stress, date-effective statutory-fee approximations, 50-bps primary adverse slippage and higher slippage stresses; spreads are not observed. |
| 5. Bounded QuantEvolve discovery | COMPLETE | 600 unique constrained candidates evaluated over 9 generations; selection used train/validation only. |
| 6. Nested chronological and OOS testing | COMPLETE — NO PASS | Final chronology evaluated; Holm-adjusted p-values, block uncertainty, split-half checks and baseline comparisons did not clear the gates. |
| 7. Robustness / execution gate | IN PROGRESS — CORRECTED RERUN | OHLC-based robustness analysis proceeds regardless of quote depth; exact execution readiness remains failed. New workflow started after its pre-run tests passed; recompute results after dated-lot proxy correction. |
| 8. Manuscript and final decision | IN PROGRESS — METRICS SUPERSEDED | Documentation records the discovered lot-size defect and the corrected bounded rerun. Final statistical conclusion is pending revised results; no tester branch per user instruction. |

## Run rule
A phase changes status only after its exit evidence exists. Workflow success alone is not evidence that a strategy is profitable. Missing execution quotes are recorded as limitations but do not halt the bounded OHLC analysis. Lot-size proxy corrections invalidate earlier P&L metrics until rerun. Stop after Phase 8; no unbounded evolutions.
