# Results — ZigZag Expiry Direction

**Status: NOT YET TESTED. No performance results available.**

No ZigZag prediction sample has been reconstructed or scored in this run. Do not interpret the existing NWCP report as a result for this indicator. The study remains data-limited until the imported ZigLib implementation, pivot confirmation timing, price provenance and historical expiry schedule are verified.

Planned reporting: eligible sample size, abstention/coverage, class balance, confusion matrix, accuracy, balanced accuracy, UP/DOWN precision and recall, baseline comparisons, confidence intervals, regime breakdown, and sensitivity checks.


## Timeframe sensitivity update — 2026-10-25
User authorized testing multiple chart timeframes. The pre-registered panel is 5m, 15m, 30m, 60m and 1-day; 1m is conditional on validated data completeness. No timeframe has yet been scored. This file remains a result ledger, not an estimate of accuracy. Current status: DATA-LIMITED / NO PERFORMANCE CLAIM.


## Data acquisition pipeline added; results still pending
Dhan acquisition and validation scripts have been committed, with a GitHub Actions workflow configured to fetch/cache 1m, 5m, 15m, 60m and daily NIFTY 50 index bars and derive 30m bars from contiguous 5m data. The workflow has not yet been confirmed successful and no resulting data artifact has been inspected. **No empirical predictions or accuracy metrics exist yet.** Exact ZigLib causality remains a separate blocker.


## Execution-verification note
The acquisition workflow and validation scripts are committed, but this session could not confirm a successful run or inspect a resulting artifact. A local clone/syntax-check attempt failed because github.com could not be resolved. Thus data status remains unverified and there are no prediction metrics or conclusions.


## CI test coverage added — execution unverified
Added tests for Dhan response parsing, timestamp conversion, OHLC validation, 30-minute aggregation, and incomplete-bar exclusion; wired them into the acquisition workflow. They have not been confirmed passing in a GitHub Actions run. No empirical forecasts or accuracy metrics are available.


## 2026-10-25 failed acquisition run
The first observed run did not produce datasets. The Actions screenshot shows cache-key validation failure, followed by missing required 5m/15m/60m/daily files and no 30m derivation. This is pipeline failure evidence, not market evidence; no predictions were scored. A cache-key correction was committed (`907e05fc8de0363aecf9fa8e7790c9b63b683b9f`); awaiting rerun confirmation.


## 2026-10-25 verified CI outcome — run #40126339052
Pipeline unit tests passed; cache restore passed. Dhan returned HTTP 401 `DH-901` for all requested intraday intervals and daily history, stating the client ID or user-generated access token is invalid or expired. No usable candles were acquired; the tiny artifact contains only reports. No predictions were scored. The next dependency is a valid `DHAN_ACCESS_TOKEN` repository secret followed by a successful acquisition rerun.


## 2026-10-25 — successful authenticated acquisition and validation

GitHub Actions run [#40127255063](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063) completed successfully. Six pipeline unit tests passed; the workflow generated a fresh Dhan token from configured secrets and validated it against the profile endpoint; the data acquisition step succeeded; validation and 30-minute resampling succeeded; and the artifact/cache were saved. Artifact: [download data artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063/artifacts/12573423696). Artifact size is approximately 11.7 MB.

This establishes that the acquisition pipeline ran successfully, not that the ZigZag prediction experiment has been scored. No accuracy/balanced-accuracy estimates or performance conclusions are available yet. The exact imported ZigLib implementation and its causal signal-availability semantics remain unverified; the expiry calendar/target table and a source-faithful signal export must be resolved before the evaluator can produce scientifically defensible results. Current decision remains **DATA ACQUIRED / PREDICTION NOT YET EVALUATED**.


## 2026-10-25 — Raw 1-minute artifact audit

The successful data artifact was inspected directly. Its 1-minute CSV contains 511,268 rows. Timestamp strings are sorted and unique, but the file contains 2,636 weekend-dated rows, 47,612 timestamps outside 09:15–15:29 IST, and 12 OHLC-inconsistent rows. Exact 10:00 rows occur on 1,236 dates. These observations identify a data-cleaning and session-completeness task; they do **not** constitute prediction results. The raw file must remain unchanged, with regular-session and valid-OHLC derived files produced separately and independently checked. No forecasts have been scored.


## Verified acquisition and diagnostic audit — 2026-10-25
Successful workflow [#40128335927](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40128335927) uploaded [artifact #12574310370](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40128335927/artifacts/12574310370). Tests, Dhan authentication, acquisition, timeframe validation, 30m resampling, and diagnostic audit all passed. Dataset counts: 1m 511,268; 5m 92,795; 15m 30,985; 30m 14,814; 60m 8,663; daily 1,240. The raw audit found 12/5/3/0/2/0 OHLC findings respectively, with weekend and broad-clock flags detailed in reports/zigzag_session_audit.json inside the artifact. The audit decision remains NOT_ELIGIBLE_FOR_SCORING_UNTIL_OFFICIAL_SESSION_CALENDAR_AND_DHAN_TIMESTAMP_CONVENTION_ARE_VERIFIED. **No predictions have been scored and no accuracy claim is available.**


## 2026-10-25 — Independent local diagnostics of public 5-minute archive

Downloaded and inspected workflow artifact 12575426805. Preliminary diagnostic counts: 92,876 rows; 1,244 dates; zero duplicate timestamps; sorted timestamps; zero OHLC-invalid rows. 1,236 dates contain 75 rows (09:15 through 15:25). Six dates fall on weekends and 48 rows are outside the regular session clock window; these are flagged for classification, not silently removed. The public archive ends 2026-04-21, whereas the Yahoo fallback begins later, so current artifacts have zero common timestamps and do not provide an overlap price-parity check.

A reusable report generator, `research/zigzag-expiry-direction/audit_public_5m.py`, was added to the workflow. **These are data diagnostics only, not prediction results. No ZigZag forecast has been scored, and no accuracy or predictive-value claim is available.**
