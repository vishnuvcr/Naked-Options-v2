# Error and defect log

Append every observed error, unsuccessful source, unexpected value, failed test, and correction attempt. Never remove historical failures. Keep secrets out of logs.

| ID | First observed | Phase | Severity | Error / defect | Root cause | Correction and verification | Status |
|---|---|---|---|---|---|---|---|
| ERR-001 | 2026-10-14 | 1 | MEDIUM | Target repository had no README, files, commits, or branches. | Repository had not been initialized. | Created a first README commit and started new NIFTY-PRED-1.0 files without overwriting any historical work. GitHub metadata and branch search verified the initial empty state; README creation returned commit SHA e0b634fdb98da9a2ed136320a24afb7fdda8afb9. | RESOLVED |
| ERR-002 | 2026-10-14 | 1 | LOW | Project-library manuscripts refer to other research repositories and tracks. | Project Library aggregates prior work, not necessarily content from this GitHub repository. | Treat them as literature/context and not as fresh experiment results. This distinction is recorded in README and literature review. | RESOLVED |
| ERR-003 | pending | 3+ | — | No data access failure recorded yet. | Acquisition workflow has not been run/verified. | Append actual source failures after workflow execution; do not invent failures. | NOT OBSERVED |

## Handling policy

| ERR-021 | 2026-10-15 | VOL-REGIME-OPT Phase 2 | MEDIUM | Dhan weekly rolling-option requests using `expiryCode=0` returned HTTP 400 (`DH-905: expiryCode is required`). | Initial weekly probe used a value rejected by endpoint; monthly control was not evidence of weekly availability. | Added bounded candidate-code probe; persisted audit shows WEEK codes 1 and 2 structurally valid for CALL/PUT in the five-day probe. Exact expiry mapping and contract identity remain unverified. | OPEN — partial source resolution |


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


## OPT-BUY-3.0 initial implementation audit — 2026-10-15

- HIGH until verified: the executable currently covers only fixed-time CALL/PUT entries and fixed-duration/EOD exits, not the full frozen random/rule-based catalogue. Treat as partial, not a completed strategy search.
- Cost audit required: inherited cost helper charges brokerage per executed order. Any straddle implementation must charge four orders per round trip; the initial screen does not yet include straddle candidates.
- Sensitivity audit required: 100-bps results must recompute slippage consistently with full cost arithmetic; do not rely on an unverified generic add-on.
- No workflow result was observed at this checkpoint. No strategy or profitability conclusion is claimed. Preserve this log item until tester review or a documented correction resolves it.


| ERR-OPT3-001 | 2026-10-15 | OPT-BUY-3.0 implementation | HIGH | Committed implementation is a partial screen, not the full registered entry × exit catalogue. | Initial coding covered fixed-time CALL/PUT entries and fixed holds/EOD only. | Explicitly recorded as incomplete in README and phase status; must implement the frozen catalogue or report a justified bounded limitation before interpreting results. | OPEN |
| ERR-OPT3-002 | 2026-10-15 | OPT-BUY-3.0 data/results | HIGH | Latest committed result reports BLOCKED_NO_VALID_QUOTES; no empirical strategy inference is available. | The runner did not find a valid option manifest/quotes in the execution environment or the cache could not be reused. | Preserve blocked status; workflow must record acquisition and schema errors without exposing secrets. Recheck on actual workflow output. | OPEN |
| ERR-OPT3-003 | 2026-10-15 | OPT-BUY-3.0 statistics | HIGH | Current code does not yet satisfy the full protocol: no 100-bps rerun, missing-trade sessions are not zero-filled, and duration exits may silently truncate to last bar. | Partial implementation does not yet encode all preregistered checks. | Must fix before confirmatory interpretation; include regression tests and retain exploratory-only status until verified. | OPEN |
| ERR-OPT3-004 | 2026-10-15 | Process governance | LOW | Previous protocol required an independent tester and separate tester branch contrary to user's latest preference. | Protocol had not been amended after user instruction. | Updated OPT-BUY-3.0 protocol to single-process automated validation; do not create a tester branch/report gate. | RESOLVED |


