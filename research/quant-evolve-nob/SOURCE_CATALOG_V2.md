# QE-NOB-2.0 — External Source Catalogue (2026-10-22)

**Status:** Public-source desktop review completed; none of the newly discovered datasets has been imported into the experimental cache. Runtime acquisition/audit remains in progress. **This file records candidate sources, not verified rows or strategy evidence.**

## 1. Primary licensed source: Dhan

- [Expired Options Data API](https://dhanhq.co/docs/v2/expired-options-data/) documents rolling expired index-option data on a relative-strike basis, with OHLC, IV, volume, OI and spot fields; up to five years of history and up to 30 days per call.
- [Historical Data API](https://dhanhq.co/docs/v2/historical-data/) documents intraday candles at 1/5/15/25/60-minute intervals for up to five years and up to 90 days per intraday request.
- The live acquisition job uses the subscribed Dhan API as primary source. The current v2 candidate universe is weekly expiry (WEEK1) only, with ATM/one-step OTM strikes (offsets -1, 0, +1) for CALL/PUT. The last sanitized cache inventory contains 314 eligible weekly option files across 53 observed chunks; the five-year date grid implies about 61 thirty-day chunks, so approximately 52 eligible option request groups remain. This count is derived from cache filenames and is an estimate—not completed-call evidence. There is no verified historical underlying series in the partial cache, so about 23 underlying-history requests are also expected. No monthly option data is present; MONTH1 is excluded from this bounded run. Requests use 25-second timeouts, two attempts, periodic progress logs, and stop after ten consecutive failed request groups. Empty option responses are not cached as valid data; the source gate requires complete request bookkeeping and at least 80% non-empty responses.
- **Known limitation:** this is rolling-relative-strike data, not proof of stable exchange contract/expiry identity. The endpoint does not establish historical bid/ask, depth or executable fills. Never use it alone to pass the execution gate.

## 2. Official Indian sources: daily regime/control features

- [NSE historical reports](https://www.nseindia.com/resources/historical-reports-capital-market-daily-monthly-archives) links historical index data and historical India VIX data, plus index report archives. Use as a daily regime/validation source after confirming downloadable field schema and date coverage.
- [NSE FII/FPI and DII activity](https://www.nseindia.com/reports/fii-dii) provides downloadable CSV reporting daily buy, sell and net values. NSE states the values are provisional and may change with custodial confirmation. Use no earlier than the verified publication time; otherwise lag by one session.
- [Nifty Indices historical data](https://www.niftyindices.com/reports/historical-data) provides index OHLC and total-return index report selectors, as well as P/E, P/B and dividend yield report selectors. It is suitable for independent daily index/return checks where its coverage matches the intended period.
- [NSE historical F&O dissemination information](https://archives.nseindia.com/content/press/Data_Details_F_n_O.pdf) describes the exchange's historical F&O data organization. The detailed EOD/order/trade products require a separate entitlement/quote rather than being assumed freely downloadable; see [NSE historical data subscription information](https://betanseapi.nseindia.com/static/market-data/eod-historical-data-subscription).

**Decision:** use public official daily data for cross-checks and lag-safe daily context where schema permits. It cannot replace minute-level option history or provide executable quote/fill evidence without further source access.

## 3. Public global volatility/macro context

- [Cboe historical VIX data](https://www.cboe.com/tradable-products/vix/vix-historical-data) offers daily VIX closing history from 1990 to present. Treat it as a global risk/volatility proxy only; align by actual publication/close time so a U.S. close that was unavailable at the Indian signal time cannot leak forward.
- [FRED observations API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html) supports historical economic-series retrieval in CSV/JSON and vintage-aware queries, but API access requires a registered key. It can supply selected macro/rates/financial-condition covariates; it is not an intraday global-index substitute.
- Global index/futures lead features remain conditional until an appropriately licensed source, timestamps, market sessions and release lag are established.

## 4. Public option-data candidates — not approved for automatic import

### Hugging Face: rissin/nse-options-intraday

- [Dataset card](https://huggingface.co/datasets/rissin/nse-options-intraday) reports roughly 259 million rows / 2.51 GB, combining daily NSE F&O bhavcopy history with Upstox-sourced one-minute data from around October 2024 onward.
- The card reports license 'other', not a specific reusable license grant. Its own schema notes intraday OI and settlement values are missing.
- **Decision: HOLD / not approved.** Verify provenance and redistribution/use rights in writing before downloading or using it. Do not infer that public visibility means permission to use the data in a trading-oriented study.

### Hugging Face: thetrademarkk/india-index-options-1m

- [Dataset card](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m) describes about 377 million rows / 4 GB and a CC BY-NC 4.0 license, with IST timestamps and strike/expiry fields for options; the maintainer warns far strikes and illiquid contracts are sparse.
- **Decision: NOT APPROVED for strategy evidence under the current trading-oriented scope** because the non-commercial restriction is incompatible with any commercial use unless separate permission is obtained. Even for a permitted non-commercial audit, coverage, duplicates, source lineage and missingness require independent checks.

## 5. Open GitHub underlying-index cross-check

- [technovusin/nifty50-historical-data](https://github.com/technovusin/nifty50-historical-data) documents NIFTY 50 one-minute OHLC from 2017 onward and 15-second bars from September 2026. Its [repository LICENSE](https://github.com/technovusin/nifty50-historical-data/blob/main/LICENSE) is MIT, but a code license is not by itself independent proof of rights in the underlying market data.
- Its README documents known defects/quirks, including missing bars and some cleaned/fixed values. **Decision: candidate for independent underlying-bar cross-check only**, after downloading a small sample, checking data provenance, hashes, timezone/session boundaries and row-level comparison with Dhan/NSE; not an option-price source.

## 6. Composite-data rules

1. Keep Dhan rolling options and Dhan underlying intraday as the primary candidate source while the current acquisition is in flight.
2. Cross-check NIFTY underlying OHLC against an independent source and use official daily India VIX/index/FII-DII data only at their valid publication time.
3. Do not merge option prices from different providers by relative strike alone. Contract identity, expiry, strike, side, timestamp and source must match, or records stay separate.
4. Preserve missing-vs-zero distinctions, duplicate/conflict counts, provenance, timezones, publication lag, checksums and licensing status for every source.
5. Do not import option datasets with unclear or incompatible licenses. Do not purchase another source before completing the licensed Dhan and free-source audits.

## 7. Current decision

The source review improves the Phase 2 catalogue, but **does not close Phase 2**: the live cache audit has not yet run. No newly discovered external dataset has been incorporated into training or candidate fitness. Empirical discovery, final OOS inference and execution validation remain blocked until the acquisition job produces auditable metadata. Exact contract/fill evidence remains a separate FAIL gate.

## Search references

- Dhan: https://dhanhq.co/docs/v2/expired-options-data/ ; https://dhanhq.co/docs/v2/historical-data/
- NSE: https://www.nseindia.com/resources/historical-reports-capital-market-daily-monthly-archives ; https://www.nseindia.com/reports/fii-dii
- Nifty Indices: https://www.niftyindices.com/reports/historical-data
- Global VIX / FRED: https://www.cboe.com/tradable-products/vix/vix-historical-data ; https://fred.stlouisfed.org/docs/api/fred/series_observations.html
- Public datasets: https://huggingface.co/datasets/rissin/nse-options-intraday ; https://huggingface.co/datasets/thetrademarkk/india-index-options-1m ; https://github.com/technovusin/nifty50-historical-data


## Latest bounded-source protocol amendment — weekly expiry only (2026-10-23)

The sanitized cache audit artifact from the interrupted ATM/OTM1 run shows 728 historical weekly option files across the seven offsets -3 through +3, 314 historical WEEK1 files within the allowed offsets -1/0/+1, 53 chunk ranges with at least one weekly file, and zero historical underlying bars (one 14-day underlying probe only). The date grid from 2021-10-23 to 2026-10-22 implies about 61 30-day option chunks and about 23 80-day underlying chunks.

**Active protocol is therefore narrowed to WEEK1 weekly expiry plus ATM/OTM1 only.** Month1 is not enabled because the runtime cache has no historical monthly option family, and code tests alone cannot certify that family is source-complete. This is a throughput/coverage decision made before seeing any candidate fitness or P&L. The estimated request gap is 52 allowed weekly-option files plus up to 23 underlying-history files, with source probes; the live run must report actual counts.

Prior estimates in the earlier protocol amendment (2 expiry families / approximately 732 groups) are historical estimates for the prior scope and are superseded by this amendment. Cache namespace data/cache/quant_evolve_nob_v1 is intentionally reused to preserve partial valid data, but report/artifact output is now isolated to reports/quant_evolve_nob_v2. A stale report copied from the old cache must never be accepted as a fresh acquisition result.


## Weekly-only acquisition estimate — 2026-10-23

The active protocol now requests only the nearest weekly expiry family (WEEK1), ATM and one-step OTM offsets (-1, 0, +1), both CALL and PUT. MONTH1 is excluded because the prior cache audit found no historical monthly option cache. The full configured grid is 61 30-day chunks × 3 offsets × 2 sides = 366 request groups before retries. The existing weekly cache appears to contain approximately 307 reusable files in this offset universe, leaving roughly 59 option groups plus up to 23 underlying-history chunks. This is a planning estimate, not a completed acquisition result. The next workflow must restore valid cache, run regression gates first, and report actual non-empty response coverage. A parse-only audit is not sufficient.
