# Data Acquisition and Acceptance — ZigZag Expiry Direction

Updated: 2026-10-25

## Required data
This experiment's target uses NIFTY 50 spot at 10:00 IST on the first trading session after the previous actual weekly expiry, and the spot regular-session close on the next actual weekly expiry. Daily OHLC alone is insufficient to reproduce the 10:00 reference price. The signal timeframe also must be fixed and documented; Pine indicators operate on the chart timeframe.

## Free sources to try first
1. **Nifty Indices historical index data** — https://www.niftyindices.com/reports/historical-data
   - Official historical index OHLC export. Suitable for daily close and target-endpoint cross-checks; not sufficient by itself for exact 10:00 intraday prices.
2. **NSE All Reports / historical index data** — https://www.nseindia.com/all-reports
   - Official index historical reports and daily snapshots; check downloadable export and license/terms before caching.
3. **NSE public archives** — https://nsearchives.nseindia.com/content/indices/
   - Candidate archive path observed in public source catalogs; verify each requested file exists and is official before use.
4. **Dhan Data API** — use the configured repository secret only inside GitHub Actions; never print or commit tokens. Query instrument/security master first and verify the NIFTY 50 spot instrument identity before downloading.
5. **Other free datasets** — only as secondary overlap checks, with explicit timezone, adjusted/unadjusted definition, timestamp and license recorded.

## Acceptance checklist
- Store source URL, retrieval timestamp, query parameters, instrument identity, bar interval, timezone and file SHA-256.
- Convert timestamps to Asia/Kolkata while preserving original source timestamps.
- Verify regular-session boundaries, duplicates, missing intervals, outliers and monotonic time.
- Cross-check overlapping dates against at least one independent source; report differences rather than silently blending conflicting prices.
- Keep index spot separate from futures and total-return index series.
- For each forecast interval, preserve actual expiry date, previous expiry date, cutoff timestamp, signal availability timestamp, reference-price timestamp/value, target timestamp/value, and source IDs.
- Build expiry dates from official circulars and holidays; do not assume one weekday across all history.
- If the 10:00 bar is missing or ambiguous, abstain for that interval; do not substitute daily open or nearby price silently.

## Current status
No source export has been acquired and validated for this experiment in the current branch. These are prioritized source leads, not claims of data acquisition.