| ERR-OPT3-005 | 2026-10-15 | OPT-BUY-3.0 cache | HIGH | Completed Actions run #3 reported BLOCKED_NO_VALID_QUOTES despite acquisition step exit success. | Acquisition step skipped because an existing manifest was present; workflow trusted existence rather than usable status/files. | Workflow now checks manifest status and cached files, retries with --refresh-options when stale/blocked, and reports usable file count. Commit `03ee91ba312977499544733dc1177b10f04d6feb`; verify run #4/#5. | IN PROGRESS |
| ERR-OPT3-006 | 2026-10-15 | OPT-BUY-3.0 execution | HIGH | Existing trade runner passed a single-leg trade to a legacy helper that only accepts two-leg structures; this had been masked by zero valid quote rows. | Helper interface mismatch; no trade ever reached the code path in run #3. | Added explicit single-leg cost calculation and fee/slippage/brokerage tests, plus a finite expanded entry/exit catalogue. Commit `fc487511aa7aa82d33c71dc4fdeca2870be153cb`; tests and data run pending. | IN PROGRESS |


| ERR-OPT3-007 | 2026-10-15 | OPT-BUY-3.0 data acquisition | HIGH | Run #6 still produced no option rows after the stale-manifest retry fix. | Acquisition manifest was BLOCKED_NO_VALID_DAILY_DATA because the ephemeral runner had no validated daily target cache; option acquisition consequently planned zero requests. | Added an explicit pre-step to acquire daily NIFTY data from Dhan, NSE official data, and Yahoo fallback when cache is absent, then require the daily CSV before option acquisition. Commit `0d9eb96d36316bf009f88e828d37812b2cd286cd`; verify run #7. | IN PROGRESS |


| ERR-018 | 2026-10-15 | 8/9 | HIGH | Main README/result narrative claims the expanded prediction study passed independent review after run #62, but the currently accessible tester report still describes run #60 and says FAIL FOR FINAL SCIENTIFIC SIGN-OFF. | Tester report was not visibly reconciled to the newer workflow/result checkpoint in the inspected branch/path. | Created research/FRESH_PREDICTION_CONTINUATION_AUDIT.md on main and research/fresh-prediction-audit. Require an independent run #62 artifact review and manuscript reconciliation before treating sign-off as current. | OPEN |


| ERR-019 | 2026-10-15 | 7/9 | MEDIUM | Run #62 exports extreme QLIKE values for some volatility models (e.g. elastic-net h=5 around 1.31e9) and 34 zero actual volatility labels. | QLIKE penalizes near-floor volatility forecasts paired with non-negligible realized volatility; floor handling is implemented in forecast_metrics.py. | Independently recomputed all 102 QLIKE rows from raw predictions; maximum model-score/improvement discrepancy 3.06e-5, baseline-score discrepancy 2.14e-14. Confirmed extreme values are expected large penalties under the documented formula, not a demonstrated arithmetic defect. Keep edge-case/floor explanation in report. | RESOLVED AS EXPECTED PENALTY; interpretation limitation retained |


| ERR-020 | 2026-10-15 | 8/9 | LOW | Tester sign-off was initially stale at run #60 despite the newer run #62 result artifact. | The tester report path had not been updated after the expanded run. | Tester independently inspected run #62, reproduced target offsets, 485 metric rows, HAC/block-bootstrap outputs, Holm adjustment, and 102 QLIKE rows; updated [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md). | RESOLVED — PASS WITH SCOPE LIMITATIONS |


| ERR-021 | 2026-10-15 | VOL-REGIME-OPT-1.0 phase 2 | HIGH | Weekly-strategy hypothesis requires historical weekly expiry contracts, but prior option studies used monthly rolling data and same-session exits. | Reusing monthly rolling rows or a changing ATM-relative series as if it were a stable weekly contract would misstate performance and could introduce look-ahead/contract-identity errors. | Added a separate frozen protocol and Dhan WEEK-vs-MONTH schema probe. Require exact expiry/strike mapping and historical expiry calendar; if not available, stop without strategy P&L. | OPEN — source gate pending |


| ERR-022 | 2026-10-15 | VOL-REGIME-OPT-1.0 phase 2 | MEDIUM | First Dhan WEEK / expiryCode=0 requests returned HTTP 400: DH-905 “expiryCode is required”; MONTH / expiryCode=1 control returned valid 375-row call and put series. | The endpoint may have a provider-side validation issue for enum value 0, or the weekly parameter combination may differ from the docs. Monthly success does not prove weekly support. | Added one bounded diagnostic probe for WEEK codes 0, 1 and 2 with monthly control. No weekly P&L will be calculated unless a code passes and actual expiry mapping is verified. | OPEN — corrective source probe running |

