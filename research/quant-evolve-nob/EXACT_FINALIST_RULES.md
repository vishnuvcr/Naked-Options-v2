# QE-NOB-2.0 — Exact definitions for the 12 statistical-gate candidates

Source: sanitized artifact from workflow [#39865627143](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143), joining `finalist_oos_metrics.csv` to `candidate_archive.json` by the cryptographic `signature` field. Candidate archive entries have island-local candidate IDs that repeat; **do not join the archive by candidate_id alone**. All 20 finalist signatures resolve to a complete strategy object.

**Interpretation caution:** This is a faithful extraction of the stored candidate specifications, not an endorsement. Every finalist's execution gate is false. Historical contract identity, bid/ask/depth and actual broker fills remain unverified. The feature formulas and timing must be checked in code before any deployment.

## Shared definitions

- Expiry family: `WEEK1` (the model's nearest-weekly family; not proof of a stable dated exchange contract).
- `OTM1`: one strike out of the money; `ATM`: at the money.
- `premium_risk_stop: 0.2`: 20% adverse premium move as represented by the simulator.
- `premium_target: 0.35`: 35% favorable premium move as represented by the simulator.
- `time_exit`: exit at the configured maximum holding horizon.
- `hold_bars`: maximum holding horizon in the simulator's bars. The report does not make the bar duration implicit in this table; see feature/simulator code.
- If a candidate contains duplicate exit kinds, retain that exact structure for audit; do not silently deduplicate or assume exit-priority semantics.

## Candidate specifications and reported metrics

| Candidate | Exact entry predicate(s), joined by AND | Side | Moneyness | Hold bars | Exit rules in stored order | OOS trades | Mean daily net (₹) | 95% CI (₹) | Holm-adjusted p | Mean daily net at 100 bps/side + ₹20/order (₹) |
|---:|---|---|---|---:|---|---:|---:|---:|---:|---:|
| 1008 | `ema_fast_slow_sign > -1` | CALL | OTM1 | 12 | stop 20%; target 35%; time | 1,551 | 1,024.18 | 626.72–1,449.46 | 0.003999 | 594.86 |
| 1163 | `opening_gap_pct < 0.01` | CALL | OTM1 | 60 | target 35%; stop 20% | 1,207 | 894.82 | 542.68–1,265.98 | 0.003999 | 561.48 |
| 799 | `opening_gap_pct < 0.0025` | CALL | OTM1 | 2 | time | 3,399 | 1,865.98 | 1,386.36–2,508.05 | 0.003999 | 525.43 |
| 1048 | `opening_gap_pct > 0.0025` | PUT | OTM1 | 2 | target 35%; time | 1,077 | 734.87 | 443.61–1,074.40 | 0.003999 | 343.43 |
| 398 | `opening_gap_pct < 0.0025` | CALL | OTM1 | 24 | stop 20%; target 35%; time | 1,698 | 1,014.52 | 631.71–1,395.20 | 0.003999 | 601.40 |
| 496 | `nifty_return_6 > 0` | PUT | ATM | 36 | target 35%; time; time (duplicate retained) | 522 | 1,450.80 | 1,024.99–1,882.39 | 0.003999 | 1,259.64 |
| 386 | `opening_gap_pct > 0.0025` | CALL | OTM1 | 2 | target 35%; time | 1,087 | 1,210.24 | 789.95–1,717.41 | 0.003999 | 767.82 |
| 78 | `opening_range_position > 0.5` | CALL | OTM1 | 12 | time | 540 | 1,150.66 | 842.13–1,548.80 | 0.003999 | 924.00 |
| 705 | `opening_gap_pct > 0.0025` | CALL | OTM1 | 3 | time | 767 | 560.41 | 209.78–949.46 | 0.007598 | 233.05 |
| 264 | `nifty_return_6 > 0 AND opening_range_position > 0 AND ema_fast_slow_sign > 0` | PUT | OTM1 | 36 | target 35%; time; target 35% (duplicate retained) | 260 | 1,158.22 | 924.19–1,375.79 | 0.003999 | 1,076.16 |
| 814 | `nifty_return_1 > -0.003` | CALL | OTM1 | 24 | stop 20%; target 35%; time | 2,141 | 1,519.20 | 1,080.10–2,026.68 | 0.003999 | 989.97 |
| 936 | `opening_gap_pct < 0.005` | CALL | OTM1 | 48 | stop 20%; target 35%; time | 1,430 | 969.69 | 590.62–1,352.98 | 0.003999 | 603.43 |

## What the rules are testing

- **1008:** an EMA-sign filter, though the threshold `> -1` may be permissive depending on feature encoding.
- **1163, 799, 398, 936:** CALL hypotheses conditioned on a relatively small opening-gap feature, with different hold horizons and exits.
- **1048:** PUT after the gap feature exceeds 0.25%.
- **386 and 705:** CALL after the gap feature exceeds 0.25%, with 2- and 3-bar limits respectively.
- **496:** contrarian PUT after a positive six-period NIFTY return; this tests reversal rather than straightforward momentum.
- **78:** CALL when the opening-range position is above its midpoint.
- **264:** PUT with three simultaneous filters; its direction is not self-evident from the feature names and requires empirical and implementation review.
- **814:** CALL when the one-period return is greater than −0.3%.

The meaning of `opening_gap_pct` (signed versus absolute), `nifty_return_1/6` units, `opening_range_position` construction, and `ema_fast_slow_sign` encoding must be taken from the actual feature builder. Do not infer these definitions from names alone.

## Corrected archive diagnosis

The previous audit incorrectly reported that only 300 candidate definitions were stored. The artifact has 1,185 candidate records and all 20 finalist strategy signatures resolve. The apparent mismatch arose because candidate IDs repeat across islands; the finalist's global candidate ID cannot safely be used as the archive key. Joining on `signature` resolves this correctly. The original E012 claim of missing strategy definitions is therefore **withdrawn**. A remaining quality issue is that candidates 496 and 264 contain duplicated exit kinds; simulator behavior must be verified before treating their exact mechanics as economically meaningful.

## Decision and next gates

1. Fix/validate candidate archive identity and add a regression test that finalist signatures resolve uniquely, rather than assuming candidate IDs are globally unique.
2. Audit the duplicated exit definitions and simulator exit ordering; retain a trace of which exit fires when multiple conditions are met in a bar.
3. Verify feature formulas and availability timestamps against look-ahead leakage.
4. Reconcile dated option contract identity, expiry, lot size, and executable bid/ask/fill assumptions. The execution gate remains false until evidence supports it.
5. Do not tune on the existing OOS block. If the execution-data requirements cannot be met within the bounded plan, close as DATA-LIMITED; no paper/live trading approval.
