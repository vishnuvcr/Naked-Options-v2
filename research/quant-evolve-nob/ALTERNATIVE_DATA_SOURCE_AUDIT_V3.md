# QE-NOB-3.0 Alternative Data Source Audit

**Date:** 2026-10-23  
**Status:** Investigation only; not a data approval or strategy result.

## Current blocker confirmed by the automated gate

Workflow [39933612441](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39933612441) completed successfully as automation, while the strict research gate returned `BLOCKED_DATA_LIMITED`. The sampled payload contained 746 underlying bars and 765 rolling-option bars, but no stable dated contract identity and no bid/ask quote fields. These are probe sample counts, not full coverage.

## Candidate legitimate sources investigated

| Source | Available evidence | Use in this research | Remaining gap |
|---|---|---|---|
| Dhan expired-options rolling endpoint | Official Dhan documentation says the API returns rolling ATM-relative strike series with OHLC, IV, volume, OI and spot, for up to 30 days per request and up to five years of history. [Dhan support](https://dhan.co/support/platforms/dhanhq-api/do-dhan-provides-expired-options-data-via-the-api-s/) · [API reference copy](https://github.com/marketcalls/dhan-api-docs/blob/main/18-expired-options-data.md) | Candidate for underlying-conditioned option-premium research if contract mapping can be reconstructed reliably. | Rolling strike-relative series is not, by itself, a stable dated contract identifier; probe has no bid/ask fields. Need prove mapping semantics and execution-price adequacy. |
| NSE Historical Contract-wise Price Volume Data | NSE offers contract-wise historical derivative price/volume records with date, expiry, strike, option type, OHLC/close, settlement, volume/contracts, turnover and OI. [Official NSE page](https://www.nseindia.com/report-detail/fo_eq_security) | Potential cross-check for daily dated contract identity, settlement and end-of-day data. | Page notes a 90-day access limit for its period filter; daily OHLC cannot validate 5-minute entry/exit fills or bid/ask slippage. Availability and bulk acquisition need to be tested. |
| NSE daily F&O UDiFF bhavcopy archives | Official NSE derivatives reports list UDiFF Common Bhavcopy Final; archives exist via the NSE reports area. [NSE derivatives reports](https://www.nse.in/all-reports-derivatives) · [Historical report index](https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives) | Free-source candidate for contract/date/strike/type and daily OHLC/volume/OI validation. | Daily records alone cannot establish intraday execution, contemporaneous spreads or depth. Must verify download rights, schema, date coverage and symbol/expiry transitions. |
| Dhan live option chain | Official docs describe live chain with security IDs, expiry, LTP, volume, OI, IV and best bid/ask. [Dhan option-chain docs](https://dhanhq.co/docs/v2/option-chain/) | Can support forward data collection and execution calibration prospectively. | Live snapshots do not recreate historical bid/ask quotes; do not backfill past execution assumptions with present quotes. |

## Decision

Do not lower the standard by substituting daily settlement/close data for intraday fills, or by treating rolling ATM-relative strike labels as stable contract identity without validation. First test whether NSE daily archives can provide a reproducible dated-contract master and daily cross-check; separately, retain the Dhan rolling history only for the fields it genuinely supports. A strategy may not pass the execution gate without a defensible price/slippage model, and the absence of historical bid/ask must be disclosed as a limitation.

## Next bounded tasks

1. Implement an NSE bhavcopy schema/coverage checker that does not depend on undocumented scraping assumptions.
2. Validate date, expiry, strike, call/put, instrument, OHLC, volume and OI consistency on a small, representative date sample.
3. Check whether the contract master can map Dhan rolling series to stable contracts for each timestamp. If not, explicitly reject this composite.
4. Preserve cache checksums, source URLs, retrieval dates, and missingness summaries.
5. Stop after this source feasibility gate if there is no lawful, reproducible route to adequate data; do not launch the 600-candidate search prematurely.
