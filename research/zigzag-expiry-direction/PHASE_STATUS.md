# Phase Status — ZigZag Expiry Direction

Updated: 2026-10-25

| Phase | Status | Evidence / blocker |
|---|---|---|
| 1. Protocol/source audit | PARTIALLY COMPLETE — BLOCKED | TradingView ZigLib page states the function returns direction and two chart points (library page dated Oct 9, 2023); TradingView's generic Zigzag documentation explicitly warns that confirmed labels are drawn into the past and the latest solid line is not final. A public GitHub mirror of the wrapper script confirms `repaint=true` is the default and that the non-repaint branch only draws on direction changes using prior-bar point values; however, it does not contain the imported ZigLib implementation and is not an authoritative source. Exact ZigLib v1 source semantics and signal-availability time remain unverified. NSE official contract page confirms current Tuesday expiry with previous-session holiday shift, but historical circular mapping remains incomplete. |
| 2. Data audit | BLOCKED | Official free source leads and acceptance criteria documented; no export has been acquired/validated, and intraday 10:00 data is required. | NSE/Nifty Indices public historical index-data portals are confirmed as free source leads; the actual export is not yet cached or validated in this branch. Existing NWCP data still has unresolved source overlap, timestamp/provenance and expiry-calendar issues and is not automatically admissible. |
| 3. Causal reconstruction | BLOCKED | Cannot safely substitute a generic ZigZag or guessed port for the exact imported library. |
| 4. Evaluation | NOT STARTED | No eligible ZigZag predictions scored. |
| 5. Robustness/inference | NOT STARTED | Depends on valid out-of-sample results. |
| 6. Manuscript/decision | PROTOCOL DRAFTED | Manuscript skeleton exists; results, figures, tables and conclusions cannot be populated without validated empirical output. |

## Evidence reviewed
- TradingView ZigLib library page: https://www.tradingview.com/script/NC3cgEcT-ZigLib/ — describes `zigzag(_low, _high, depth, deviation, backstep)` and its returned direction and two chart points, but the accessible page summary does not expose enough implementation detail to validate historical availability.
- TradingView ZigZag++ page: https://www.tradingview.com/script/lj8djt1n-ZigZag/ — release notes mention advanced repainting control; that does not prove this exact pasted script/library combination is non-repainting.
- TradingView general ZigZag explanation: https://www.tradingview.com/support/solutions/43000591664-zigzag-indicator/ — explains confirmation lag and that the latest displayed line may be revised. This is general background, not a substitute for ZigLib v1 source.

**Current decision:** DATA-LIMITED / NO PERFORMANCE CLAIM. This run did not produce an empirical accuracy estimate. No tester gate was added because the user explicitly waived independent tester review for this experiment.


## Timeframe sensitivity update — 2026-10-25
Phase 1 protocol amendment: user requested “Test various timeframes.” Added TIMEFRAME_SENSITIVITY.md with a predeclared 5m, 15m, 30m, 60m and 1-day panel; 1m is conditional on validated data completeness. This resolves the protocol ambiguity by testing variants rather than silently picking one. It does not resolve source parity or data blockers.

| Phase | Updated status | Evidence / blocker |
|---|---|---|
| 1. Protocol/source audit | TIMEFRAME PANEL PRE-REGISTERED; SOURCE BLOCKED | Multi-timeframe variants documented; exact ZigLib v1 causality remains unverified. |
| 2. Data audit | BLOCKED | Validated intraday spot data and date-specific expiry schedule still not acquired. |
| 3. Causal reconstruction | BLOCKED | Must verify exact imported-library semantics for each timeframe. |
| 4. Evaluation | NOT STARTED | No eligible forecasts scored. |
| 5. Robustness/inference | NOT STARTED | Multi-timeframe comparisons require multiple-testing controls. |
| 6. Manuscript/decision | PROTOCOL DRAFTED | No empirical results. |

Current result remains DATA-LIMITED / NO PERFORMANCE CLAIM.


## 2026-10-25 execution update — acquisition pipeline added
Added `acquire_dhan_timeframes.py` to request NIFTY 50 spot index bars from Dhan v2 (security ID 13, segment `IDX_I`, instrument `INDEX`) for 1m/5m/15m/60m and daily data, in chunks no longer than 90 days. Added `prepare_timeframes.py` for timestamp/OHLC/duplicate checks and a 30m series resampled from six contiguous 5m bars anchored at 09:15 IST. Added `.github/workflows/zigzag-expiry-timeframes.yml` with cache, manual inputs, optional refresh, and an artifact that includes data plus provenance/validation manifests.

| Phase | Status | Evidence / blocker |
|---|---|---|
| 1. Protocol/source audit | PARTIAL — BLOCKED | Timeframe variants registered; exact ZigLib source/timing still unverified. |
| 2. Data audit | PIPELINE ADDED — EXECUTION NOT VERIFIED | Dhan acquisition code/workflow committed; no successful workflow artifact or validated dataset is yet confirmed in this chat. |
| 3. Causal reconstruction | BLOCKED | No source-faithful ZigLib implementation yet. |
| 4. Evaluation | NOT STARTED | No predictions scored. |
| 5. Robustness/inference | NOT STARTED | Requires valid predictions and multiple-comparison control. |
| 6. Manuscript/decision | DRAFT ONLY | No empirical results. |

