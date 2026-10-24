# Official NSE Session and Weekly-Expiry Calendar Protocol

Updated: 2026-10-25

## Purpose

Create a reproducible date-level mapping for each prediction cutoff and its next actual NIFTY weekly expiry. Do not infer exchange sessions from weekdays alone and do not score against a guessed expiry date.

## Source-backed findings

1. NSE's current NIFTY 50 F&O product page says weekly options expire on Tuesday of the expiry week; if Tuesday is a trading holiday, expiry moves to the previous trading day.
   - Source: https://www.nseindia.com/static/products-services/equity-derivatives-nifty50
   - Retrieved/reviewed: 2026-10-25.
2. NSE circular **NSE/FAOP/68747**, dated 2025-06-25, revises NIFTY weekly expiry from Thursday to Tuesday. It states that already introduced contracts expiring on/before 2025-08-31 generally remain unchanged, with separate treatment for long-dated NIFTY/BANKNIFTY option contracts from September 2025 onward; existing long-dated contracts were to be realigned at EOD 2025-07-31.
   - Official PDF: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAOP68747.pdf
3. NSE circular **NSE/FAOP/65336**, dated 2024-11-29, says there was no change to NIFTY monthly, weekly, quarterly, or half-yearly expiry days; its January 2025 effective change concerns other indices.
   - Official PDF: https://nsearchives.nseindia.com/content/circulars/FAOP65336.pdf
4. NSE's market timing and holiday page is the authoritative starting point for regular and special sessions. Special weekend sessions exist, so weekend rows must not be discarded solely because their weekday is Saturday/Sunday.
   - Source: https://www.nseindia.com/resources/exchange-communication-holidays
5. Dhan v2 historical-data documentation says intraday timestamps are Unix epoch timestamps and lists 1/5/15/25/60-minute intervals with a maximum 90-day request window. The documentation reviewed does **not** unambiguously state whether each candle timestamp denotes its opening time or closing time.
   - Source: https://dhanhq.co/docs/v2/historical-data/
   - This uncertainty is a hard blocker for exact 10:00 target selection and signal cutoff alignment.

## Calendar construction requirements

- Store a versioned session file with at least `date,is_trading_day,session_type,source_url,source_retrieved_at`.
- Include official regular sessions, declared holidays, special sessions, shortened sessions, and exceptional closures. Preserve source evidence per row or by clearly linked official year-specific files.
- Store a separate expiry-rule table with `effective_from, effective_to, weekday, source_circular, applicability_notes`; do not encode transition rules only as undocumented code.
- For weekly expiry, choose the relevant rule regime from the actual contract/expiry date, then shift a holiday expiry to the previous *actual trading session* as directed by the applicable NSE rule.
- The transition requires contract-level care: the 2025 circular distinguishes existing contracts from newly generated contracts and long-dated contracts. The calendar builder must not claim every contract was switched based solely on announcement date.
- Record each target interval as: prior actual expiry session close cutoff; next actual trading session's 10:00 IST reference; next actual weekly expiry session close. Missing required reference bars make that interval ineligible; do not forward-fill.
- Keep raw vendor data immutable. Create derived eligible data and a row-level inclusion/exclusion ledger with reason codes.
- Independently compare expiry dates against official NSE contract-master/report evidence where available. Any disagreement blocks scoring.

## Validation gates

1. No duplicate session dates in the official session table.
2. Every date used as an expiry is an official trading session.
3. Every holiday-shifted expiry resolves to the prior official trading session, not merely the previous calendar day.
4. Special sessions are explicitly identified.
5. For every scored interval, the 10:00 reference timestamp and expiry close timestamp match the verified vendor candle convention.
6. Unit tests cover ordinary week, expiry holiday, adjacent holidays, special Saturday session, Thursday-to-Tuesday regime transition, and missing 10:00 bar.
7. Preserve circular URL and the rule version used for every target label.

## Current decision

**NOT READY FOR SCORING.** Circular-level expiry rules are partially mapped, but the complete official session-day table and contract-level transition mapping have not yet been ingested and tested. Dhan's published timestamp field definition alone does not resolve candle start/end semantics. Exact ZigLib v1 causal signal timing is a separate blocker.

## Explicit prohibition

Do not substitute a hand-written weekday calendar for the official session table; do not treat a public wrapper as the ZigLib library implementation; do not infer performance from the mere success of data acquisition or validation.


## Official holiday-source leads by year

These are official NSE circulars or the official NSE holiday portal. They establish a source collection route, **not yet a complete ingested session calendar**.

- 2021 Capital Market holiday circular: https://archives.nseindia.com/content/circulars/CMTR46623.pdf
- 2022 F&O holiday circular: https://nsearchives.nseindia.com/content/circulars/FAOP50561.pdf
- 2024 Capital Market holiday circular: https://archives.nseindia.com/content/circulars/CMTR59722.pdf
- 2025 official NSE holiday page: https://www.nseindia.com/static/holidays-for-the-calendar-year-2025
- 2026 F&O holiday circular: https://nsearchives.nseindia.com/content/circulars/FAOP71777.pdf
- Current interactive official holiday portal (must select the relevant product/segment and year): https://www.nseindia.com/resources/exchange-communication-holidays

**Important:** Capital Market and F&O holiday lists can differ in purpose and need not be treated as interchangeable without checking segment applicability. The target is the NIFTY 50 spot index, while the weekly-expiry schedule is a derivatives contract schedule. Use the official session calendar applicable to the underlying spot index for spot timestamps and the applicable F&O circular/contract record for expiry dates. Check special sessions and any ad-hoc circulars before certifying dates.
