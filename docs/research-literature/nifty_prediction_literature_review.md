# Literature Review — NIFTY 50 Direction Prediction and Financial Forecast Evaluation

**Reviewed:** 2026-10-25  
**Purpose:** Inform the prediction-only benchmark design. This is a targeted initial review, not a claim of exhaustive coverage.

## 1. Directly relevant Indian-index research

### Revathi et al. (2026), “AI-Driven Dynamic Asset Allocation: Walk-Forward Evidence on a Bi-LSTM and Duelling DDQN Agent for the Nifty 50 Index”
- Source: https://www.jidmis.org/index.php/jidmis/article/view/5225
- The paper reports an expanding walk-forward evaluation over 672 out-of-sample days and compares an agent with buy-and-hold and simple momentum/volatility rules. Its abstract reports that the agent did not outperform the benchmarks under the reported experiment and that transaction costs reduced returns amid high turnover.
- Relevance: complexity must be compared with simple baselines; report costs in any future trading study; do not infer economic value from classification accuracy alone.
- Caveat: the paper is recent and its full methods/results require independent review before relying on numerical claims.

### Shakeel, Yadav, and co-authors (2026), “A multimodal deep learning framework for stock direction prediction with granger-based predictive explainability”
- Source: https://ideas.repec.org/a/spr/jecfin/v50y2026i1d10.1007_s12197-026-09761-1.html
- The indexed abstract describes NIFTY 50 data aligned with financial news and rolling-origin time-series validation, with benchmark comparisons, ablations, a White Reality Check, and transaction-cost-aware simulation.
- Relevance: news and point-in-time feature availability may be valuable future extensions, but must be timestamp-aligned and tested against simpler baselines.
- Caveat: this source is an abstract/indexing record; obtain and inspect the full paper and supplements before treating its results as replicated evidence.

### Nag and Choudhury (2026), “A large language model framework for predicting significant equity index fluctuations”
- Source: https://doi.org/10.1007/s11334-026-00655-3
- The available summary describes daily NIFTY 50, NIFTY BANK and NIFTY IT data, rolling-window validation, and the importance of minority-sensitive metrics for rare large-move labels.
- Relevance: ordinary up/down direction and rare-event prediction are different tasks; class imbalance can make raw accuracy misleading.
- Caveat: this review currently uses a secondary summary, not a fully extracted manuscript.

### Arora (2026), “Directional Prediction of Indian Thematic Equity Indices Using Machine Learning Ensemble Classifiers”
- Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6748042
- The abstract reports one-day accuracy close to a random-walk baseline and much higher reported accuracy at longer horizons, evaluated with a random split.
- Relevance: forecast horizon must be stated explicitly and results from different horizons are not interchangeable.
- Caveat: the reported random split is weaker evidence for deployment-time forecasting than a strict chronological walk-forward protocol; SSRN posting does not itself establish peer review.

## 2. Statistical validity and backtest selection

### Bailey, Borwein, López de Prado, and Zhu (2017), “The Probability of Backtest Overfitting”
- Source: https://escholarship.org/uc/item/4w1110bb
- Proposes combinatorially symmetric cross-validation to estimate the probability of backtest overfitting in investment simulations.
- Implication for this study: avoid tuning against the final holdout, record the number of variants tried, and reserve any strategy-selection framework for a later phase. CSCV is not a replacement for chronology in a forward prediction task.

### Bailey et al. (2014), “Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance”
- Source: https://scholarworks.wmich.edu/math_pubs/40/
- Explains how searching many configurations can create deceptively strong historical results.
- Implication: keep model families and metrics predeclared; report all attempted variants and qualify exploratory comparisons.

### “Assessing the accuracy of directional forecasts” (2024)
- Source: https://doi.org/10.1080/00036846.2024.2393902
- Discusses tests of directional forecast accuracy, including settings with serial dependence and costly extreme misses.
- Implication: classification accuracy alone is not a complete statistical comparison. Follow-up work should add paired forecast-comparison tests suited to the data and the metric.

## 3. Synthesis for the current protocol

1. **Simple baselines first.** Complex neural or agent systems must beat naive direction forecasts on identical chronological test observations.
2. **Use time-aware validation.** Random splits can mix market regimes and do not replicate the sequence in which information becomes available.
3. **Separate prediction from trading.** Predictive accuracy is not net profitability. Any later strategy study must model spread, slippage, brokerage, taxes/fees, liquidity, turnover, and realistic execution.
4. **Use class-sensitive metrics.** Balanced accuracy, confusion matrix, class-wise precision/recall/F1 and calibration metrics supplement raw accuracy.
5. **Control research degrees of freedom.** Preserve an untouched final period and document the number of model/feature variants.
6. **Require point-in-time data.** News, global indices, FII/DII flows, options and regime variables must be available at the simulated prediction time, with source and timestamp provenance.

## 4. Gaps and next searches

- Retrieve and inspect full texts and supplements for the recent NIFTY papers above.
- Search for original papers on NIFTY directional prediction, India VIX, global lead-lag effects, FII/DII flows, and option-implied information.
- Search open datasets and official NSE/Nifty Indices documentation for daily index OHLC and market calendars.
- Add source-quality grading and a bibliography of inclusion/exclusion reasons before expanding the model stack.

## 5. Evidence boundary

This literature review is contextual. None of the cited papers supplies the empirical score for the repository's current benchmark, and their reported results are not presented as independently replicated. The current benchmark remains pending verified execution artifacts.
