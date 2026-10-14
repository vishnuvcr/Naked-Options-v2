# OPT-BUY-2.0 strike-grid results — run #5

**Date:** 2026-10-14  
**Workflow:** [Run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651)  
**Artifact SHA-256:** `e727095479b645703252832956a99a2924a5b5f68c507d68ec38b66ec9bd61e5`  
**Disposition:** **NO-GO for all tested candidates; exploratory only.**  
**Developer branch:** `research/option-strike-selection-developer`

## Executive result

The frozen 16-pair × 2-horizon strike grid does not identify a candidate with acceptable evidence of profitability. At the primary cost setting (₹10 per order and 50 bps adverse slippage per premium side), all 32 alert-filtered candidate/horizon cells have negative mean net daily P&L, and every reported 95% block-bootstrap interval lies entirely below zero. Both chronological-half means are negative for every cell. This is evidence against these specific implementations on this dataset, not proof that every possible strategy fails.

The classifier reduced exposure relative to buying every eligible date, but reduced losses versus a worse baseline is not profitability.

## Data and quality gates

| Item | Observed | Frozen gate | Outcome |
|---|---:|---:|---|
| Raw quote rows | 1,058,956 | — | — |
| Usable quote rows | 1,026,569 | — | — |
| Conflicting duplicate groups | 452 / 31,935 = 1.4154% | ≤1% | **FAIL** |
| Parse failures | 0 | 0 | PASS |
| Test dates | 980 | — | — |
| Candidate coverage | 17.45%–83.67% | ≥80% per candidate | **Only ATM/ATM passes** |
| Primary comparisons | 32 | — | — |
| Alert trades | 44–259 across cells | ≥100 per candidate | Several fail |

The confirmatory data gate fails. All ranking/inference must therefore be considered exploratory even before considering the negative P&L.

## Primary-cost results (₹10/order; 50 bps per premium side)

Across the 32 model-filtered cells:
- **32/32 mean net P&L values are negative.**
- **32/32 95% block-bootstrap upper bounds are below zero.**
- **0/32 chronological-half pairs have positive means in both halves.**
- Daily mean P&L ranges from **−₹316.87 to −₹622.96** per eligible-date slot.
- Mean return per executed trade ranges from approximately **−5.75% to −19.99%** on the recorded premium-debit denominator.
- Win rate ranges from **0% to 18.9%**.
- The least-negative cell is ATM/ATM, 5-session alert: mean **−₹316.87 per eligible date**, 224 trades, 83.67% coverage, 95% interval **−₹406.77 to −₹233.80**; first/second half means **−₹210.59 / −₹423.14**.
- ATM/ATM, 20-session alert: mean **−₹328.84 per eligible date**, 259 trades, 83.67% coverage, 95% interval **−₹416.06 to −₹245.86**; first/second half means **−₹244.43 / −₹413.26**.

The ATM/ATM candidates have adequate coverage, but still fail every profitability gate. No candidate is approved.

## Inference defect retained as an explicit limitation

The artifact's `primary_tests_holm.csv` contains zero observations and blank raw/Holm p-values for all 32 rows, despite nonempty candidate metric summaries. Therefore the planned primary paired significance/Holm inference was **not produced** by run #5. This is an unresolved report/implementation defect, not evidence of non-significance. Do not claim a valid p-value or adjusted significance result from this artifact. Because the frozen data gate already fails and all candidate P&L intervals are negative, do not expand parameter search to rescue the study; log the inference defect and stop this grid.

## Drawdown interpretation

This run is not a capital-normalized portfolio backtest. The ledger is a one-lot-proxy P&L per eligible date; cumulative rupee drawdown depends on the proxy sizing, capital and compounding assumptions. It must not be presented as a percentage drawdown or as a live-account estimate. The daily ledger contains large negative days (roughly ₹4,487–₹7,517 across candidate cells under the primary costs), which reinforces that the current implementations do not satisfy a low-loss objective.

## Conclusion and next action

**Stop OPT-BUY-2.0 at the frozen grid.** Do not relax data gates, tune the classifier, choose a strike based on relative loss reduction, or paper/live trade these candidates. Record the blank p-value output as an error, independently audit arithmetic and gate conclusions on a separate tester branch, and update the repository status. Any future work requires a separately versioned protocol and better point-in-time quote quality; it must not be an unbounded optimization loop.

This result is a bounded historical study, not investment advice and not a guarantee about future losses.
