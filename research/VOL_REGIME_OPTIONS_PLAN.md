# Volatility-regime weekly options study — VOL-REGIME-OPT-1.0

**Created:** 2026-10-15  
**Developer branch:** `research/vol-regime-options-developer`  
**Status:** Phase 1 protocol freeze; empirical work pending  
**Parent studies:** NIFTY-PRED-1.0 (closed prediction-only) and OPT-BUY-1.0 / OPT-BUY-2.0 (closed, not approved). This is a new, separate hypothesis; no prior strategy result is reused as proof of profitability.

## 1. Research question

Can an out-of-sample NIFTY 50 volatility-regime forecast select between (A) buying an ATM NIFTY weekly call + put (long straddle) when volatility is forecast high and (B) selling an OTM call + put, each near absolute delta 0.07 (short strangle), when volatility is forecast low, with positive net performance after realistic costs and controlled tail risk?

## 2. Aim and objectives

**Aim:** test the economic value of a volatility-regime switch, not merely forecast accuracy.

Objectives:
1. Verify weekly expired-option history availability and exact strike/time coverage before computing P&L.
2. Freeze a point-in-time regime rule using only information available by the prior NIFTY close.
3. Select actual ATM weekly contracts for the high-regime straddle and approximate ±0.07-delta OTM contracts for the low-regime short strangle.
4. Hold each structure from next-session entry to the relevant weekly expiry session close; do not substitute monthly options or same-day trades and call them weekly.
5. Reconstruct P&L with correct historical lot sizes where verified; otherwise report premium-point returns and mark rupee P&L blocked.
6. Apply Paytm Money brokerage assumptions plus exchange/statutory charges and adverse-slippage sensitivity.
7. Compare the regime switch against always-buy-straddle, always-sell-strangle, no-trade and a simple non-forecast regime baseline.
8. Report drawdown, tail loss, worst trade/week, trade counts, coverage, confidence intervals and adjusted inference.
9. Produce a structured manuscript, machine-readable outputs, data-quality report and independent tester disposition.

## 3. Frozen strategy hypotheses

### Primary signal
Use the existing technical Logistic volatility-expansion classifier at the **5-session horizon** as the primary weekly-aligned signal. Refit only on the historical development window with purged chronological folds. Determine the high-regime threshold from development-only out-of-fold probabilities (75th percentile) and low-regime threshold from the 25th percentile of the same OOF probability distribution. Never choose thresholds from option-test P&L. High regime means probability ≥ high threshold; low regime means probability ≤ low threshold; middle regime is no trade. This operationalizes “high/low predicted volatility” as forecast probability of volatility expansion; it is not a direct calibrated forecast of absolute volatility level.

### Secondary signal
Repeat with the 20-session volatility-expansion classifier as a clearly labelled secondary, horizon-mismatched analysis. Do not promote it to primary because weekly options expire on a shorter horizon.

### Position definitions
- **High regime:** buy one ATM weekly call and one ATM weekly put, using the actual strike returned at the entry timestamp; both legs must be the same expiry.
- **Low regime:** sell one OTM weekly call and one OTM weekly put, selecting each independently to the closest available absolute delta of 0.07 (tolerance ±0.02). Delta is computed from point-in-time IV/spot/strike/time-to-expiry and a documented risk-free-rate assumption if historical Greeks are absent. If the delta cannot be computed or no leg meets tolerance, skip the date; do not silently choose a farther strike.
- **Entry:** next eligible NIFTY session at the first available 5-minute bar starting 09:20 IST; price both legs at executable-side adverse-adjusted prices (buy at ask proxy / sell at bid proxy). OHLC-only data do not contain historical bid/ask, so this limitation must be explicit and slippage must be stressed.
- **Exit:** same weekly expiry date, final valid bar ending no later than 15:25 IST. If the selected exact numeric strike is not observed at exit, count a missing-contract exit and fail the coverage gate; do not use another strike or a rolling ATM-relative contract as if it were the same contract.
- **Expiry calendar:** use verified historical NIFTY weekly expiry dates, including historical weekday changes and exchange holidays. Do not assume every expiry is Thursday.
- **Sizing:** one lot per leg for research comparability. Exact expiry-specific lot sizes must come from a verifiable historical contract master. If unavailable, publish premium-point results and block rupee-based acceptance claims.

### Execution-cost cases
Primary: ₹10 brokerage per executed order, plus documented exchange charges, GST, STT, stamp duty and SEBI charges as applicable to each historical date. Sensitivity: ₹20 brokerage/order and 0/25/50/100 bps adverse slippage per option premium per side. Costs are applied per leg and per entry/exit order. Report a fee schedule/version; do not imply these are guaranteed Paytm Money charges without a dated official tariff source. Use the applicable historical statutory rates, including changes over time.

## 4. Benchmarks and outcome measures

