# Timeframe Sensitivity Protocol — ZigZag Expiry Direction

**Status:** PRE-REGISTERED; empirical execution pending.  
**Decision recorded:** User instruction on 2026-10-25: “Test various timeframes.”

## Purpose
The supplied Pine script has no explicit timeframe override, so indicator output depends on the active chart timeframe. Instead of silently choosing one, test a predeclared panel of chart-timeframe variants while keeping all other settings and prediction rules fixed.

## Variants
Primary panel, in increasing aggregation:
- 5-minute
- 15-minute
- 30-minute
- 60-minute
- 1-day

Additional 1-minute variant is conditional on validated historical spot data and adequate completeness; if the data source cannot support it reliably, mark it unavailable rather than silently substituting another interval. Use standard NIFTY 50 spot index bars, IST exchange-session timestamps, and the same indicator settings (Depth=12, Deviation=5, Backstep=2) on every timeframe.

## Fixed signal/target protocol
- At the prior actual weekly expiry session's close, use only a pivot whose signal-availability time is at or before the cutoff.
- Latest confirmed low label LL/HL => UP; latest confirmed high label HH/LH => DOWN; otherwise abstain.
- Target remains the spot index at 10:00 IST on the first trading session after the prior expiry compared with the regular-session close of the next actual expiry. Higher=UP, lower=DOWN, tie separately.
- Historical expiry dates must be built from dated exchange rules and actual holiday shifts.

## Comparability and statistics
- Score each timeframe on the same eligible expiry intervals wherever possible; also report each timeframe's full available sample and why rows differ.
- Report sample count, coverage/abstention, UP/DOWN prevalence, confusion matrix, accuracy, balanced accuracy, class precision/recall, baseline performance, and dependence-aware confidence intervals.
- The primary comparison is balanced accuracy. Report all timeframe results; do not select a winner from in-sample performance.
- Because several timeframes are tested, treat timeframe ranking as exploratory and adjust for multiple comparisons (e.g. Holm correction for any formal family of tests). Reserve a chronological holdout untouched until protocol and implementation gates pass.
- Report the same-timeframe benchmark and baseline metrics; do not compare different samples as if they were directly equivalent.

## Implementation gate
Do not calculate a timeframe's performance until (1) exact DevLucem/ZigLib/1 behavior and confirmation timing are verified or faithfully reproduced, (2) intraday spot data and timestamps pass provenance/completeness checks, and (3) the date-specific expiry schedule is validated. A generic ZigZag implementation is not proof of parity. If exact source is unavailable, publish the blocker and do not present proxy scores as results.

## Limitations and decision rule
A timeframe can change both the pivot sequence and the time a pivot becomes knowable. This is not just a parameter optimization. The comparison is scientifically valid only if each variant uses the same causal rule and comparable data. Conclude “no verified result” if required gates remain blocked; do not manufacture predictions or infer accuracy from chart screenshots.

## Required artifacts
Update PHASE_STATUS.md, ERROR_LOG.md, RESULTS.md, MANUSCRIPT.md, and INTERACTION_LOG.md after the relevant step. Cache raw data and manifests with checksums when acquired. No options strategy or trading rules are in scope.
