# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25 (new OHLC hypothesis workflow verified successfully)

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Daily-source provenance | COMPLETE WITH LIMITATION | 4,686 daily rows, 2007-09-17 to 2026-10-23. Yahoo and public parquet mirror OHLC match exactly but neither is exchange-certified. |
| P1 Daily next-session baseline | COMPLETE | Existing chronological benchmark completed. |
| P2 Daily baseline statistics | COMPLETE FOR INITIAL BENCHMARK | Previous-session direction achieved 54.19% accuracy / 54.10% balanced accuracy on the existing daily holdout. No ML model established improvement. |
| P3 Daily candidate rules | COMPUTED; EXPLORATORY | Candidate-rule JSON persisted; none establishes a trading edge. |
| P4 Volatility and optional libraries | COMPUTED WITH LIMITATIONS | GARCH QLIKE comparison persisted; MAPIE skipped due API mismatch; PySR and tick not fitted. |
| P5 Weekly-expiry direction | COMPLETED; NO CLEAR EDGE | Run #6 succeeded; 923 examples, chronological 692/231 split; balanced accuracy near 50%. Approximate expiry calendar remains a limitation. |
| P6 New OHLC hypothesis tranche | COMPLETED; NO CLEAR EDGE | Workflow [#40146027941](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40146027941) succeeded. Full-feature logistic regression: 53.79% accuracy / 53.67% balanced accuracy; volatility specialists: 53.01% / 52.60%; OHLC core ablation: 51.38% / 51.01%. One-, three-, and five-session balanced accuracy: 52.58%, 48.03%, 48.02%. Selective prediction covered 15.06% at 53.37% balanced accuracy. Results are screening-only and not untouched confirmation. |
| P7 External-data hypotheses | BLOCKED ON POINT-IN-TIME INPUTS | Global lead-lag, constituent breadth, options-implied expectations, opening pressure and event-aware models are explicitly marked blocked in the report until archived timestamped data exists. Residual correction is deferred pending a leakage-safe out-of-fold residual protocol. |
| P8 Final synthesis | IN PROGRESS; EVIDENCE SYNTHESIZED | Persisted OHLC hypothesis report and updated manuscript. No strategy is authorized; external-data hypotheses remain blocked and the reused screening test requires fresh confirmation. |

## Current decision

Do not infer an edge from the earlier daily or weekly-expiry experiments. The new OHLC-only tranche is a bounded screening experiment, not a final confirmation. The corrected workflow passed after fixing a training-label alignment error; see NP-020 in the error log. External-data ideas must not be fabricated from current snapshots. Any candidate requires repeatable chronological improvement and separate confirmation before strategy evaluation; execution costs apply if a later candidate survives prediction testing.