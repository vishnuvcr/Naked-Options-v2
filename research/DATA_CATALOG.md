# Data catalog and provenance

Version: NIFTY-PRED-1.0  
Last audit update: 2026-10-14  
Status: Source capabilities researched; no repository dataset yet verified.

## Primary schema

The daily index table is normalized to: date (exchange-local session date), open, high, low, close, volume_or_traded_quantity (nullable only when source does not provide an equivalent), source_id, retrieved_at_utc, source_asof_timestamp, raw_record_hash and source_version. Any missing OHLC element invalidates that bar. Missing volume is recorded as unavailable; it is never silently converted to zero. Duplicate session dates, non-positive prices and OHLC consistency are hard validation errors.

All merged auxiliary inputs must add their own source_id, observation_date, known_at timestamp / publication lag, units and raw provenance. A same-calendar-day US-market close cannot be used for a prediction made before the US market closes. It is shifted so that only a previously available observation is exposed. Data joins use as-of logic with an explicit known-at field, not indiscriminate same-date joins.

## Source register

| Source | Target / variables | Preferred method | Expected frequency / span | Status at repository start | Caveats |
|---|---|---|---|---|---|
| DhanHQ Data API | NIFTY underlying candles; possible historical intraday candles and derivatives if eligible instruments can be resolved | API using DHAN_ACCESS_TOKEN secret; daily endpoint first, intraday only with timestamp/ID verification | Daily from instrument inception per provider docs; minute intervals up to five years per provider support docs | Access not yet tested; requires secret/subscription and known valid instrument identifiers | Token never echoed or committed. Log HTTP status and redacted error only. Preserve response schema / identifier. |
| NSE / NSE Indices | Official NIFTY 50 daily OHLC; India VIX; exchange daily reports | Official historical-data pages / APIs after observed access check | Daily; exact obtainable span determined in run | Public source identified; programmatic retrieval not yet verified | Website HTML/anti-bot responses must not be accepted as JSON. Record terms and raw hash. |
| Yahoo Finance via yfinance | NIFTY 50 proxy series, India VIX/global indexes, commodity, FX and rates series | Public fallback / external features | Daily; instrument-specific | Public data path identified; acquisition not yet run | Not official exchange data; ticker may be missing or revised. Must cite source and keep retrieval date. Never merge same-date foreign closing values without availability lag. |
| Global equity proxies | S&P 500, Nasdaq, Nikkei, Hang Seng or other documented market indices | Yahoo Finance or other free source when present | Daily | Not acquired | Only earlier close values that existed by forecast origin are eligible. Calendar mismatch / holidays need explicit handling. |
| FX / commodity / bond proxies | USD/INR, gold, crude oil, U.S. 10-year yield and other predeclared macro proxies | Public financial source or official public data (RBI/FRED) | Daily / release frequency specific to source | Not acquired | Unit, timezone, close-time, release time, revisions and stale observations tracked. |
| India VIX | Spot VIX daily OHLC / closes | NSE official historical data preferred; fallback clearly marked | Daily | Source definition verified; data not acquired | India VIX is option-implied expected volatility, not realized volatility. No historical surface is implied by a VIX series. |
| NSE F&O / NIFTY options | Historical option price/OI/volume, implied vol, skew, put-call measures | NSE historical reports or Dhan, only when contract/expiry/security definitions can be mapped | Contract-level, daily or intraday | Not acquired / availability requires testing | Current option chain cannot substitute for point-in-time historical quotes. Expiry and lot-size changes must be date-effective. Bid/ask cannot be fabricated from settlement or close price. |
| FII/FPI and DII activity | Daily buy/sell/net flow | Official NSE daily participation report; RBI/other official source only where series definitions align | Daily | Not acquired | Reporting/publishing time matters; flow data may be available after the forecast cut-off and then must be lagged. |
| Market breadth / constituents | Advance-decline, constituent returns / volume, sector breadth | Official historical constituent files where available | Daily | Not acquired | Current membership must not be backfilled into historical periods. Require point-in-time membership to avoid survivorship bias. |
| Corporate actions | constituent adjustments, corporate events if constituent features used | NSE/BSE official corporate-action reports | Event frequency | Not acquired | Avoid constituent features until action and membership history are available; an index level itself may already incorporate index reconstitution. |
| News / sentiment | timestamped India / global finance news, sentiment | Open sources with explicit time/license; otherwise mark unavailable | event-based | Not acquired | No undated daily sentiment retrofitted to past observations; no paywalled article dumps; no sentiment generated from future-known headlines. |
| Uploaded project literature | NIFTY prediction paper and prior-market manuscripts stored in project Library | Project Files search/read | Static documents | Partially reviewed, see literature review | Prior research refers to different repository paths and experiments; not treated as an existing dataset for this repository. |

