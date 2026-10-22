# Literature and external-source review — QE-NOB-1.0

**Status:** initial source qualification; continue through Phase 2. This review generates testable hypotheses only. It does not treat literature findings as proof a NIFTY options strategy can profit.

## 1. Regulatory/base-rate context

### SEBI — equity derivatives P&L study, FY22–FY24
SEBI's 23 September 2024 release of its updated study states that 93% of individual traders in equity F&O incurred losses over FY22–FY24 and aggregate individual-trader losses exceeded ₹1.8 lakh crore over those three years. It is an important base-rate and risk-context source, not a forecast of any specific candidate's outcome.
- Official release: https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html
- Official study page: https://www.sebi.gov.in/reports-and-statistics/research/sep-2024/study-analysis-of-profits-and-losses-in-the-equity-derivatives-segment-fy22-fy24-_86905.html

## 2. Broker/exchange cost sources

### Paytm Money official tariff and brokerage calculator
Paytm Money's official pricing page states regulatory/exchange charges are levied at actual rates and that tariff changes may be made. Its official educational page has described options brokerage of ₹10 per order, but it is older than the current research date. Therefore ₹10/order is a provisional calculation seed, not yet frozen; Phase 4 must verify the current tariff/calculator and stress a higher rate if ambiguity remains.
- Pricing: https://www.paytmmoney.com/stocks/pricing
- Options brokerage explainer/calculator: https://www.paytmmoney.com/blog/calculate-brokerage-on-paytm-money-app/
- Fee update article: https://www.paytmmoney.com/blog/paytm-money-pricing-update-revised-charges-effective-1st-october/

### NSE STT and contract terms
NSE's official STT page lists, effective 1 April 2026, a 0.15% tax on the sale of an option (computed on premium) and 0.15% for an option exercised (computed on intrinsic value). Historical trades must use the rate applicable on the actual trade date, not a single current value. Current contract specs should be re-read before the data map is frozen. An NSE circular dated 3 October 2025 revises the NIFTY lot size from 75 to 65 for the specified contract introduction cohorts; contract-master/date-based sizing must supersede a coarse static assumption.
- NSE STT: https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax
- NSE index derivatives specs: https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications
- NSE lot-size revision circular: https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf

## 3. Primary data-source feasibility

### DhanHQ historical and expired option data
DhanHQ documents historical OHLC APIs and a rolling expired-option endpoint for expired contracts with strike-relative retrieval; official support describes access to expired-option data. The API is attractive because it is part of the user's subscribed source, but contract identity, time granularity, exact return fields, coverage and licence restrictions must be tested before backtesting.
- Historical data API: https://dhanhq.co/docs/v2/historical-data/
- Expired options: https://dhanhq.co/docs/v2/expired-options-data/
- Option chain / current bid-ask, IV, OI and volume: https://dhanhq.co/docs/v2/option-chain/
- Support statement on expired data: https://dhan.co/support/platforms/dhanhq-api/do-dhan-provides-expired-options-data-via-the-api-s/

Dhan's official docs describe the rolling expired-option endpoint as strike-relative and request windows of no more than 30 days; never infer fixed-contract identity solely from rolling-relative labels.

## 4. Academic hypotheses

### Choy (2015), “Retail clientele and option returns”
Journal of Banking & Finance 51, 26–42. Abstract reports that higher retail trading proportion is associated with lower option returns in its studied US equity options setting and discusses a lottery premium in options with expensive implied volatility. This is not directly a NIFTY index result; it motivates explicitly measuring IV, moneyness and the movement needed to cover paid premium.
- DOI: https://doi.org/10.1016/j.jbankfin.2014.11.004

### Heston, Jones, Khorram, Li and Mo (2022), “Option Momentum”
The SSRN abstract studies monthly returns of ATM straddles on individual equities and reports cross-sectional continuation in its studied sample. It does not establish short-horizon intraday profitability in NIFTY index options; this study will treat time-series and cross-sectional momentum as separate hypotheses, not import reported effect sizes.
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4113680

### Eaton, Green, Roseman and Wu (2026), “Retail option traders and the implied volatility surface”
Journal of Financial Economics, 177 (March 2026), article 104238. The abstract reports that retail traders are net purchasers of short-dated options, particularly OTM contracts, and that retail-demand shocks move implied volatility in the studied market. This supports testing whether entry conditions control the IV/premium paid, but it is not a strategy-profit result and may not generalize to Indian index derivatives.
- DOI: https://doi.org/10.1016/j.jfineco.2026.104238
- Publisher page: https://www.sciencedirect.com/science/article/pii/S0304405X26000097

## 5. Educational media / online strategies

YouTube/blog strategy claims are candidate-generation material only. No strategy is accepted because a video shows a chart or win rate. During Phase 2, collect a small provenance-recorded set of independently replicable candidates with published rule parameters; exclude claims without timestamps, actual fills, cost accounting or reproducible losing-trade samples. Do not copy code or use social claims as validation evidence.

## 6. Research gaps this study addresses

1. Generic breakout/indicator claims are not evidence that option premium P&L is positive; premium, delta, gamma, theta, IV, spread and execution must be measured.
2. Rolling option candles may lack contemporaneous bid/ask. OHLC backtests should not be called execution-proven without conservative fills and quote-quality sensitivity.
3. Evolutionary searches create selection bias. Candidate counts, frozen search bounds, temporal validation and multiple-testing adjustment are required.
4. Indian tax and lot/expiry rules change over time; cost and contract-master inputs must be date-effective.
5. Public/free data may extend or cross-check results, but composites cannot combine different strikes, timestamps or units without proven lineage.

## 7. Initial source inventory status

| Source | Type | Initial relevance | What it can support | What it cannot support alone |
|---|---|---|---|---|
| SEBI FY22–FY24 F&O study | Official regulator | High | Base-rate/risk context | Candidate profitability |
| NSE STT and contract specs | Official exchange | High | Date-effective costs / contract map | Actual filled prices |
| Paytm Money official pricing | Broker | High | Brokerage and fee inputs | Historical option execution |
| DhanHQ historical/expired option docs | Data provider | High | Data-access plan, schema expectations | Coverage until verified in fresh run |
| Choy (2015) | Peer-reviewed finance | Medium | IV/retail-demand hypothesis | NIFTY intraday rule |
| Heston et al. (2022) | Working paper | Medium | Option momentum hypothesis | Indian index option profit |
| Eaton et al. (2026) | Peer-reviewed finance | Medium | Short-dated retail demand/IV hypothesis | Actionable strategy |

Further literature searching and source validation are Phase 2 outputs. The study stops at the eight preregistered phases.
