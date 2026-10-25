# Free historical data assessment for follow-up NIFTY prediction hypotheses

Updated: 2026-10-25

## Findings

- Official NSE derivatives reports list daily UDiFF F&O bhavcopy, settlement prices, volatility, participant-wise open interest, and FII derivatives statistics. The legacy F&O bhavcopy format was replaced on 2024-07-08. These are promising for end-of-day contract-level features, but daily bhavcopy is not a timestamped intraday option-chain snapshot.
  - [NSE derivatives reports](https://www.nseindia.com/all-reports-derivatives)
  - [NSE historical reports](https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives)
  - [SEBI derivatives source index](https://www.sebi.gov.in/curation/equity_derivatives.html)
- A third-party [NSE F&O Data Bank](https://github.com/SantoshSrinivas79/NSE-FNO-Data-bank) reports 1,579 validated daily archives from 2020-04-13 through 2026-08-31. Verify exact files, hashes, schemas, and samples against official NSE downloads before accepting it.
- The [Hugging Face NSE Options Historical Data dataset](https://huggingface.co/datasets/rissin/nse-options-intraday) advertises daily index-option history from 2001 and 1-minute data from 2024 onward. This is a coverage candidate, not accepted ground truth; inspect provenance, licensing, files and cross-source agreement.
- Official NSE pages list historical index data, India VIX, advances/declines, and FII/DII activity: [historical reports](https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives), [all reports](https://www.nseindia.com/all-reports), and [Nifty Indices reports](https://www.niftyindices.com/reports).
- Current option-chain pages are not equivalent to archival point-in-time data. Confirm terms before any aggregation or bulk copying.

## Decision and next bounded step

Status: **FREE SOURCES IDENTIFIED; INGESTION AND VALIDATION NOT COMPLETE**.

First ingest a limited reproducible sample of daily F&O bhavcopies and corresponding index, India VIX, advances/declines and FII/DII reports. Preserve raw files, retrieval date, hashes, schema versions, coverage and missingness. Reconcile the pre-/post-2024-07-08 format change and validate sample records against official NSE downloads.

Only use features available at the forecast timestamp. EOD bhavcopy may support next-session forecasts after publication; it cannot support intraday opening-pressure predictions. Intraday option snapshots, global lead-lag, breadth and event-aware tests remain blocked until appropriate point-in-time history is acquired and audited.

No model result is attributed to these sources yet. No strategy evaluation is authorized by this source assessment. If a prediction candidate later survives an untouched confirmation set, evaluate executable instruments with realistic Paytm Money brokerage, exchange charges, taxes, slippage, spread, lot sizing and turnover.

These public listings establish that source pages exist, not that every historical file is complete, independently validated, downloadable, or redistributable.
