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



## Developer correction log — 2026-10-14

| Ref | Issue found | Correction | Result handling |
|---|---|---|---|
| OPT-DEV-001 | Initial implementation retained NIFTY lot size 75 after 2024-11 and did not account for the NSE 2025 revision from 75 to 65 for newly revised-expiry contracts. This was detected during pre-results source review, before any result was accepted. | Lot-size proxy now uses 50 before 2024-04-26, 25 from 2024-04-26 through 2024-11-19, 75 through the 2025-12-30 expiry-transition date, and 65 from 2025-12-31 as a trade-date approximation. NSE circular 176/2025 specifies the 75-to-65 change and expiry-specific effective dates: https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf | Outputs from the initial uncorrected run are not accepted as final results. The corrected branch commit triggers a fresh run; currency P&L remains a proxy and premium-point results are primary. |

<!-- OPTION_VALIDATION_ERRORS_START -->
## Option-validation acquisition error log — OPT-BUY-1.0

Stage: BLOCKED; workflow: https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38542754673; commit: 8a3d9a3c7f47628501c60229c5802653a637b1e5.

Request failure summaries (individual redacted request windows are preserved in the Actions cache manifest):
- RequestOrSchemaFailure:REQUEST_SCHEMA_HTTP_400: 1

Credentials/authorization headers are not logged. See reports/option_validation/acquisition_summary.json for the sanitized status summary.
<!-- OPTION_VALIDATION_ERRORS_END -->
| ERR-DATA | 2026-10-14 | 3 | MEDIUM | nse_official: ValueError: NSE response contains no recognized data rows | Source access/schema/data quality issue | Appended by acquisition workflow; inspect reports/data_manifest.json | OPEN |
| ERR-DATA | 2026-10-14 | 3 | MEDIUM | yahoo:INR=X: ValueError: invalid OHLC range in 237 rows | Source access/schema/data quality issue | Appended by acquisition workflow; inspect reports/data_manifest.json | OPEN |
| ERR-DATA | 2026-10-14 | 3 | MEDIUM | yahoo:GC=F: ValueError: invalid OHLC range in 149 rows | Source access/schema/data quality issue | Appended by acquisition workflow; inspect reports/data_manifest.json | OPEN |
| ERR-DATA | 2026-10-14 | 3 | MEDIUM | yahoo:CL=F: ValueError: non-positive OHLC | Source access/schema/data quality issue | Appended by acquisition workflow; inspect reports/data_manifest.json | OPEN |
