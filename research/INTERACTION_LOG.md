# Auditable activity / interaction log

Record user-facing decisions, concrete operations, results and links. This is not a verbatim transcript and must never contain private internal reasoning or hidden chain-of-thought.

## 2026-10-14 — initialization

- User requested fresh NIFTY 50 prediction research; no trading-strategy development; nine fixed phases; broad model comparison; robust statistics; separate developer/tester branches; manuscript; automated workflows and logs.
- Checked GitHub metadata for vishnuvcr/Naked-Options-v2. Repository is public, default branch main, initially reported size 0. README retrieval returned not found. Branch search returned no branches.
- Initialized README.md; first commit SHA returned by GitHub was e0b634fdb98da9a2ed136320a24afb7fdda8afb9.
- Searched the Project Library for previous studies and literature. Found a NIFTY ML paper in Cureus Journal of Computer Science (published 2026-10-01) and prior manuscripts from other research repositories. Read selected methods/results/limitations/reference pages. Treated these as contextual literature, not fresh output from this repository.
- Researched official NSE NIFTY 50 and India VIX pages, NSE historical reports, Dhan API support docs, NIFTY forecasting papers, Diebold-Mariano and Clark-West tests, White's Reality Check and data-snooping / PBO literature.
- Created the frozen research plan, questions, literature matrix, data catalog, experiment log, preliminary results register, phase status, error log, tester checklist, manuscript shell and reproducibility guide.
- At this checkpoint no source data API has been called, no market dataset has been acquired, no model has been trained, and no Actions run or Pages deployment is claimed.

## Interaction summary policy

Log actions and outcomes rather than private reasoning or a word-for-word chat transcript. If a workflow later runs, record its actual run ID / URL and status. If it fails or is not observable, state that honestly.

## 2026-10-14 — first data validation, compute bound, and source expansion

- Actual GitHub Actions logs (run 29) showed the Dhan cache contained 4,901 NIFTY daily records dated 2007-01-02 through 2026-10-13, with SHA-256 b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050. No API token value was printed.
- Run 29 reported 20 weekend-dated records and the first version of the validator rejected them. Review concluded that weekend dates can include special exchange sessions; the validator was changed to report the dates as a warning and preserve them rather than silently discard observations. Later run 30 and run 31 passed the target validation, tests and feature-matrix steps.
- Target-construction and metric tests passed 8/8 in the inspected Actions log. This is test evidence, not a forecast performance result.
- A full catalogue run remained in the technical-model step long enough to trigger the fixed plan's compute budget. Sequence comparisons were bounded to next-session return/direction, three training epochs, two chronological folds; all other sequence target/horizon pairs are explicitly marked not run under the budget.
- Independent code inspection found that the metric field called out-of-sample R-squared used the realized holdout sample mean rather than a forecast available at the origin. The phase-5 branch was corrected to report benchmark-relative R-squared (1 - candidate MSE / benchmark MSE). The corrected run and a unit-test confirmation remain required before adopting results.
- Public free-source review recorded official NSE index/India VIX/breadth/FII-DII/derivatives reports and two Hugging Face options collections. The collections are not ingested yet: one is CC-BY-NC-4.0 and ~4 GB, the other has 'other' licensing, ~2.5 GB and incomplete intraday OI/settlement fields. See DATA_CATALOG.md.
- At the last check, run 30 on main, run 31 on research/phase-5-models, and the corrected run 32 were respectively active/active/queued. No completed model metrics have yet been accepted.


## 2026-10-14 — separate option-buying validation initialized

- User approved extending the closed prediction-only study with a separate, bounded option-buying validation phase. The original NIFTY-PRED-1.0 plan/results remain unchanged.
- Audited README, the frozen plan, data catalog, execution policy, phase status, results register, error log, experiment log, original workflow, feature-construction code, classifier/model-selection implementation and source availability before initiating this track.
- DhanHQ v2 expired-options documentation describes historical rolling-option intraday OHLC/IV/OI/spot data, up to 30 calendar days per request and a rolling five-year window. The current option-chain endpoint is real-time, so it cannot substitute for historical option quotes.
- Scope chosen: same-session intraday entry/exit only. Rolling relative strikes/expiry data do not prove a stable contract can be tracked across multiple days; multi-day P&L is excluded unless contract identity and expiry are available and verified.
- Cost plan includes Paytm Money ₹10/order baseline, ₹20/order sensitivity, option-sale STT, stamp duty, SEBI/exchange charges and adverse 0/25/50/100 bps-per-side slippage sensitivity. Since the rolling OHLC source lacks historical bid/ask, this is a sensitivity analysis, not an observed-spread simulation.
- No historical option data has yet been downloaded and no option P&L has been computed at this point. The log records auditable actions and decisions, not hidden reasoning or verbatim internal chain-of-thought.


## 2026-10-14 — option source diagnostic update

- Verified official DhanHQ expired-options documentation and official DhanHQ-Py request construction. Dhan documents POST /charts/rollingoption, NSE_FNO, NIFTY securityId 13, instrument OPTIDX, intervals 1/5/15/25/60, MONTH/WEEK, and a maximum 30-day range; the published example uses MONTH and expiryCode=1. Sources: https://dhanhq.co/docs/v2/expired-options-data/ and https://github.com/dhan-oss/DhanHQ-py/blob/main/src/dhanhq/_historical_data.py
- Runs #4 and #5 failed at the first request with HTTP 400 and zero acquired option records. No option strategy result is claimed.
- Updated the adapter to use the published MONTH/1 example and capture a short redacted error detail. Run #6 is the retest for that request format.
- Verified official NSE costs: option-sale STT was 0.10% through 2026-03-31 and is 0.15% from 2026-04-01; option stamp duty is 0.003% on buyer turnover; SEBI turnover fee is ₹10/crore; NSE Circular 1 dated 2026-02-27 gives a combined equity-options charge outflow of approximately ₹3,553/crore from 2026-03-01. Sources: https://www.nseindia.in/static/products-services/equity-derivatives-securities-transaction-tax, https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies, https://nsearchives.nseindia.com/content/circulars/FA73061.pdf
- Paytm Money's current public F&O FAQ lists ₹10 brokerage per executed unique order: https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web. ₹20/order remains the sensitivity case.
- No live order will be placed. The test is intraday-only and stays blocked until options quotes, cost accounting, statistics and independent review pass.