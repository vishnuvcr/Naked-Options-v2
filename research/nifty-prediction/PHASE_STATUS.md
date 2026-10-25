# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25 (NSE source smoke test run; semantic parser correction required)

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Daily-source provenance | COMPLETE WITH LIMITATION | 4,686 daily rows, 2007-09-17 to 2026-10-23. Yahoo and public parquet mirror OHLC match exactly but neither is exchange-certified. |
| P1 Daily next-session baseline | COMPLETE | Existing chronological benchmark completed. |
| P2 Daily baseline statistics | COMPLETE FOR INITIAL BENCHMARK | Previous-session direction achieved 54.19% accuracy / 54.10% balanced accuracy on the existing daily holdout. No ML model established improvement. |
| P3 Daily candidate rules | COMPUTED; EXPLORATORY | Candidate-rule JSON persisted; none establishes a trading edge. |
| P4 Volatility and optional libraries | COMPUTED WITH LIMITATIONS | GARCH QLIKE comparison persisted; MAPIE skipped due API mismatch; PySR and tick not fitted. |
| P5 Weekly-expiry direction | COMPLETED; NO CLEAR EDGE | Run #6 succeeded; 923 examples, chronological 692/231 split; balanced accuracy near 50%. Approximate expiry calendar remains a limitation. |
| P6 New OHLC hypothesis tranche | COMPLETED; NO CLEAR EDGE | Workflow [#40146027941](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40146027941) succeeded. Full-feature logistic regression: 53.79% accuracy / 53.67% balanced accuracy; volatility specialists: 53.01% / 52.60%; OHLC core ablation: 51.38% / 51.01%. One-, three-, and five-session balanced accuracy: 52.58%, 48.03%, 48.02%. Selective prediction covered 15.06% at 53.37% balanced accuracy. Results are screening-only and not untouched confirmation. |
| P7 External-data hypotheses | SOURCE SMOKE TEST; SEMANTIC VALIDATION PENDING | Workflow [#40162669263](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40162669263) downloaded three official NSE ZIPs (legacy 2024-07-05, UDiFF 2024-07-08, and 2026-10-23). CSV parsing succeeded, but the first parser missed UDiFF aliases and did not establish NIFTY option-row validity; see NP-022. Correct parser and verify sample rows before data use. |
| P8 Final synthesis | IN PROGRESS; EVIDENCE SYNTHESIZED | Persisted OHLC hypothesis report and updated manuscript. No strategy is authorized; external-data hypotheses remain blocked and the reused screening test requires fresh confirmation. |

## Current decision

Do not infer an edge from the earlier daily or weekly-expiry experiments. The new OHLC-only tranche is a bounded screening experiment, not a final confirmation. The corrected workflow passed after fixing a training-label alignment error; see NP-020 in the error log. Free historical source candidates are identified, but data must be ingested, hashed, coverage-audited and sample-validated before use. External-data ideas must not be fabricated from current snapshots. Any candidate requires repeatable chronological improvement and separate confirmation before strategy evaluation; execution costs apply if a later candidate survives prediction testing.
| P6b Weekly-expiry hypothesis suite | SCREENING RUN COMPLETE; NO CONFIRMED EDGE | [Workflow #40163121234](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40163121234). Regime specialists: 54.18% balanced accuracy; logistic: 52.69%; gradient boosting: 49.11%; selective output: 9.1% coverage and 35.0% balanced accuracy; residual correction: 50.0%; 3-expiry horizon: 53.26%. Same reused test block and approximate expiry dates; not confirmatory. External data families remain blocked. |
