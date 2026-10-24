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


## Dhan acquisition implementation update (2026-10-25)
Dhan v2 documentation supports `/charts/intraday` with 1, 5, 15, 25 and 60-minute intervals, a last-five-years intraday horizon, and up to 90 days per request. NIFTY 50 is listed in Dhan's public instrument reference as security ID `13` in `IDX_I`; request instrument type is `INDEX`. Sources: [Dhan historical-data API](https://dhanhq.co/docs/v2/historical-data/), [Dhan instrument reference](https://github.com/dhan-oss/dhanhq-skills/blob/main/skills/dhanhq/references/instruments.md).

Added `acquire_dhan_timeframes.py`, `prepare_timeframes.py`, and `.github/workflows/zigzag-expiry-timeframes.yml`. The workflow stores data in an Actions cache and uploads CSVs plus SHA-256/provenance and validation manifests as a 30-day artifact; raw data is not committed to Git. The script can reuse an exact-key cached dataset or force a refresh. Dhan token is passed only through `DHAN_ACCESS_TOKEN` secret. Acquisition success remains unverified until run logs and the artifact are inspected.
