# Uploaded-PDF Method Audit and Expanded Test Register

Date opened: 2026-10-14
Scope: NIFTY 50 forecasting methods. This audit is based on all 13 uploaded PDFs, their extracted text, the repository model registry, and the existing bounded chronological experiment design. A method mentioned in background literature is not automatically treated as a method empirically evaluated by that paper. Final method-level status is assigned only from a completed workflow artifact.

## Scope rules
- Forecasting methods are in scope: price/return/direction/volatility models, sequence models, feature-selection variants, and hybrid architectures.
- The three option-strategy papers are inventoried but strategy replication is outside the current prediction-only research question: D0801051829.pdf, ssrn-3323746.pdf, and 50375.pdf. Their trading rules, transaction costs and option-contract assumptions need a separate protocol; they must not be represented as forecasting-model tests.
- BERT/news sentiment is data-dependent. It is only testable if timestamped, point-in-time news text and matching market features can be acquired and audited. No sentiment result will be fabricated from price-only data.
- Methods are compared using chronological out-of-sample evaluation and identical eligible target dates wherever feasible. Sequence models have a fixed three-epoch CPU budget and are limited to one-session return/direction in this run to bound compute. This is a screening experiment, not exhaustive hyperparameter optimization.
- “Implemented” means code exists; “run pending” means not yet empirically tested; “blocked” means a necessary input or valid protocol is absent; “not applicable” means outside the prediction scope.

## Source-by-source method inventory

| PDF | Source-derived method families / specific methods | Initial status in this expanded run |
|---|---|---|
| ISMLA+7481.pdf — Deep Learning Approaches for Stock Price Prediction: A Comparative Study on Nifty 50 Dataset | Linear regression; LSTM; GRU; CNN; RNN; TCN; hybrid LSTM+GRU, CNN+RNN, CNN+TCN, LSTM+TCN | Classic baseline in existing suite; sequence/hybrid candidates added; run pending |
| IJSDR2309053.pdf — NIFTY-50 Stock Prediction Master | RNN/LSTM-style forecasting and ARIMA references in the paper | LSTM/ARIMA candidate families available; exact protocol reproduction pending source-level extraction |
| D0801051829.pdf — Options Trading Strategy: A quantitative study from an Investor’s POV | Options strategy/portfolio analysis, not a NIFTY forecasting model catalogue | Not applicable to prediction-only scope; separately register for later strategy research |
| Stock_Market_Index_Forecasting_of_Nifty.pdf — Stock Market Index Forecasting of Nifty 50 Using Machine Learning Techniques with ANN Approach | ANN, fuzzy/neuro-fuzzy references and technical predictors | MLP proxy is in suite; self-organizing fuzzy neural network is not implemented and remains blocked/not tested |
| CureusJournals_1986620261002-185337-d4go5h.pdf — Open and Close Price Forecasting of the NIFTY 50 Stock Index Using Machine Learning | Linear regression, Lasso, Ridge, Elastic Net, SGD regressor, SVR, KNN, Decision Tree, Random Forest, Gradient Boosting, AdaBoost, XGBoost; feature engineering and time-series tuning | Expanded classical registry added; run pending |
| Stock Market Prediction of NIFTY 50 Index Applying Machine Learning Techniques.pdf | RNN, LSTM, CNN; discussion of MLP/DBN/GRU and classical ML methods; sentiment and wavelet-related literature | RNN/LSTM/CNN/GRU candidates added; DBN, wavelet decomposition and news sentiment not yet reproduced |
| IJCSE-V11I10P106.pdf — Bridging Temporal Dependencies and Sentiment | LSTM plus BERT sentiment; India VIX, FII/DII, PCR and market features | LSTM candidate test pending; BERT/news and VIX/FII/DII/PCR inputs blocked unless point-in-time series validate |
| jrfm-16-00423.pdf — Forecasting of NIFTY 50 Index Price by Using Backward Elimination with an LSTM Model | LSTM; backward-elimination feature selection; RSI and OHLCV | LSTM candidate available; backward-elimination ablation not yet implemented; RSI/price features partially available |
| ssrn-3323746.pdf — An Empirical Study on Options Trading Strategy Using Commodity Channel Index for NSE's Nifty Options in India | CCI-based options strategy | Not applicable to prediction-only scope; separately register for strategy replication |
| 9472-Article Text-11108-2-10-20231228.pdf — An Efficient Approach to Forecasting the NIFTY-50 with Artificial Neural Networks | ANN forecasting | MLP proxy in expanded registry; run pending |
| 1-s2.0-S1877050922020993-main.pdf | NIFTY/market prediction approaches discussed in source, including classical ML and recurrent/deep learning families; exact primary method mapping to be verified against full title/method section | Method-level extraction remains incomplete; no unsupported exact replication claim |
| 1912.07700v1.pdf — A Robust Predictive Model for Stock Price Prediction Using Deep Learning and Natural Language Processing | Classification and regression, LSTM, sentiment/NLP, Granger-causality screening, Self-Organizing Fuzzy Neural Network | LSTM/classification candidates in suite; NLP and fuzzy model blocked/not implemented; Granger feature-selection test not yet implemented |
| 50375.pdf — Developing A Machine Learning-Based Options Trading Strategy for the Indian Market | ML-based options trading strategy | Not applicable to prediction-only scope; separately register for strategy replication |

