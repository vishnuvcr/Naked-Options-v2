# Error and defect log

Append every observed error, unsuccessful source, unexpected value, failed test, and correction attempt. Never remove historical failures. Keep secrets out of logs.

| ID | First observed | Phase | Severity | Error / defect | Root cause | Correction and verification | Status |
|---|---|---|---|---|---|---|---|
| ERR-001 | 2026-10-14 | 1 | MEDIUM | Target repository had no README, files, commits, or branches. | Repository had not been initialized. | Created a first README commit and started new NIFTY-PRED-1.0 files without overwriting any historical work. GitHub metadata and branch search verified the initial empty state; README creation returned commit SHA e0b634fdb98da9a2ed136320a24afb7fdda8afb9. | RESOLVED |
| ERR-002 | 2026-10-14 | 1 | LOW | Project-library manuscripts refer to other research repositories and tracks. | Project Library aggregates prior work, not necessarily content from this GitHub repository. | Treat them as literature/context and not as fresh experiment results. This distinction is recorded in README and literature review. | RESOLVED |
| ERR-003 | pending | 3+ | — | No data access failure recorded yet. | Acquisition workflow has not been run/verified. | Append actual source failures after workflow execution; do not invent failures. | NOT OBSERVED |

## Handling policy

HTTP 200 returning HTML instead of the required payload is a source failure. Empty response, missing token, invalid instrument ID, schema drift, duplicate dates, invalid OHLC, target NaNs, model runtime, NaN metrics, statistical-test issues and workflow errors are separate classes. Record source ID, redacted request metadata, status/content type, traceback summary, commit and retest outcome. Never log API tokens, authorization headers or secrets.

| ERR-004 | 2026-10-14 | 3 | MEDIUM | Validator rejected 20 weekend-dated NIFTY observations, even though weekend dates can represent exchange special sessions. | Weekends were treated as invalid by default instead of being reported as a source/calendar warning. | Changed validation to preserve these rows, list exact dates and show a warning; later workflow run passed the data gate and feature matrix. SHA and source manifest are checked. | Verified by run 30/31 step summaries. | RESOLVED |
| ERR-005 | 2026-10-14 | 5 | MEDIUM | First full model catalogue remained computationally heavy and was superseded before producing interpretable results. | Sequence models were initially evaluated across all targets/horizons with more folds/epochs than suitable for the hosted runner budget. | Bound sequence models to next-session return and direction, use 3 epochs and 2 chronological folds; explicitly mark excluded sequence target/horizon cells BLOCKED_COMPUTE_BUDGET. | Phase-5 branch contains the restriction; current rerun outcome pending. | IN PROGRESS |
| ERR-006 | 2026-10-14 | 5/7 | HIGH | Regression helper labelled skill relative to the realized holdout sample mean as out-of-sample R-squared, which is not an available ex-ante forecast benchmark. | The formula uses test-target mean in the denominator for the reported R². | Changed the field to benchmark-relative R² = 1 - model MSE / benchmark MSE on the phase-5 branch, matching the existing benchmark-relative skill calculation. | Correction commit 470d7444a95af0fe3c3fbdc319bbe55ee874de14; awaiting unit test and completed rerun. | OPEN |

| ERR-013 | 2026-10-14 | 5/7 | MEDIUM | Research status documentation was stale after corrected run #49 completed. | Prior checkpoint wording had not been replaced with final workflow evidence. | Updated main README, RESULTS.md and PHASE_STATUS.md with corrected run #49 evidence; tester report updated on independent-tester branch. | Run #49 succeeded; artifact SHA-256 97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7. | DOCUMENTATION UPDATED; PHASE 7 REVIEW OPEN |

| ERR-014 | 2026-10-14 | 8/9 | LOW | Manuscript placeholders remained after corrected results. | Manuscript had not been updated with run #49. | Updated manuscript and added selected-results figure; tester report passes with scope limitations. | Run #49 artifact and manuscript reviewed. | RESOLVED |
