# NWCP-1.0 Data, Code and Source Catalogue

Review date: 24 October 2026. "Candidate" means not yet accepted for model inputs until the named audit passes. This list records source availability and limits without asserting that all endpoints are currently accessible from GitHub Actions.

## A. Target prices and session calendar

| Source | Candidate use | What is documented | Required check / decision |
|---|---|---|---|
| Dhan Historical Data API v2 | Primary 1-minute NIFTY 50 spot history, if credentialed access works | Official docs list POST /v2/charts/intraday, minute intervals including 1, an epoch timestamp field, and a maximum 90-day request window | Dynamically resolve NSE index/security ID from Dhan scrip master; check token success, instrument/segment and date coverage; compare exact overlapping bars with independent public data; empirically verify whether epoch is bar-start; never log token. Dhan data rows remain in an ephemeral action-runner folder until usage/redistribution terms are verified. |
| Dhan instrument master | Resolve current NIFTY 50 index ID | Official instrument-master files are documented by Dhan; use current daily master, not hard-coded ID | Require exactly one row matching index name, exchange and IDX_I / INDEX; record sanitized row identity/schema; fail closed on ambiguity. |
| NSE index historical data | Target cross-check / daily close check | NSE provides historical index data and official exchange sources | Confirm 10:00 and expiry-close target prices on overlap; check terms and download limits. Do not use current daily close to replace 10:00 spot. |
| NSE current NIFTY 50 F&O page | Current weekly contract convention | Current product page says weekly NIFTY 50 index options expire Tuesday, shifted to preceding trading day when Tuesday is a holiday | This rule is not applied to all historical samples: weekly expiry was Thursday until the 2025 change. |
| NSE circular NSE/FAOP/68747 (25 June 2025) | Regime boundary | Official circular changes NSE index weekly expiry from Thursday to Tuesday; first revised NIFTY weekly expiry is 2 September 2025, with old contracts on or before 31 August unchanged | Archive URL/document metadata and compare generated historical dates. Do not infer actual dates from a current weekday rule alone. |
| NSE trading holiday / session list | First session after previous actual expiry; special sessions | Exchange holiday/session calendars provide authoritative market-session dates | Audit holiday-adjusted expiry; include special sessions only under an explicit rule and only if target bars exist. |
| pandas_market_calendars NSE calendar | Fallback session-grid cross-check | Python calendar package supplies exchange-session schedules where supported | Not an authoritative options expiry calendar. Cross-check with NSE; log package version, date range and holidays; never silently call the inferred calendar "official". |

