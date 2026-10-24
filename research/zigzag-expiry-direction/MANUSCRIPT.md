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

## Results
No empirical results have been established. The indicator library's exact causal behavior and market-data provenance remain unresolved.

## Discussion
The key threat is retrospective pivot placement: the bar at which a pivot is drawn may precede the time when the indicator can confirm it. Until the library's behavior is reproduced causally, apparent chart labels cannot be used as forecast features.

## Strengths and limitations
Strengths: simple fixed rule; explicit abstention; no strategy/P&L conflation; predeclared evaluation metrics. Limitations: imported library dependency, unverified historical data provenance and expiry calendar, no confirmed out-of-sample scores, and no TradingView compilation evidence.

## Conclusion
This is a preregistered protocol, not a validated forecasting method. No conclusion about predictive performance or practical usefulness is justified yet.

## Future research
After data and implementation gates pass: conduct the fixed holdout evaluation, dependence-aware uncertainty analysis, volatility-regime breakdown, and independent reproduction if later authorized.
