# Preliminary historical diagnostic — results

**Status:** Preliminary results computed; not the final benchmark.  
**Dataset:** Public third-party CSV mirror, 2000-01-03 to 2019-12-02. 4,954 raw rows; zero duplicate dates and zero basic OHLC invariant failures. Source is not exchange-certified and ends in 2019.

## Holdout design

Chronological 75/25 split after feature construction; 3,669 training rows and 1,224 test rows. Test dates: 2014-12-16 through 2019-11-29. Up-class share: 53.02%; two exact zero-return labels were assigned DOWN.

The logistic model is a custom Node.js gradient-descent implementation refit on expanding history every 20 test observations. It is not the scikit-learn model in the primary benchmark. Naive baselines are scored on the same test dates. Balanced-accuracy intervals use a circular block bootstrap (block length 10, 1,000 replicates).

## Results

| Model | Accuracy | Balanced accuracy | 95% block-bootstrap interval |
|---|---:|---:|---:|
| Majority-class baseline | 53.02% | 50.00% | [50.00%, 50.00%] |
| Previous-session direction | 52.78% | 52.60% | [49.72%, 55.56%] |
| Zero-return forecast (DOWN tie convention) | 46.98% | 50.00% | [50.00%, 50.00%] |
| Custom expanding logistic regression | 52.86% | 52.78% | [50.11%, 55.36%] |

Logistic Brier score: 0.2494. Log loss: 0.6919.

## Interpretation

The custom logistic diagnostic improves balanced accuracy by only about 0.18 percentage points over the previous-session-direction baseline. Their approximate bootstrap intervals overlap substantially. This does **not** establish a reliable predictive edge. The majority-class baseline has higher raw accuracy because the test set has more up than down sessions.

These are preliminary historical results only. The source ends in 2019; the logistic implementation differs from the committed scikit-learn pipeline; random forest and gradient boosting have not been scored in this diagnostic. No trading strategy, option profitability, or execution costs are evaluated.

## Reproducibility

- Data file: `data/cache/nifty-prediction/nifty50_daily.csv`
- Source manifest: `data/cache/nifty-prediction/source_manifest.json`
- Reproducible Node diagnostic: `research/nifty-prediction/preliminary_historical_diagnostic.js`
- JSON results: `reports/nifty-prediction/preliminary_historical_diagnostic.json`

Run with Node.js:
```bash
node research/nifty-prediction/preliminary_historical_diagnostic.js
```