Official references: [Dhan Historical API](https://dhanhq.co/docs/v2/historical-data/), [Dhan instrument master](https://dhanhq.co/docs/v2/instruments/), [NSE NIFTY 50 F&O](https://www.nseindia.com/static/products-services/equity-derivatives-nifty50), [NSE contract specifications](https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications), [NSE data policy](https://www.nseindia.com/static/market-data/nse-data-policy).

## B. Candidate public 1-minute price histories

| Dataset / source | Available description | NWCP treatment |
|---|---|---|
| [technovusin/nifty50-historical-data](https://github.com/technovusin/nifty50-historical-data) | Repository documents 1-minute bars from April 2017, yearly CSVs for 2017–2025 and monthly files for 2026; times are IST, timestamps are candle starts; repository notes known gaps, frozen-price stretches, removed partial sessions and a handful of corrected OHLC rows. Repository shows a code license. | Primary free fallback / overlap reference only. Upstream market-data provenance and redistribution terms are not settled by a code license alone. Cache locally in Actions, audit all known quirks and exact timestamps. Never publish raw rows or per-week price labels to the Pages site. |
| [gsidhu/nse-intraday-data](https://github.com/gsidhu/nse-intraday-data) | Public historical intraday archive, structured by year/month/day/symbol; license file states MIT for repository. Exact NIFTY index completeness and upstream source lineage require checking. | Secondary cross-check, not canonical until instrument coverage and overlap accuracy are proven. |
| [sandeepkapri/Nifty50-Minute-Data](https://github.com/sandeepkapri/Nifty50-Minute-Data) | Describes NIFTY 50 minute history from 9 January 2015 to 27 March 2024; its README cites a third-party provider rather than a fully specified raw provenance. A repository license is shown. | Backup free source if the first dataset is insufficient; inspect actual file structure, timezone, missing sessions, duplicate epochs and rights. |
| [beingRajat/data-scraping](https://github.com/beingRajat/data-scraping) | Educational data-collection code for NIFTY 50 and other indices; documentation warns that market data may be incomplete, delayed or inaccurate and emphasizes provider terms. | Code could help source discovery, but its output is not historical truth unless actual date coverage and point-in-time provenance are validated. |
| Kaggle / Hugging Face / Zenodo / other GitHub archives | Additional free dataset candidates | Search and log them if first sources leave gaps. For each: record identifier/version, author, upload/update date, license, upstream lineage, timestamp basis, row count/gap rate, overlapping price error and whether redistribution is permitted. HF_TOKEN may be used in runner environment for bulk download, but the token must never be printed. Do not prioritize an unverified mirror merely because it is on Hugging Face. |

### Canonical-source and composite policy

Do not average price records from different vendors. Choose one canonical series only after bar alignment, timestamp, OHLC, missingness and overlap checks. If a second source only partly overlaps, use it for cross-validation. A composite may be admitted only through a deterministic, documented precedence rule supported by robust overlap agreement; conflicting rows are quarantined. All label rows must record source identity and provenance. Keep raw vendor data in private/ephemeral cache unless rights to commit or publish are confirmed.

## C. Features that are conditionally eligible

| Feature family | Candidate sources | Forecast-time restrictions |
|---|---|---|
| Price action / technical | Canonical 1-minute NIFTY spot OHLC; trailing daily bars | At forecast time 10:00 IST, use only finalized bars ending by 10:00 and complete prior sessions. No future windows, centered smoothing, negative offsets or final-bar values from the anchor day. |
| India VIX | NSE India VIX historical/index feed; verified public archives | Must have an observation known by cutoff. Do not assign the day’s close to a 10:00 forecast. Use only if timestamp/publication time and coverage are validated. |
| Option chain, OI, IV, PCR | Dhan/NSE/API data if licensed and historical point-in-time availability exists | Daily post-close snapshots cannot be used at 10:00 that same day. Per-minute OI/IV must represent true point-in-time values; otherwise exclude/lag. This study predicts index direction only and does not optimize option P&L. |
| FII/DII | NSE official data / other licensed sources | Daily values published after the session are not available at 10:00 that session; use prior-known publication only. |
| Global markets / GIFT NIFTY / FX / commodities | Validated vendor/public time series with exchange timestamps | Respect each venue's timezone and exact close/release times. Feature availability in India at cutoff is mandatory; no future New York close values. |
| News / sentiment | Timestamped news source, public archives or licensed feeds | Require original publication timestamp and collected/available-at timestamp. Revised stories and daily sentiment aggregates require care. Do not use future corpus metadata or model-generated sentiment from a later version without recording availability constraints. |
| Calendar/events | NSE holiday calendars, expiry circulars, scheduled economic announcements | Only information known at 10:00; record historical expiry regime and holiday shift. Actual unplanned news after cutoff cannot be a predictor. |

## D. Open-source Pine indicator candidates

See [PINE_INDICATOR_CATALOG.md](PINE_INDICATOR_CATALOG.md) for candidate-by-candidate notes.

- Donchian Channels [Gu5]: https://www.tradingview.com/script/Cc7xGmYO-Donchian-Channels-Gu5/
- Bollinger Bands: https://www.tradingview.com/script/ViWAOiIc-Bollinger-Bands/
- Better Bollinger Bands: https://www.tradingview.com/script/BP8qbzQm-Better-Bollinger-Bands/
- SuperTrend [everget]: https://www.tradingview.com/script/VLWVV7tH-SuperTrend-everget/
- Donchian Channels Strength: https://www.tradingview.com/script/hCfZsNU2-Donchian-Channels-Strength/
- Relative Channel Bandwidth: https://www.tradingview.com/script/MCmQBod1-Relative-Channel-Bandwidth/
- ADX and DI by MiG, https://www.tradingview.com/script/ZPS2KYg2/, is labelled protected source; do not copy it.

TradingView "open-source" visibility is not a blanket permissive source-code license. Do not rehost community source unless licence/House Rules make reuse clear. Independently implement documented formulas; record version, source URL, author, hash/retrieval date, Pine version, security/request lookahead, future shift, realtime/confirmed-bar behavior and formula regression tests.

## E. Method/source repositories

- [QuantEvolve paper](https://arxiv.org/abs/2510.18569) and [official repository](https://github.com/CiubancanC/QuantEvolve): the study describes multi-agent, hypothesis-driven evolutionary search and quality-diversity. Current NWCP runner implements a smaller constrained typed-rule evolutionary adaptation; it does not claim to execute the full original research system.
- [tarsyang/quantevolve](https://github.com/tarsyang/quantevolve): optional code alternative; license, lineage and execution model still require auditing.
- [TradingView repainting docs](https://www.tradingview.com/pine-script-docs/concepts/repainting/): required reading for any port.
- [TradingView strategy FAQ](https://www.tradingview.com/pine-script-docs/faq/strategies/): execution and historical/realtime calculation caveats.
- [Sullivan et al.](https://onlinelibrary.wiley.com/doi/full/10.1111/0022-1082.00163), [Probability of Backtest Overfitting](https://escholarship.org/uc/item/4w1110bb), and [Arian et al. 2024](https://doi.org/10.1016/j.knosys.2024.112477): methods sources for multiple testing and time-series validation.

## F. Acquisition acceptance checklist

For each source, report the following before accepting it:
- exact source identity, version, author, collection date and license/data-use note;
- coverage start/end, date count, bar count, timezone and candle-start/end convention;
- duplicate timestamp count, invalid OHLC count, session-coverage distribution, per-session missing-minute distribution and implausible return count;
- aligned timestamp agreement with reference source (median, p95, maximum absolute error, fraction within 1 point and 5 points);
- holiday/special-session/outage list, with each exclusion/repair explained;
- publication/availability timestamp for non-price predictors;
- local cache key, file hash, schema version and whether raw data may legally be committed/published;
- error/warning report even when acquisition fails.

No source is accepted just because it downloaded successfully. Target labels remain blocked until the anchor candle, expiry candle and actual expiry calendar pass their audits.