Primary comparison: regime-switch strategy vs the better of the two always-on structures is **not** used for confirmatory model selection; report both separately. Confirmatory comparisons are:
1. Regime switch vs always-buy straddle on common eligible dates.
2. Regime switch vs always-sell 0.07-delta strangle on common eligible dates.
3. Regime switch vs no-trade (zero P&L).
4. Forecast regime vs a non-forecast historical-volatility regime baseline.

Primary endpoint: mean net P&L per eligible date in premium points and, only if historical lot sizes are verified, rupees. Secondary: return on premium/debit or margin proxy, win rate, annualized return only where mathematically justified, max drawdown, expected shortfall / 95th percentile loss, worst week, trade frequency, turnover and coverage. For naked short strangles, show theoretically unbounded upside loss exposure, observed tail losses, and stress losses; do not infer safety from a historical sample.

Use paired common-date comparisons, circular moving-block bootstrap confidence intervals, HAC/Diebold-Mariano-style paired-loss tests only where assumptions fit, and Holm correction across the frozen primary family. Report raw and adjusted p-values, effect sizes and confidence intervals. Statistical significance is not enough: positive net expectancy, robust cost sensitivity, and tail-risk limits are separate gates.

## 5. Data and provenance hierarchy

1. Cached verified NIFTY daily data and existing cached option records, with source manifest/hash.
2. DhanHQ expired rolling-option endpoint, requesting `expiryFlag=WEEK`, 5-minute data and actual strike/spot/IV/OHLC. Official documentation: https://dhanhq.co/docs/v2/expired-options-data/
3. Official NSE contract master / expiry calendar / historical derivatives reports for expiry and lot-size verification: https://www.nseindia.com/all-reports-derivatives
4. Other free public datasets only if license, provenance, exact contract identity, timestamps, and coverage are verified. Do not use unverified Hugging Face/Kaggle files as ground truth.
5. No paid-source purchase or claim of unavailability until free-source avenues are documented.

Raw option records and credentials remain out of commits, public artifacts, logs and Pages. Cache licensed/private data in the runner cache; publish only sanitized manifests and aggregates. Record every request outcome, schema validation, duplicate conflicts, gaps and hashes. Never log the access token.

## 6. Frozen quality and decision gates

- Weekly endpoint request/schema gate: must return valid weekly series; if it only returns monthly, the study is blocked rather than relabelled.
- Contract identity gate: entry/exit same expiry and exact numeric strike for every counted leg.
- Expiry/lot-size provenance gate: historical expiry calendar verified; rupee P&L only if date-specific lot size verified.
- Coverage: ≥80% eligible date coverage for each strategy structure; missing exact-strike exits count against coverage.
- Conflicting duplicate groups: ≤1%; no arbitrary duplicate winner.
- Data integrity: nonpositive/missing premiums excluded and counted; no forward-fill; no future data in signal/strike selection.
- Costs: all primary results net of fees/statutory charges and 50 bps adverse slippage; robustness at 100 bps and ₹20/order.
- Statistical gate: primary comparisons have adjusted p < .05 **and** positive confidence-interval lower bound for incremental net P&L; absolute strategy profitability requires its own positive net-P&L interval.
- Risk gate: explicit maximum drawdown / tail-loss limits must be evaluated; a statistically positive mean cannot override catastrophic short-strangle tail exposure.
- No-go if any critical data gate fails, all costs-inclusive expectancy is non-positive, robustness fails, or results rely on threshold/contract changes after inspecting test P&L. No paper/live deployment without independent tester PASS and separate explicit user approval.

## 7. Phases, deliverables and stop rules

| Phase | Work | Required artifact / gate |
|---|---|---|
| 1. Protocol and repo audit | Review parent studies, preserve prior scope, freeze signal/contract/cost rules | This plan; protocol hash; branch status |
| 2. Source/expiry/contract audit | Verify Dhan WEEK API, NSE expiry calendar, historical lot sizes and tariff schedule | `source_audit.json`, `expiry_calendar.csv`, provenance notes; block if unverified |
| 3. Data acquisition/cache | Fetch weekly options in ≤30-calendar-day windows, cache each request, validate schema/coverage/duplicates | Private cache; sanitized acquisition manifest and SHA-256 |
| 4. Signal reconstruction | Rebuild 5-session primary and 20-session secondary OOF regime probabilities | Signal manifest; no test-period threshold tuning |
| 5. Contract selection and backtest | Exact weekly expiry, ATM straddle and ±0.07-delta short strangle, same-contract exits | Trade ledger and skip/coverage report |
| 6. Cost/risk/statistical analysis | Historical fee schedule, slippage, drawdown/tail metrics, bootstrap/Holm | Metrics CSV/JSON, charts, frozen comparisons |
| 7. Developer quality gate | Unit tests for expiry, strike identity, delta, cost signs, missing data, look-ahead | Automated tests + developer report |
| 8. Independent tester | Separate tester branch; independently reproduce formulas, ledger totals, p-values, CIs, gates | PASS / PASS WITH LIMITATIONS / FAIL report; developer must address findings |
| 9. Manuscript and closure | Results, discussion, limitations, appendices and links; update root README/status/error/interaction logs | Manuscript; final go/no-go; stop after tester disposition |

