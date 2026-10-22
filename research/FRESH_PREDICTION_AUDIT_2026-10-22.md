# Fresh NIFTY prediction audit — 2026-10-22

## Finding
Workflow [#39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966) completed at workflow level, but its 291,886-row `predictions.csv` contained 798 rows with null `target_date` while actual, prediction and baseline values were populated. Breakdown: volatility h5=60, h20=360; volatility-expansion h5=54, h20=324. The multi-session target builder skipped missing future returns at the data boundary, allowing partial future windows.

## Correction and current gate
Correction commit `e8133a582cbe6c06ce46514f871d1393fc142f6f` on [developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-developer) uses `skipna=False` and adds tail-window tests. Corrective [workflow #39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) was in progress at the last check. The [independent tester branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-independent-tester) records the defect and requires review of the corrected artifact before final sign-off.

## Numerically reproduced prior h1 result
The selected global ExtraTrees one-session volatility-proxy cell has n=981 and no missing target dates. Recomputed mean QLIKE loss difference (model minus baseline) −0.31559705, HAC p=1.74758e−9, block-bootstrap 95% CI [−0.42298094, −0.21014542], and Holm p=4.26410e−7 over 299 comparisons match the saved artifact formulas. This remains a replication candidate, not evidence of a trading edge. Return/direction forecasting has not demonstrated a robust edge.

## Independent-period limitation
Current new data are insufficient for a meaningful untouched future-period replication. Historical folds that informed model screening will not be described as independent. Record replication as future work. Options P&L and strategy approval remain blocked.

## Finalization gate
Wait for the corrected workflow; verify tests, target-date completeness, model metrics, loss signs, CI/HAC, Holm family and manuscript consistency independently; then update all status records. Do not expand the frozen model catalogue.


## Additional artifact sensitivity — same-holdout temporal and distribution diagnostics

The selected global ExtraTrees h1 volatility-proxy result (n=981) was split into four equal-count chronological slices. The mean QLIKE loss difference stayed negative in each slice, with moving-block intervals and Holm-adjusted HAC tests across the four slices:

| Slice | Dates | n | Mean QLIKE loss difference | 95% block CI | HAC p | Holm p |
|---|---|---:|---:|---:|---:|---:|
| 1 | 2022-11-04–2023-11-01 | 246 | −0.2640 | [−0.4370, −0.1046] | 0.001492 | 0.003871 |
| 2 | 2023-11-02–2024-10-25 | 245 | −0.3516 | [−0.5893, −0.0959] | 0.006660 | 0.006660 |
| 3 | 2024-10-28–2025-10-21 | 245 | −0.2770 | [−0.4582, −0.1261] | 0.000793 | 0.003174 |
| 4 | 2025-10-23–2026-10-19 | 245 | −0.3700 | [−0.6041, −0.1589] | 0.001290 | 0.003871 |

**Material qualification:** 50.97% of the daily model-minus-baseline loss differences are positive (higher model loss) and the median is +0.00662, while the mean remains −0.31560. A 10% winsorized mean is −0.10137. This indicates an average-score advantage with a skewed loss-differential distribution, not universal daily superiority. This is a post hoc partition of the same final holdout, not independent-period replication.

Reproducible artifact utility: [`research/audits/audit_nifty_predictions.py`](audits/audit_nifty_predictions.py). Example after extracting a workflow artifact: `python research/audits/audit_nifty_predictions.py predictions.csv --metrics metrics.csv --output audit.json`.


## QLIKE interpretation caveat — 2026-10-22

The pipeline trains the h1 volatility model on absolute next-session log return and then squares the target, forecast and baseline before applying QLIKE. This makes the scored realized quantity (r_{t+1}^2), but the model forecast is the square of a fitted absolute-return estimate, not a separately trained conditional-variance estimate. Therefore the reported improvement is metric-specific evidence for a variance-scaled volatility proxy; it should not be described as a fully calibrated conditional-variance forecast without additional validation.
