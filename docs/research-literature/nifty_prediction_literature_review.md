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


## 6. Additional user-provided papers screened (PDFs attached to the project)

These papers were screened directly from the supplied PDFs. The summaries below are limited to the abstract/front matter extracted for this pass; numerical results and detailed experimental design must be checked against each full paper before being used as evidence.

### Kumar and Sharma (2016), “Stock Market Index Forecasting of Nifty 50 Using Machine Learning Techniques with ANN Approach”
- Local source: `Stock_Market_Index_Forecasting_of_Nifty.pdf`.
- Abstract emphasizes MLP/ANN approaches to NIFTY 50 forecasting.
- Use in this study: historical comparator for neural-network forecasting; not sufficient evidence by itself that ANN forecasts beat simple walk-forward baselines.

### Fathali, Kodia, and Ben Said (2022), “Stock Market Prediction of NIFTY 50 Index Applying Machine Learning Techniques”
- Local source: `Stock Market Prediction of NIFTY 50 Index Applying Machine Learning Techniques.pdf`; DOI: https://doi.org/10.1080/08839514.2022.2111134.
- The abstract frames RNN, LSTM and CNN models for Indian market time-series prediction and discusses feature selection and evaluation metrics.
- Use: supports considering temporal models only after a baseline is established; reported predictive metrics must be checked for chronological leakage and compared on a common target.

### Jafar et al. (2023), “Forecasting of NIFTY 50 Index Price by Using Backward Elimination with an LSTM Model”
- Local source: `jrfm-16-00423.pdf`.
- Abstract describes 15 years of daily Bloomberg data and LSTM versus backward-elimination LSTM with technical indicators.
- Use: motivates feature selection as a research hypothesis, but price-level error metrics are not equivalent to next-session direction or tradable performance.

### Bumrah and Budhani (2023), “An Efficient Approach to Forecasting the NIFTY-50 Indian Stock Market's Daily Closing Price with Artificial Neural Networks”
- Local source: `9472-Article Text-11108-2-10-20231228.pdf`.
- Abstract describes comparisons including SVM, RBF and perceptron variants, and mentions dollar exchange rates and FII flows.
- Use: motivates evaluating global/FX and institutional-flow features when point-in-time series can be assembled. Abstract claims about a preferred model are not transferred into this project's results.

### “NIFTY-50 Stock Prediction Master” (2023)
- Local source: `IJSDR2309053.pdf`.
- Abstract describes an LSTM-based approach using about ten years of historical NIFTY 50 data.
- Use: another deep-learning comparator; details such as exact target, split, leakage controls and baseline strength require full-text review.

### “Bridging Temporal Dependencies and Sentiment: A Comprehensive Approach to NIFTY 50 Index Prediction” (2024)
- Local source: `IJCSE-V11I10P106.pdf`.
- Abstract describes an LSTM with BERT-based news sentiment and features including FII/DII activity, India VIX and near-expiry option put-call ratio.
- Use: directly motivates future feature groups (sentiment, institutional flows, VIX, options PCR). These require historical point-in-time alignment; contemporaneous or revised data can leak future information.

### “Deep Learning Approaches for Stock Price Prediction: A Comparative Study on Nifty 50 Dataset” (2024)
- Local source: `ISMLA+7481.pdf`.
- Abstract lists linear regression, LSTM, GRU, CNN, RNN, TCN and hybrid models.
- Use: broad model-family survey. Model count alone is not evidence of predictive superiority; evaluation protocol and naive baselines matter more.

### Mehtab and Sen, “A Robust Predictive Model for Stock Price Prediction Using Deep Learning and Natural Language Processing” (arXiv:1912.07700)
- Local source: `1912.07700v1.pdf`.
- Abstract describes a hybrid machine-learning, deep-learning and NLP approach to stock-movement prediction.
- Use: background for sentiment/NLP hypotheses. It is not NIFTY-specific evidence unless the paper's data and evaluation establish that scope.

### “Stock Market Prediction with High Accuracy using Machine Learning Techniques” (Procedia Computer Science, 2022)
- Local source: `1-s2.0-S1877050922020993-main.pdf`.
- Abstract discusses supervised stock-market prediction.
- Use: general background only; claims of “high accuracy” require scrutiny of target construction, class balance, chronological validation and comparison to naive baselines.

### Shaha, “An Empirical Study on Options Trading Strategy Using Commodity Channel Index for NSE’s Nifty Options in India”
- Local source: `ssrn-3323746.pdf`.
- Abstract describes CCI/technical analysis for NIFTY options.
- Use: relevant to a later options-specific strategy phase, but not evidence for spot-index direction prediction; option pricing, volatility, expiry and transaction costs must be modeled separately.

### Sherasiya, “Developing A Machine Learning-Based Options Trading Strategy for the Indian Market”
- Local source: `50375.pdf`.
- Abstract describes NIFTY options data, Greeks, implied volatility, underlying movement and classification models, with backtesting.
- Use: informs later feature and execution design. Full results, time split, survivorship/leakage controls, fill assumptions and net-cost accounting must be audited before reuse.

### “Options Trading Strategy: A Quantitative Study from an Investor’s POV” (2019)
- Local source: `D0801051829.pdf`.
- Abstract discusses option-trading behavior across stocks/sectors and an index.
- Use: contextual background only; it is not a direct next-session NIFTY prediction benchmark.

### Sain and Singh (2026), “Open and Close Price Forecasting of the NIFTY 50 Stock Index Using Machine Learning: A Multi-Window Study of Feature Engineering and Model Tuning”
- Local source: `CureusJournals_1986620261002-185337-d4go5h.pdf`; DOI: https://doi.org/10.7759/s44389-026-00306-5.
- Abstract describes 12 supervised models, naïve persistence, 5/10/20-year windows and raw versus engineered features.
- Use: particularly relevant to multi-window evaluation and persistence baselines. Because the target is open/close price forecasting, its metrics must not be conflated with directional accuracy or net trading return.

## 7. Synthesis and implications for the current experiment

Across the supplied studies, common themes are neural/sequence models, technical indicators, sentiment, institutional flows, volatility and options-derived features. Their abstract-level claims are heterogeneous: some forecast price levels, some classify direction, and others backtest option strategies. These are different targets and cannot be compared using headline accuracy alone.

The current project's empirical baseline remains the controlling evidence: the simple previous-session direction rule outperformed the tested supervised models on the common chronological holdout. The first rule screen did not identify a better candidate. The immediate next experiment is therefore a GARCH-family volatility forecast (scored as volatility, not direction) and then only a small number of point-in-time feature experiments. Options-specific papers will be used in a separate phase once expiry-specific historical option-chain/Greeks data and execution costs can be aligned without look-ahead.

## 8. Limitations of this review

- The additional local-PDF summaries in Section 6 are based on extracted abstracts/front matter, not a full-text audit of every equation, split, table and appendix.
- We have not independently reproduced the published models or verified their raw datasets.
- Published accuracy figures are not compared numerically unless target, horizon, data period, class balance and validation protocol match.
- No article's reported claim is treated as a result of the present research.
