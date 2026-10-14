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


| ERR-OPT-001 | 2026-10-14 | OPT-BUY-1.0 data acquisition | HIGH | The first Dhan historical rolling-option request (WEEK/expiryCode=0, ATM CALL) returned HTTP 400. | The request configuration or API/data entitlement was rejected; first failed run did not log the provider response body, so the precise cause was initially unknown. | Corrected attempt uses the documented MONTH/expiryCode=1 example and adds secret-redacted provider error text. See [run #6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38543046923). No prices/P&L were produced from the failed request. | IN PROGRESS — resolve from run #6; if still blocked, inspect provider message and try only a documented configuration or another permitted free source. |


| ERR-OPT-002 | 2026-10-14 | OPT-BUY-1.0 acquisition/matching | HIGH | First successful Dhan acquisition queried only four relative-strike series and left 17.45% of trade dates eligible. | A fixed numeric strike can move to another rolling offset by exit. | Expanded requests to ATM−3…ATM+3 for both option types; primary paired metric changed to daily net rupee P&L with zero P&L on no-alert dates. Percentage-return comparisons remain secondary. Run #9 retests. | RETEST RUNNING |
| ERR-OPT-003 | 2026-10-14 | OPT-BUY-1.0 CI | MEDIUM | Run #7 failed one response-redaction unit test because the fake response no longer contained errorCode/errorMessage, and review found a legacy ATM cache filename omitted the year in the second date. | Test fixture and cache fallback path were edited inconsistently. | Restored fake response fields and corrected the legacy ATM filename. Run #9 retests. | FIXED; RETEST RUNNING |

| ERR-OPT-004 | 2026-10-14 | OPT-BUY-1.0 code audit | MEDIUM | The strangle builder chooses the nearest available strike above/below ATM. If the exact adjacent strike quote is missing at entry, it could silently use a farther OTM strike while the plan labels it one-step OTM. | Code does not require adjacent relative offsets or verify the strike interval before accepting the strangle. | After run #9 finishes, add a request-relative-offset field and require entry CALL ATM+1 / PUT ATM−1; if either exact leg is absent, skip the date. Keep exit matching fixed by actual numeric strike. Rerun from cache, then independent tester review. | OPEN — correction required before final inference |

| ERR-OPT-005 | 2026-10-14 | OPT-BUY-1.0 acquisition manifest | LOW | The request manifest currently reports attempted windows as planned minus cached, which can overstate attempts if the loop stops early after auth/schema rejection. | Attempt count is derived from planned work, not completed request records. | Set attempted network windows to max(0, len(request_records) + len(failures) - cached_records); keep planned, cached, success and failure counts separate. Add arithmetic assertions to the independent tester. | OPEN — include in final code correction |

| OPT-TEST-001 | 2026-10-14 | OPT-BUY-1.0 independent review | HIGH | Frozen acceptance gates remain unmet: strangle coverage 69.18% (<80%), conflicting quote groups 1.409% (>1%), and all four candidates have negative mean net P&L and negative 95% intervals. | The bounded monthly rolling quote universe lacks sufficient eligible strangle dates; modeled net outcome is not profitable. | Independent tester reproduced ledger arithmetic and paired comparisons from run #11 artifact; result is closed as no-go. Do not relax thresholds to force a pass. | CLOSED — NO-GO FOR TESTED CANDIDATES; BROADER HYPOTHESIS INCONCLUSIVE |

## OPT-BUY-2.0 errors and corrective actions — 2026-10-14

| ID | Severity | Observation | Correction / disposition |
|---|---|---|---|
| OPT-BUY-2-001 | HIGH | Run #1: 13 existing tests passed, but strike-grid analysis reported no usable quote rows; result artifacts were skipped. [Run](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551789841) | Modified script to emit sanitized blocked summary and empty tables so the acquisition failure remains inspectable. Verify in run #2. |
| OPT-BUY-2-002 | HIGH | Initial grid code did not implement the frozen family-wise Holm adjustment. | Added primary block-bootstrap p-values and Holm correction across 32 candidate/horizon tests in commit `aac22f3b8092160d98a28d3c7445ef0b2d300253`; verify in run #3 and independent review. |
| OPT-BUY-2-003 | OPEN | Quote coverage, data conflict rate and actual acquisition failure cause remain unverified for OPT-BUY-2.0. | Await sanitized run diagnostics; no confirmatory conclusions until gates are checked. |

### OPT-BUY-2.0 root-cause update — 2026-10-14

Run #2 confirmed the actual blocker was upstream of options acquisition: `BLOCKED_NO_VALID_DAILY_DATA`, with `requests_planned=0`. The strike workflow omitted the predecessor workflow's daily-series acquisition/validation step when the cache was absent. Corrected the workflow to acquire the daily NIFTY series with configured repository secrets when needed, validate it, then proceed to options acquisition. Retest: [run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097). Until that run resolves the input-data gate, no option quote coverage or P&L inference is valid.


### OPT-BUY-2.0 live checkpoint — 2026-10-14 17:34 IST

- [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) completed its daily target acquisition/validation and pre-analysis regression step (13 tests passed) but remains in the “Acquire/reuse options cache” step. The step has been active since 10:49:21 UTC; no sanitized artifact is available yet.
- This is recorded as a **long-running step under observation**, not a confirmed API defect: live job metadata does not expose an error or a terminal conclusion. Job timeout is 180 minutes. Do not infer quote availability, strike performance, or profitability before terminal logs/artifacts exist.
- Next check: after the job transitions to completed or failed, retrieve its logs and artifacts, classify any real source/API/cache failure, and update this entry with the evidence.


### OPT-BUY-2.0 live checkpoint — 2026-10-14 — subsequent live poll

- A newer poll of [run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) shows the options-cache step has completed and “Run frozen strike grid” has started. Daily validation and 13 pre-analysis regression tests completed. The options step's workflow-level conclusion is success, but it is configured with `continue-on-error: true`; therefore this status does not verify a `PASS` acquisition manifest or acceptable quote coverage.
- No artifacts are available yet because artifact upload is still pending. This is a status transition, not a confirmed data-quality result or a strike-performance finding. Review sanitized acquisition and grid outputs once the run reaches artifact upload/terminal state.


### OPT-BUY-2.0 — run #4 terminal findings (2026-10-14)

- [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) completed successfully at workflow level. 13 tests passed before and after the grid. Artifact SHA-256: `7fae1922403e398f040ee8ca3a80f607e07e0d6569c98eb35b3ae0c6f168d285`.
- Fresh quote diagnostics: raw 1,055,699; usable 1,023,541; 452 conflicting groups / 31,706 duplicate groups = 1.4256% (>1% gate). Coverage by candidate ranged from 83.27% to 16.94%, with only ATM/ATM >=80%.
- At primary costs, every model-filtered candidate/horizon had negative mean net P&L and a 95% block interval wholly below zero. These outcomes are exploratory because the frozen data-quality gate failed.
- **High-severity inference defect:** all 32 raw and Holm-adjusted p-values in `primary_tests_holm.csv` were blank/NaN although the ledger contained observations. Root cause was not conclusively isolated in the prior run; a self-contained null-centered circular block-bootstrap p-value implementation has been committed as a543eed8059de79dbcc6b2dc53a3dd31f14298a9. Corrective [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress; require finite p-values and test output before closing.
- Common-date sensitivity promised in the frozen plan is absent from the artifact. Log as not completed; no cross-candidate superiority claims.


| ERR-015 | 2026-10-14 | PDF method audit / phase 5–7 | HIGH | Expanded workflow #55 failed while merging empty model-error CSV files. | The report merger assumed every CSV contained a header/rows; empty CSV raised pandas EmptyDataError. | Added EmptyDataError handling in commit `cdf8bab26d9234a6312b1ae00a3f35370574c792`; corrected [run #56](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38585954777) completed successfully. | RESOLVED for workflow; model error CSVs remain empty and should not be interpreted as independent proof of zero model exceptions. |
| ERR-016 | 2026-10-14 | PDF method audit / phase 7 | HIGH | `qlike_skill_vs_baseline` is NaN in merged metrics although QLIKE and baseline QLIKE are finite. | Export/metric derivation is incomplete or incorrectly propagated; exact root cause not yet isolated. | Recorded in [PDF_METHOD_AUDIT_RESULTS.md](PDF_METHOD_AUDIT_RESULTS.md); independent tester must trace the formula, add a unit test, and report whether a bounded correction is required. | OPEN — no QLIKE-skill claim allowed |
| ERR-017 | 2026-10-14 | PDF method audit / phase 5 | MEDIUM | Sequence metadata says `epochs: 8` while the frozen method-audit budget was documented as three epochs. | Metadata and/or actual training configuration do not agree with the preregistered compute limit. | Compare run config, sequence model implementation and actual fit calls; update protocol only if justified and transparently recorded. | OPEN — independent review required |
| ERR-018 | 2026-10-14 | PDF method audit / phase 3 | MEDIUM | USD/INR, gold and WTI external series failed OHLC validation; NSE endpoint returned no recognized rows. | Source format/schema/value conventions differ from the validator's expected positive OHLC format, or endpoint response schema changed. | Kept failed sources excluded rather than imputing/forcing data. Investigate a separate validated free source only if needed; no model inference relies on these rejected rows. | OPEN AS DATA LIMITATION |


| ERR-015 | 2026-10-14 | PDF method audit / phase 5 | MEDIUM | Expanded workflow #55 failed while merging empty model-error CSV files. | Report merger assumed every CSV contained a header/rows; empty CSV raised pandas EmptyDataError. | Added EmptyDataError handling in commit `cdf8bab26d9234a6312b1ae00a3f35370574c792`; corrected [run #56](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38585954777) completed successfully. | RESOLVED for workflow; empty error CSVs are not independent proof of zero model exceptions. |
| ERR-016 | 2026-10-14 | PDF method audit / phase 7 | HIGH | `qlike_skill_vs_baseline` is NaN in merged metrics although QLIKE and baseline QLIKE are finite. | Export/metric derivation is incomplete or incorrectly propagated; root cause not isolated. | Recorded in [PDF_METHOD_AUDIT_RESULTS.md](PDF_METHOD_AUDIT_RESULTS.md); tester must trace formula, add a unit test, and decide if a bounded correction is required. | OPEN — no QLIKE-skill claim allowed |
| ERR-017 | 2026-10-14 | PDF method audit / phase 5 | MEDIUM | Sequence metadata says `epochs: 8` while the frozen method-audit budget was documented as three epochs. | Metadata and/or actual training configuration conflict with the documented compute limit. | Compare run config, implementation and actual fit calls; disclose any protocol change. | OPEN — independent review required |
| ERR-018 | 2026-10-14 | PDF method audit / phase 3 | MEDIUM | USD/INR, gold and WTI external series failed OHLC validation; NSE endpoint returned no recognized rows. | Source format/schema/value conventions differ from expected positive OHLC format, or endpoint schema changed. | Kept failed sources excluded rather than forcing/imputing data. Revisit validated free alternatives only if needed; no inference relies on rejected rows. | OPEN AS DATA LIMITATION |


| ERR-019 | 2026-10-14 | PDF audit / phase 7 | HIGH | QLIKE skill ratio was defined as `1 - model_mean / baseline_mean` but QLIKE means were negative, making the ratio uninterpretable and triggering null values. | A score ratio is not appropriate for an unshifted QLIKE scoring rule that may be negative. | Added `qlike_improvement_vs_baseline = mean(baseline_score - model_score)` in `scripts/forecast_metrics.py`, wired it into the experiment runner, and added sign/negative-score/empty-overlap unit tests. See [developer submission](PDF_METHOD_AUDIT_DEVELOPER_SUBMISSION.md). | FIX COMMITTED; bounded workflow/tester verification pending |
| ERR-020 | 2026-10-14 | PDF audit / phase 5 | LOW | Sequence run metadata reported eight epochs although each sequence estimator is configured and fit for three epochs. | Status JSON contained a hard-coded value inconsistent with the actual estimator configuration. | Changed metadata to three; included in the same bounded retest. | FIX COMMITTED; workflow/tester verification pending |


## Run #60 additional risks

- **ERR-021 — HIGH, open for independent audit:** The paired-loss test is two-sided for `mean(model loss - baseline loss)=0`; a small p-value alone does not establish improvement. Negative mean loss difference favors the model; positive favors baseline. Tester must reproduce signs and p-values from predictions.
- **ERR-022 — MEDIUM, documented:** Classification accuracy and minimum regression error do not define a universal winner across objectives. Class prevalence, thresholding and calibration affect classification metrics. Tester should check balanced accuracy, Brier/log loss and benchmark skill alongside accuracy.
- **ERR-023 — MEDIUM, data limitation:** Twenty weekend-dated observations and global-market timestamp alignment remain unresolved risks. Preserve the source rows with warnings; do not infer verified point-in-time availability from daily data alone.


## Tester finding T-01 and correction

- **ERR-024 — HIGH:** Some `target_future_vol_5` and `target_future_vol_20` labels were computed from partial future-return windows near the end of the series. Those rows could have valid numeric labels but null `target_date_h`, violating full-horizon target integrity.
- **Correction committed:** `scripts/build_feature_matrix.py` now emits h-session volatility only when all h future returns are present. `tests/test_research.py` asserts non-null labels have future target dates and partial future windows are not labelled. Corrected workflow retest is pending; do not claim the issue resolved until its artifact has zero null target dates among evaluated rows.
