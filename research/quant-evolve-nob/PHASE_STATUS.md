# Phase status — QE-NOB-1.0

Last updated: 2026-10-22

Governance note: User explicitly declined an independent tester. No tester branch/report is required. Developer-side automated tests and explicit scientific/execution gates remain required.

| Phase | Status | Evidence / required exit gate |
|---|---|---|
| 1. Fresh protocol, literature seed, source audit | IN PROGRESS | Protocol and research questions frozen; verify official source register and implementation contract. |
| 2. Fresh data acquisition and cache | NOT STARTED | New isolated data cache; source/time coverage report, manifest hashes, licence and request-error log. |
| 3. Feature panel and option contract identity | NOT STARTED | Point-in-time alignment and fixed-contract continuity tests pass; no guessed strike/expiry mapping. |
| 4. Cost model and baseline tests | NOT STARTED | Paytm Money tariff frozen; unit tests verify brokerage, GST, exchange charges, stamp duty, STT by effective date and adverse slippage. |
| 5. Bounded QuantEvolve discovery | NOT STARTED | Candidate budget at most 600, max 25 generations, train/validation only, deterministic seeds. |
| 6. Nested chronological and OOS testing | NOT STARTED | Locked final OOS, Holm correction, block uncertainty, placebo and no-leakage tests pass. |
| 7. Robustness / execution gate | NOT STARTED | Base/stress costs, quote quality, regime and period stability, drawdown gates satisfied. |
| 8. Manuscript and final decision | NOT STARTED | Machine-readable data/results, figures, structured manuscript, final PASS / NO-GO / DATA-LIMITED decision. |

## Run rule
A phase changes status only after its exit evidence exists. Workflow success alone is not evidence that a strategy is profitable. A failed API/data/quality gate is recorded and is never converted into a strategy result. Stop after Phase 8; no unbounded evolutions.
