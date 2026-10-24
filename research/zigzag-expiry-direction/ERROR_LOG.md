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
