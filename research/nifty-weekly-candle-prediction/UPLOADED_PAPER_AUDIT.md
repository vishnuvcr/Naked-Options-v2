# Audit of User-Supplied Papers — NWCP-1.0

Review date: 24 October 2026. Thirteen supplied PDFs were text-extracted and visually checked via page contact sheets. This audit summarizes only claims visible in the supplied material; it does not reproduce paper tables or claim their results are independently replicated. The uploaded PDFs remain conversation/project attachments; they are not copied into the public repository.

## Summary finding

The supplied corpus is dominated by continuous price-level regression, generic directional classification, or options trading strategies. None of the reviewed papers precisely defines the NWCP-1.0 target: NIFTY 50 spot at 10:00 IST on the first trading session after a prior actual weekly expiry versus the close on the next actual weekly expiry. Their headline accuracies are therefore not NWCP benchmarks.

## Paper-by-paper evidence audit

### 1. Mehtab and Sen — closest horizon/classification precedent
**Paper:** Sidra Mehtab and Jaydip Sen, A Robust Predictive Model for Stock Price Prediction Using Deep Learning and Natural Language Processing. Supplied file: 1912.07700v1.pdf. [arXiv record](https://arxiv.org/abs/1912.07700).

**Reported design:** daily NIFTY 50 values from 2015–2017 used to build predictive models; forecasts evaluated over January 2018–June 2019 with a one-week horizon. The approach combines machine-learning/deep-learning prediction with Twitter sentiment, including sentiment causality tests and a Self-Organizing Fuzzy Neural Network (SOFNN) augmentation. Authors report the sentiment-augmented approach as the strongest tested.

**Relevance:** the closest supplied work in horizon and movement classification, and a reason to investigate sentiment only if publication timestamps and historical data coverage are defensible.

**Limits for NWCP:** the endpoint and anchor are not weekly-expiry-specific; daily rather than timestamped intraday target construction; sentiment availability may be later than the forecast cutoff; the result is not a clean estimate for the NWCP labels.

### 2. Fathali, Kodia and Ben Said — NIFTY deep-learning comparison
**Paper:** Zahra Fathali, Zahra Kodia and Lamjed Ben Said (2022), Stock Market Prediction of NIFTY 50 Index Applying Machine Learning Techniques, Applied Artificial Intelligence 36(1), DOI [10.1080/08839514.2022.2111134](https://doi.org/10.1080/08839514.2022.2111134). Supplied file: Stock Market Prediction of NIFTY 50 Index Applying Machine Learning Techniques.pdf.

**Reported design/result:** compares RNN, LSTM and CNN for NIFTY time-series forecasting; reports lower MSE for LSTM under the authors’ setup. The data is daily market history and the method includes feature selection/hyperparameter work; the paper describes an 80/20 split and K-fold-based validation.

**Relevance:** NIFTY-specific architectural comparison.

**Limits:** target is price/trend forecasting, not NWCP binary expiry direction. MSE is not directional hit rate. The fold construction must be chronological to support future-period claims; K-fold validation that mixes dates would not be a valid primary time-series estimate.

### 3. Naik and Inamdar — news sentiment and market-state features
**Paper:** Pranav P. Naik and Vadiraj G. Inamdar (2024), Bridging Temporal Dependencies and Sentiment: A Comprehensive Approach to NIFTY 50 Index Prediction, SSRG International Journal of Computer Science and Engineering 11(10), 46–53, DOI [10.14445/23488387/IJCSE-V11I10P106](https://doi.org/10.14445/23488387/IJCSE-V11I10P106). Supplied file: IJCSE-V11I10P106.pdf.

**Reported design/result:** combines LSTM with BERT-based financial-news sentiment and considers FII/DII activity, India VIX and put-call ratio of nearby expiries; the paper describes an 80/20 split and bullish/bearish/neutral prediction.

**Relevance:** makes global/news/volatility/derivatives groups reasonable *candidate feature families* to audit.

**Limits:** the outcome is three classes, not the fixed NWCP comparison. FII/DII, PCR and news may be published after 10:00 or may have been revised. Every observation needs its actual publication/availability timestamp or it must be lagged/excluded.

### 4. Kallimath, Darapaneni and Paduri — multi-architecture price prediction
**Paper:** Sushma P. Kallimath, Narayana Darapaneni and Anwesh Reddy Paduri, Deep Learning Approaches for Stock Price Prediction: A Comparative Study on Nifty 50 Dataset, EAI Endorsed Transactions on Intelligent Systems and Machine Learning Applications, DOI [10.4108/eetismla.7481](https://doi.org/10.4108/eetismla.7481), published 2025. Supplied file: ISMLA+7481.pdf.

**Reported design/result:** compares linear regression, LSTM, GRU, CNN, RNN, TCN and hybrid combinations using MSE, R², RMSE, MAE and MAPE; results text describes 2,350 training and 235 test points and reports good performance for LSTM / some hybrids.

**Relevance:** informs the architecture survey and highlights that model and optimizer choice can change reported errors.

**Limits:** regression metrics are not weekly directional skill. The supplied text does not establish a matching expiry-based target or OOS test of sufficient size for this research.

### 5. Bumrah and Budhani — daily close prediction with FII and dollar inputs
**Paper:** Kuljinder Singh Bumrah and Sandeep Kumar Budhani (2023), An Efficient Approach to Forecasting the NIFTY-50 Indian Stock Market’s Daily Closing Price with Artificial Neural Networks, International Journal on Recent and Innovation Trends in Computing and Communication 11(11). Supplied file: 9472-Article Text-11108-2-10-20231228.pdf.

**Reported design/result:** 1 April 2018–31 March 2023, 1,183 records, daily NIFTY close with dollar exchange rate and FII gross purchases/sales; the paper describes a 65/35 train/test split and reports MLP as the stronger method versus SVM, RBF and SLP.

**Relevance:** motivates a conditional macro/flow feature ablation.

**Limits:** target is daily close regression. FII flow data released later in a day cannot be used as a same-day 10:00 feature. The split details and publication timestamp integrity need audit before drawing future-period conclusions.

### 6. Jafar et al. — backward-elimination LSTM
**Paper:** Syed Hasan Jafar, Shakeb Akhtar, Hani El-Chaarani, Parvez Alam Khan and Ruaa Binsaddig (2023), Forecasting of NIFTY 50 Index Price by Using Backward Elimination with an LSTM Model, Journal of Risk and Financial Management 16, 423, DOI [10.3390/jrfm16100423](https://doi.org/10.3390/jrfm16100423). Supplied file: jrfm-16-00423.pdf.

**Reported design/result:** roughly 15 years of daily data (3,986 described records) from Bloomberg/Yahoo-era sources, OHLC plus volume/trades/value and RSI; compares LSTM and backward-elimination LSTM for a 30-day closing-price horizon and states 95% “accuracy.”

**Relevance:** feature-selection research context.

**Limits:** a 30-day price-level forecast is not a five-ish-session binary expiry target. The word “accuracy” cannot be compared without matching the metric definition, target and scaling. Feature selection must be restricted to training data in NWCP.

### 7. Sain and Singh — recent NIFTY price-regression study
**Paper:** Rohit K. Sain and Amresh K. Singh, Open and Close Price Forecasting of the NIFTY 50 Stock Index Using Machine Learning: A Multi-Window Study of Feature Engineering and Model Tuning, Cureus Journal of Computer Science 3, published 1 October 2026, DOI [10.7759/s44389-026-00306-5](https://doi.org/10.7759/s44389-026-00306-5). Supplied file: CureusJournals_1986620261002-185337-d4go5h.pdf. The article is CC BY 4.0.

**Reported design/result:** 12 regression models versus naïve persistence; next-day open/close targets across 5-, 10- and 20-year windows; compares raw OHLCV with indicators such as SMA, RSI, return and rolling volatility. Uses chronological 80/20 splits and TimeSeriesSplit tuning for Random Forest/XGBoost. The authors report that linear models (Linear Regression, Ridge and Lasso) were more stable across the 10- and 20-year windows, while tree models can fit extremely well in sample yet underperform naïve persistence in some long-window tests. They call for rolling-origin/walk-forward validation and statistical uncertainty as future work.

**Relevance:** the most current supplied warning against assuming model complexity or technical-indicator enrichment helps. Supports strong naive and linear baselines.

**Limits:** price regression is not NWCP directional classification; its split and outcomes do not establish this project’s result. The authors restrict their conclusions to their own dataset and targets.

### 8. Harish B. G. et al. — LSTM prediction report
**Paper:** Harish B. G., ChetanKumar G. S., Raghavendrareddy Radder and Manoj K. (2023), NIFTY-50 Stock Prediction Master, International Journal of Scientific Development and Research 8(9). Supplied file: IJSDR2309053.pdf.

**Reported design/result:** daily NIFTY history from 10 December 2011 to 10 December 2021, normalization and LSTM; claims 83.88% accuracy.

**Relevance:** shows that high headline “accuracy” figures recur in this area.

**Limits:** in the supplied report, the exact definition of accuracy, target class/metric, time-ordered test protocol, confusion matrix, uncertainty and reproducible baseline are not sufficiently specified to compare with NWCP. The reported figure is treated as non-comparable, not a target.

### 9. Kumar and Sharma — next-day OHLC neural prediction
**Paper:** Gourav Kumar and Vinod Sharma (2016), Stock Market Index Forecasting of Nifty 50 Using Machine Learning Techniques with ANN Approach, International Journal of Modern Computer Science 4(3). Supplied file: Stock_Market_Index_Forecasting_of_Nifty.pdf.

**Reported design/result:** MLP / multiple-back-propagation forecasts next-day OHLC using OHLC, volume and turnover over 3 April 2006–16 May 2016. It reports a normalized RMSE of 0.0079 and average “accuracy” of 99.2152%.

**Limits:** continuous OHLC regression is a different task. A “99% accuracy” derived from a normalized price forecast is not directional hit rate for NWCP.

### 10. Kallimath et al. source record and additional NIFTY index study notes
The separate architecture paper is cited under item 4 above; it remains a regression benchmark rather than an accepted directional prediction result. Its architecture suite is not added wholesale to NWCP due the small number of independent weekly labels and the larger selection burden.

### 11. Bansal et al. — company-level stock regression
**Paper:** Stock Market Prediction with High Accuracy using Machine Learning Techniques, Procedia Computer Science 215 (2022), 247–265. Supplied file: 1-s2.0-S1877050922020993-main.pdf.

**Reported design/result:** compares KNN, linear regression, support-vector regression, decision-tree regression and LSTM on price histories for 12 companies, using data across 2015–2021; the paper identifies LSTM as strongest in its experiments.

**Limits:** individual equities and price regression are not NIFTY expiry direction. It contributes no NWCP-specific model evidence.

## Papers deliberately excluded from prediction-skill evidence

### 12. Atheetha et al. — options strategy
**Paper:** Atheetha S., Simran Mondal, Dhanusha N. and Raghunandan H. J. (2019), Options Trading Strategy: A Quantitative Study from an Investor’s POV. Supplied file: D0801051829.pdf.

The paper studies Simple Average Method, timing risk and speculative option strategies across a small mix of stocks and an index. It does not test the NWCP outcome and is not used to seed or rank models.

### 13. Pinkal Shaha — CCI-based NIFTY options strategy
**Paper:** An Empirical Study on Options Trading Strategy Using Commodity Channel Index for NSE’s Nifty Options in India. Supplied file: ssrn-3323746.pdf.

The paper studies CCI rules for identifying ITM option-price rises and reports option strategy outcomes. Option P&L is explicitly excluded from NWCP; this paper is retained in the inventory only and contributes no evidence for the index-direction label.

### 14. Sherasiya — ML option-chain strategy
**Paper:** Firoz A. Sherasiya (2025), Developing A Machine Learning-Based Options Trading Strategy for the Indian Market. Supplied file: 50375.pdf.

The study reports Random Forest, XGBoost and LSTM buy/sell signals from option-chain/Greeks/implied-volatility and underlying moves, with strategy metrics such as accuracy, Sharpe and return. The task is options strategy optimization, not NWCP index-direction classification; results are excluded.

## Cross-paper conclusions

1. The supplied literature mostly predicts price level, not our target direction. Metric values from these studies cannot be pooled or used as direct comparators.
2. At least one recent NIFTY multi-window paper found that simple linear regression models were more stable than some tree ensembles over longer test windows. NWCP therefore retains majority/base-rate and logistic baselines before evolutionary methods.
3. Indicator/news/option features are hypotheses only. Timestamp availability is particularly important for news, option aggregates and FII/DII flow features.
4. The weekly sample size will be orders of magnitude smaller than minute-bar rows. The number of unique labels, not bars or overlapping windows, is the independent forecasting sample size.
5. High model capacity, extensive evolutionary search and many indicator variants increase selection risk. Every candidate must be logged, all choices frozen before final chronological test, and multiplicity/uncertainty reported.

## Sources for method and protocol

- QuantEvolve (Yun, Lee and Jeon, 2025), “QuantEvolve: Automating Quantitative Strategy Discovery through Multi-Agent Evolutionary Framework.” [arXiv:2510.18569](https://arxiv.org/abs/2510.18569) and [official project repository](https://github.com/CiubancanC/QuantEvolve). NWCP uses a constrained, typed-rule evolutionary adaptation inspired by quality-diversity; it does not claim to run the complete original multi-agent framework.
- Sullivan, Timmermann and White, “Data-Snooping, Technical Trading Rule Performance, and the Bootstrap.” [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1111/0022-1082.00163), [CEPR](https://cepr.org/publications/dp1976). Motivates evaluating the full tested rule family rather than reporting a selected winner.
- Bailey, Borwein, López de Prado and Zhu, “The Probability of Backtest Overfitting.” [Author-access source](https://escholarship.org/uc/item/4w1110bb), [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253). Motivates keeping final OOS separate from model selection.
- Arian, Norouzi Mobarakeh and Seco (2024), “Backtest overfitting in the machine learning era: A comparison of out-of-sample testing methods in a synthetic controlled environment,” Knowledge-Based Systems 305, 112477. [DOI](https://doi.org/10.1016/j.knosys.2024.112477). Synthetic-method findings motivate validation controls but are not a guarantee for markets.
- TradingView [repainting documentation](https://www.tradingview.com/pine-script-docs/concepts/repainting/) and [strategy FAQ](https://www.tradingview.com/pine-script-docs/faq/strategies/). Community scripts require per-source audit for unconfirmed bars, future shifts, higher-timeframe lookahead and rights.
- NSE [NIFTY 50 F&O product page](https://www.nseindia.com/static/products-services/equity-derivatives-nifty50), [contract specifications](https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications), and [data policy](https://www.nseindia.com/static/market-data/nse-data-policy).
- Dhan [Historical Data API v2](https://dhanhq.co/docs/v2/historical-data/): 1-minute intraday candles in bounded 90-day requests, with timestamp and instrument mapping to verify.

## Review boundary

This is a structured review of the 13 supplied PDFs and the directly relevant sources listed above, not a claim that every paper on market prediction has been retrieved. Further searching should prioritize exact NIFTY weekly-expiry directional targets, temporally valid evaluation and source timestamps rather than merely collecting higher advertised “accuracy” reports.
