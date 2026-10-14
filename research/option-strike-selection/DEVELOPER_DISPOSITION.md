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
