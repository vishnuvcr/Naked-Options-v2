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
