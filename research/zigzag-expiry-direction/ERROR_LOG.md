# Error and Limitation Log — ZigZag Expiry Direction

## ZZD-001 — External library behavior not yet verified
- **Severity:** High; open
- **Issue:** Supplied Pine code imports DevLucem/ZigLib/1; public library metadata describes inputs/outputs but did not provide enough accessible implementation detail in this run to verify exact pivot-confirmation timing.
- **Risk:** Look-ahead leakage and false historical accuracy if chart pivot time is mistaken for signal availability.
- **Mitigation:** Obtain and version-pin exact library source; test causal availability time and repaint behavior before scoring.

## ZZD-002 — Existing price-data provenance unresolved
- **Severity:** High; open
- **Issue:** Main-branch NWCP report documents failed Dhan source overlap and unresolved source/timestamp provenance.
- **Risk:** Misaligned or unsuitable historical spot data may bias target labels.
- **Mitigation:** Treat existing bars as unverified until provenance, timezone and bar convention are documented; seek independent overlap checks.

## ZZD-003 — Historical expiry calendar must be versioned
- **Severity:** High; open
- **Issue:** NIFTY weekly expiry weekday changed historically and holidays can shift expiry.
- **Risk:** Incorrect interval endpoints and target labels.
- **Mitigation:** Use date-specific official exchange circulars/calendars and preserve evidence for each rule period.

## ZZD-004 — TradingView compilation not demonstrated
- **Severity:** Medium; open
- **Issue:** No TradingView compiler result is available in this run.
- **Risk:** A Python reconstruction could be mistaken for a compiled Pine implementation.
- **Mitigation:** Label any Python checks accurately; claim Pine compilation only when verified.

## ZZD-005 — Generic ZigZag behavior cannot be assumed to equal ZigLib
- **Severity:** High; open
- **Issue:** TradingView's general ZigZag documentation describes retrospective confirmation and revisable latest pivots, but this does not prove exact behavior of the imported DevLucem library version.
- **Risk:** Incorrectly inferred signal timing or false equivalence between implementations.
- **Mitigation:** Keep general documentation as contextual evidence only; block empirical scoring until source-level behavior is verified.


## ZZD-006 — Historical expiry regime mapping incomplete
- **Severity:** High; open
- **Evidence:** NSE current product page says NIFTY weekly expiry is Tuesday, moved to the previous trading day for a holiday. NSE circular FAOP/68747 dated 2025-06-25 revised NIFTY weekly expiry from Thursday to Tuesday and states existing contracts expiring on/before 2025-08-31 remained unchanged (with specified long-dated exceptions). Earlier 2025 Monday change was withheld/modified, so announcement dates cannot be treated as simple effective dates without circular-level mapping.
- **Risk:** Wrong target endpoint for historical intervals.
- **Mitigation:** Build and test a date-by-date expiry schedule from official circulars and contract masters; retain source references per row.


## ZZD-007 — Scoring harness exists but has no validated input dataset
- **Severity:** High; open
- **Issue:** A leakage-guarded CSV scoring utility was added, but the repository's main-branch tree contains no canonical NIFTY spot dataset suitable for this experiment; prior research documents unresolved provenance. No signal rows have been scored.
- **Mitigation:** Supply a validated dataset/export with cutoff and signal-availability timestamps, or acquire and cache one with documented provenance before evaluation.

## ZZD-008 — Wrapper source mirror is not the library source
- **Severity:** Medium; open
- **Issue:** A public GitHub mirror reproduces the indicator wrapper and repaint toggle, but does not expose DevLucem/ZigLib/1 internals and may not match the currently published revision exactly.
- **Mitigation:** Use it only to inspect wrapper logic; do not treat it as proof of imported library semantics.


## ZZD-009 — Free official data source identified but not yet acquired
- **Severity:** Medium; open
- **Evidence:** NSE/Nifty Indices publish historical NIFTY 50 index data via official historical-data portals (NSE and Nifty Indices reports pages). The public pages confirm the source exists, but no downloadable export has yet been validated and cached in this branch.
- **Risk:** The source lead could be mistaken for an acquired dataset.
- **Mitigation:** Acquire a dated CSV export, preserve retrieval date and source URL, validate OHLC/timestamps and cross-check overlapping dates before use.


