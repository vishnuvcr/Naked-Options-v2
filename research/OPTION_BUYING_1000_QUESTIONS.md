# OPT-BUY-4.0 — Research questions and hypotheses

## Primary question
Among at least 1,200 preregistered NIFTY 50 single-leg long-call/long-put entry × strike × exit configurations, does any show positive out-of-sample net rupee expectancy after modeled costs and pass data-quality, uncertainty, multiple-testing and stability gates?

## Secondary questions
1. Which entry families, if any, improve net expectancy relative to matched random-time/random-direction and fixed-time controls?
2. How do strike bucket and exit policy interact with entry family?
3. Does any result survive 100 bps adverse slippage per premium side and ₹20 brokerage per executed order?
4. Are candidate outcomes stable across chronological halves and prior-known volatility/trend regimes?
5. How much do missing bars, conflicting duplicate quotes, contract/lot-size uncertainty, and fee/slippage assumptions affect inference?
6. Do any apparent winners remain after Holm family-wise correction across the full confirmatory family?

## Hypotheses
- H0: every tested candidate has mean net expectancy per scheduled eligible session <= 0, or fails at least one frozen validity gate.
- H1: at least one candidate has positive out-of-sample expectancy, a positive 95% lower confidence bound, corrected statistical support, robust cost sensitivity, adequate coverage/trade count, and stability in both chronological halves.
- H2: rule-based entries improve on matched controls after costs; this is secondary and cannot substitute for H1.
- H3: exit-policy differences are reproducible on common dates, rather than artifacts of different eligible samples.

## Primary estimand
Mean net rupee P&L per scheduled eligible session, including zero on no-trade sessions, under the frozen primary cost setting. Secondary estimands: net P&L per completed trade, win rate, profit factor, drawdown, trade frequency and paired difference against matched controls.

## Analysis commitments
Use chronological splits, no look-ahead, a frozen cell registry, common-date controls, block-bootstrap confidence intervals, raw and Holm-adjusted p-values, and full reporting of failed/blocked cells. No live-trading conclusion follows from retrospective screening alone.
