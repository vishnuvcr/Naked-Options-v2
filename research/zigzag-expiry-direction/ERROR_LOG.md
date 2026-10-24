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
