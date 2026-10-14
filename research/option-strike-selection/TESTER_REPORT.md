# Independent tester report — OPT-BUY-2.0 strike grid

**Review date:** 2026-10-14  
**Source workflow:** [Run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651)  
**Artifact SHA-256:** `e727095479b645703252832956a99a2924a5b5f68c507d68ec38b66ec9bd61e5`  
**Reviewed candidate:** developer result in `research/option-strike-selection/RESULTS.md`  
**Tester disposition:** **FAIL — NO-GO for every tested candidate.**  
**Scope:** independent audit of saved artifact and conclusions; not a live-execution or data-source certification.

## 1. Independent reproduction

I extracted the workflow artifact and independently filtered the candidate metrics to `mode=model_filtered`, `slippage_bps_per_side=50`, `brokerage_per_order_rupees=10`. The resulting primary family contains 32 cells (16 strike pairs × 2 horizons).

| Check | Independent result | Verdict |
|---|---:|---|
| Primary cells | 32 | PASS |
| Cells with positive mean daily net P&L | 0/32 | FAIL profitability |
| Cells with 95% CI lower bound above zero | 0/32 | FAIL profitability |
| Cells with 95% CI upper bound below zero | 32/32 | Negative measured outcomes |
| Cells with both chronological-half means positive | 0/32 | FAIL robustness |
| Cells with coverage ≥80% | 2/32 | Only ATM/ATM at horizons 5 and 20 |
| Cells with ≥100 alert trades | 28/32 | Four fail sample-size gate |
| Candidate/horizon rows in `primary_tests_holm.csv` with nonempty p-values | 0/32 | FAIL inference deliverable |

Reproduced extremes: mean net daily P&L spans **−₹316.87 to −₹622.96** per eligible-date slot; mean return per trade spans about **−5.75% to −19.99%**. The least-negative cell is ATM/ATM with horizon 5 (224 alert trades, 83.67% coverage, mean −₹316.87/date, 95% interval −₹406.77 to −₹233.80). Its two chronological halves are both negative (−₹210.59 and −₹423.14).

These are the stored one-lot-proxy ledger metrics. They are not account-level performance or capital-normalized drawdown estimates.

## 2. Data-quality gate audit

The run summary reports 1,058,956 raw quote rows, 1,026,569 usable rows, and 452 conflicting duplicate groups out of 31,935 duplicate groups, or **1.4154%**. The frozen maximum is 1%; therefore the source-quality gate fails. Only ATM/ATM coverage exceeds the 80% threshold. These failures prohibit confirmatory ranking.

## 3. High-severity inference/report defect

All 32 rows in `primary_tests_holm.csv` have `n_observations=0` and blank raw/Holm p-values. Candidate metric rows also contain blank p-values. This contradicts the plan's requirement for primary paired tests and multiplicity correction. The p-value correction in the commit message did not yield usable output in this run. The exact root cause is not established by the artifact, so I do not infer it.

**Required disposition:** log a new error, do not claim adjusted significance, and do not run another model/strike parameter search. The grid's frozen data gate failed and every candidate's after-cost outcome is negative, so the present study should stop as NO-GO. A narrowly scoped code/report correction may be undertaken only if needed to make the artifact accurately report that inference is unavailable; it must not be used to re-open candidate optimization.

## 4. Developer report checks

- The developer's central conclusion—no candidate meets profitability gates—is supported.
- The conflict-rate and coverage gate conclusions are supported.
- The missing p-values must remain explicitly marked as an unresolved defect.
- Rupee cumulative drawdown from this proxy ledger must not be presented as a percentage portfolio drawdown. A capital model, position-sizing rule and compounding assumptions are absent.
- Positive paired differences versus an always-buy baseline, if computed later, would indicate only relative loss reduction unless absolute net P&L is positive and the full gates pass.

## 5. Final independent decision

**FAIL / NO-GO.** Do not paper-trade or live-trade these candidates. No candidate has acceptable measured losses, positive net expectancy, or evidence of minimum drawdown. Preserve the artifact and logs, update README/status, and stop the frozen OPT-BUY-2.0 grid. Any future study must be a separately versioned protocol with improved quote quality and a prespecified risk/capital model.

### Instructions to developer

Record this tester disposition and the blank p-value defect in the main error/status logs and README. Do not proceed to a new strategy or parameter loop under OPT-BUY-2.0. Any future research must be separately versioned and have independent tester review after results acquisition.
