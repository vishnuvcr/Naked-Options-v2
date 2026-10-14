# OPT-BUY-3.0 research questions and hypotheses

This file is part of the frozen [OPT-BUY-3.0 plan](OPTION_ENTRY_EXIT_PLAN.md). The protocol is fixed before outcome computation.

## Primary question
Which, if any, of the registered NIFTY 50 long-option entry × compatible exit combinations has positive mean net P&L per scheduled eligible session after Paytm Money brokerage, statutory/exchange-fee estimates, GST and slippage, with adequate data coverage and multiple-testing-adjusted evidence?

## Secondary questions
1. How do seeded random entries compare with simple fixed-time and deterministic rule-based entries?
2. How do fixed duration, EOD, premium target/stop, trailing stop and underlying/signal exits alter after-cost trade outcomes?
3. Do results survive 100 bps adverse slippage per premium side and both chronological halves?
4. Does apparent expectancy vary by prior-known volatility or trend regime, if adequate point-in-time regime inputs are cached?
5. How many apparent candidates are removed by missing quotes, duplicate conflicts, small samples and family-wise statistical correction?

## Hypotheses
- H0: candidate mean net P&L/date <= 0.
- H1: candidate mean net P&L/date > 0.
- Robustness: candidate remains net-positive at 100 bps/side and in both chronological halves.
- Relative comparison: candidate exceeds a matched random/simple control; this is not sufficient without positive absolute expectancy.

## Primary metric
Mean after-cost rupee P&L over scheduled eligible sessions; no-trade sessions are zero, while missing outcome for a generated signal remains NA and is charged against completion/coverage gates.

## Statistical protocol
Circular block bootstrap, 2,000 replicates, five-session block, one-sided null-centered test of positive expectancy, Holm correction over every eligible entry × compatible exit. Report the full candidate family, including incompatible/blocked cells and blank p-values, without dropping failures from the status report.

## Approval gate
No candidate is accepted without passing every preregistered data-quality, coverage, sample-size, primary-CI, 100-bps, half-sample, Holm and independent tester gate in OPTION_ENTRY_EXIT_PLAN.md. The existing >1% duplicate-conflict condition is a frozen stop against confirmatory status, not permission to loosen the gate.