## ZZD-010 — Indicator timeframe was not pre-specified
- **Severity:** High; open
- **Issue:** The supplied Pine indicator does not specify an explicit timeframe; calculations use the active chart timeframe. The study protocol must pin a timeframe before historical reconstruction.
- **Risk:** Results cannot be reproduced and signal labels differ across timeframes.
- **Mitigation:** Treat timeframe as a protocol defect; do not score until resolved. Because user asked to proceed without further input, document the missing detail and prepare the data workflow, but do not silently choose a timeframe.

## ZZD-011 — Target reference requires intraday data
- **Severity:** High; open
- **Issue:** The target protocol uses a 10:00 IST NIFTY 50 spot reference, which daily OHLC data cannot establish exactly.
- **Risk:** Substituting daily open/close or futures prices would change the target definition.
- **Mitigation:** Acquire validated intraday spot data or amend the protocol explicitly before scoring; no silent substitution.


## ZZD-012 — Timeframe variants pre-registered; implementation/data blockers persist
- **Severity:** High; open
- **Date:** 2026-10-25
- **Issue:** User asked to test various chart timeframes. The supplied script does not pin a timeframe; each timeframe can create different pivot sequences and confirmation times.
- **Mitigation:** Added TIMEFRAME_SENSITIVITY.md pre-registering 5m, 15m, 30m, 60m and 1-day variants, with 1m conditional on data quality. Keep signal rules and targets fixed, use common intervals where possible, report per-timeframe coverage, and correct formal multi-comparison tests. Do not score until exact ZigLib behavior, intraday prices and expiry schedule are validated.
- **Status:** Protocol decision complete; empirical execution still blocked.


## ZZD-013 — Dhan multi-timeframe acquisition workflow added; execution not yet verified
- **Severity:** High; open until a successful artifact is inspected
- **Date:** 2026-10-25
- **Change:** Added Dhan v2 API downloader for NIFTY 50 index security ID 13 (`IDX_I`, `INDEX`), 1m/5m/15m/60m bars, daily OHLC, 90-day request chunks, SHA-256 manifests, retry handling, and a validation/resampling script that derives 30m bars from contiguous 5m bars anchored at 09:15 IST.
- **Risk:** API schema, token validity, plan entitlements, timestamp semantics, and index bar availability have not been verified by a successful run yet. Cached CSVs are not a result until checks pass.
- **Mitigation:** Workflow uploads the data and validation manifests as an artifact; inspect actual run logs and artifact before declaring data phase complete. Never expose token values.

## ZZD-014 — Workflow-run confirmation unavailable in this execution context
- **Severity:** Medium; open
- **Issue:** The available GitHub integration exposes workflow-job/artifact reads and reruns, but no direct workflow dispatch action was found; a successful run/artifact could not yet be confirmed through the available interface.
- **Mitigation:** Workflow is configured to run on matching branch pushes and supports manual dispatch. Verify a resulting run before claiming acquisition success.


## ZZD-015 — repaint default conflicts with causal historical prediction
- **Severity:** High; open pending exact-source verification
- **Date:** 2026-10-25
- **Evidence:** Public wrapper mirror https://github.com/rohitbhure65/pine-scripts/blob/master/zigzag.pine sets `repaint = input(true, 'Repaint Levels')`; the alternate branch draws only on direction changes using prior-bar points.
- **Risk:** Using retrospective pivot labels in a historical prediction backtest leaks future information.
- **Mitigation:** Primary comparison is explicitly non-repaint mode; use direction-change availability timestamp and prior-bar point values, and do not label results as default repaint-on performance. Still block scoring until the imported ZigLib v1 source behavior is verified or faithfully reproduced.


## ZZD-016 — Local runtime could not retrieve repository for static execution
- **Severity:** Medium; open
- **Date:** 2026-10-25
- **Issue:** Attempted a shallow clone of the active GitHub branch in the local container to run Python syntax checks; DNS/network access to github.com was unavailable. The GitHub integration in this session did not expose a direct workflow-dispatch action, and no successful workflow artifact was confirmed.
- **Risk:** The acquisition and resampling scripts have not been executed end-to-end in this environment; potential API/schema or runtime errors remain possible.
- **Mitigation:** The configured branch-push workflow should run the scripts and upload logs/data/validation manifests. Inspect its actual run/artifact before considering the data gate passed. No result is claimed in the absence of that evidence.


