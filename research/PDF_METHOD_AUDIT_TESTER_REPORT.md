# Independent tester report — expanded PDF-method audit run #56

**Review date:** 2026-10-14  
**Workflow:** [run #56](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38585954777)  
**Tested commit:** `cdf8bab26d9234a6312b1ae00a3f35370574c792`  
**Disposition:** **PASS WITH LIMITATIONS for workflow/data screening; statistical sign-off withheld pending bounded developer correction.**

## Independent checks performed

1. Confirmed workflow #56 completed successfully: validation, target/scoring tests, feature matrix, technical/global catalogues, ARIMA, result merge, run-status summary and artifact upload all completed.
2. Inspected the uploaded artifact and cross-checked the manifest: 4,901 Dhan NIFTY daily observations, 2007-01-02 through 2026-10-13, target SHA-256 `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050`.
3. Confirmed source manifest flags seven external series as passing and rejects USD/INR, gold and WTI; NSE endpoint parsing failed. Weekend-dated observations are preserved and flagged, not silently removed.
4. Recomputed headline interpretation from the merged metrics: one-session return RMSE is tightly clustered around 0.00794; top displayed return rows have Holm-adjusted p-values of 1.0. No robust return winner is supported by these rows. Direction and volatility-expansion outcomes vary by horizon; some adjusted p-values are below .05 and must be checked against their paired loss definition and exact Holm family.
5. Inspected the implementation rather than relying only on metadata. `SequenceEstimator` defaults to three epochs and `run_experiments.py` sets all sequence estimators to `epochs=3`; however, the status JSON hard-codes `"epochs": 8`. This is a metadata defect, not evidence that the training loop used eight epochs.
6. Inspected the volatility scoring formula: `qlike = log(pv) + actual_variance / pv`; the model and baseline QLIKE means are negative in the exported rows. The current skill formula `1 - mean(qlike_model)/mean(qlike_baseline)` is mathematically misleading for a score that can be negative, and the code guard emits null/NaN whenever the baseline mean is not positive. Compare the paired score difference (baseline QLIKE minus model QLIKE) with an interval/test instead; do not ratio-normalize negative QLIKE scores.

## Required developer corrections

- Change the sequence status metadata to report the actual configured three epochs; add a test so metadata cannot diverge from estimator configuration.
- Replace or remove the QLIKE ratio-skill field. Prefer an explicitly named score improvement `qlike_improvement_vs_baseline = mean(qlike_baseline - qlike_model)`; positive means the model score is lower/better. Keep the paired loss difference and uncertainty tests, and add formula/sign tests for negative score values.
- Re-run the bounded workflow once after the changes. Do not retune hyperparameters or broaden the catalogue.
- Independently validate the p-value/Holm implementation for the rows below .05, including the direction and volatility-expansion families. Keep all results exploratory unless the family definition and loss metric are confirmed.
- Add a short report in the developer branch, update README/results/error log/phase status and link the rerun artifact.

## Limitations that remain even after these corrections

- USD/INR, gold and crude oil were not admitted; the NSE endpoint did not yield recognized rows.
- Global market close-time/holiday alignment and weekend-session dates still require verification.
- Historical option chains, FII/DII, PCR, breadth, point-in-time news and corporate actions were not acquired in this run.
- BERT/news sentiment, self-organizing fuzzy neural networks, deep belief networks, wavelet preprocessing and paper-specific feature-selection procedures were not reproduced.
- A single chronological holdout and a bounded catalogue do not prove stable forecasting skill. This is a forecasting-method screening only, not a trading strategy or P&L test.

## Tester conclusion

The workflow fix is verified and the run is reproducible at artifact level, but the result export has a QLIKE skill formula/field defect and an epoch-metadata defect. The actual sequence training configuration appears to remain at three epochs. The developer should perform the two small corrections and one bounded rerun; then the tester can issue a final disposition. No best model or trading strategy is approved.

**Developer → Tester instruction:** after the single corrective rerun, recompute the affected QLIKE summaries and inspect p-value/Holm families before closing the research gate.
