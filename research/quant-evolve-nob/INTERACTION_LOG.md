## 2026-10-22 — corrected frozen-candidate reprice audit
- User instructed that unavailable bid/ask/depth and fully reconciled broker tariffs must not block the analysis; use available OHLC with explicit cost/slippage assumptions.
- Downloaded the saved sanitized artifact from [workflow #39741806754](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754/artifacts/12417631602) and re-priced all 483,706 rows using the corrected WEEK1/MONTH1 lot proxy and the same cost model.
- Audit result: no candidate in the frozen prior 600-candidate set met the combined daily-median, validation and cost-stress prerequisites. Candidate 86 revised OOS mean/day about ₹6.14 and loses about ₹104/day at 100-bps/₹20-order stress; candidate 558 OOS mean/day about ₹70.37 but daily median is zero and 200-bps stress is about −₹80.53/day. Full table and method are in [LOT_SIZE_REPRICE_AUDIT.md](LOT_SIZE_REPRICE_AUDIT.md).
- Because seven zero-trade session dates were omitted from the ledger export, the HAC/Holm reprice diagnostic inserted zero days evenly; the current full underlying-grid workflow remains the source for final exact inference. This is disclosed and not presented as an independent review.
- Corrected full workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) was still running at last status check. It is a bounded supplementary confirmation; missing bid/ask/depth does not block the OHLC research conclusion.
- User explicitly declined a tester; no tester branch/report is created or claimed.

## 2026-10-22 — corrected rerun started
- Current corrected workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) is in progress. The pre-run automated test step passed with the dated-lot regression test included.
- Stale workflow [#39741823249](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741823249) was canceled during the lot-size correction and its report commit hit rebase conflicts in `source_probe.json` and `acquisition_summary.json`. This is recorded as QE-NOB-E007; concurrency was updated to let corrected source supersede stale runs. The current run should be checked for clean report persistence.
- No corrected P&L is claimed yet; previous candidate numbers remain superseded until the current run's report is committed and inspected.

## 2026-10-22 — execution-validation policy and dated lot-size correction
- User explicitly directed that historical bid/ask/depth and a fully verified Paytm Money tariff should not block the research; continue with available OHLC price data and disclose assumptions.
- Verified official NSE lot schedules from [FAOP47854](https://archives.nseindia.com/content/circulars/FAOP47854.pdf) (NIFTY 75→50 for monthly July-2021 and weekly August-2021 expiries onward), [FAOP61415](https://nsearchives.nseindia.com/content/circulars/FAOP61415.pdf) (50→25, first revised weekly 2-May-2024 and monthly 30-May-2024), [FAOP64672](https://nsearchives.nseindia.com/content/circulars/FAOP64672.pdf) (25→75; last old weekly 19-Dec-2024 / first new 2-Jan-2025; last old monthly 30-Jan-2025 / first new 27-Feb-2025), and [FAOP70616](https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf) (75→65; first revised weekly 6-Jan-2026 and monthly 27-Jan-2026).
- Found QE-NOB-E006: the old proxy mistakenly used 25 units for all dates before 2024-11-20. Replaced it with an expiry-family/date-based proxy for WEEK1 vs MONTH1 and added transition tests.
- Existing P&L metrics are superseded until corrected backtest reruns. The research will use next-bar option OHLC, ₹10/order primary brokerage per the current Paytm Money FAQ, ₹20/order cost stress, modeled adverse slippage, and date-based exchange/statutory-fee approximations. Missing spreads/depth remain a separate execution-readiness limitation.
- Source commit: `3889440`; regression tests: `7ff4039`; concurrency update: `8523f51`. Corrected workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) is pending; older run #39741823249 is not treated as final.
- No independent tester branch/report is created or awaited, as the user explicitly declined a tester.

# Activity log — QE-NOB-1.0

## 2026-10-22 — duplicate-key correction and rerun
- Investigated the duplicate diagnostics. The source request filename and request body encode ATM offset, while the prior deduplication key omitted it; identical strikes can occur across different rolling ATM offsets.
- Added offset to the duplicate key and added a regression test ensuring same timestamp/strike rows from different offsets remain separate.
- Workflow [#39741806754](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754) completed successfully: 2,600,975 option rows, 0 duplicate groups, 0 conflicting groups, 0 rows dropped, 99.772% timestamp coverage, 100% row-grid coverage; 11 automated tests passed.
- The statistical result remains negative: 0/600 candidates passed the preregistered statistical gate. Best validation-selected candidate (ID 86) had OOS mean daily net ₹10.68, 95% block CI −₹188.62 to ₹237.43, Holm p=1.0, and −₹98.54/day under 100-bps/₹20-per-order stress. Execution/contract gate remains blocked.
- Follow-up workflow [#39741823249](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741823249) was triggered by the regression-test commit and is still running at this log update.
- User-facing instruction remains “No tester”; no independent tester is claimed.



This is an audit of user-facing scope decisions and concrete work. It is not a verbatim transcript and does not store private hidden reasoning.

## 2026-10-22 — fresh-start instruction
- User instructed: forget existing findings and start a new QuantEvolve study to find profitable strategies using naked option buying.
- Scope interpreted as NIFTY 50 long-premium options, constrained evolution and after-cost net profitability; no short-option legs.
- Existing performance reports are explicitly excluded from priors, strategy seeding, score computation and evidence. New run/cache/results identifiers are isolated.
- User previously said “No tester”; the fresh workflow therefore proceeds developer-led and does not rely on a tester branch/report.
- Phase 1 protocol created. No QE-NOB-1.0 market data has been acquired and no profitability claim is made.

## 2026-10-22 — developer-led workflow preference reaffirmed
- User explicitly reiterated: “No tester.” The QE-NOB-1.0 work will proceed without creating, invoking, or waiting on an independent tester branch/report.
- Quality controls remain automated developer-side gates: unit tests before/after the run, locked chronological OOS, family-wide multiple-testing correction, cost stress tests, and an explicit execution-data limitation. These are not described as independent testing.
- At the latest check, GitHub Actions run 39712854501 remained in progress at “Run fresh QuantEvolve study”; the run had not yet produced a report that supports profitability conclusions. No strategy is approved at this point.


## 2026-10-22 — tester explicitly declined
- User clarified: “No tester”. This fresh QE-NOB study will proceed developer-led; do not create, invoke, or wait for an independent tester branch/report.
- This changes the governance route only, not the statistical or data-quality gates. Developer-side validation and automated tests remain mandatory; limitations and unresolved execution-data gates must be disclosed.
- At this update, workflow #39712854501 was still running in the QuantEvolve study step. No strategy result is inferred from an in-progress run.


## Run #39712854501 — 2026-10-22
- The bounded QE-NOB run completed its analysis stage: 600 candidates evaluated; zero passed statistical or execution/promotion gates.
- Data quality failed on 453 conflicting duplicate groups out of 471 duplicate groups. Historical bid/ask/depth and exact expiry/lot-size mapping remain unverified.
- Best validation-selected gap-continuation candidate had OOS mean daily net ₹10.68, 95% block CI -₹188.62 to ₹237.43, Holm p=1.0, and stressed mean daily net -₹98.54 at 100-bps/₹20-order assumptions. No strategy is approved.
- GitHub Actions tests passed (11 passed before and after the run), but the final commit step failed during rebase due to a concurrent INTERACTION_LOG.md conflict. A workflow correction is required; full report artifact remains available at [run #39712854501](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501).
- User reiterated “No tester”; this research proceeds developer-led and does not claim independent testing.