## Missingness and composite policy

- Never make synthetic prices or labels to bridge gaps.
- Report missing dates against NSE trading calendar if an official calendar is available; otherwise label the trading-day check approximate.
- Do not forward-fill the target series, OHLCV, options quote, FII/DII, VIX or price-like inputs. A stale macro observation may be carried forward only if the variable is defined as a last-known state and maximum staleness/publication lag are explicit.
- Composite auxiliary series only join when their units and definitions agree. Keep raw sources separately and generate a manifest of source and rows used in each final table.
- Use secondary data only as cross-check or fallback and never label a fallback as official. Compare overlap values and log discrepancies.
- Every raw dataset receives a SHA-256 hash, row count, min/max observation date, retriever version and retrieval timestamp. Every processed dataset records its input hash(es), code commit and transformation version.
- Vendor-license restrictions override convenience: licensed raw data may be kept as artifacts / cache per allowed terms but not published as public repository files if redistribution is prohibited.


## Actual acquisition results from Actions run #41 (2026-10-14)

Evidence: machine-generated reports from [Actions run #41](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38526229786), artifact ID 11876376800. The raw target/auxiliary files were not included in the artifact; hashes and coverage were retained in data_manifest.json. The workflow used a cached target plus the acquisition script's free external-data adapters.

### Primary target

| Series | Source | Rows | Coverage | SHA-256 | Validation |
|---|---|---:|---|---|---|
| NIFTY 50 daily OHLCV | Dhan daily API cache | 4,901 | 2007-01-02 to 2026-10-13 | b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050 | PASS; OHLC/date/hash checks passed; 20 weekend dates retained and flagged for exchange special-session verification |

The Dhan series was cross-checked against Yahoo Finance's NIFTY proxy over 4,679 overlapping dates. Median absolute close difference in the normalized source representation was 0.0001953 and maximum 0.0007813. The values were compared only; no row-by-row averaging or source substitution occurred.

### External daily features actually acquired

| Input feature family | Source/proxy | Rows | First–last date | Status / caveat |
|---|---|---:|---|---|
| U.S. large-cap equities | Yahoo Finance ^GSPC | 4,976 | 2007-01-03 to 2026-10-13 | PASS |
| Nasdaq | Yahoo Finance ^IXIC | 4,976 | 2007-01-03 to 2026-10-13 | PASS |
| Japan equities | Yahoo Finance ^N225 | 4,833 | 2007-01-04 to 2026-10-13 | PASS |
| Hong Kong equities | Yahoo Finance ^HSI | 4,870 | 2007-01-02 to 2026-10-13 | PASS |
| U.S. implied volatility proxy | Yahoo Finance ^VIX | 4,978 | 2007-01-03 to 2026-10-13 | PASS |
| India VIX proxy | Yahoo Finance ^INDIAVIX | 4,560 | 2008-03-03 to 2026-10-13 | PASS; Yahoo proxy, not official NSE source |
| U.S. 10-year yield proxy | Yahoo Finance ^TNX | 4,974 | 2007-01-03 to 2026-10-13 | PASS; yield index convention needs interpretation |
| USD/INR | Yahoo Finance INR=X | — | — | FAIL; 237 rows violated OHLC range checks; no file used |
| Gold futures | Yahoo Finance GC=F | — | — | FAIL; 149 rows violated OHLC range checks; no file used |
| WTI crude futures | Yahoo Finance CL=F | — | — | FAIL; non-positive OHLC values rejected by generic validation; no file used. The source can contain valid negative futures prices, so a dedicated price-change transformation must be preregistered before re-use. |

Global feature construction used only earlier-date auxiliary observations than the NIFTY forecast-origin date, conservatively avoiding same-date closes from other markets. Feature matrix output reported 4,901 rows and 106 columns. The technical-only model run reported COMPLETE with 278 experiment records / 72,253 out-of-sample prediction rows; global-augmented run reported COMPLETE with 210 experiment records / 64,413 out-of-sample prediction rows. Per-run CSVs were not included in artifact 11876376800 due an artifact-path defect; performance ranking is therefore pending the corrected run's artifacts.

### Not acquired in the run

Historical options chains / contract-level implied volatility, PCR, strike/expiry/OI time series; official historical FII/FPI and DII flows; breadth/advances-declines; point-in-time constituents and constituent corporate actions; timestamped news/sentiment; and official NSE historical India VIX were not confirmed as acquired. The sources are documented above as candidates, but no feature-family effect is claimed. The community options datasets reviewed remain excluded pending license/provenance approval.

## Actual acquisition status

This document records sources researched, not sources successfully downloaded. The first data workflow run must populate a machine-readable manifest and update this section with actual outcomes, sample ranges, missing values and hashes. Until this happens, source availability remains unverified.
