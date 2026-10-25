# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25 (weekly-expiry experiment run #6 passed; no edge established)

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Daily-source provenance | COMPLETE WITH LIMITATION | 4,686 daily rows, 2007-09-17 to 2026-10-23. Yahoo and public parquet mirror OHLC match exactly but neither is exchange-certified. |
| P1 Daily next-session baseline | COMPLETE | Existing chronological benchmark completed. |
| P2 Daily baseline statistics | COMPLETE FOR INITIAL BENCHMARK | Previous-session direction achieved 54.19% accuracy / 54.10% balanced accuracy on the existing daily holdout. No ML model established improvement. |
| P3 Daily candidate rules | COMPUTED; EXPLORATORY | Candidate-rule JSON persisted; none establishes a trading edge. |
| P4 Volatility and optional libraries | COMPUTED WITH LIMITATIONS | GARCH QLIKE comparison persisted; MAPIE skipped due API mismatch; PySR and tick not fitted. |
| P5 Weekly-expiry target implementation | COMPLETE FOR EXPLORATORY SCREEN | Dedicated runner and three unit tests committed. Target is next observed weekly-expiry close vs previous observed weekly-expiry close. Calendar is approximate, not official holiday-adjusted. |
| P6 Weekly-expiry model evaluation | COMPLETED; NO CLEAR EDGE | [Workflow run #6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40145451144) succeeded and persisted [weekly-expiry report](../../reports/nifty-prediction/weekly_expiry_experiments.json). 923 examples; chronological split 692 train / 231 test. Majority accuracy 54.98%; previous expiry direction 50.65%; logistic regression 50.65%; random forest 50.22%; gradient boosting 52.81%. Balanced accuracy is near 50% for all; no predictive edge established. |
| P7 Point-in-time feature enrichment | BLOCKED ON HISTORICAL DATA AVAILABILITY | Options-chain, intraday, breadth, global markets, FII/DII, event/news data require timestamped historical inputs. Do not backfill current snapshots as if historical. |
| P8 Final synthesis | IN PROGRESS | Update manuscript and README with weekly results; retain no-edge conclusion and data/calendar caveats. |

## Current research decision

Weekly-expiry spot direction has now been tested on daily OHLC with a chronological holdout. None of the tested methods improves materially on the majority baseline; balanced accuracy is approximately 50%. This is not evidence of options-premium predictability or a tradable strategy. Do not proceed to live trading or cost-based strategy claims. Next useful work is to validate exact historical expiry dates and source provenance, then add only point-in-time features supported by real archived data; if those sources cannot be obtained, report that limitation rather than simulate missing history.