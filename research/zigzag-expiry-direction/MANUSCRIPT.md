# ZigZag++ for NIFTY 50 Weekly Expiry Direction: Protocol Manuscript

## Abstract
This protocol specifies a prediction-only evaluation of the ZigZag++ [LD] indicator for forecasting whether NIFTY 50 spot finishes above or below a defined reference price at the next actual weekly expiry. No empirical score is claimed because causal reconstruction and data validation are incomplete.

## Introduction and research question
Technical pivot indicators can appear predictive in historical charts when pivot locations are plotted retrospectively. The central scientific question is whether the most recent confirmed pivot, using only information available at the forecast cutoff, predicts the next expiry interval's direction out of sample.

## Aim and objectives
Aim: evaluate the predictive value of the last confirmed ZigZag pivot class.
Objectives: verify source behavior; define information timing; validate market data and expiry dates; evaluate out-of-sample predictions against baselines; quantify uncertainty and coverage; publish reproducible results.

## Methods
Indicator settings: Depth 12, Deviation 5, Backstep 2, using the supplied Pine script and imported DevLucem/ZigLib/1. At the previous actual weekly expiry session close, the latest confirmed low label (LL/HL) predicts UP and latest confirmed high label (HH/LH) predicts DOWN. No eligible confirmed pivot is an abstention. Target compares the NIFTY 50 spot value at 10:00 IST on the first trading session after the previous expiry with the regular-session close on the next actual expiry; ties are separately identified. Historical expiry rules and holiday shifts must be date-specific.

## Source audit update
Public documentation confirms that the library exposes a direction and two chart points, while general ZigZag documentation warns that pivot labels are confirmed retrospectively and the latest displayed point may be revised. These are contextual source findings only; the exact ZigLib v1 implementation and its causal signal-availability timing have not been verified. Therefore no safe source-faithful backtest can be run from the supplied wrapper alone.

## Results
No empirical results have been established. The indicator library's exact causal behavior and market-data provenance remain unresolved. No accuracy, balanced accuracy, or predictive significance estimate is reported.

## Discussion
The key threat is retrospective pivot placement: the bar at which a pivot is drawn may precede the time when the indicator can confirm it. Until the library's behavior is reproduced causally, apparent chart labels cannot be used as forecast features.

## Strengths and limitations
Strengths: simple fixed rule; explicit abstention; no strategy/P&L conflation; predeclared evaluation metrics. Limitations: imported library dependency, unverified historical data provenance and expiry calendar, no confirmed out-of-sample scores, and no TradingView compilation evidence.

## Conclusion
This is a preregistered protocol, not a validated forecasting method. No conclusion about predictive performance or practical usefulness is justified yet.

## Future research
After data and implementation gates pass: conduct the fixed holdout evaluation, dependence-aware uncertainty analysis, volatility-regime breakdown, and independent reproduction if later authorized.


## Multi-timeframe sensitivity amendment
Following the user instruction to test various timeframes, the protocol now pre-registers 5-minute, 15-minute, 30-minute, 60-minute and daily variants; 1-minute is conditional on data availability and quality. The primary metric remains out-of-sample balanced accuracy, with coverage and baselines reported for every timeframe. Since multiple variants are compared, any formal tests must account for multiplicity and use comparable expiry intervals. The exact ZigLib implementation, signal availability, intraday price provenance and historical expiry schedule are still unresolved; therefore no empirical result or winner is reported.


## Data acquisition implementation status
A Dhan v2 acquisition workflow has been added for NIFTY 50 index ID 13, requesting 1m, 5m, 15m and 60m bars (plus daily bars) and deriving 30m bars from six contiguous 5m bars. Validation checks timestamp order/duplicates, timezone awareness, OHLC consistency, and records SHA-256 hashes. Dhan documents minute bars for the last five years and a maximum 90-day request window; this constrains the common intraday sample. The acquisition workflow's success and actual dataset are not yet verified, and this is not a prediction result.