Important: adding the workflow is not evidence that Dhan authentication succeeded or that data was acquired. The next gate is inspect the workflow result/artifact, correct any logged API/data errors, then validate source parity before scoring.


## Wrapper timing finding — 2026-10-25
The accessible public wrapper mirror shows `repaint=true` as the default and a separate non-repaint branch that only draws when `direction != direction[1]`, using prior-bar points (`z1[1]`, `z2[1]`). This is useful wrapper-level evidence, not authoritative proof of the imported ZigLib implementation. To keep a causal prediction study, primary timeframe evaluation is now specified for `repaint=false`; its signal availability must be the direction-change bar, never the earlier pivot timestamp. Results must be labeled non-repaint-mode results and not default-setting results. Exact library internals and the successful Dhan acquisition artifact remain unverified.


## Latest execution check — 2026-10-25
- Dhan acquisition and 30m preparation scripts plus an Actions workflow are committed.
- A local clone/syntax-check attempt failed because this execution environment could not resolve github.com. Available GitHub tools did not provide direct workflow dispatch or a confirmed run artifact.
- Therefore workflow execution and data acquisition are **UNVERIFIED**, not complete. Exact ZigLib source/causal parity is still blocked. No predictions have been scored.


## 2026-10-25 follow-up — unit tests added
Added `tests/test_zigzag_data_pipeline.py` to test epoch-to-IST conversion, OHLC response parsing, mismatched array rejection, invalid OHLC detection, 30m resampling, and exclusion of incomplete bars. Updated the timeframe workflow to run these tests before attempting data acquisition. This is test coverage added, not a passing CI result; the run has not been confirmed. Data artifact, exact ZigLib parity, expiry mapping and prediction scoring remain open.


## 2026-10-25 cache-key failure and correction
The user supplied screenshots of the failed Actions run. The cache restore step failed with a `Key Validation Error` for a key containing the comma-separated interval list. The validation step then reported all required CSVs missing and could not derive 30-minute bars. Updated the cache key to omit the interval-list field in commit `907e05fc8de0363aecf9fa8e7790c9b63b683b9f`. The correction is committed, but the rerun has not yet been verified. Phase 2 remains BLOCKED; no prediction results exist.


