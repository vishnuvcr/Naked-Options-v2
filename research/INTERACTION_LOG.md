# Auditable activity / interaction log

Record user-facing decisions, concrete operations, results and links. This is not a verbatim transcript and must never contain private internal reasoning or hidden chain-of-thought.

## 2026-10-14 — initialization

- User requested fresh NIFTY 50 prediction research; no trading-strategy development; nine fixed phases; broad model comparison; robust statistics; separate developer/tester branches; manuscript; automated workflows and logs.
- Checked GitHub metadata for vishnuvcr/Naked-Options-v2. Repository is public, default branch main, initially reported size 0. README retrieval returned not found. Branch search returned no branches.
- Initialized README.md; first commit SHA returned by GitHub was e0b634fdb98da9a2ed136320a24afb7fdda8afb9.
- Searched the Project Library for previous studies and literature. Found a NIFTY ML paper in Cureus Journal of Computer Science (published 2026-10-01) and prior manuscripts from other research repositories. Read selected methods/results/limitations/reference pages. Treated these as contextual literature, not fresh output from this repository.
- Researched official NSE NIFTY 50 and India VIX pages, NSE historical reports, Dhan API support docs, NIFTY forecasting papers, Diebold-Mariano and Clark-West tests, White's Reality Check and data-snooping / PBO literature.
- Created the frozen research plan, questions, literature matrix, data catalog, experiment log, preliminary results register, phase status, error log, tester checklist, manuscript shell and reproducibility guide.
- At this checkpoint no source data API has been called, no market dataset has been acquired, no model has been trained, and no Actions run or Pages deployment is claimed.

## Interaction summary policy

Log actions and outcomes rather than private reasoning or a word-for-word chat transcript. If a workflow later runs, record its actual run ID / URL and status. If it fails or is not observable, state that honestly.

## 2026-10-14 — first data validation, compute bound, and source expansion

- Actual GitHub Actions logs (run 29) showed the Dhan cache contained 4,901 NIFTY daily records dated 2007-01-02 through 2026-10-13, with SHA-256 b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050. No API token value was printed.
- Run 29 reported 20 weekend-dated records and the first version of the validator rejected them. Review concluded that weekend dates can include special exchange sessions; the validator was changed to report the dates as a warning and preserve them rather than silently discard observations. Later run 30 and run 31 passed the target validation, tests and feature-matrix steps.
- Target-construction and metric tests passed 8/8 in the inspected Actions log. This is test evidence, not a forecast performance result.
- A full catalogue run remained in the technical-model step long enough to trigger the fixed plan's compute budget. Sequence comparisons were bounded to next-session return/direction, three training epochs, two chronological folds; all other sequence target/horizon pairs are explicitly marked not run under the budget.
- Independent code inspection found that the metric field called out-of-sample R-squared used the realized holdout sample mean rather than a forecast available at the origin. The phase-5 branch was corrected to report benchmark-relative R-squared (1 - candidate MSE / benchmark MSE). The corrected run and a unit-test confirmation remain required before adopting results.
- Public free-source review recorded official NSE index/India VIX/breadth/FII-DII/derivatives reports and two Hugging Face options collections. The collections are not ingested yet: one is CC-BY-NC-4.0 and ~4 GB, the other has 'other' licensing, ~2.5 GB and incomplete intraday OI/settlement fields. See DATA_CATALOG.md.
- At the last check, run 30 on main, run 31 on research/phase-5-models, and the corrected run 32 were respectively active/active/queued. No completed model metrics have yet been accepted.

<!-- OPTION_VALIDATION_INTERACTION_START -->
## 2026-10-14 — option-buying validation workflow stage

- Stage: BLOCKED; status: BLOCKED_REQUEST_AUTH_OR_SCHEMA; run: https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38542434374; commit SHA: 944ec84c8047d31dce66165bd8db0a094133dc23.
- Dhan option data requests planned/successful-or-empty/failed: 196/0/1.
- Result file: research/option-validation/RESULTS.md; sanitized summary: reports/option_validation/results_summary.json.
- Raw option prices remain in Actions cache only; no credentials or raw quote file is intentionally staged.
<!-- OPTION_VALIDATION_INTERACTION_END -->
