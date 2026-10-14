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
