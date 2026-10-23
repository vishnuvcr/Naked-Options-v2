# QE-NOB-2.0 Candidate Reproducibility Audit

**Date:** 2026-10-23  
**Branch:** `research/quant-evolve-nob-v2-discovery-developer`  
**Evidence:** sanitized artifact from workflow [#39865627143](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143), including `finalist_oos_metrics.csv`, `oos_cost_stress.csv`, `candidate_archive.json`, and `run_summary.json`.  
**Role:** Developer-led audit only, per user instruction: no independent tester.

## Decision

**DATA-LIMITED — do not promote any candidate to paper or live trading.** Twelve of the 20 finalists pass the stored statistical gate after Holm correction, but every finalist has `execution_gate_pass=false`. Rolling ATM-relative OHLC data do not establish exact historical exchange contract identity, bid/ask/depth, or actual broker fills.

## Important reproducibility defect

The archive declares `actual_unique_candidate_count=1185` but the `candidates` array contains only 300 records (candidate IDs 0–299). As a result, the full rule objects for 15 of the 20 OOS finalists are missing from this archive. The OOS CSV still records their entry predicates, instrument, expiry family, moneyness, holding bars, and exit *kinds*, but it does not preserve all exact exit thresholds or exit priority details. Thus the earlier plain-language descriptions must not be treated as fully reproducible specifications.

This is logged as QE-NOB2-E012. Fix requirement: persist a complete candidate archive keyed by all 1,185 candidate IDs or, at minimum, include complete serialized strategy JSON for every finalist in the sanitized artifact; add a test that archive count equals the declared candidate count and that each finalist resolves to exactly one strategy definition.

## The 12 statistical-gate candidates

Values below are from the saved OOS metrics. Mean daily P&L is modeled net P&L, not a forecast or promise. Stress column is the stored scenario of 100 bps adverse slippage per side and ₹20 brokerage per order.

| ID | Entry predicate(s) | Instrument | Expiry / moneyness | Max hold (bars) | Exit kinds in report | OOS trades | Mean daily net (₹) | 95% CI for mean daily (₹) | Holm p | Mean daily net under stress (₹) |
|---:|---|---|---|---:|---|---:|---:|---:|---:|---:|
| 1008 | ema_fast_slow_sign > -1 | CALL | WEEK1 / OTM1 | 12 | risk stop + target + time | 1,551 | 1,024.18 | 626.72 to 1,449.46 | 0.003999 | 594.86 |
| 1163 | opening_gap_pct < 0.01 | CALL | WEEK1 / OTM1 | 60 | target + risk stop | 1,207 | 894.82 | 542.68 to 1,265.98 | 0.003999 | 561.48 |
| 799 | opening_gap_pct < 0.0025 | CALL | WEEK1 / OTM1 | 2 | time | 3,399 | 1,865.98 | 1,386.36 to 2,508.05 | 0.003999 | 525.43 |
| 1048 | opening_gap_pct > 0.0025 | PUT | WEEK1 / OTM1 | 2 | target + time | 1,077 | 734.87 | 443.61 to 1,074.40 | 0.003999 | 343.43 |
| 398 | opening_gap_pct < 0.0025 | CALL | WEEK1 / OTM1 | 24 | risk stop + target + time | 1,698 | 1,014.52 | 631.71 to 1,395.20 | 0.003999 | 601.40 |
| 496 | nifty_return_6 > 0 | PUT | WEEK1 / ATM | 36 | target + time + time | 522 | 1,450.80 | 1,024.99 to 1,882.39 | 0.003999 | 1,259.64 |
| 386 | opening_gap_pct > 0.0025 | CALL | WEEK1 / OTM1 | 2 | target + time | 1,087 | 1,210.24 | 789.95 to 1,717.41 | 0.003999 | 767.82 |
| 78 | opening_range_position > 0.5 | CALL | WEEK1 / OTM1 | 12 | time | 540 | 1,150.66 | 842.13 to 1,548.80 | 0.003999 | 924.00 |
| 705 | opening_gap_pct > 0.0025 | CALL | WEEK1 / OTM1 | 3 | time | 767 | 560.41 | 209.78 to 949.46 | 0.007598 | 233.05 |
| 264 | nifty_return_6 > 0 AND opening_range_position > 0 AND ema_fast_slow_sign > 0 | PUT | WEEK1 / OTM1 | 36 | target + time + target | 260 | 1,158.22 | 924.19 to 1,375.79 | 0.003999 | 1,076.16 |
| 814 | nifty_return_1 > -0.003 | CALL | WEEK1 / OTM1 | 24 | risk stop + target + time | 2,141 | 1,519.20 | 1,080.10 to 2,026.68 | 0.003999 | 989.97 |
| 936 | opening_gap_pct < 0.005 | CALL | WEEK1 / OTM1 | 48 | risk stop + target + time | 1,430 | 969.69 | 590.62 to 1,352.98 | 0.003999 | 603.43 |

The conditions above reproduce the stored predicates. Their economic interpretation remains uncertain until feature definitions are checked, especially whether `opening_gap_pct` is signed or absolute and what the feature's observation time is. A positive six-period index return paired with a PUT (candidate 496) is a contrarian hypothesis, not evidence that reversals occur.

## Statistical interpretation

- The table is conditional on the saved experimental pipeline and its modeled prices/costs.
- Statistical significance does not establish causality, stability, or executable profitability.
- The 100 bps / ₹20 stress result remains positive in this table for these 12 candidates, but the scenario is still a model assumption and does not solve missing historical contract identity or executable quotes.
- The experiment considered 1,185 unique candidates; the multiple-testing correction is important, but cannot correct data/contract mismatch or fill-model error.
- The table's reported exit kinds do not contain exact premium thresholds or same-bar exit priority. Do not infer these missing parameters.

## Required developer actions

1. Correct the candidate archive to retain all 1,185 candidate definitions and all finalist JSON.
2. Add regression checks for declared-versus-actual archive count, unique IDs, finalist coverage, exact exit parameter serialization, and exit-priority behavior.
3. Rerun the artifact generation; do not change the frozen OOS period or tune to its results.
4. Audit feature formulas/timestamps and contract mapping. Keep execution gate false until stable contract IDs and credible historical bid/ask/fill assumptions are supported.
5. Update results, phase status, error log and README from the new artifact. If the archive or execution data cannot be repaired within the bounded protocol, close as DATA-LIMITED rather than continuing an unbounded search.

## Scope note

No tester branch/report is required. This is a developer-side reproducibility audit; automated regression tests and evidence gates remain required.
