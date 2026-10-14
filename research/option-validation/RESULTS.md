# Option-buying validation results — OPT-BUY-1.0

**Last updated UTC:** 2026-10-14T09:29:18.472712+00:00
**Decision status:** BLOCKED_REQUEST_AUTH_OR_SCHEMA
**Acquisition status:** BLOCKED_REQUEST_AUTH_OR_SCHEMA

This report never treats volatility-classification accuracy as option profitability. The original NIFTY-PRED-1.0 study remains closed and unchanged. Raw Dhan option quote files are not published.

## Empirical result

**BLOCKED_REQUEST_AUTH_OR_SCHEMA** — Dhan historical option acquisition was blocked; no option P&L is claimed.

Option requests planned: 196; successful/empty: 0; failed: 1.

No option profit/loss result is claimed. The next decision is a data-quality/credential gate, not selection of a trading structure.

## Files and reproducibility

- Sanitized acquisition summary: reports/option_validation/acquisition_summary.json
- Classifier metadata and fixed OOF thresholds: reports/option_validation/classifier_manifest.json
- Quote coverage: reports/option_validation/quote_quality.json
- Primary comparisons: reports/option_validation/primary_comparisons.csv
- Cost sensitivity matrix: reports/option_validation/performance.csv
- Sanitized trade-outcome ledger: reports/option_validation/trade_ledger.csv
- Raw option responses remain only in Actions cache at data/cache/options_rolling and are not uploaded.

Developer handoff: independently inspect data/strike/time matching, cost formulae, date cutoff and results ledger before recommending even paper-trading validation.
