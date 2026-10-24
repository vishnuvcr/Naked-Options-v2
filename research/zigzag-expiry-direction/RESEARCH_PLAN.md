# ZigZag++ NIFTY Expiry-Direction Prediction — Research Plan

**Version:** 1.0  
**Status:** Protocol registered; empirical test pending; no performance claim.

## Scope
Test only whether the supplied ZigZag++ [LD] indicator predicts NIFTY 50 spot direction between weekly expiries. No options, delta rules, entries, exits, P&L, or trading strategy. This study is separate from NWCP-1.0 and must not reuse its reported results as evidence.

## Fixed signal rule
- Pine indicator: ZigZag++ [LD], imported DevLucem/ZigLib/1, Depth=12, Deviation=5, Backstep=2.
- At the previous actual expiry session's close, inspect the latest pivot confirmed and knowable at that timestamp.
- Last confirmed low label (LL or HL) => UP forecast.
- Last confirmed high label (HH or LH) => DOWN forecast.
- No usable confirmed pivot at cutoff => abstain and report coverage separately.
- Target: NIFTY 50 spot regular-session close on the next actual weekly expiry compared with the 10:00 IST spot value on the first trading session after the previous actual expiry. Higher=UP, lower=DOWN, equal=TIE. Reference and target timestamps must be exact and consistently sourced.
- Actual expiry calendar must reflect historical exchange rules and holiday shifts; do not hard-code one weekday across the full history.

## Research questions
1. Does the last confirmed ZigZag pivot class predict the next expiry interval's NIFTY 50 direction out of sample?
2. Is accuracy better than the majority-class baseline and 50% direction baseline?
3. Are results stable across time, direction class, and volatility regimes?
4. How much data is excluded because no pivot or trustworthy aligned price is available?
5. Can the historical indicator signal be reproduced without look-ahead or repainting leakage?

## Phases and gates
1. **Protocol/source audit:** record exact script/library version and cutoff/target semantics. Gate: source behavior and pivot confirmation timing understood.
2. **Data audit:** verify provenance, timestamp timezone/convention, missing bars, duplicates, spot series and historical expiry schedule. Gate: data-quality report passes.
3. **Causal signal reconstruction:** implement or extract exact ZigLib behavior; preserve signal-availability time separately from plotted pivot time. Gate: known examples and no-future-data tests pass. Python parity is not TradingView compilation.
4. **Evaluation:** chronological walk-forward/holdout only; publish confusion matrix, accuracy, balanced accuracy, UP/DOWN precision and recall, coverage, majority and 50% baselines, confidence intervals, and regime breakdowns. No tuning on final holdout.
5. **Robustness and inference:** sensitivity only as secondary analysis; multiple-testing correction if variants are explored; report uncertainty and limitations.
6. **Manuscript and decision:** publish methods, data dictionary, results, plots, tables, appendices, limitations, and reproducibility instructions. Stop after this fixed phase list.

## Statistical plan
Primary metric: balanced accuracy on eligible out-of-sample forecasts. Secondary metrics: accuracy, confusion matrix, class-specific precision/recall, coverage/abstention, Brier score only if calibrated probabilities exist. Compare with majority-class and 50% baselines. Use chronological block bootstrap or another dependence-aware interval method; do not treat adjacent expiry observations as independent without qualification. Report sample counts and confidence intervals. No claim of statistical significance without a predeclared test and verified implementation.

## Non-negotiable controls
- Never backdate a pivot's information-availability timestamp to its chart location.
- Repainting/provisional points are not eligible signals.
- Keep source files, raw/cache provenance, transformation logs, code version, and checksums.
- Missing/failed data sources are logged; do not silently fill gaps or fabricate observations.
- Do not use NWCP-1.0 scores, selected models, or labels as ZigZag results.
- Do not claim Pine compilation unless a TradingView compile result is actually observed.
- User explicitly waived independent tester review for this task; no tester gate is part of this protocol.
