# Independent tester report — NIFTY-PRED-1.0 corrective audit

**Audit date:** 2026-10-22 (Asia/Kolkata)  
**Status:** BLOCKING DEFECT CONFIRMED IN PRIOR RUN; CORRECTIVE-RUN REVIEW PENDING  
**Prior run:** [GitHub Actions #39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966)  
**Prior commit:** `cecac3a63878d3a189c94b143f875bcb9be33983`  
**Prior artifact SHA-256:** `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`  
**Developer correction commit:** `e8133a582cbe6c06ce46514f871d1393fc142f6f`  
**Corrective workflow:** [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) (must be inspected after completion)

## Independence and scope

This report records an independent inspection of the published prior-run artifact and the target-construction source. It does not claim to be a completed review of the corrected run while that run is still executing. No strategy or options-P&L testing is in scope.

## Confirmed finding — high severity / blocks final sign-off

I downloaded the run #39699761966 workflow artifact and inspected its `predictions.csv` (291,886 rows, 11 columns). **798 rows have a missing `target_date` while `actual`, `prediction`, and `baseline` are populated.** The rows are concentrated in forward-volatility and volatility-expansion outcomes:

| Task | Horizon | Rows with missing target date |
|---|---:|---:|
| Volatility | 5 sessions | 60 |
| Volatility | 20 sessions | 360 |
| Volatility expansion | 5 sessions | 54 |
| Volatility expansion | 20 sessions | 324 |
| **Total** | | **798** |

This is 6 missing-target-date rows per evaluated model at horizon 5 and 36 per evaluated model at horizon 20. The feature builder uses `fr.std(axis=1, ddof=1)`; pandas skips missing values by default. At the dataset boundary, partial forward windows were consequently allowed to form targets. The affected rows are not valid observations for the declared 5-/20-session target because no corresponding target date exists.

The prior run’s successful workflow status and aggregate summary JSON do not override this row-level finding. It invalidates unqualified sign-off for those horizon/task results. The 1-session volatility result has no missing target dates in this specific defect family, but it still lacks a completed, new independent-period replication and requires reconciliation with the corrected artifact before it can be promoted beyond a replication candidate.

## Developer correction observed

Commit `e8133a582cbe6c06ce46514f871d1393fc142f6f` changes the multi-session volatility target construction to `std(..., skipna=False)` and adds a boundary regression test requiring each task’s last h labels to be missing for h in {1, 5, 20}. This is a plausible local correction, not yet a passed gate: the complete workflow and regenerated output must be checked.

## Required independent review after corrective run #39704420478 completes

1. Confirm the workflow conclusion, all test results, and new artifact SHA-256.
2. Inspect the new prediction artifact. Require zero missing `target_date` among any rows emitted as evaluated predictions, and ensure no NaN or partial-window target is evaluated.
3. From the regenerated feature matrix or focused tests, verify tail labels for volatility and volatility expansion are NA over the full declared h-session window; verify the preceding eligible row is valid.
4. Independently recompute selected 1-session volatility forecast metrics from saved predictions, including positive variance transformation, QLIKE direction/sign, HAC p-value, block-bootstrap confidence interval, and Holm adjustments for the exact declared testing family.
5. Verify each key number cited in RESULTS.md and MANUSCRIPT.md matches the corrected artifact; confirm the one-session candidate is described as a narrow replication candidate rather than a trading edge.
6. Preserve prior-run defect history and keep historical results clearly distinguished from the corrected result.

## Current gate decision

**FAIL / HOLD FOR FINAL SCIENTIFIC SIGN-OFF on prior run #39699761966.** The 798 invalid target-date rows are confirmed. The correction is committed, but this tester report remains pending until the corrective workflow is complete and its artifact is reviewed. No phase may advance to final publication approval based solely on a green workflow status. No trading strategy, option P&L, paper trading, or live deployment is approved.

## Developer instructions

After run #39704420478 completes, submit the artifact and exact commit to this branch for independent review. Do not change thresholds, testing families, or the model catalogue to obtain a preferred result. If any evaluated target-date or arithmetic discrepancy remains, return a defect-specific disposition and require one bounded correction; otherwise issue a final PASS WITH SCOPE LIMITATIONS or FAIL with reproducible evidence.