## ZZD-017 — Unit tests added but not yet executed by confirmed CI
- **Severity:** Medium; open until CI result reviewed
- **Date:** 2026-10-25
- **Change:** Added unit tests for epoch conversion, API response array alignment, OHLC validation, six-bar 30m aggregation, and incomplete-bar exclusion; workflow now runs tests before data requests.
- **Status:** Code committed; no CI success evidence is available in this session. Do not state tests passed until the workflow logs confirm it.


## ZZD-018 — GitHub Actions cache key validation failure
- **Severity:** High; fix committed, rerun pending
- **Date:** 2026-10-25
- **Observed evidence:** User-provided Actions screenshots show the `Restore reusable cached market data` step failed with `Key Validation Error` for the key beginning `zigzag-dhan-v1-Linux-2021-1...`. Since restore failed, acquisition did not produce the required CSV files; the subsequent validation step correctly reported missing `nifty50_5m.csv`, `nifty50_15m.csv`, `nifty50_60m.csv`, `nifty50_daily.csv`, and inability to derive 30m.
- **Root-cause assessment:** The cache key interpolated the comma-separated interval input (`1,5,15,60`) directly. This is consistent with the key-validation failure shown in the run. The exact complete annotation text is truncated in the screenshot, so this is a high-confidence diagnosis, not a verbatim full log.
- **Fix:** Removed the comma-separated intervals value from the cache key while retaining OS and date-range scope. Commit: `907e05fc8de0363aecf9fa8e7790c9b63b683b9f`.
- **Verification:** Fix is committed to the active developer branch and should trigger another push run. Its outcome is not yet available; do not claim the cache or acquisition succeeded until the new run is inspected.


