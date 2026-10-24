# User-Visible Interaction and Decision Log — NWCP-1.0

This log tracks visible research scope changes and decisions, not private hidden chain-of-thought.

## 2026-10-24 — Research restart

**User request (verbatim):**
> Hey let's freeze and forget everything  
> Let's restart a new research  
>   
> NIFTY WEEKLY CANDLE PREDICTION  
>   
> This research's sole purpose is just to predict if nifty value at the end of weekly expiry would be greater than lesser than that of nifty value at 10 am of the next trading day to the previous weekly expiry!  
>   
> Use quant evolve, tradingview open source pine code indicators/strategies, your own new invented indicators, etc

**Protocol decisions:**
- Research ID NWCP-1.0; separate from existing NIFTY prediction and naked-option strategy research.
- Target direction from NIFTY 50 spot value at 10:00 IST on the first trading day after prior actual weekly expiry to NIFTY 50 spot close on the next actual weekly expiry.
- UP if expiry close is above anchor; DOWN if below; exact ties recorded separately and excluded from primary binary metrics.
- Forecast cutoff is 10:00 IST; only point-in-time available features eligible.
- Use bounded QuantEvolve-style evolution, audited open-source Pine indicator ports and original hypothesis-driven indicators.
- No option strategy, P&L optimization or live trading development in this study.
- Historical expiry conventions, source licensing, target timestamps and look-ahead tests must pass before model discovery.