## Repaint-mode limitation
The publicly accessible wrapper mirror sets repainting on by default and has a separate non-repaint branch that emits drawings only when direction changes, using prior-bar point values. The causal multi-timeframe study therefore specifies non-repaint mode and uses the time the direction change becomes available, not the historical pivot location. This setting differs from the wrapper default and any future performance result must be labeled accordingly. The mirror does not expose the imported ZigLib v1 implementation, so it does not remove the source-verification limitation.

## Final study outcome and evidence gate

### Results
No eligible forecast observations were scored. The five-minute public archive contains 92,876 rows, with sorted unique timestamps and no invalid OHLC values in the detailed audit. There are 1,244 distinct dates; 1,236 dates contain 75 bars from 09:15 through 15:25. Eight dates have nonstandard row counts or times, requiring official session classification. The combined weekend/out-of-clock diagnostic flags 315 rows, including special evening sessions. The Yahoo fallback has no timestamp overlap with the archive, so source price parity remains untested.

### Interpretation
The key implementation gate failed: the accessible documentation describes the imported ZigLib API but does not establish the exact algorithm or the time at which a pivot becomes knowable. The wrapper source mirror is not the imported library source. A generic ZigZag reconstruction would not be source-faithful and could misdate signals. Consequently, no forecast score is reported. This outcome indicates insufficient evidence to test the specified indicator rigorously in this run; it does not demonstrate that the indicator lacks predictive power.

### Conclusion
**No-go for a predictive-accuracy claim under the preregistered protocol.** No timeframe is selected as a winner. No strategy is proposed. The protocol can be resumed when exact ZigLib implementation/confirmation timestamps, official session and expiry mapping, and independent overlapping spot prices are available.

### Reproducibility and supplementary materials
- Data acquisition/audit workflow: [run #40132605202](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40132605202)
- Diagnostic audit implementation: research/zigzag-expiry-direction/audit_public_5m.py
- Source and data limitations: ERROR_LOG.md
- Preregistered protocol: RESEARCH_PLAN.md
- Dataset source: [public five-year NIFTY 5-minute release](https://github.com/voletiramu/nse-fno-1min-data/releases/tag/indices-v1.0.0)

## User instruction to proceed with available data — 2026-10-25

The user authorized continued work with the available dataset. Inspection of the downloadable workflow artifact confirms the archive includes 1m/5m/15m/30m-resampled/60m/daily CSVs and associated validation/session reports. This permits further diagnostics, but does not by itself validate the forecast target or the indicator implementation.

The primary protocol remains unchanged. The analysis will not relabel a generic ZigZag approximation as the imported ZigZag++ [LD] indicator. Until the source/confirmation-time and session/expiry gates are resolved, performance metrics remain unreported. If an explicitly exploratory proxy is evaluated later, it must be a separate experiment with its own algorithm definition, limitations, and labels, and cannot support a conclusion about the specified TradingView indicator.


## Source-quality audit update (2026-10-25)

The Dhan and independent public five-minute sources have 82,451 exact timestamp matches. About 94.99% of matching close prices differ by at most 0.05 points, but 800 rows differ by more than 1 point and the largest difference is 10.90 points. On the diagnostic subset of 78,374 rows across 1,045 dates with 75 bars in both sources, 95.52% of close pairs are within 0.05 points and 666 rows differ by more than 1 point. This subset is not an official-session classification.

The pipeline now writes Dhan, public archive, and Yahoo five-minute data to distinct paths, quarantines the old ambiguous cache with a hash record, validates a source-selected copy, and includes a cross-source report. The public archive is cached unless refresh is explicitly requested. The malformed token-renewal shell block has been replaced, but the new workflow run is not yet verified.

No prediction performance result exists. Exact ZigLib v1 signal timing, official session/expiry mapping, and candle timestamp semantics remain open, so forecast scoring is still blocked. This indicates insufficient evidence for the registered experiment, not absence of predictive value.
