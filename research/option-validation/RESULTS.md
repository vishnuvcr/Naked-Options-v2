# Option-buying validation results — OPT-BUY-1.0

**Last updated UTC:** 2026-10-14T09:44:11.830793+00:00
**Decision status:** INCONCLUSIVE_PARTIAL_OR_INCOMPLETE_DATA
**Acquisition status:** PASS

This report never treats volatility-classification accuracy as option profitability. The original NIFTY-PRED-1.0 study remains closed and unchanged. Raw Dhan option quote files are not published.

## Primary comparisons

Primary costs are ₹10/order and 50 bps adverse slippage per premium side. Returns are mean daily net premium return (non-alert dates are 0); P&L is calculated using a date-based lot-size proxy.

| Alert horizon | Structure | Alert trades | Mean daily net return | 95% block CI | Always-buy mean | Paired diff | Paired 95% CI | Raw p | Holm p | 100 bps positive? | Half 1 / half 2 positive? | Gate |
|---:|---|---:|---:|---|---:|---:|---|---:|---:|---|---|---|
| 5 | straddle | 44 | -2.831% | -4.054% to -1.752% | -10.537% | 7.706% | 5.551% to 10.033% | 0.0005 | 0.0020 | False | -2.992% / -2.672% | NO |
| 5 | strangle | 44 | -3.393% | -4.895% to -2.077% | -12.521% | 9.128% | 6.479% to 12.014% | 0.0005 | 0.0020 | False | -3.663% / -3.127% | NO |
| 20 | straddle | 60 | -3.609% | -5.026% to -2.411% | -10.537% | 6.928% | 4.594% to 8.969% | 0.0005 | 0.0020 | False | -4.435% / -2.792% | NO |
| 20 | strangle | 60 | -4.361% | -6.193% to -2.841% | -12.521% | 8.160% | 5.360% to 10.651% | 0.0005 | 0.0020 | False | -5.471% / -3.264% | NO |

## Cost and execution notes

- Four executed orders per completed 2-leg intraday trade; brokerage sensitivity is ₹10/₹20 per order.
- Option sale STT: 0.10% through 2026-03-31, 0.15% from 2026-04-01. Buyer stamp duty 0.003%, SEBI turnover fee, current exchange transaction-fee approximation and GST are included.
- Slippage is charged by increasing each entry premium and reducing each exit premium by 0/25/50/100 bps per side. This is a stress proxy because historical bid/ask is absent from the rolling endpoint.
- Currency P&L uses a date-based lot-size proxy; premium-point returns and costs are more reliable than treating proxy lot-sized P&L as exact contracts.

## Data quality and limitations

- Options acquisition status: PASS; requests failed: 0.
- Quote coverage: {'straddle': 0.17448979591836736, 'strangle': 0.17448979591836736}.
- Skip counts: {'MISSING_SAME_STRIKE_EXIT': 1607, 'MISSING_ENTRY_BAR': 6, 'MISSING_EXIT_BAR': 2, 'NO_COMMON_CALL_PUT_STRIKES': 2, 'NO_ONE_STEP_OTM_STRIKES': 1}.
- Conflicting duplicate quote groups: 45.
- This only tests intraday positions. It does not prove multi-day straddles/strangles, because rolling relative strikes are not stable contract identifiers.
- One chronological historical sample cannot establish live profitability. Even a passing gate supports only a prospective paper-trading validation, not live deployment.

## Files and reproducibility

- Sanitized acquisition summary: reports/option_validation/acquisition_summary.json
- Classifier metadata and fixed OOF thresholds: reports/option_validation/classifier_manifest.json
- Quote coverage: reports/option_validation/quote_quality.json
- Primary comparisons: reports/option_validation/primary_comparisons.csv
- Cost sensitivity matrix: reports/option_validation/performance.csv
- Sanitized trade-outcome ledger: reports/option_validation/trade_ledger.csv
- Raw option responses remain only in Actions cache at data/cache/options_rolling and are not uploaded.

Developer handoff: independently inspect data/strike/time matching, cost formulae, date cutoff and results ledger before recommending even paper-trading validation.