| ERR-022 | 2026-10-15 | VOL-REGIME-OPT Phase 2b | HIGH | Exact expiry date and fixed-contract identity are not established by the persisted rolling-option probe. | Response schema has rolling strike-relative bars and no explicit expiry-date field; code-3 result and HF fallback audit are not persisted/verified. | Added [source-gate disposition](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/SOURCE_GATE_DISPOSITION.md); stopped before P&L. Tester has one bounded check to verify expiry-code semantics, official expiry calendar/contract master, fresh code-3 audit and HF fallback status. | OPEN — blocks empirical P&L and strategy conclusion |


| ERR-023 | 2026-10-15 | VOL-REGIME-OPT Phase 2 source audit | HIGH | Workflow run #10 completed Dhan weekly schema requests but was marked failed after the runner received a shutdown signal during the Hugging Face fallback probe; cache-save, audit-commit and artifact steps were skipped. | External runner shutdown/cancellation; not a market-data result. | Recovered the Dhan request evidence from the workflow log and persisted a sanitized audit on the developer branch. HF fallback remains NOT VERIFIED; no P&L ran. See [run #10](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667). | Dhan schema evidence recovered; HF fallback unresolved; study BLOCKED at contract identity |

| ERR-VOL-022 | 2026-10-16 | VOL-REGIME-OPT C1 | HIGH | Available short-window Dhan weekly probes show structurally valid CALL/PUT arrays for candidate codes but do not prove actual expiry dates or exact-contract continuity; the HF fallback run was interrupted. | Schema-level probe and workflow interruption are insufficient to establish a tradable historical contract series. | Created bounded continuation plan on `research/vol-regime-options-continuation`; next action is to verify expiry mapping and exact-strike/expiry continuity using documented Dhan metadata and free official/public sources. No P&L may be calculated until verified. | OPEN — BLOCKING SOURCE GATE |


| ERR-VOL-023 | 2026-10-16 | VOL-REGIME-OPT C1 | MEDIUM | Previous source-gate run ended with runner shutdown while probing the Hugging Face fallback; cache save and artifact publication were skipped. | Runner interruption prevented the fallback audit from completing. | Re-ran failed GitHub Actions job for [run #38676451667](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667), attempt 2. Verify completed logs/artifacts before treating the fallback as evidence. | OPEN — RETRY IN PROGRESS |


| ERR-VOL-024 | 2026-10-16 | VOL-REGIME-OPT C1 | MEDIUM | Earlier Dhan rolling-option response did not establish historical expiry-code mapping or fixed-contract continuity, while the HF fallback was interrupted. | The Dhan endpoint is rolling-relative strike data and the prior workflow did not finish its HF probe. | Located the already-used `thetrademarkk/india-index-options-1m` source in `vishnuvcr/Nifty`; added a cached exact-expiry/strike/type audit workflow on the continuation branch. Verify run #38807375042 and reconcile against official NSE evidence before P&L. | OPEN — WORKFLOW RUNNING / AUDIT PENDING |


| ERR-RESEARCH-025 | 2026-10-22 | NIFTY prediction pipeline | MEDIUM | Workflow [39676907630](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39676907630) failed at result merging because a model output CSV existed but was empty/headerless; pandas raised `EmptyDataError`. | A blocked/not-run model can legitimately produce no rows, but the merger treated the empty file as malformed fatal input. | Added `read_csv_if_populated` to skip missing, empty, and headerless outputs while recording skipped paths in `feature_ablation.json`; regression test added. | REGRESSION TEST PASSED IN RUN 39699761966; END-TO-END MERGE VERIFICATION PENDING |


| ERR-RESEARCH-026 | 2026-10-22 | Phase 5 reporting | LOW | Technical-run metadata reported 8 sequence epochs although the estimator objects were explicitly set to 3 epochs before fitting. | The sequence-status metadata field retained the estimator default rather than the effective compute budget. | Corrected metadata to 3 and added a regression assertion; model weights/metrics from run 39699761966 used 3 epochs, so this is a reporting-only correction and does not require retraining. | RESOLVED — metadata-only fix committed with CI skipped to avoid an unnecessary full refit |
| ERR-RESEARCH-027 | 2026-10-22 | Phase 3 data acquisition | MEDIUM | In run [39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966), NSE official endpoint returned no recognized rows; USD/INR had 237 invalid OHLC rows; gold had 149 invalid OHLC rows; WTI contained non-positive OHLC. | Source response/schema/data quality did not satisfy the strict OHLC validator; exact provider-side cause is not established. | Failures remain in the run manifest; those sources were excluded from the feature matrix. Do not silently repair or synthesize them. Seven other external series passed validation. | SOURCE LIMITATION DOCUMENTED; RETRY ONLY WITH A NEW VALIDATED METHOD |
