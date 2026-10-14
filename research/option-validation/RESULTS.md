# Option-buying validation results — OPT-BUY-1.0

**Last updated UTC:** 2026-10-14T10:08:50.809817+00:00
**Decision status:** INCONCLUSIVE_PARTIAL_OR_INCOMPLETE_DATA
**Acquisition status:** PASS

This report does not treat volatility-classification accuracy as option profitability. The original NIFTY-PRED-1.0 study remains closed and unchanged. Raw Dhan option quote files are not published.

## Primary comparisons

Primary costs are ₹10/order and 50 bps adverse slippage per premium side. The primary outcome is daily net P&L in rupees per one-lot-proxy trade slot: an alert-filtered strategy holds cash (zero P&L) on non-alert dates, while always-buy enters one lot on each identical eligible date. The paired difference and Holm test use that common daily P&L series. Premium-normalized return is secondary because its denominator varies by trade and is undefined on no-trade dates.

| Alert horizon | Structure | Alert trades | Alert net P&L/date (₹) | 95% block CI (₹) | Always-buy net P&L/date (₹) | Paired difference/date (₹) | Paired 95% block CI (₹) | Raw p | Holm p | Mean net return/trade | Positive at 100 bps? | Half 1 / half 2 P&L/date (₹) | Gate |
|---:|---|---:|---:|---|---:|---:|---|---:|---:|---:|---|---|---|
| 5 | straddle | 224 | -315.71 | -405.17 to -230.81 | -1097.15 | 781.44 | 653.66 to 924.65 | 0.0005 | 0.0020 | -6.316% | False | -210.08 / -421.09 | NO |
| 5 | strangle | 178 | -349.35 | -449.83 to -258.22 | -1265.49 | 916.14 | 769.77 to 1070.68 | 0.0005 | 0.0020 | -10.886% | False | -265.66 / -433.04 | NO |
| 20 | straddle | 259 | -327.64 | -414.94 to -244.21 | -1097.15 | 769.50 | 587.27 to 967.60 | 0.0005 | 0.0020 | -5.751% | False | -243.83 / -411.25 | NO |
| 20 | strangle | 210 | -369.43 | -473.19 to -268.35 | -1265.49 | 896.05 | 678.13 to 1143.47 | 0.0005 | 0.0020 | -10.546% | False | -327.78 / -411.09 | NO |

## Secondary premium-return measures

| Horizon | Structure | Alert mean daily premium return | Always-buy mean daily premium return | Paired return difference | Raw p (secondary only) |
|---:|---|---:|---:|---:|---:|
| 5 | straddle | -1.719% | -5.510% | 3.791% | 0.0005 |
| 5 | strangle | -2.858% | -9.072% | 6.214% | 0.0005 |
| 20 | straddle | -1.810% | -5.510% | 3.700% | 0.0005 |
| 20 | strangle | -3.267% | -9.072% | 5.806% | 0.0005 |

## Cost and execution notes

- Four executed orders per completed 2-leg intraday trade; brokerage sensitivity is ₹10/₹20 per order.
- Option sale STT: 0.10% through 2026-03-31 and 0.15% from 2026-04-01. Buyer stamp duty 0.003%, SEBI turnover fee, current NSE transaction-fee approximation, and GST are included.
- Slippage increases each entry premium and reduces each exit premium by 0/25/50/100 bps per side. This is a stress proxy because historical bid/ask is absent from the rolling endpoint.
- Currency P&L uses a date-based lot-size proxy, not expiry-specific contract-master lot sizing.

## Data quality and limitations

- Requests planned / attempted / cached / failed: 686 / 490 / 196 / 0.
- Quote coverage: {'straddle': 0.8397959183673469, 'strangle': 0.6918367346938775}. The data gate requires at least 80% coverage for both structures.
- Skip counts: {'MISSING_SAME_STRIKE_EXIT': 450, 'MISSING_ENTRY_BAR': 6, 'MISSING_EXIT_BAR': 2, 'NO_ONE_STEP_OTM_STRIKES': 1}.
- Conflicting duplicate groups dropped: 452; conflict rate among duplicate groups: 1.409%.
- Rolling relative strikes are used only to follow fixed numeric strikes within one session. No overnight or multi-day option P&L is tested.
- If quote coverage is below threshold, output is INCONCLUSIVE even if a paired comparison has a small p-value.
- One historical holdout cannot establish live profitability. Even a passing gate would support prospective paper testing only, not live deployment.

## Files and reproducibility

- Sanitized acquisition summary: reports/option_validation/acquisition_summary.json
- Classifier metadata and fixed OOF thresholds: reports/option_validation/classifier_manifest.json
- Quote coverage: reports/option_validation/quote_quality.json
- Primary comparisons: reports/option_validation/primary_comparisons.csv
- Cost sensitivity matrix: reports/option_validation/performance.csv
- Sanitized trade-outcome ledger: reports/option_validation/trade_ledger.csv
- Raw option responses remain only in Actions cache at data/cache/options_rolling; they are not committed or uploaded.

Developer handoff: independently inspect date/strike matching, costs, P&L units, split integrity, and all acceptance gates before discussing even paper-trading validation.
