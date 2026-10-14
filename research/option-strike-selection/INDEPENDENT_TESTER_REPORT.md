# Independent tester report — OPT-BUY-2.0 strike selection

**Status:** FAIL / BLOCKED — no confirmatory candidate review possible  
**Reviewed commit:** `aac22f3b8092160d98a28d3c7445ef0b2d300253`  
**Run evidence:** [Run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551789841); [run #2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551939491)  
**Scope:** independent code/protocol review; no raw quote dataset was available to independently reproduce P&L.

## Findings
1. **Data blocker reproduced operationally:** run #1's 13 existing regression tests passed, acquisition step exited, but the strike-grid step reported `BLOCKED: no usable option quote rows`. Therefore no candidate metrics or profitability conclusion may be inferred from that run.
2. **Initial inference implementation gap:** the first strike-grid implementation emitted confidence intervals but did not implement the prespecified family-wise multiple-testing adjustment. Developer added a block-bootstrap test and Holm correction in commit `aac22f3b8092160d98a28d3c7445ef0b2d300253`; that correction still needs to pass a run and independent numeric checks on usable data.
3. **Coverage gate:** predecessor study had 69.18% strangle coverage and 1.409% conflicting duplicate groups, both outside the frozen gates. OPT-BUY-2.0 must report fresh diagnostics; predecessor values cannot be substituted as current measurements.
4. **Execution-data limitation:** rolling relative-offset quotes are not stable expiry-specific historical contracts and do not provide bid/ask. Results, if computable, remain a proxy, not an executable historical options backtest.
5. **No strategy approval:** minimum 80% per-candidate coverage, conflict rate <=1%, at least 100 alert trades, positive after-cost mean with 95% block interval above zero, 100-bps robustness, both-half consistency, and corrected inference must all be demonstrated. No gate may be waived.

## Required developer actions
- Run #2 confirmed the daily target cache was missing/unusable; developer added a cache-aware daily acquisition and validation step to the workflow. Verify in run #4. [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552069292) is the Pages run; strike workflow follow-up run is triggered by the workflow change.
- If no usable quotes remain, classify the phase as data-blocked and stop rather than fabricate candidate results or repeatedly redownload without a diagnosed cause.
- If usable quotes exist, independently check candidate strike/offset mapping, exact numeric-strike exit matching, fee arithmetic, bootstrap output, and Holm adjustment against a separate implementation.
- Add the required common-date sensitivity or clearly record it as not implemented and do not claim cross-candidate apples-to-apples superiority.
- Update README, phase status, experiment log, error log, interaction log and manuscript/disposition after the terminal evidence.

## Tester disposition
**FAIL / BLOCKED.** This is not a claim that all strikes are unprofitable. It means the evidence is currently insufficient to identify any reliable strike-selection edge. Developer must not progress to prospective paper testing.
