# Literature and External Source Review — NWCP-1.0

Last reviewed: 2026-10-24. This is an initial source-backed bibliography, not yet a comprehensive systematic review.

## 1. QuantEvolve

**Yun, Lee and Jeon (2025), “QuantEvolve: Automating Quantitative Strategy Discovery through Multi-Agent Evolutionary Framework,” arXiv:2510.18569.** [arXiv](https://arxiv.org/abs/2510.18569) · [Open-source implementation/docs](https://github.com/CiubancanC/QuantEvolve)

The paper describes hypothesis-driven, multi-agent evolutionary search with quality-diversity so candidates can span different behavior/features instead of optimizing only one scalar fitness. NWCP adapts the discovery concept to classification and indicator discovery, not option P&L. Train-only fitness, validation-only selection and a sealed OOS test are mandatory. Paper claims do not prove the adaptation predicts NIFTY weekly direction.

Additional implementation candidate: [tarsyang/quantevolve](https://github.com/tarsyang/quantevolve), described as a quantitative strategy evolution system forked from OpenEvolve. Before adoption, inspect current revision/license/dependencies/security and evaluation semantics. Never execute arbitrary evolved code with access to secrets; prefer a typed expression tree and allowlisted interpreter.

## 2. Technical indicators, data snooping and overfitting

**Sullivan, Timmermann and White (1999/2002), “Data-Snooping, Technical Trading Rule Performance, and the Bootstrap,” Journal of Finance 54(5), 1647–1691.** [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1111/0022-1082.00163) · [CEPR](https://cepr.org/publications/dp1976)

This study uses White's Reality Check bootstrap to account for data-snooping over a universe of technical rules. NWCP will log all candidates and correct predeclared model/family comparisons instead of cherry-picking the best indicator.

**Bailey, Borwein, López de Prado and Zhu (2017), “The Probability of Backtest Overfitting.”** [Author-access source](https://escholarship.org/uc/item/4w1110bb) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)

The paper proposes estimating probability of backtest overfitting through combinatorially symmetric cross-validation. It motivates accounting for selection across many candidates. Since NWCP is temporal, chronological holdout and walk-forward tests remain primary; PBO/CSCV is supplementary, not a replacement for future-period testing.

**Arian, Norouzi Mobarakeh and Seco (2024), “Backtest overfitting in the machine learning era: A comparison of out-of-sample testing methods in a synthetic controlled environment,” Knowledge-Based Systems 305, 112477.** [ScienceDirect](https://doi.org/10.1016/j.knosys.2024.112477)

The study compares OOS schemes under synthetic non-stationarity, dependence and regime shifts and reports benefits for combinatorial purged cross-validation in its setting. NWCP should report temporal robustness and use purge/embargo where samples overlap; synthetic findings are not guarantees for NIFTY.

## 3. Pine source integrity and repainting

**TradingView Pine Script — Repainting.** [Official documentation](https://www.tradingview.com/pine-script-docs/concepts/repainting/)

Historical and real-time outputs can differ when a script uses unconfirmed bars, higher-timeframe requests or time-dependent behavior. Community Pine scripts are not assumed non-repainting. Each candidate needs source/license capture, version identification, request.security/lookahead inspection, confirmed-bar review and formula regression tests.

**TradingView Pine Script — Strategy FAQ.** [Official documentation](https://www.tradingview.com/pine-script-docs/faq/strategies/)

Realtime tick/fill recalculation can make historical and realtime behavior differ. While NWCP does not backtest trades, these semantics still matter for whether a Pine feature could have been known at the forecast cutoff and whether historical and live indicator values are comparable.

## 4. Current expiry and market-data use

**NSE — NIFTY 50 F&O product page.** [Official NSE page](https://www.nseindia.com/static/products-services/equity-derivatives-nifty50)

Current documentation states NIFTY 50 weekly index options expire Tuesday of expiry week, moved to the preceding trading day for a Tuesday holiday. Historical circulars/contract metadata are required to handle previous expiry conventions correctly.

**NSE — Contract specifications.** [Official page](https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications)

Provides current expiry and index-derivatives contract conventions.

**NSE — Data Sharing and Usage Policy.** [Official policy](https://www.nseindia.com/static/market-data/nse-data-policy)

Market-data access, use and redistribution have restrictions. Downloadability does not mean a dataset can be committed or published on Pages.

**Dhan — Historical Data API.** [Official documentation](https://dhanhq.co/docs/v2/historical-data/)

Dhan documents daily and intraday OHLC endpoints; minute bars include 1, 5, 15, 25 and 60-minute intervals and intraday requests are limited to 90 days. Timestamp semantics and NIFTY index security/segment mapping still require empirical validation.

## 5. Candidate open data sources — pending audit

- [technovusin/nifty50-historical-data](https://github.com/technovusin/nifty50-historical-data) — describes NIFTY 50 minute data beginning in 2017 and documents its own cleaning choices. Verify current license, original source, session coverage and overlap agreement with Dhan.
- [gsidhu/nse-intraday-data](https://github.com/gsidhu/nse-intraday-data) — public intraday archive with NIFTY-related files. Verify exact index coverage, licensing, time zone, duplicate/gap issues and provenance.
- Official NSE index history, holidays and expiry circulars; other Kaggle/Hugging Face/Zenodo candidates after review.

## 6. Literature review gaps

Continue targeted review on: NIFTY direction classification and expiry-related returns; technical indicators with strict temporal validation; financial model calibration and purged/embargo validation; quality-diversity/symbolic evolution on small samples; and event/regime-conditioned forecasts. For each source record instrument/period/frequency/sample size, features, split design, baseline, metric, statistical test, code and limitations. Clearly label peer-reviewed articles, preprints, repositories and vendor claims separately.
