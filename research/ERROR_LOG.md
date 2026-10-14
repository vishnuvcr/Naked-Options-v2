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


| OPT-DEV-002 | 2026-10-14 | OPT-BUY-1.0 | HIGH | Initial successful Dhan acquisition queried only four relative-strike series and left only 17.45% of trade dates eligible. Primary paired percentage returns also used a varying premium denominator for trades but zero for no-trade dates. | Fixed numeric strikes can drift to a different rolling offset at exit; the return measure was not a comparable capital/P&L unit across active and inactive dates. | Expand monthly source requests to ATM−3 through ATM+3 for both option types, reuse only verified MONTH/1 cache files, index by exact strike, and make daily one-lot-proxy net rupee P&L the primary paired outcome. Percentage-return statistics remain secondary. | First-pilot inference superseded; corrected rerun pending. |

<!-- OPTION_VALIDATION_ERRORS_START -->
## Option-validation acquisition error log — OPT-BUY-1.0

Stage: ACQUISITION; workflow: https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621480232; commit: 6c4f94e28c2dd88744071e5c7156a2397e55f4c1.

Request failure summaries (individual redacted request windows are preserved in the Actions cache manifest):
- FileNotFoundError: Validated daily NIFTY cache is missing: data/cache/nifty50_daily.csv

Credentials/authorization headers are not logged. See reports/option_validation/acquisition_summary.json for the sanitized status summary.
<!-- OPTION_VALIDATION_ERRORS_END -->
| ERR-DATA | 2026-10-14 | 3 | MEDIUM | nse_official: ValueError: NSE response contains no recognized data rows | Source access/schema/data quality issue | Appended by acquisition workflow; inspect reports/data_manifest.json | OPEN |
| ERR-DATA | 2026-10-14 | 3 | MEDIUM | yahoo:INR=X: ValueError: invalid OHLC range in 237 rows | Source access/schema/data quality issue | Appended by acquisition workflow; inspect reports/data_manifest.json | OPEN |
| ERR-DATA | 2026-10-14 | 3 | MEDIUM | yahoo:GC=F: ValueError: invalid OHLC range in 149 rows | Source access/schema/data quality issue | Appended by acquisition workflow; inspect reports/data_manifest.json | OPEN |
| ERR-DATA | 2026-10-14 | 3 | MEDIUM | yahoo:CL=F: ValueError: non-positive OHLC | Source access/schema/data quality issue | Appended by acquisition workflow; inspect reports/data_manifest.json | OPEN |

| OPT-DEV-003 | 2026-10-14 | OPT-BUY-1.0 CI | MEDIUM | Workflow run #7 failed one response-redaction unit test because the fake JSON response no longer contained the errorCode/errorMessage fields the assertions expected; the same review found a wrong date directive in the legacy ATM cache filename. | A test fixture and a fallback-cache path were edited inconsistently. | Restore the two fake provider error fields and correct the legacy ATM filename to use full YYYYMMDD dates; rerun the complete option-validation test suite. | FIXED IN COMMIT PENDING CI RETEST |

| OPT-DEV-004 | 2026-10-14 | OPT-BUY-1.0 code review | MEDIUM | Strangle selector used nearest available strikes, potentially substituting farther OTM legs for the prespecified one-step OTM structure. | Relative request offset was not retained in quote rows. | Preserve requested offset on ingest; require CALL +1 and PUT −1; skip absent/inconsistent adjacent legs; add unit tests. | Fix committed; cached rerun pending. |

| OPT-DEV-005 | 2026-10-14 | OPT-BUY-1.0 acquisition manifest | LOW | The attempted-window count was derived from planned minus cached; early-stop cases could overstate network requests. | Count derived from intended work rather than resolved request records. | Count request attempts from returned records plus failures minus cached records. | Fix committed; cached rerun pending. |

| OPT-TEST-001 | 2026-10-14 | OPT-BUY-1.0 independent review | HIGH | Frozen acceptance gates remain unmet after the corrected cached run: strangle coverage 69.18% (<80%) and conflicting duplicate group rate 1.409% (>1%). All four candidate average net P&Ls and 95% block intervals are negative at the primary cost setting. | The bounded monthly rolling quote data and model-filtered immediate intraday monetization did not yield sufficient eligible quotes or a profitable result. | Independent reviewer audited the artifact, verified 48,032 ledger rows, reproduced P&L/cost arithmetic to <2e-12 rupees, and reproduced the four paired block-bootstrap comparisons. Do not relax thresholds; close this version as no-go and preserve the data-quality limitation. | CLOSED AS NEGATIVE/INCONCLUSIVE — NO STRATEGY APPROVED |

- OPT-BUY-4.0 catalogue audit run 38636658709 status: failure; inspect Actions logs for failures. Secrets are not recorded.


| OPT-BUY-4.0-001 | 2026-10-14 | OPT-BUY-4.0 | MEDIUM | First catalogue workflow run #38636658709 failed before catalogue generation. | actions/setup-python pip cache was enabled without a requirements.txt or pyproject.toml cache dependency file. | Removed pip cache configuration; subsequent push triggered run #38636831601. Verification is pending. | OPEN pending rerun |
