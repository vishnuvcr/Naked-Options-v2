# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25 (weekly-expiry track implemented; execution pending)

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Daily-source provenance | COMPLETE WITH LIMITATION | 4,686 daily rows, 2007-09-17 to 2026-10-23. Yahoo and public parquet mirror OHLC match exactly but neither is exchange-certified. |
| P1 Daily next-session baseline | COMPLETE | Existing chronological benchmark completed. |
| P2 Daily baseline statistics | COMPLETE FOR INITIAL BENCHMARK | Previous-session direction achieved 54.19% accuracy / 54.10% balanced accuracy on the existing daily holdout. No ML model established improvement. |
| P3 Daily candidate rules | COMPUTED; EXPLORATORY | Candidate-rule JSON persisted; none establishes a trading edge. |
| P4 Volatility and optional libraries | COMPUTED WITH LIMITATIONS | GARCH QLIKE comparison persisted; MAPIE skipped due API mismatch; PySR and tick not fitted. |
| P5 Weekly-expiry target implementation | IMPLEMENTED; RUN PENDING | Added [weekly-expiry experiment runner](evaluate_weekly_expiry.py), [protocol](WEEKLY_EXPIRY_DIRECTION_EXPERIMENTS.md), and [automated/manual workflow](../../.github/workflows/nifty-weekly-expiry.yml). It uses daily spot OHLC only. The expiry weekday rule (Thursday before 2025-09-01, Tuesday after) is based on NSE circular FAOP/68747 but the official holiday-adjusted contract calendar has not been ingested. |
| P6 Weekly-expiry model evaluation | PENDING RUN AND ARTIFACT REVIEW | Workflow must run successfully and persist reports/nifty-prediction/weekly_expiry_experiments.json. Inspect label dates, eligible sample size, baselines, metrics and failures before interpreting results. |
| P7 Point-in-time feature enrichment | BLOCKED ON HISTORICAL DATA AVAILABILITY | Options-chain, intraday, breadth, global markets, FII/DII, event/news data require timestamped historical inputs. Do not backfill current snapshots as if historical. |
| P8 Final synthesis | NOT READY | Update manuscript with results only after weekly-expiry workflow completes. No tester review or tester branch. |

## Current research decision

The earlier daily next-session study is not evidence for weekly-expiry prediction. The new weekly-expiry runner and workflow exist, but no weekly-expiry result is yet claimed. Current priority is execution and correction of the new bounded experiment, then adding feature families only where point-in-time data is genuinely available.
