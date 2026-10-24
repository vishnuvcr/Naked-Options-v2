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
