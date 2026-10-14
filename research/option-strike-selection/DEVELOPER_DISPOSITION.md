# Developer disposition — OPT-BUY-2.0

**Current status:** BLOCKED pending daily-data acquisition retry  
**Branch:** `research/option-strike-selection-developer`  
**Current study workflow:** [GitHub Actions](https://github.com/vishnuvcr/Naked-Options-v2/actions/workflows/option-strike-selection.yml)

## What happened
- Run #1 failed in the grid stage because no usable option quote rows were loaded, despite 13/13 existing unit tests passing.
- Run #2 successfully preserved diagnostic artifacts. Its summary shows `acquisition_status=BLOCKED_NO_VALID_DAILY_DATA`, `requests_planned=0`, zero usable rows. Therefore this was not yet an options-API or strike-coverage result: the underlying daily NIFTY input needed by the frozen classifier was missing/unusable.
- A workflow defect was identified: unlike the predecessor workflow, OPT-BUY-2.0 did not first acquire/validate the daily target if the cache was absent. The developer added cache-aware daily acquisition and validation using the repository's existing acquisition scripts, including `DHAN_ACCESS_TOKEN` and `HF_TOKEN` secrets.
- A second code defect was identified: the initial grid lacked the frozen family-wise inference adjustment. Prespecified block-bootstrap p-values and Holm correction across 32 candidate/horizon tests were added. This remains unverified until a run has sufficient usable observations.

## Gates
No strike outcomes exist yet. Do not infer profit or loss, do not name a winner, and do not approve paper/live deployment. The phase may continue only through the bounded workflow retry with actual sanitized diagnostics. If daily data cannot be acquired/validated, record the error and stop as data-blocked.

## Next developer action
Wait for the run triggered by the daily-data workflow correction. If acquisition succeeds, evaluate the 16 fixed call/put offset pairs and two fixed horizons, then update the manuscript and results. If blocked, preserve error evidence and stop. Independent tester must review before any progression.


## Run #4 final evidence and disposition — 2026-10-14

- [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) completed successfully; 13 tests passed before and after the grid. Sanitized artifact SHA-256: `7fae1922403e398f040ee8ca3a80f607e07e0d6569c98eb35b3ae0c6f168d285`.
- Quote data: 1,055,699 raw rows, 1,023,541 usable rows, 452 conflicting groups / 31,706 duplicate groups = 1.4256%, which fails the frozen 1% conflict gate. Coverage over 980 test dates ranged from 83.27% to 16.94%, with only ATM/ATM meeting 80%.
- All 32 model-filtered candidate × horizon mean net P&Ls at primary costs (50 bps/side, ₹10/order) were negative and their 95% block-bootstrap upper bounds were below zero. These results are exploratory because data gates failed; no strike candidate is approved.
- The artifact had NaN p-values for the full 32-test primary family. The developer corrected p-value calculation in commit `a543eed8059de79dbcc6b2dc53a3dd31f14298a9`; [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress. Do not start another grid or parameter loop. If this one correction still fails, record the statistical defect and close OPT-BUY-2.0 as NO-GO / non-confirmatory rather than retrying indefinitely.
- The planned common-date sensitivity was not generated. No cross-candidate superiority claim is allowed.
- User explicitly waived separate tester review. Scientific gates remain unchanged.

## Developer decision

**NO-GO — no strategy approved.** The historical quote universe fails frozen data-quality and coverage requirements, and primary after-cost outcomes are negative. The one in-flight p-value correction is for statistical completeness only; it cannot reverse the no-go decision unless the fixed data gates pass, which they do not in run #4.
