# Error and defect log

Append every observed error, unsuccessful source, unexpected value, failed test, and correction attempt. Never remove historical failures. Keep secrets out of logs.

| ID | First observed | Phase | Severity | Error / defect | Root cause | Correction and verification | Status |
|---|---|---|---|---|---|---|---|
| ERR-001 | 2026-10-14 | 1 | MEDIUM | Target repository had no README, files, commits, or branches. | Repository had not been initialized. | Created a first README commit and started new NIFTY-PRED-1.0 files without overwriting any historical work. GitHub metadata and branch search verified the initial empty state; README creation returned commit SHA e0b634fdb98da9a2ed136320a24afb7fdda8afb9. | RESOLVED |
| ERR-002 | 2026-10-14 | 1 | LOW | Project-library manuscripts refer to other research repositories and tracks. | Project Library aggregates prior work, not necessarily content from this GitHub repository. | Treat them as literature/context and not as fresh experiment results. This distinction is recorded in README and literature review. | RESOLVED |
| ERR-003 | pending | 3+ | — | No data access failure recorded yet. | Acquisition workflow has not been run/verified. | Append actual source failures after workflow execution; do not invent failures. | NOT OBSERVED |

## Handling policy

HTTP 200 returning HTML instead of the required payload is a source failure. Empty response, missing token, invalid instrument ID, schema drift, duplicate dates, invalid OHLC, target NaNs, model runtime, NaN metrics, statistical-test issues and workflow errors are separate classes. Record source ID, redacted request metadata, status/content type, traceback summary, commit and retest outcome. Never log API tokens, authorization headers or secrets.

| ERR-004 | 2026-10-14 | 3 | MEDIUM | Initial validation rejected 20 weekend-dated bars as automatically invalid. | Validator assumed no weekend exchange sessions. | Preserved rows and report exact weekend dates as a warning; subsequent workflow passed. | Runs 30/31 passed validation and feature construction. | RESOLVED |
| ERR-005 | 2026-10-14 | 5 | MEDIUM | Full run stayed in the model-selection step beyond the intended compute budget. | Four folds across a large target/horizon/model grid plus deep models increased fit count. | Restrict sequence models to next-session return/direction, three epochs; use two expanding chronological folds for all candidate model selection. | Run #34 pending completion. | IN PROGRESS |
| ERR-006 | 2026-10-14 | 5/7 | HIGH | OOS R-squared used the realized holdout sample mean rather than an available benchmark. | The denominator used sum of squared deviations about test-target mean. | Formula now uses benchmark-relative OOS R-squared, 1 - candidate MSE / benchmark MSE, with a dedicated unit test. | Formula commit 470d7444a95af0fe3c3fbdc319bbe55ee874de14; unit test added in commit 09a92967d9a6634a96b8bfccab14ce2b3e9066c5. Run #34 must pass before closure. | OPEN |

| ERR-007 | 2026-10-14 | 5 | MEDIUM | The run with two folds but full catalogue over all tasks/horizons still did not emit result artifacts and remained in the model step. | Total model-fit count and expensive boosted/MLP/sequence fits exceeded the useful hosted-run budget. | Added a dated, explicit compute-budget amendment: full catalogue for next-session return/direction, core regression/classification set for all other targets/horizons, smaller fixed estimators, and a row for each excluded candidate. | Run #40+ must complete and its budget statuses/tests be verified. | IN PROGRESS |
