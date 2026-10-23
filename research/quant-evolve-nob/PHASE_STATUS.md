# Phase status — QE-NOB-1.0

## QE-NOB-2.0 TOTP acquisition recovery update — 2026-10-23

- Authentication: PASS in workflow [#39844476476](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39844476476); fresh token passed Dhan `/profile` validation.
- Acquisition: BLOCKED/INCOMPLETE in run #39844476476. Three bounded passes ended partial; the last pass recorded 363/366 option requests (358 cached, 5 newly downloaded in that pass) with 3 transient read timeouts. Underlying requests passed. No candidate discovery ran.
- Cache audit: PASS, 816 JSON files parsed, zero parse failures; 25 underlying files and 791 option files. Audit explicitly says exact contract identity and historical bid/ask/depth are unverified.
- Correction: request timeout increased from 25s to 40s; attempts increased from 2 to 4; bounded exponential retry backoff 2/4/8s. Regression expectations updated. Error QE-NOB2-E010 logged.
- Current status: validation reruns [#39865638080](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865638080) and [#39865638057](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865638057) are queued/running after sequential commits; verify final test/acquisition outcome before advancing. Keep candidate discovery blocked unless acquisition is PASS and quality gates pass.

Last updated: 2026-10-22 (final corrected rerun completed)

Governance note: User explicitly declined an independent tester. No tester branch/report is created or awaited. Developer-side automated tests and explicit scientific/execution gates remain required.

## Latest completed acquisition/discovery run

- Latest completed data-quality run: [#39741806754](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754). A lot-size defect was identified and fixed in code; corrected full rerun completed successfully at [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025); its pre-run test step passed. Earlier stalled run [#39741823249](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741823249) is not final evidence.
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
| 7. Robustness / execution gate | COMPLETE WITH LIMITATIONS — NO-GO | Repricing 483,706 saved trades with corrected dated lot proxies yielded no frozen candidate meeting the joint median/validation/stress gates. Quote/depth and stable contract identity remain execution limitations. Corrected full search workflow #39774033025 is supplementary and was still in progress at the last check. |
| 8. Manuscript and final decision | COMPLETE — NO-GO ON SAVED CANDIDATE SET | Reprice audit and structured manuscript are committed. No strategy is approved; a single corrected full-run workflow is already active as supplementary confirmation. No tester branch per user instruction. |

## Run rule
A phase changes status only after its exit evidence exists. Workflow success alone is not evidence that a strategy is profitable. Missing execution quotes are recorded as limitations but do not halt the bounded OHLC analysis. Lot-size proxy corrections invalidate earlier P&L metrics until rerun. Stop after Phase 8; no unbounded evolutions.


## Bounded reprice disposition — 2026-10-22

[LOT_SIZE_REPRICE_AUDIT.md](LOT_SIZE_REPRICE_AUDIT.md) reprices 483,706 trade-ledger rows using the corrected NSE effective-date/family lot proxy. The frozen prior candidate set has no strategy passing the combined daily-median, corrected-validation and stress-cost prerequisites. The research decision is NO-GO for strategy approval. A running full corrected re-evolution workflow has completed, but absent bid/ask/depth is not a reason to pause OHLC-based research. Do not expand the search budget.


## Final corrected full-run checkpoint — 2026-10-22

- Corrected full evolution workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025): **completed successfully**. The bounded search finished after the date/family lot-size correction; pre-run and post-run automated test steps passed; reports were uploaded and committed.
- Final output: 600 unique candidates, four islands, nine generations; 0/600 statistical gate passes and 0 execution/promotion gate passes. Basic OHLC data-quality gate passed; execution-data gate failed due missing historical bid/ask/depth and unverified exact contract identity.
- Final research decision: **NO_STATISTICAL_CANDIDATE / NO-GO for strategy approval**. No additional search expansion is authorized. See [corrected run results](../../reports/quant_evolve_nob_v1/RESULTS.md), [workflow](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025), and [frozen-candidate reprice audit](LOT_SIZE_REPRICE_AUDIT.md).
- Independent tester: not performed, as explicitly declined by the user. This is developer-led research with automated checks only.


## QE-NOB-2.0 acquisition/discovery checkpoint — 2026-10-23

- Corrected bounded acquisition workflow [#39865627143](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143) completed successfully after increasing Dhan request timeout to 40s and attempts to four with bounded backoff. Fresh TOTP authentication and profile validation passed.
- Cache: 819 JSON files (25 underlying, 794 option); 92,891 underlying rows and 467,834 option rows read. Duplicate groups/conflicts: 0. Option timestamp coverage: 99.9897%; row-grid coverage: 100%.
- Feature panel: 46,443 rows across 621 sessions. Seven price/time-derived features passed the coverage/variation gates; VWAP distance was excluded because no usable volume-derived values were present. Global markets, India VIX, option IV/OI, FII/DII, news/event and contract-level features are still absent.
- Bounded discovery ran: 1,185 unique candidates, 4 islands, 20 generations, 20 finalists; 12 candidates passed the statistical screen. This is not evidence of executable profitability. `execution_gate_pass=false` because rolling OHLC cannot establish stable exchange contract identity, historical bid/ask/depth, or actual broker fills.
- Chronology report in the run summary uses 621 training sessions, 207 validation sessions, and 208 OOS sessions (OOS dates 2025-02-25 to 2025-12-30). Verify candidate-level OOS statistics, cost-stress tables, and source failures in artifact [12464009881](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143/artifacts/12464009881) before any promotion decision.
- Primary modelled costs: 50 bps adverse slippage per side and ₹10/order brokerage; stress grid covers 0–200 bps and ₹10/₹20 per order. These are assumptions, not observed fills. Statistical gate allows further simulation only; no paper/live authorization.
- Decision: **DATA-LIMITED; statistical candidate(s) found, executable profitability unverified**. Do not treat workflow success as strategy validation. Preserve this boundary in all downstream summaries.

Last updated: 2026-10-23 after completed run #39865627143.
