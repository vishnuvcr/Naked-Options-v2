# Fresh NIFTY prediction request — repository continuation audit

**Date:** 2026-10-15 (Asia/Kolkata)  
**Request:** Continue the project’s “Fresh Research: NIFTY 50 Prediction” work.  
**Scope boundary:** Prediction only; do not design a trading strategy as part of this request.

## Repository evidence checked

- Read the main README, frozen research/RESEARCH_PLAN.md, research/PHASE_STATUS.md, the expanded model audit results, the prediction manuscript, error log, interaction log, and tester-branch report.
- Existing NIFTY-PRED-1.0 is already marked closed for its bounded nine-phase scope, with accepted limitations.
- Expanded PDF/model comparison workflow run [#62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792) completed successfully. The Actions job shows acquisition, validation, target tests, feature construction, technical and global model catalogues, ARIMA benchmark, report merge, and artifact upload all succeeded. Artifact SHA-256: 14c9d6fc1bcb0f00ff28e708cb10c6cab9b378e5e60ff31f6e66aaa5e977172b.
- The latest result summary states that the bounded model comparison did not establish a robust return/direction winner. One-session global XGBoost volatility QLIKE improvement is reported after configured Holm correction; this does not establish general predictive superiority or a trading signal.
- Important unacquired/unverified input families remain: historical options/PCR, FII/DII, breadth, timestamped news, corporate actions/point-in-time constituents, and robust global close-time/holiday alignment. Twenty weekend-dated observations were retained and flagged for calendar verification.

## Integrity issue found during continuation

The main README and result narrative refer to run #62 and say the independent tester passed with scope limitations. However, the currently readable file research/PDF_METHOD_AUDIT_TESTER_REPORT.md on research/pdf-audit-tester-final still identifies run #60 and gives **FAIL FOR FINAL SCIENTIFIC SIGN-OFF**, with blocking target-date and inference/reporting issues. The report is therefore stale relative to the claimed run #62 closure, unless a newer independent review exists elsewhere. A successful workflow alone is not a substitute for the missing tester evidence.

## Disposition

- Do not claim the study has an unqualified scientific sign-off until the tester artifact is reconciled with run #62 and its zero-null-target-date, metric, multiple-testing, and manuscript claims are checked.
- Do not rerun or expand the model catalogue merely to search for a winner. The frozen prediction scope is bounded; only a defect-driven verification run is justified.
- Do not start strategy development under this prediction-only request.
- Keep the published conclusion conservative: no robust return/direction edge demonstrated by the tested data and protocol; selected volatility result is narrow and must remain tied to its specified metric and correction family.

## Tester instructions

Independently locate the actual tester report and artifact for run #62 (or document that none exists), verify target-date completeness and correct horizon alignment, recompute key metric/sign conventions and Holm families from saved predictions, and reconcile every manuscript headline to the artifact. Do not mark PASS unless these checks are evidenced. If the report on the tester branch is stale, update it only after the independent checks are complete; preserve run #60 findings in the error/history log.