No repeated parameter searches. One bounded corrective run is allowed only for a reproducible implementation defect that does not change the frozen hypothesis. If a required data source/gate is unavailable, stop with a documented blocked/inconclusive result instead of manufacturing a result or broadening the search.

## 8. Current status and initial known risks

## 9. Resume checkpoint — 2026-10-15

- A bounded correction was made to the source-probe matrix in commit `8755f4b2739762982595571ab95937cc7da67bd0`, adding `WEEK expiryCode=3` to the already bounded candidate set; it does not alter strategy hypotheses or thresholds.
- The last persisted sanitized source audit (2026-10-15 03:27 UTC) reports structurally valid 5-minute CALL and PUT arrays for `WEEK` codes 1 and 2 (375 rows per side in the five-day probe), with monotonic timestamps. `WEEK` code 0 returned the explicit error `expiryCode is required`; the monthly control passed. This establishes schema availability for candidate codes, not actual expiry mapping, stable contract identity, historical coverage, or profitability.
- **Current gate:** Phase 2 partial PASS (weekly schema candidates found); exact expiry/contract identity and coverage are still NOT VERIFIED. Phase 3–9 remain NOT STARTED. No P&L computation or strategy conclusion is permitted until expiry mapping and contract identity pass.
- Next bounded action: inspect the newly triggered workflow and sanitized artifact for code 3; then map each returned series to verified expiry dates and confirm same numeric strike/expiry across entry and exit. If the endpoint cannot establish this without guessing, stop as BLOCKED and do not use monthly data as a substitute.



- **Phase 1:** in progress; plan frozen on developer branch.
- **Phase 2:** pending API/contract source check.
- **Phase 3–9:** not started.
- Prior option studies found quote-coverage and duplicate-conflict failures. The earlier option-buying study tested monthly rolling series and same-session trades, not this weekly-to-expiry strategy.
- The prior prediction work's volatility-expansion classifier showed exploratory predictive signal, but this does not prove an options edge.
- Main technical risk: rolling ATM-relative series are not stable contract identifiers. The implementation must reconstruct exact numeric strikes and expiry; otherwise coverage/identity gate fails.
- No strategy is approved. No live orders are in scope.

## Developer-to-tester instructions

At the end, independently verify expiry/strike identity, delta selection, look-ahead controls, historical fee/lot-size arithmetic, sign conventions, missing-data treatment, cost monotonicity, paired-date comparisons, bootstrap/Holm math, and every gate. Do not accept a result merely because unit tests pass.

## Tester-to-developer instructions

Return a line-item reproducibility report with exact paths, independently recalculated figures and blockers. If any hard gate fails, request only the smallest frozen-protocol correction; never tune strategy parameters to rescue performance.


## Protocol amendment log — 2026-10-15 (source gate only)

The first automated request using documented WEEK / expiryCode=0 returned HTTP 400 with sanitized provider message “expiryCode is required”, while MONTH / expiryCode=1 passed schema validation. This is consistent with a provider validation issue for code 0, not proof that weekly data are unavailable. One bounded diagnostic correction tests WEEK codes 0, 1 and 2 against the monthly control. The strategy rules, thresholds, costs and acceptance gates are unchanged. Any successful WEEK code must still be mapped to actual expiry dates; a schema pass alone does not clear contract identity.

## 2026-10-15 bounded source-gate checkpoint

Phase 2b is **BLOCKED** pending verified mapping of Dhan weekly expiry codes to actual expiry dates and proof of exact contract continuity. See [source-gate disposition](../reports/vol_regime_options/SOURCE_GATE_DISPOSITION.md). The persisted code-1/code-2 schema probe is insufficient to establish expiry dates or a fixed-contract entry/exit series; the persisted audit predates the code-3 probe edit. The HF fallback audit file was not present on the developer branch and its dataset license is marked `other`, so it is not accepted as confirmatory evidence. No P&L phase has run. Hypothesis/parameters remain frozen; do not substitute monthly options or weaken gates. Independent tester to make one bounded check, then either identify verifiable provenance or close BLOCKED.


## Final bounded source-gate disposition — 2026-10-15

The workflow log confirms candidate WEEK codes 1, 2 and 3 return structurally valid CALL/PUT arrays in the five-day probe. Code 3 returned 357 CALL and 349 PUT rows. The workflow was canceled during the Hugging Face fallback probe by a runner shutdown signal; no HF audit result is available. The available Dhan fields still do not map the rolling expiry code to actual expiry dates or prove exact contract continuity across entry and expiry exit. The independent tester's disposition is BLOCKED. This frozen study stops here: no full data acquisition, P&L, statistical comparison, or strategy approval. Any renewed effort must begin as a new version after a verifiable contract-level source is identified.