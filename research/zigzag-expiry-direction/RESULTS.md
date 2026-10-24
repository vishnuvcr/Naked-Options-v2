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
