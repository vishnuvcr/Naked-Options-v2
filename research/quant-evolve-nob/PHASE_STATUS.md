# Phase status — QE-NOB-1.0

Last updated: 2026-10-22

Governance note: User explicitly declined an independent tester. No tester branch/report is created or awaited. Developer-side automated tests and explicit scientific/execution gates remain required.

## Latest completed acquisition/discovery run

- Latest completed workflow: [#39741806754](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754); follow-up [#39741823249](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741823249) is still in progress.
- Run status: `PASS_ANALYZED`; workflow and bounded report commit succeeded. Offset-aware duplicate identity reduced duplicate/conflicting groups to zero; no rows were removed by conflict filtering.
- Data window: 2021-10-25 to 2026-10-21; 1,241 sessions; 92,510 underlying rows; 2,600,975 option rows. Timestamp coverage 99.772%; row-grid coverage 100%.
- Evolution: 600 unique candidates, 4 islands, 9 generations completed.
- Candidate gates: 0/600 met the statistical gate; 0 passed the strict execution/promotion gate.
- Duplicate/grid gate: PASS after adding ATM offset to the duplicate key (0 duplicate groups; 0 conflicting groups; 0 rows dropped). This is a request-identity check, not proof of stable exchange contract identity.
- Execution gate: FAIL. Historical best bid/ask/depth and exact expiry-level contract/lot-size mapping are not validated.
- Decision: `DATA_LIMITED`; no profitability conclusion and no strategy approved.
- Best validation-selected candidate was a 0.15% opening-gap continuation rule, but OOS mean daily net was only ₹10.68, its 95% block-bootstrap interval included large losses (-₹188.62 to ₹237.43/day), Holm-adjusted p=1.0, and stressed costs produced -₹98.54/day at the 100-bps/₹20-order scenario. This is not a usable profitable strategy.

| Phase | Status | Evidence / required exit gate |
|---|---|---|
| 1. Fresh protocol, literature seed, source audit | COMPLETE WITH LIMITATIONS | Frozen protocol and source audit recorded; no prior study performance imported. |
| 2. Fresh data acquisition and cache | COMPLETE WITH LIMITATIONS | Dhan acquisition produced a multi-year rolling ATM-relative OHLC dataset; corrected duplicate key yields zero duplicate groups, but exact contract identity and failed source requests remain documented. |
| 3. Feature panel and option contract identity | BLOCKED | Rolling ATM-relative rows do not establish stable exact expiry/strike continuity or dated lot-size truth. |
| 4. Cost model and baseline tests | PARTIAL / PROVISIONAL | Brokerage/fees and slippage are modeled; exact historical Paytm Money tariff and observed bid/ask spreads are not verified. |
| 5. Bounded QuantEvolve discovery | COMPLETE | 600 unique constrained candidates evaluated over 9 generations; selection used train/validation only. |
| 6. Nested chronological and OOS testing | COMPLETE — NO PASS | Final chronology evaluated; Holm-adjusted p-values, block uncertainty, split-half checks and baseline comparisons did not clear the gates. |
| 7. Robustness / execution gate | BLOCKED / FAIL | Data-quality gate and execution-data gate failed; stress-cost results were not robust. |
| 8. Manuscript and final decision | IN PROGRESS | Results and report uploaded; commit reconciliation, durable report links, and manuscript appendices/figures remain to be completed. |

## Run rule
A phase changes status only after its exit evidence exists. Workflow success alone is not evidence that a strategy is profitable. A failed API/data/quality gate is recorded and is never converted into a strategy result. Stop after Phase 8; no unbounded evolutions.
