# Developer corrective submission — run 56 audit

**Source review:** [independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester/research/PDF_METHOD_AUDIT_TESTER_REPORT.md)  
**Scope:** two bounded reporting corrections only; no model retuning.

## Corrections submitted

1. `scripts/run_experiments.py`: sequence status now reports three epochs, matching the actual `SequenceEstimator(epochs=3)` configuration and the frozen protocol.
2. `scripts/forecast_metrics.py`: added `qlike_metrics`, which returns model QLIKE, baseline QLIKE, and `qlike_improvement_vs_baseline = mean(baseline_score - model_score)`. This score difference is interpretable when score means are negative; ratio skill was removed.
3. `scripts/run_experiments.py`: uses the new QLIKE helper and retains paired per-observation QLIKE loss differences for HAC/block interval analysis.
4. `tests/test_qlike_metrics.py`: tests positive/negative improvement signs, negative QLIKE means, and empty finite overlap.

## Validation

A single bounded workflow run on this branch is the retest gate. Do not accept the correction until unit tests, target validation, both model catalogues, ARIMA, merge, and artifact generation finish. The tester should then independently inspect output columns and reproduce QLIKE score differences from prediction rows.

## Remaining non-code limitations

Rejected external sources, global close-time/calendar alignment, weekend-date review, unavailable option/FII-DII/PCR/breadth/news/corporate-action data, and non-reproduced paper methods remain limitations. No model is promoted as best and no trading strategy is proposed.

**Tester → Developer instruction:** review the corrected workflow artifact once; if the two formula/metadata gates pass, close with PASS WITH LIMITATIONS. If they fail, identify the exact failing assertion and request at most one targeted correction, not a parameter-search loop.