## ZZD-019 — Dhan credential rejected by acquisition run
- **Severity:** High; external secret/configuration required
- **Date:** 2026-10-25
- **Run:** [GitHub Actions run #40126339052](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40126339052)
- **Observed:** Unit tests passed and cache restoration passed. Acquisition requests for 1m, 5m, 15m, 60m and daily all returned HTTP 401 `DH-901`: `Client ID or user generated access token is invalid or expired.` No market datasets were acquired; subsequent validation correctly failed due to missing files. The artifact is only 899 bytes and contains reports, not usable candles.
- **Cause:** `DHAN_ACCESS_TOKEN` secret currently contains an invalid/expired Dhan user access token, or otherwise does not match the active credential. This cannot be fixed by changing Python parsing logic.
- **Next action:** Update the GitHub Actions repository secret `DHAN_ACCESS_TOKEN` with a fresh valid Dhan access token, then rerun the workflow. Never expose the token in chat or commit it.
- **Status:** Open; data phase blocked. No prediction metrics exist.


## ZZD-020 — Automated token generation verified; acquisition pending
- **Severity:** Medium; pipeline execution in progress
- **Date:** 2026-10-25
- **Run:** [GitHub Actions run #40126973037](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40126973037)
- **Observed:** Unit tests passed. Token generation from repository secrets succeeded and the resulting token passed Dhan `/v2/profile` validation for the configured client ID. Acquisition step started; no data completion has yet been verified.
- **Security:** Token is masked and used at runtime; no token value is logged, committed, or uploaded as an artifact.
- **Next action:** Verify data acquisition, manifest coverage and validation outputs before starting prediction scoring.
- **Status:** Open until data acquisition/validation concludes. No prediction metrics exist.


## ZZD-021 — Intraday timestamp/session eligibility not verified
- **Severity:** High; open
- **Date:** 2026-10-25
- **Evidence:** Direct audit of artifact [12573423696](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063/artifacts/12573423696) found weekend-dated observations in every intraday timeframe and substantial 1m records outside a broad 09:00–16:00 IST clock screen. Counts: 1m 511,268 rows / 2,636 weekend timestamps / 40,975 outside broad clock screen; 5m 92,795 / 484 / 37; 15m 30,985 / 166 / 13; 30m derived 14,814 / 69 / 0; 60m 8,663 / 51 / 5. Daily data contains six weekend dates.
- **Interpretation:** Some weekend sessions may be legitimate special sessions; do not blindly drop all weekend data. The current validator checks sorting, duplicates, timezone and OHLC, but does not establish exchange-session eligibility or confirm Dhan bar timestamp semantics.
- **Risk:** Wrong bars may alter pivot sequences, 10:00 target references, and timeframe comparisons.
- **Mitigation:** Add an official NSE session-calendar audit, check Dhan interval timestamp conventions, investigate 1m pre-open/extended-time rows, and retain a row-level exclusion report. Do not score any timeframe until this passes.
- **Status:** Open; evaluation remains blocked.


## ZZD-021 — Raw 1-minute file contains weekend and out-of-session timestamps
- **Severity:** High; open
- **Date:** 2026-10-25
- **Artifact:** [Actions run #40127255063, artifact #12573423696](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063/artifacts/12573423696)
- **Observed:** 511,268 1-minute rows; sorted timestamps and no duplicate timestamp strings. There are 2,636 rows dated Saturday/Sunday, 47,612 rows outside the regular-session time window 09:15–15:29 IST, 12 OHLC-inconsistent rows, and exact 10:00 timestamp rows on 1,236 dates. The first/last timestamps are 09:01 IST and 15:29 IST.
- **Risk:** Unfiltered out-of-session rows can distort ZigZag pivots; incomplete/missing 10:00 bars or sessions can corrupt target labels. A basic monotonic timestamp check alone is insufficient.
- **Mitigation:** Preserve raw data. Add a separate session-audit report; filter regular-session observations only in derived data, document the rule, enumerate affected dates, and cross-check 10:00 and expiry close against an independent source before target construction. Do not score the raw 1m series.
- **Status:** Open. No prediction metrics exist.


## ZZD-022 — Session diagnostic is not official calendar certification
- **Severity:** High; open
- **Date:** 2026-10-25
- **Change:** Added `research/zigzag-expiry-direction/audit_sessions.py` and workflow artifact `reports/zigzag_session_audit.json`. The diagnostic audits timestamps, duplicates/order, OHLC, weekends and broad clock-time flags across 1m/5m/15m/30m/60m/daily files. It deliberately does not remove rows.
- **Remaining limitation:** No official NSE session calendar is yet ingested or reconciled, and Dhan timestamp labeling (bar start vs bar end) is not independently confirmed. Weekend dates can be valid special sessions; broad clock bounds are diagnostic only.
- **Mitigation:** Add official session-day evidence and test Dhan timestamp conventions before creating a final eligible dataset.
- **Status:** Open; no scoring permitted.


## ZZD-023 — Existing 30-minute resampling unit test used wrong return type
- **Severity:** Medium; fix committed, CI rerun pending
- **Date:** 2026-10-25
- **Evidence:** Actions run [#40127961418](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127961418) failed in the unit-test step before acquisition. The test treated the third return value from `derive_30m` as a dictionary, but the function returns the output path as a `Path` object.
- **Fix:** Changed the assertion to check `Path(info).exists()` in commit `1b6845b3b0d81b333ede7be9071ecd6ebbff2d10`.
- **Impact:** This was a test defect, not evidence of market-data failure. Because the test gate stopped the job, no new data were acquired in that run; downstream validation/audit steps correctly reported missing files.
- **Status:** Fix committed; confirm the next Actions run before calling it resolved.


## ZZD-024 — CI path filters initially omitted audit/test files
- **Severity:** Medium; fixed, run pending
- **Date:** 2026-10-25
- **Evidence:** After fixing the failing 30m test, the commit triggered the separate NIFTY research workflow but did not trigger the ZigZag acquisition workflow because its push path filters did not include `tests/test_zigzag_data_pipeline.py` or `audit_sessions.py`.
- **Fix:** Added both paths to the ZigZag workflow's push filters in commit `2f2719e99f7159a2121d0d745b111c07249d3bd2`, which should trigger the intended CI run.
- **Status:** Fix committed; await and inspect the resulting ZigZag Actions run.


## ZZD-025 — Session audit assumed every valid dataset report had a status field
- **Severity:** Medium; fix committed, CI rerun pending
- **Date:** 2026-10-25
- **Evidence:** Run [#40128132592](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40128132592) passed tests, Dhan authentication, acquisition and timeframe validation, then failed in `audit_sessions.py` with `KeyError: 'status'`. Missing/schema-invalid datasets have a `status` field; valid audit results instead contain row statistics without that field.
- **Fix:** Changed the decision check to use `result.get("status")` in commit `2345caf6d58be354987464a5e3010621a6e11427`.
- **Impact:** Market data and validation were acquired successfully; the session report generation crashed before artifact upload completed (the other files were still uploaded). No prediction metrics were computed.
- **Status:** Fix committed; verify next run.


## ZZD-026 — Dhan token generation returned no accessToken and audit conflated raw findings with fatal errors
- **Severity:** High; auth open, audit logic corrected
- **Date:** 2026-10-25
- **Run:** [Actions run #40128212164](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40128212164)
- **Observed:** Unit tests passed and cache restoration succeeded. Automated token generation received a response without a usable `accessToken`; the response body was intentionally not logged. The workflow's audit then failed because it treated raw OHLC findings as fatal, and because the optional 1m file may be absent from the restored cache.
- **Fix:** Commit `1bb420e55cfdfa64ef26bfe594437b4665fa0639` separates timestamp parse/timezone failures, duplicate timestamps, unsorted timestamps, and missing required datasets from raw OHLC findings. Raw OHLC anomalies are reported without deleting source rows; 1m is marked optional as preregistered. The audit still explicitly blocks scoring until official session-calendar and Dhan timestamp conventions are verified.
- **Remaining action:** Re-run workflow; diagnose Dhan token response using safe status/field-name logging only, and do not expose credentials or token values. If token generation is unavailable, validate the configured access-token secret as a fallback before requesting fresh data.
- **Status:** Audit correction committed; CI verification pending. Authentication remains unresolved for this run. No prediction metrics exist.


## ZZD-027 — Official session calendar and Dhan candle timestamp semantics remain unresolved
- **Severity:** High; open
- **Date:** 2026-10-25
- **Evidence:** Official NSE product documentation and circular NSE/FAOP/68747 establish the current Tuesday weekly expiry rule and the 2025 transition from Thursday, with contract-specific exceptions. NSE session/holiday pages are available, but a complete dated session table (including special sessions and exceptional closures) has not yet been ingested and validated. Dhan v2 docs describe the timestamp field as Unix epoch but do not clearly define whether each intraday candle timestamp denotes bar start or bar end.
- **Risk:** Wrong expiry targets or a one-bar timing shift can change both the label and whether a ZigZag signal was knowable at cutoff.
- **Mitigation:** Added OFFICIAL_CALENDAR_PROTOCOL.md with required source fields, expiry-regime handling, row-level eligibility ledger, and unit-test cases. Continue sourcing the official session table and verify timestamp convention independently; do not score until both gates pass.
- **Status:** Open. No prediction metrics exist.


## TA-001 — Compatibility workflow setup failed before upstream tests
- **Severity:** Medium; corrective change committed, rerun pending.
- **Evidence:** GitHub Actions run [#40129671248](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40129671248) failed in `actions/setup-python` because pip caching searched the research repository root for `requirements.txt` or `pyproject.toml`; neither is present at that root. The upstream repository had not yet been cloned, so this is a workflow configuration failure, not an upstream TradingAgents test failure.
- **Correction:** Removed `cache: pip` from `.github/workflows/tradingagents-compatibility.yml` in commit `93c6f58360276259f702c61fecc3d29756bb857d`. No test pass is claimed until a subsequent run executes the upstream suite.


## TA-002 — First compatibility workflow configuration failure (resolved)
- **Severity:** Medium; fixed.
- **Evidence:** Run [#40129671248](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40129671248) failed before upstream checkout because `actions/setup-python` pip caching searched the research repository root for `requirements.txt` or `pyproject.toml`.
- **Correction:** Removed `cache: pip` from the workflow. The subsequent run [#40129883044](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40129883044) passed dependency installation, upstream unit tests, Ruff, and clean-install import. The error is retained as a resolved issue to prevent recurrence.



## TA-003 — Yahoo live probe scope limitation (open gate, not a code failure)
- **Severity:** Medium; research gate remains open.
- **Evidence:** [Run #40130052739](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40130052739) retrieved 21 daily and 375 five-minute `^NSEI` rows in short windows.
- **Limitation:** Current short-window availability does not establish historical intraday coverage, exact 10:00 IST cutoff semantics, official-session completeness, or point-in-time news/fundamentals. Passing the probe must not be represented as formal backtest data validation.
- **Required action:** Use a frozen historical dataset and verify its timestamps/session membership before evaluating any predictions.



## TA-004 — Standard TradingAgents market data is not cutoff-safe for 10:00 IST by default (open blocker)
- **Severity:** High; formal historical evaluation blocked.
- **Evidence:** Pinned `tradingagents/agents/tools.py` market tool requests date-based windows; `tradingagents/dataflows/vendors/yahoo/market.py` strips timezone info from the Yahoo OHLCV index before formatting; the default graph includes social, news, and fundamentals analysts.
- **Risk:** A historical run could receive daily or ancillary data that does not represent only information available by the 10:00 IST cutoff. A forecast-record timestamp validator cannot independently prove the model's actual input set.
- **Mitigation:** Use a custom frozen market-only snapshot/adapter, no unrestricted Yahoo market retrieval, no undated news/fundamentals/social data, and hash the exact input manifest. Add tests proving any requested data timestamps are <= cutoff. Keep formal evaluation blocked until this is demonstrated.



## TA-005 — Snapshot validator is not yet a source or session certification (open gate)
- **Severity:** Medium; historical evaluation remains blocked.
- **Details:** New validator checks timestamp and OHLC record integrity, but cannot prove source timestamps are bar-start vs bar-end, completeness of official trading sessions, immutability/revision history, or source accuracy.
- **Mitigation:** Require source/query provenance, SHA-256 of frozen source files, independent overlap checks, official session membership, and a cutoff-specific materialized snapshot before graph invocation.



## TA-006 — Dhan access token rejected; free-source fallback used
- **Severity:** High for premium data acquisition; workaround succeeded.
- **Evidence:** [Initial run #40131454946](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40131454946) reported HTTP 401 during Dhan profile validation. The configured token was not printed or committed.
- **Mitigation:** Added a public Yahoo Finance `^NSEI` fallback and robust token validation/fallback logic. Successful acquisition and validation: [run #40131619468](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40131619468).
- **Residual risk:** Yahoo's intraday retention is limited (1m ~7 days; 5m/15m ~60 days; 60m ~2 years). It does not replace the five-year intraday dataset required by the original study. Refresh the Dhan token/secrets to acquire the longer history. Yahoo daily timestamps are midnight labels and cannot be treated as close timestamps.



## TA-007 — Public five-year intraday source provenance not yet certified
- **Severity:** Medium / open validation gate.
- **Finding:** A public release claims five-year NIFTY 50 spot 5-minute data; acquisition and OHLC/schema audit passed in [run #40131891819](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40131891819). Archive digest: `0c1f3de848a4e8c05e233c195685e7ae560d56d08df8baba8b2ffcfac699d3f8`; normalized CSV digest: `a36106d04852bedc95019f3fc480e858961e654373a65108d4963bc9233c56cb`.
- **Residual risk:** publisher provenance is third-party; session coverage and bar-start semantics are not independently certified. The automated audit explicitly remains `NOT_VERIFIED` for official NSE sessions. Keep model scoring blocked until overlap comparison and session-calendar checks pass.



## ZZD-017 — Public 5-minute archive has nonstandard session rows and no overlap with Yahoo fallback
- **Severity:** Medium; validation gate remains open.
- **Evidence:** Local inspection of artifact 12575426805 found 92,876 rows across 1,244 dates, sorted/unique timestamps, and zero invalid OHLC rows. 1,236 dates have 75 bars from 09:15 through 15:25. Six weekend-dated dates and 48 rows outside the regular 09:15–15:25 clock window were observed. Public archive ends 2026-04-21; Yahoo fallback begins later, yielding zero overlapping timestamps in current artifacts.
- **Interpretation:** Weekend/special-session records may be legitimate or erroneous; do not silently delete them. The absence of overlap means independent price parity is not established.
- **Mitigation:** Added `research/zigzag-expiry-direction/audit_public_5m.py` and integrated it into the acquisition workflow to persist a full diagnostic report. Classify candidate sessions against official exchange records and establish timestamp semantics before any evaluation.

## ZZD-018 — Source-faithful scoring gate failed; research closed as no-go
- **Severity:** Critical for the requested empirical claim; no score generated.
- **Evidence:** TradingView's public ZigLib page documents function signature and outputs, but the source materials available in this run did not expose enough implementation detail to establish exact pivot confirmation and signal-availability timing. The reviewed public wrapper mirror imports DevLucem/ZigLib/1 and is not the library implementation. The public five-minute data archive also has unresolved official-session classification, and its current Yahoo fallback has no overlapping timestamps for price parity.
- **Risk:** A guessed ZigZag port or retrospective pivot location could create look-ahead leakage and a false accuracy estimate.
- **Decision:** Do not substitute a generic ZigZag; do not score. Close this run as **NO-GO FOR SOURCE-FAITHFUL PREDICTION CLAIM**, not as evidence of no predictive value.
- **Restart criteria:** Exact library source or a reproducible TradingView signal export with confirmation timestamps; official session/expiry schedule; and an authoritative overlapping spot-price series for reconciliation.

## ZZD-019 — Public wrapper source located; imported library still unavailable
- **Severity:** Medium; source gate remains open.
- **Evidence:** https://github.com/rohitbhure65/pine-scripts/blob/master/zigzag.pine mirrors the ZigZag++ [LD] wrapper and confirms Depth=12, Deviation=5, Backstep=2, `repaint=true` default, imported dependency `DevLucem/ZigLib/1`, use of prior-bar point references in the non-repaint branch, and direction-change alert frequency at bar close.
- **Limitation:** The file imports the library but does not include the library internals. The public TradingView library page exposes the API and outputs, not enough source lines to reproduce the algorithm and confirmation timing.
- **Decision:** Use the mirror only as wrapper evidence. Do not treat it as exact library source; no empirical scoring until causal behavior is source-verified or an export provides confirmed signal timestamps.

## ZZD-020 — Available dataset does not close source/target validity gates
- **Severity:** High; empirical claim remains blocked.
- **Evidence:** At user direction, downloaded workflow artifact 12575253300 and verified that the archive contains 1m/5m/15m/30m-resampled/60m/daily data plus validation/session reports.
- **Limitation:** Data presence does not establish exact ZigLib v1 signal timing, official session classification, contract-specific weekly expiry dates, or the semantics of the required 10:00 and expiry-close prices.
- **Mitigation:** Continue using available data for descriptive diagnostics. Keep the preregistered primary score unreported until the required source and target evidence exists. Do not pass a generic ZigZag approximation off as ZigZag++ [LD].


## ZZD-023 — Shared five-minute cache path mixed providers (resolved in code; CI pending)
- **Severity:** High.
- **Issue:** Dhan acquisition, Yahoo fallback, and the independent public 5-minute archive reused `nifty50_5m.csv`. The public archive step could overwrite the downloaded Dhan series, and the cached file could later be mistaken for Dhan data.
- **Correction:** The Dhan, public-archive, and Yahoo 5-minute outputs now use unique filenames. Old ambiguous `nifty50_5m.csv` data is quarantined using a SHA-256-derived filename. The 30-minute resampler uses an explicitly selected and source-specific validated file.
- **Verification:** Code changes committed; the new GitHub Actions test/run outcome has not yet been checked.

## ZZD-024 — Cross-source price outliers (open)
- **Severity:** High for source acceptance.
- **Evidence:** 82,451 exact timestamp overlaps across 1,105 dates. 94.99% of close pairs are within 0.05 points, but 800 rows differ by more than 1 point and the maximum close difference is 10.90 points. In the subset with 75 bars in both sources, 666 rows differ by more than 1 point.
- **Risk:** Treating both sources as interchangeable or averaging them could alter pivots and target labels.
- **Mitigation:** Keep raw sources separate; inspect large discrepancies, certify source timestamps/session dates, and never silently merge or drop the affected rows.

## ZZD-025 — Dhan authentication workflow contained a malformed shell/heredoc section (corrected; CI pending)
- **Severity:** High for workflow execution.
- **Issue:** The checked-in token-renewal step contained an unmatched/duplicated `python - <<'PY'` section that was not valid as a standalone shell sequence.
- **Correction:** Replaced the section with a single Python block that validates an existing token, attempts TOTP renewal when configured, masks token values, and falls back to Yahoo if Dhan authentication cannot be established.
- **Verification:** Updated workflow is committed; do not claim the renewed block has passed CI until the new run is inspected.
