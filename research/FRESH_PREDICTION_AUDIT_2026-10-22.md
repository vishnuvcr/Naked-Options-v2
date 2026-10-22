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
