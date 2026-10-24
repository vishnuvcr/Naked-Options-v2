# Data and Label Protocol — NWCP-1.0

## Target and session grid

All times use Asia/Kolkata (IST). The target is built from actual historical weekly NIFTY 50 option expiry dates. Current NSE product documentation states weekly NIFTY 50 index options expire on Tuesday, shifted to the preceding trading day if Tuesday is a holiday. Historical conventions changed, so use official historical circulars/contract metadata rather than today's rule across all years.

For expiry dates E(i-1) and Ei, define Ai as the first regular trading session after E(i-1). Reference P0,i is the official NIFTY 50 spot index observation at 10:00 IST on Ai, using only observations available at that time. With bar data, confirm the timestamp convention and choose the last finalized one-minute bar ending no later than 10:00. Outcome P1,i is the final valid regular-session spot bar close on expiry date Ei. Target is UP, DOWN or TIE by source precision. Quarantine rows with missing target prices, unresolved source conflicts, ambiguous timestamps or unsupported special sessions; do not interpolate target prices.

## Primary source candidate: Dhan API

Use historical intraday NIFTY 50 index candles through the configured DHAN_ACCESS_TOKEN repository secret. Verify current authentication, endpoint, security ID, instrument and segment mapping before acquisition. Dhan documentation describes a one-minute intraday OHLC endpoint and a 90-day maximum request period; all requests must be chunked to fit the limit. Validate timestamp semantics empirically. See [Dhan Historical Data API](https://dhanhq.co/docs/v2/historical-data/).

The source adapter must:
- Never print tokens or request headers.
- Record endpoint/source, instrument ID, interval, start/end, status, timestamps, row count and response content hash.
- Retry at most three times with bounded timeout/backoff; halt after ten consecutive failures or no cache progress.
- Persist raw responses in the dedicated cache and generate a sanitized manifest.
- Audit missing bars, duplicate timestamps, monotonic ordering, trading-session coverage, OHLC invariants and implausible returns.

## Free-source cross-check and composite policy

Audit free alternatives rather than declaring data unavailable based on one failed provider:
- Official NSE index history, expiry circulars, holidays/sessions and India VIX.
- Public NIFTY intraday datasets in GitHub, Kaggle, Hugging Face or Zenodo after checking licenses and data provenance.
- Additional public sources found during literature/source search.

Potential public candidates include [technovusin/nifty50-historical-data](https://github.com/technovusin/nifty50-historical-data) and [gsidhu/nse-intraday-data](https://github.com/gsidhu/nse-intraday-data); neither is accepted as canonical until licensing, upstream lineage, timestamps, completeness and overlap checks pass.

Do not blindly average prices from sources. Select one canonical target source and use other sources to cross-check aligned timestamps. Build a composite only with deterministic source precedence or a documented discrepancy rule after overlap agreement checks. Quarantine discrepancies. Public availability does not establish redistribution rights.

## Feature cutoff

At the 10:00 forecast cutoff, every feature timestamp and information-publication time must be <= cutoff. Use global exchange timestamps and true close availability. FII/DII flows published after the session are not known at same-day 10:00. Daily option OI/IV is not eligible for same-day prediction unless its record provides verified point-in-time information.

For each feature store name/version, source fields, computation definition, max source timestamp, availability time, missingness/coverage, eligibility reason and deterministic tests. No full-sample imputation, scaling, feature selection or filtering. Learned preprocessing is fit only inside each training fold.

## Cache and data rights

Use data/cache/nifty_weekly_candle_prediction_v1/public/ for license-reviewed public bars; use reports/nifty_weekly_candle_prediction_v1/ for manifests and audit summaries. Do not persist raw Dhan rows in the shared cache of this public repository while data/cache/redistribution terms remain unverified; the workflow uses an ephemeral runner directory for Dhan rows and publishes only sanitized aggregates. Actions should restore/save the reusable public cache and upload sanitized reports. Commit raw data only when terms permit; otherwise commit hashes/manifests and publish only license-safe derived outputs. Never put secrets or licensed raw market-data rows on GitHub Pages.
