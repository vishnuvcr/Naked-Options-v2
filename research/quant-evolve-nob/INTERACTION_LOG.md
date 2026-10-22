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
