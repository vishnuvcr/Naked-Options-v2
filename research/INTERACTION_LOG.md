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

- Stage: ANALYSIS; status: INCONCLUSIVE_PARTIAL_OR_INCOMPLETE_DATA; run: https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38545503819; commit SHA: 08c7663b8f8a1321ab2b23b5e9bba6dc088fd5d7.
- Dhan option data requests planned/successful-or-empty/failed: 686/490/0.
- Result file: research/option-validation/RESULTS.md; sanitized summary: reports/option_validation/results_summary.json.
- Raw option prices remain in Actions cache only; no credentials or raw quote file is intentionally staged.
<!-- OPTION_VALIDATION_INTERACTION_END -->


## 2026-10-14 - pilot result and method correction

- Option validation run #6 completed 196 Dhan MONTH/expiryCode=1 requests with no request failures. It produced 303,548 raw rows, 294,419 usable rows, 45 conflicting duplicate groups out of 9,084 duplicate groups, and only 171/980 (17.45%) eligible dates for both structures.
- All four pilot model-filtered candidates had negative mean daily premium-normalized returns and fewer than 100 alert trades. Because quote coverage failed the prespecified 80% gate, no pilot trading inference is accepted.
- Data/method review found the initial source query requested only ATM calls/puts plus one call and one put relative offset. Fixed numeric strikes could move beyond that restricted set by exit. The source query is being expanded to the documented monthly ATM−3…ATM+3 grid for both option types; strategy entry/exit selection is unchanged.
- Review also found that the percentage-return paired difference compared varying premium-debit denominators and assigned zero on non-alert dates. The primary comparison is now daily net P&L in rupees per one-lot-proxy slot, with premium-normalized return secondary. This correction is disclosed and is not used to select a different model or trade structure.
- Code improvements: vectorized block bootstrap, grouped date quote tables, exact-strike exit lookup, and private-cache persistence before statistical analysis. New tests cover same-strike matching and daily P&L when the alert skips a date.

## Run #7 test-fixture correction — 2026-10-14

- Actions run #7 failed before its data acquisition step because one response-redaction test expected errorCode and errorMessage in a fake provider response that no longer contained those fields. The implementation itself redacted the bearer token correctly, but the fixture/assertions disagreed.
- Code review also caught a legacy ATM cache fallback date format that omitted the year in the second date; this would have missed existing ATM cache files and unnecessarily repeated two monthly-option requests per date window.
- Corrected the fake response and full-date filename. The complete suite will be rerun by the next automatic Actions workflow.


## Run #9 audit and exact-offset cached rerun — 2026-10-14

- Run #9 expanded acquisition succeeded: 686 request windows planned, 196 reused from cache, 490 new valid/empty responses, zero failed. Data contained 1,062,082 raw rows and 1,029,545 usable rows.
- Eligibility: 83.98% straddle dates and 69.18% strangle dates, below the 80% minimum for strangle. Conflicts: 452 / 32,085 duplicate groups = 1.41%, above the 1% ceiling. Data gate fails.
- Four model-filtered variants had mean daily net P&L at ₹10/order and 50 bps slippage between −₹315.71 and −₹369.43 per one-lot-proxy slot. Paired daily P&L improvement against always-buy was significant after Holm adjustment (~0.002), but the candidates themselves lost money; all 100 bps checks and both-half profitability checks failed. This is loss reduction against a worse benchmark, not a profitable option-buying result.
- Independent ledger audit passed 48,032 row-level P&L/cost checks, bootstrap intervals, paired comparisons and Holm adjustment; the data gate still blocks acceptance.
- Corrected cached rerun retains source-request offsets, requires actual CALL +1 / PUT −1 strangle entry, uses exact numeric exit strike, fixes the request counter, and generates the structured manuscript and SVG charts. Gate limits stay unchanged.
