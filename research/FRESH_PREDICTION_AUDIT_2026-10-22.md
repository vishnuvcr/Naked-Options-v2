# Fresh NIFTY prediction audit — 2026-10-22

## Scope

Continue NIFTY-PRED-1.0 strictly as a bounded prediction study. The frozen plan is unchanged. This audit documents a target-integrity defect found in the latest completed workflow, the narrow correction, and the tester gate.

## Evidence

- Prior workflow: [#39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966), head commit `cecac3a63878d3a189c94b143f875bcb9be33983`.
- Artifact: `nifty-prediction-reports-39699761966`, SHA-256 `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`.
- Inspected `predictions.csv`: 291,886 rows; 798 rows have null `target_date` but populated `actual`, `prediction`, and `baseline`.
- Breakdown: volatility h5=60, volatility h20=360, volatility-expansion h5=54, volatility-expansion h20=324.
- At the prior data boundary, `fr.std(axis=1, ddof=1)` skipped missing future-return values and allowed partial windows to produce nonmissing labels. The evaluated rows consequently did not all represent the declared h-session forward target.

## Research questions for this corrective audit

1. Does every emitted out-of-sample forecast correspond to a fully observed future target window and a nonmissing target date?
2. Does the defect-specific correction pass boundary and regression tests?
3. Does the reported one-session global ExtraTrees volatility-proxy comparison remain arithmetically consistent when reconstructed from the saved corrected predictions?
4. Do every stated p-value, confidence interval, Holm family and manuscript claim match the corrected artifact?

## Correction performed

- Developer branch: [research/fresh-prediction-developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-developer).
- Commit: `e8133a582cbe6c06ce46514f871d1393fc142f6f`.
- Changed the h-session forward-return standard deviation to `std(axis=1, ddof=1, skipna=False)`, ensuring incomplete windows produce missing labels rather than silently using fewer observations.
- Added a regression test requiring the final h labels for volatility and volatility-expansion targets to be missing at h=1,5,20, and requiring the preceding eligible target to remain valid.
- Corrective workflow [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) was triggered automatically and was in progress at the last observation. Its successful completion is not assumed.

## Independent review

The post-results review branch [research/fresh-prediction-independent-tester](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-independent-tester) contains the audit disposition. It records a blocking finding on the prior run and requires exact artifact, target-date, tail-window, metric/sign, CI/HAC and Holm checks on the corrected run before a final decision.

## Current scientific interpretation

- The latest prior workflow's green status was operational evidence, not sufficient proof of complete future-label construction.
- The affected h5/h20 volatility and volatility-expansion results are blocked pending the correction.
- Return/direction forecasting has not established a robust edge under the prior protocol.
- The one-session global ExtraTrees volatility-proxy result has no missing target dates in this specific defect family, but it remains a narrow replication candidate until the tester reconciles the corrected artifact and familywise inference.
- A genuinely independent future-period replication is not available from the current data window. The small post-holdout extension is inadequate and previously screened historical folds cannot be relabeled as untouched replication. Record this as future work rather than making an unsupported claim.
- No options P&L, strategy, paper trading or live deployment is approved.

## Finalization gate

Do not close the correction gate until the following are documented:
1. Corrective Actions run conclusion and artifact digest.
2. Tests pass, including the new boundary regression test.
3. Zero missing target dates among evaluated predictions and no incomplete target windows.
4. Independent recomputation of the selected one-session volatility comparison and the declared Holm family.
5. Revised phase status/results/manuscript/README and final tester disposition.