Note: all 13 uploaded files are represented above; repeated references are deduplicated. Some paper-specific method mapping requires further source-level verification. The inventory intentionally flags uncertainty rather than inventing details.

## Expanded model registry added
### Classical regressors
- Linear Regression, Ridge, Lasso, Elastic Net, SGD Regressor
- SVR, KNN, Decision Tree
- Random Forest, Extra Trees
- Histogram Gradient Boosting, Gradient Boosting, AdaBoost
- XGBoost, LightGBM and CatBoost when their optional packages import successfully
- Existing persistence/zero-return baselines and ARIMA benchmark

### Classifiers
- Logistic Regression, SVM, KNN, Decision Tree
- Random Forest, Extra Trees
- Histogram Gradient Boosting, Gradient Boosting, AdaBoost
- MLP and optional XGBoost/LightGBM/CatBoost

### Sequence/deep candidates
- LSTM, GRU, vanilla RNN, CNN, TCN, Transformer
- LSTM+GRU, CNN+RNN, CNN+TCN, LSTM+TCN
- Fixed short CPU training budget; test targets restricted by existing runner's explicit compute gate

## Not yet represented by a completed result
Until the expanded workflow completes and artifacts are inspected, all new methods remain RUN PENDING. A package import, code addition, or passing unit test is not an empirical forecast result. Failed model fits and missing optional packages must be retained in the error/status output.

Potentially blocked or not yet implemented families:
- BERT/FinBERT/news sentiment fusion: no verified timestamped news corpus currently established.
- Self-Organizing Fuzzy Neural Network and neuro-fuzzy systems.
- Deep Belief Network.
- Wavelet preprocessing.
- Granger-causality feature screening.
- Backward-elimination LSTM and other feature-selection variants.
- Any paper-specific tuning, windowing, target, or preprocessing protocol not yet reproduced exactly.

## Acceptance criteria
1. Model output exists for the method and task, with training/test dates and a reproducible artifact.
2. Test windows are chronological; no future target window overlaps the training information set.
3. Report skill relative to a task-matched simple baseline, uncertainty, and multiple-testing correction for candidate comparisons.
4. Record runtime/import/data failures as blocked/failed, never as a score of zero or as a win.
5. Do not name a “best” model from validation scores alone or declare trading usefulness from forecasting metrics.
6. After the bounded run, stop. Any remaining data-dependent methods are explicitly listed as not tested/blocked; no endless parameter loops.