## 2026-10-25 confirmed workflow run — authentication blocker
Run [#40126339052](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40126339052) confirms the cache-key fix worked and the pipeline unit tests passed. All five Dhan datasets failed with HTTP 401 `DH-901` (access token invalid or expired), so no usable data was acquired and validation failed due to missing CSVs. Phase 2 remains BLOCKED until the GitHub Actions secret is updated with a valid Dhan token and a fresh run verifies acquisition. Prediction evaluation remains NOT STARTED.


## 2026-10-25 — Automated Dhan authentication implemented
Updated workflow commit `0705e9aeafec15949f55ebb983f1f77ec60b62ef` to generate a fresh token from the existing `DHAN_CLIENT_ID`, `DHAN_PIN`, and `DHAN_TOTP_SECRET` secrets, mask it, and validate `/v2/profile` before acquisition. Run [#40126973037](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40126973037): unit tests and token generation/profile validation passed. Historical data acquisition is still in progress; phase 2 remains IN PROGRESS, not complete. No prediction results exist yet.


## 2026-10-25 — authenticated acquisition pipeline verified

Run [#40127255063](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063) passed all six unit tests, cache restoration, fresh Dhan token generation/profile validation, historical acquisition, OHLC/timestamp validation, 30-minute derivation, artifact upload, and cache save.

| Phase | Status | Evidence / blocker |
|---|---|---|
| 1. Protocol/source audit | PARTIAL — BLOCKED | Multi-timeframe panel is preregistered; exact imported ZigLib source and availability semantics are still unverified. |
| 2. Data audit | ACQUISITION/VALIDATION PIPELINE PASSED | Successful run and artifact [12573423696](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063/artifacts/12573423696); audit the manifest and actual coverage before treating every date as usable. |
| 3. Causal reconstruction | BLOCKED | Need source-faithful ZigLib behavior and signal availability timestamps; do not infer signals from retrospective pivot labels. |
| 4. Evaluation | NOT STARTED | Evaluator requires a verified, interval-level signal/target CSV. No metrics yet. |
| 5. Robustness/inference | NOT STARTED | Depends on validated predictions and multiple-testing control. |
| 6. Manuscript/decision | DRAFT ONLY | Manuscript must remain explicit that no empirical prediction result has been obtained. |

Current decision: **DATA ACQUISITION SUCCESSFUL; PREDICTION NOT EVALUATED; NO PERFORMANCE CLAIM.** User waived independent tester review for this experiment.


## Artifact audit — 2026-10-25

Downloaded and inspected the successful Actions artifact [12573423696](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063/artifacts/12573423696). The validation report has no structural errors. Raw coverage runs from 2021-10-25 through 2026-10-23: 92,795 5m bars (5 invalid OHLC rows excluded in validated copy), 30,985 15m bars (3 excluded), 8,663 60m bars (2 excluded), and 1,240 daily bars (0 excluded). The 30m derived series contains 14,814 bars and 21 incomplete/noncontiguous bins were dropped. The artifact also contains 1m raw bars; 1m validation was not included in the current validator's required dataset report and must be added before using 1m in scoring.

This audit verifies data pipeline output, not the exact imported ZigLib implementation or prediction performance. Source audit located the public wrapper [ZigZag++ [LD]](https://github.com/rohitbhure65/pine-scripts/blob/master/zigzag.pine), which imports DevLucem/ZigLib/1; public TradingView library metadata describes the function signature and returned direction/two points but does not expose sufficient source details in the available retrieval to prove exact causal pivot availability. The wrapper's default is repaint=true. No source-faithful causal signal stream has been produced, and the historically correct expiry/10:00-to-expiry target table has not been audited. Therefore no scoring should be run yet; phase 3 remains blocked and phase 4 has not started.


## Timestamp/session audit — 2026-10-25

A second audit of the actual downloaded CSVs found an important issue not caught by the existing structural validator: unique, sorted, timezone-aware timestamps and valid OHLC do not prove the observations belong to the intended regular-session calendar. Weekend timestamps occur in the intraday series, including known special trading sessions and other dates that need session-calendar reconciliation. The 1m file also includes many timestamps outside 09:00–16:00 IST (40,975 of 511,268 records under a broad clock-time screen), so 1m cannot be included without determining whether these are pre-open/extended-session observations, timestamp-convention artifacts, or invalid records. The broad clock screen is diagnostic only and is not itself the final exclusion rule.

Counts from the downloaded artifact:
- 15m: 30,985 rows; 166 timestamps fall on Saturday/Sunday; 13 fall outside the broad 09:00–16:00 IST screen.
- 1m: 511,268 rows; 2,636 timestamps fall on Saturday/Sunday; 40,975 fall outside the broad screen.
- 5m: 92,795 rows; 484 timestamps fall on Saturday/Sunday; 37 fall outside the broad screen.
- Derived 30m: 14,814 rows; 69 timestamps fall on Saturday/Sunday.
- 60m: 8,663 rows; 51 timestamps fall on Saturday/Sunday; 5 fall outside the broad screen.
- Daily: 1,240 rows; 6 dates fall on weekends, which may include officially scheduled special sessions and must not be blindly deleted.

This is a calendar/provenance issue, not proof that every weekend row is wrong: India has special Saturday/Sunday sessions on certain dates. Next data gate must compare every observation date/time to an official NSE trading-session calendar and inspect the downloader's timestamp conversion/interval conventions. Until then, the earlier phrase “no structural errors” means only basic CSV structure passed; it does not mean session eligibility is verified. Prediction scoring remains blocked.


## 2026-10-25 — Independent 1-minute timestamp/session audit

Inspected the actual downloaded CSV artifact from successful Actions run [#40127255063](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063), rather than treating workflow success as sufficient. The raw 1-minute file has 511,268 rows, from 2021-10-25 09:01 IST to 2026-10-23 15:29 IST. It is sorted and has no duplicate timestamp strings, but it includes 2,636 weekend-dated rows and 47,612 rows outside the regular-session window 09:15–15:29 IST; 12 rows violate OHLC consistency. Exact 10:00 timestamp rows exist on 1,236 dates. This means the raw 1-minute file is not yet suitable for indicator reconstruction or target pricing without a documented regular-session filter and per-session completeness audit. These are raw-source quality findings, not proof that every out-of-session row is invalid; retain raw rows and explicitly classify them.

| Phase | Current status | Evidence |
|---|---|---|
| 1. Protocol/source audit | PARTIAL — BLOCKED | Exact DevLucem/ZigLib v1 implementation and signal availability semantics remain unverified. |
| 2. Data audit | ACQUISITION PASSED; SESSION/PROVENANCE AUDIT INCOMPLETE | Artifact is present and basic OHLC/timestamp checks exist; 1m audit found weekend/out-of-session/invalid-OHLC rows. Cross-source price parity and historical expiry calendar are still unresolved. |
| 3. Causal reconstruction | BLOCKED | Do not substitute a generic ZigZag for the imported library. |
| 4. Evaluation | NOT STARTED | No eligible forecasts scored. |
| 5. Robustness/inference | NOT STARTED | Requires valid causal forecasts. |
| 6. Manuscript/decision | DRAFT ONLY | No performance claims or result plots. |

Next action: improve validation to report regular-session rows, weekday anomalies, exact 10:00 availability, session completeness and OHLC exclusions for 1m, then build a source-backed historical expiry schedule. Prediction scoring remains prohibited until source parity and target mapping gates pass.
