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

## 2026-10-24 — First automated workflow and corrective run

- User instructed: “Proceed. Run the workflow yourself.”
- Triggered GitHub Actions run [#14](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40104096953). Dependency installation and unit tests completed; **13 tests passed**. The data/baseline stage then failed with KeyError f1 in the evolutionary search because archive wrapper records were carried forward as candidates.
- Logged the defect as NWCP-E011. Corrected the evolutionary generation population to carry candidate dictionaries, adjusted mutation/crossover references, and added a multi-generation regression test.
- Corrective push run [#18](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486) completed successfully. The workflow reports **14 tests passed**, **398 valid labels**, **398 features**, and decision status `OOS_GATE_NOT_PASSED_OR_INSUFFICIENT`.
- Operational pipeline completion is not a scientific pass. No accuracy edge or winning rule is accepted; source provenance, timestamp semantics, expiry completeness, and OOS gate details still require audit.


## 2026-10-24 — Results artifact audit and manuscript

- User said “Ok proceed.” Retrieved and inspected sanitized artifact from [run #18](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486).
- Results: 884,552 one-minute bars; 398 labels (224 UP / 174 DOWN); 10 excluded intervals; 28 features; 120 sealed test labels. Evolved rule balanced accuracy 0.577, Holm-adjusted p=0.1159; logistic balanced accuracy 0.558, reported Holm-adjusted p=0.0107. The evolved rule does not pass its adjusted significance gate. No method is accepted as a predictor.
- New audit defects NWCP-E012–E015: Dhan security ID/source overlap failure, expiry aggregate count reconciliation, inconsistent evolved-rule bootstrap p-value, and unresolved public source provenance/timestamp semantics.
- Added [RESULTS.md](RESULTS.md) and [MANUSCRIPT.md](MANUSCRIPT.md). Phase remains DATA-LIMITED / NO CONFIRMATORY CLAIM; no further tuning against the sealed test is permitted.
