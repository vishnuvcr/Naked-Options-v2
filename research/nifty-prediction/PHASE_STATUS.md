# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25 (new hypothesis tranche implemented; automated run pending verification)

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Daily-source provenance | COMPLETE WITH LIMITATION | 4,686 daily rows, 2007-09-17 to 2026-10-23. Yahoo and public parquet mirror OHLC match exactly but neither is exchange-certified. |
| P1 Daily next-session baseline | COMPLETE | Existing chronological benchmark completed. |
| P2 Daily baseline statistics | COMPLETE FOR INITIAL BENCHMARK | Previous-session direction achieved 54.19% accuracy / 54.10% balanced accuracy on the existing daily holdout. No ML model established improvement. |
| P3 Daily candidate rules | COMPUTED; EXPLORATORY | Candidate-rule JSON persisted; none establishes a trading edge. |
| P4 Volatility and optional libraries | COMPUTED WITH LIMITATIONS | GARCH QLIKE comparison persisted; MAPIE skipped due API mismatch; PySR and tick not fitted. |
| P5 Weekly-expiry direction | COMPLETED; NO CLEAR EDGE | Run #6 succeeded; 923 examples, chronological 692/231 split; balanced accuracy near 50%. Approximate expiry calendar remains a limitation. |
| P6 New OHLC hypothesis tranche | IMPLEMENTED; AUTOMATED RUN PENDING | Added [new hypothesis runner](evaluate_new_hypotheses.py) and [automatic/manual workflow](../../.github/workflows/nifty-new-hypotheses.yml). Tests volatility-regime specialists, feature ablation, 1/3/5-session targets, and calibration-threshold selective prediction. |
| P7 External-data hypotheses | BLOCKED ON POINT-IN-TIME INPUTS | Global lead-lag, constituent breadth, options-implied expectations, opening pressure and event-aware models are explicitly marked blocked in the report until archived timestamped data exists. Residual correction is deferred pending a leakage-safe out-of-fold residual protocol. |
| P8 Final synthesis | IN PROGRESS | Incorporate new hypothesis results after workflow completes; do not promote a winner from the reused screening test. |

## Current decision

Do not infer an edge from the earlier daily or weekly-expiry experiments. The new OHLC-only tranche is a bounded screening experiment, not a final confirmation. External-data ideas must not be fabricated from current snapshots. Any candidate requires repeatable chronological improvement and separate confirmation before strategy evaluation; execution costs apply if a later candidate survives prediction testing.