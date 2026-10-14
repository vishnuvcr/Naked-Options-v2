# Expanded NIFTY 50 model catalogue — run 56 results

**Date:** 2026-10-14  
**Workflow:** [NIFTY prediction research run #56](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38585954777)  
**Branch/commit:** `research/pdf-method-audit` / `cdf8bab26d9234a6312b1ae00a3f35370574c792`  
**Status:** Workflow PASS; scientific inference remains provisional pending independent audit. Prediction only; no trading-strategy conclusion.

## Data and execution

- Dhan daily NIFTY target: 4,901 rows, 2007-01-02 through 2026-10-13; SHA-256 `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050`.
- Yahoo NIFTY overlap: 4,679 rows; median absolute close difference 0.0001953 and maximum 0.0007813 in source units.
- Target validation and feature-matrix construction passed. Twenty weekend-dated rows were retained and flagged for exchange-calendar/source verification.
- S&P 500, Nasdaq, Nikkei 225, Hang Seng, CBOE VIX, India VIX proxy and US 10-year yield proxy passed the configured source validator. USD/INR, gold and WTI were rejected by OHLC checks; NSE endpoint returned no recognized rows.
- Technical catalogue: 632 experiment cells and 244,839 out-of-sample predictions reported complete. Global-augmented catalogue and ARIMA benchmark completed. Empty model-error CSVs were handled by the report merger. Artifact: `nifty-prediction-reports-38585954777.zip`, artifact SHA-256 `02a222453c7ac4e21e82253f407893e1943da0d5e6fec874750a350ba11aceb2`.

## Selected OOS metrics from merged report

Values below are descriptive model rows, not a declaration of a winning model. The model table includes technical-only and global-augmented feature sets; comparisons are across a single chronological holdout and are vulnerable to residual non-stationarity and selection uncertainty.

| Target / horizon | Best displayed row by task metric | OOS result | Statistical interpretation |
|---|---|---|---|
| Return, 1 session | CNN regression (technical) | MAE 0.005770; RMSE 0.007940; MSE skill +0.0875% vs baseline | p=.790; Holm p=1.000; no evidence of return skill |
| Return, 5 sessions | XGBoost (technical) | MAE 0.013527; RMSE 0.017352; MSE skill +2.0023% | p=.0967; Holm p=1.000; not significant |
| Return, 20 sessions | Gradient boosting (global) | MAE 0.026134; RMSE 0.033100; MSE skill +3.3303% | p=.4452; Holm p=1.000; not significant |
| Direction, 1 session | CatBoost (global) | Accuracy 54.29%; balanced accuracy 53.35% | Holm p=1.000 for this row; direction evidence mixed |
| Direction, 5 sessions | SVM / AdaBoost (technical) | Accuracy 53.38%; balanced accuracy 50.00% | No robust balanced-accuracy evidence; Holm p=1.000 |
| Direction, 20 sessions | SVM (technical) | Accuracy 59.73%; balanced accuracy 51.47% | Class imbalance explains much of apparent accuracy; Holm p=1.000 |
| Volatility, 1 session | XGBoost (global) | MAE 0.003950; RMSE 0.005280; QLIKE -8.7674 vs baseline -8.4312 | QLIKE improved descriptively; the exported QLIKE-skill field is NaN and needs code-level review |
| Volatility expansion, 20 sessions | Logistic (technical) | Accuracy 66.09%; balanced accuracy 66.24%; log loss 0.6194 vs baseline 0.6933 | Holm p=.04147 as emitted; exploratory until independent tester validates hypothesis family and test implementation |

ARIMA(1,0,0) return benchmark: at 1/5/20 sessions RMSE was 0.007957/0.017518/0.033486, with MSE skill vs configured baseline -0.3482%/+0.1095%/+1.0657%. Its p-values were .4917/.9351/.8420 and all displayed Holm values were 1.0. These figures do not establish ARIMA superiority.

## Defects and interpretation gates

1. **Sequence epoch metadata mismatch:** run metadata reports `epochs: 8`, whereas the frozen audit protocol and prior code note specified a three-epoch CPU budget. Verify actual fit calls/configuration before claiming the protocol was followed. Treat this as an unresolved audit finding.
2. **QLIKE skill export:** `qlike_skill_vs_baseline` is NaN across the inspected merged rows even where QLIKE and baseline QLIKE are finite. Do not use the skill field; fix or explain its calculation and add a regression test before final statistical sign-off.
3. **Statistical family:** a few adjusted p-values are below .05 (e.g., direction/hist-gradient at 1 session and technical logistic volatility expansion at 20 sessions). Independent tester must inspect the loss definition, pairing, dependence correction, and exact Holm family before these can be interpreted as confirmatory.
4. **Data limitations:** global sources are not fully holiday/close-time aligned; weekend target observations require calendar review. No verified historical options, FII/DII, PCR, market breadth, point-in-time news or corporate-action dataset was included. USD/INR, gold and crude failed validation.
5. **Scope coverage:** BERT/news sentiment, self-organizing fuzzy neural networks, deep belief networks, wavelet preprocessing and paper-specific feature-selection protocols remain blocked/not reproduced. This is a method-screening audit, not exact replication of every uploaded paper.
6. **No strategy inference:** these forecasts are not trading P&L. No options execution, Paytm Money brokerage, spread, taxes, slippage, liquidity or margin analysis is part of this prediction-only run.

## Provisional conclusion

The corrected workflow completed and supports a broad empirical screening, but it does **not** yet support a single best forecasting model. One-session return errors are similar across model families and adjusted evidence is weak; direction results vary with horizon and class balance. Some volatility/volatility-expansion rows are promising descriptively but have unresolved output and inference checks. The study should close with a qualified “no robust return/direction winner established” conclusion unless the independent tester finds a reproducible issue requiring one bounded correction.

## Required independent review

- Recompute headline metrics directly from predictions, including target/horizon alignment and baseline construction.
- Verify QLIKE and QLIKE skill signs/formulae, missing-value propagation and confidence intervals.
- Inspect all p-value/Holm families and dependence correction; reproduce the rows with adjusted p below .05.
- Reconcile declared versus actual sequence epochs and any compute-budget exclusions.
- Review weekend sessions and global-market timestamp alignment.
- Submit a concise PASS / PASS WITH LIMITATIONS / FAIL report; no parameter search loops.


## Corrected bounded run — run #60

**Workflow:** [run #60](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38593936036)  
**Branch/commit:** `research/pdf-audit-developer` / `e93fe35d8bb11df65d1c466434d5401298c077ed`  
**Artifact:** `nifty-prediction-reports-38593936036.zip`; artifact SHA-256 `b601320f64ab8ec0c62f0a07e458287cba781eca73107f1b2c38beda140a8151`.  
**Workflow disposition:** all research and artifact steps succeeded. This is result acquisition, not independent sign-off.

### Run-level accounting

- Validated Dhan NIFTY series: 4,901 rows (2007-01-02–2026-10-13), SHA-256 `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050`; 20 weekend-dated observations remain flagged for exchange-calendar/source verification.
- The merged metric table contains 1,097 rows: 485 OOS-evaluated rows, 482 model-selection/status rows, and 130 explicit `BLOCKED_COMPUTE_BUDGET` rows. The two per-run model error CSVs are empty (no recorded model fit/runtime failures). The artifact contains 244,839 prediction rows across the technical/global catalogues plus a separate ARIMA prediction file; global metadata reports 462 catalogue cells and technical metadata reports 632 catalogue cells.
- Sequence estimators ran in the technical-only catalogue for one-session return and direction under the three-epoch budget; other sequence target/horizon cells were deliberately blocked. Corrected metadata records three epochs.
- The QLIKE export now records score improvement as baseline mean score minus model mean score, rather than a ratio of potentially negative means.

### Headline results, interpreted conservatively

| Target / horizon | Best descriptive error row in run #60 | Benchmark comparison / inference |
|---|---|---|
| Return, 1 session | CNN sequence, technical: MAE 0.005770; RMSE 0.007940; MSE skill +0.0875% | p=.7901; Holm p=1.0. No evidence of useful return skill. |
| Return, 5 sessions | XGBoost, technical: MAE 0.013527; RMSE 0.017352; MSE skill +2.0023% | p=.0967; Holm p=1.0. Not statistically supported. |
| Return, 20 sessions | Gradient boosting, global: MAE 0.026134; RMSE 0.033100; MSE skill +3.3303% | p=.4452; Holm p=1.0. Not statistically supported. |
| Direction, 1 session | The highest accuracy is not treated as a winner; many classifier probabilities underperform prevalence log-loss/Brier baselines | Report accuracy together with balanced accuracy and proper scoring rules; no directional edge is established by this screening. |
| Direction, 5/20 sessions | Several high-accuracy rows have poor recall/balanced accuracy or poor log loss, consistent with threshold/class-imbalance effects | Accuracy alone is insufficient; no robust directional winner established. |
| Volatility, 1 session | Ridge technical has MAE 0.003627; XGBoost global has RMSE 0.005280 and QLIKE -8.7674 vs baseline -8.4312 | Error rankings differ by metric. QLIKE improvement is +0.3362 for the XGBoost global row, but its interpretation needs independent formula and alignment review. |
| Volatility, 5 sessions | ElasticNet global: MAE 0.002381; RMSE 0.003724 | Some rows improve MSE or QLIKE descriptively, but adjusted paired-loss results are not uniformly significant. |
| Volatility, 20 sessions | KNN technical: MAE 0.001967; RMSE 0.002892 | Best MAE is not the same as best QLIKE; no single volatility winner is selected without metric-specific preregistration and independent validation. |
| Volatility expansion, 1/5/20 sessions | Classifier accuracy ranges depend strongly on horizon and threshold; several rows have high accuracy but weak/degenerate class recall | Exploratory only. Proper-score and class-balance checks take precedence over headline accuracy; no trading inference. |

### Statistical interpretation and known caveats

The workflow's paired-loss convention is `model loss - baseline loss`; negative mean loss difference favors the model, positive favors the baseline. A two-sided p-value tests difference from zero, not whether the model is better. Some highly significant rows are significantly worse than baseline. Thus p-values and Holm-adjusted p-values must always be interpreted alongside the sign of `mean_loss_diff`, benchmark-relative skill, confidence intervals and proper scores. The run is a broad screening over a single chronological holdout, not proof of generalization.

### Data/method limitations retained

Timestamped news/BERT sentiment, historical options chains/PCR, FII/DII, market breadth, verified USD/INR/gold/WTI series, corporate-action point-in-time features, and exact replication of several PDF-specific methods remain unavailable, rejected, or not implemented. Seven global/context series passed the configured validator, but full release-time/holiday alignment has not been independently established. No trading strategy, option P&L, Paytm Money brokerage, slippage, spread, taxes, margin or live execution was evaluated.

### Final research conclusion before independent audit

**No robust NIFTY 50 return or direction forecasting winner is established by this bounded run.** Some volatility metrics show descriptive improvement, but rankings differ by metric and the source/timing and statistical protocol limitations prevent confirmatory claims. Volatility-expansion results are exploratory. Preserve negative and blocked results; do not turn these forecasts into trading recommendations.

## Independent tester handoff checklist

The separate tester branch is created only after this completed result acquisition and documentation. Tester: independently recompute a stratified sample and the headline rows from the downloaded artifact; verify metric units and signs, `mean_loss_diff`, HAC lag choice, Holm family definitions, confidence intervals, target-date alignment, QLIKE calculations, class prevalence and probability calibration; inspect data calendar/global close timing; check manuscript claims against the run #60 artifact. Report PASS / PASS WITH LIMITATIONS / FAIL and return concrete defects to the developer branch. Do not expand the model universe or begin strategy work.


## Corrected bounded run — run #60

**Workflow:** [run #60](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38593936036)  
**Branch/commit:** `research/pdf-audit-developer` / `e93fe35d8bb11df65d1c466434d5401298c077ed`  
**Artifact:** `nifty-prediction-reports-38593936036.zip`; SHA-256 `b601320f64ab8ec0c62f0a07e458287cba781eca73107f1b2c38beda140a8151`.  
**Workflow disposition:** all research and artifact steps succeeded. Independent audit has not yet occurred.

### Run-level accounting

- Validated Dhan NIFTY series: 4,901 rows (2007-01-02–2026-10-13), SHA-256 `b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050`; 20 weekend-dated observations remain flagged for exchange-calendar/source verification.
- Merged metric table: 1,097 rows, including 485 OOS-evaluated rows, 482 selection/status rows and 130 `BLOCKED_COMPUTE_BUDGET` rows. Technical/global model-error CSVs were empty. Catalogue metadata reports 632 technical and 462 global cells. Sequence models ran for one-session return/direction under the three-epoch budget; other sequence cells were explicitly blocked.
- QLIKE improvement is now exported as baseline mean score minus model mean score, not as a ratio of potentially negative score means.

### Representative results

| Target / horizon | Descriptive row | Inference |
|---|---|---|
| Return, 1 session | CNN sequence, technical: MAE 0.005770; RMSE 0.007940; MSE skill +0.0875% | p=.7901; Holm p=1.0. No evidence of useful return skill. |
| Return, 5 sessions | XGBoost, technical: MAE 0.013527; RMSE 0.017352; MSE skill +2.0023% | p=.0967; Holm p=1.0. Not statistically supported. |
| Return, 20 sessions | Gradient boosting, global: MAE 0.026134; RMSE 0.033100; MSE skill +3.3303% | p=.4452; Holm p=1.0. Not statistically supported. |
| Volatility, 1 session | Ridge technical MAE 0.003627; XGBoost global RMSE 0.005280, QLIKE -8.7674 vs -8.4312 baseline | Error rankings differ by score; the XGBoost QLIKE improvement is +0.3362 descriptively. Needs independent formula/alignment review. |
| Volatility, 5 sessions | ElasticNet global MAE 0.002381; RMSE 0.003724 | Some descriptive MSE/QLIKE improvements, not uniformly significant after correction. |
| Volatility, 20 sessions | KNN technical MAE 0.001967; RMSE 0.002892 | Best MAE need not be best QLIKE; no universal volatility winner is declared. |
| Direction / volatility expansion | Accuracy varies with class prevalence and threshold; several rows have weak balanced accuracy or proper scores | Exploratory only; accuracy alone does not establish predictive skill. |

### Statistical interpretation

The paired-loss convention is `model loss - baseline loss`: negative mean loss difference favors the model; positive favors the baseline. A two-sided p-value tests whether the loss difference is zero, not whether the model is better. Some highly significant rows can therefore be significantly worse than baseline. Interpret p-values with the sign of `mean_loss_diff`, benchmark-relative skill, confidence intervals and proper scores. This is a broad screening on one chronological holdout, not proof of generalization.

### Data and method limitations

Timestamped news/BERT sentiment, historical options/PCR, FII/DII, breadth, verified USD/INR/gold/WTI, point-in-time corporate actions and several PDF-specific methods remain unavailable, rejected or unimplemented. Global-market release-time/holiday alignment has not been independently established. No trading strategy, option P&L, Paytm Money brokerage, slippage, spread, taxes, margin or live execution was evaluated.

### Conclusion before independent audit

**No robust NIFTY 50 return or direction forecasting winner is established.** Some volatility metrics improve descriptively, but rankings differ by score and require independent reproduction. Volatility-expansion results remain exploratory. Do not turn these results into trading recommendations.

## Independent tester handoff

Tester: recompute headline metrics from the run #60 artifact; verify metric units/signs, `mean_loss_diff`, HAC lag choice, Holm families, confidence intervals, target-date alignment, QLIKE, class prevalence and probability calibration; inspect weekend dates and global close timing; compare manuscript claims to artifact. Return PASS / PASS WITH LIMITATIONS / FAIL with concrete defects. Do not expand the model universe or begin strategy work.
