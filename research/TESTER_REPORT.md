# Independent tester report

**Status:** NOT YET REVIEWED — there are no empirical artifacts at bootstrap.  
**Research version:** NIFTY-PRED-1.0.

## Independence statement

The review is intended to use a separate branch, a separate checklist and independently recomputed core metrics. A scripted self-test is not represented as a second human review. The final report must state the actual degree of independence and any permission or automation limitations.

## Required checklist

- [ ] Verify source coverage, hashes, timestamps, timezone, schema, missingness and data-use conditions.
- [ ] Verify target construction uses strictly future observations and correct horizon labels.
- [ ] Verify global-market alignment uses only data available at each forecast origin.
- [ ] Verify chronological split boundaries are frozen and holdout is not used for selection.
- [ ] Recompute regression, classification, volatility, and proper probability-score metrics from saved predictions.
- [ ] Check metric signs, denominators, units, baseline comparisons, overlapping-horizon inference.
- [ ] Verify confidence intervals, HAC / DM or Clark-West assumptions, p-values and Holm adjustments.
- [ ] Check calibration, feature importance leakage, regime thresholds and sample sizes.
- [ ] Re-run core tests in a clean environment with recorded package versions.
- [ ] Reconcile every manuscript number with a generated CSV/JSON artifact.
- [ ] Confirm failed experiments and errors remain in the logs.
- [ ] Reject unsupported claims about unrun model families, statistical significance, workflow runs or Pages deployment.
- [ ] Give PASS / CONDITIONAL PASS / REJECT with defect severity, file, reproduction, correction and retest.

## Current decision

NO DECISION. Review cannot pass before data and experiment artifacts exist. This file must be replaced with the actual findings after result acquisition.
