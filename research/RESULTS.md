# Results and evidence register

Version: NIFTY-PRED-1.0  
Last updated: 2026-10-14  
Status: NO EMPIRICAL RESULTS YET.

## Research design status

Repository bootstrap and first-pass literature review are documented. The target repository was empty at initialization. Data collection, baseline fitting, systematic model experiments, and the final out-of-sample test have not yet been verified as run.

## Result table (to be populated only from machine-generated artifacts)

| Target | Horizon | Candidate / benchmark | OOS n | Baseline metric | Candidate metric | Difference + CI | Raw p | Adjusted p | Regime stability | Gate |
|---|---:|---|---:|---:|---:|---|---:|---:|---|---|
| Future log return | 1 session | pending | — | — | — | — | — | — | — | BLOCKED |
| Direction | 1 session | pending | — | — | — | — | — | — | — | BLOCKED |
| Future realized volatility | 5 sessions | pending | — | — | — | — | — | — | — | BLOCKED |
| Price level | 1 session | persistence | — | — | — | — | — | — | — | BLOCKED |
| Return / direction / volatility | 5 / 20 sessions | pending | — | — | — | — | — | — | — | BLOCKED |

## Rules for result statements

- A result is empirical only if its data hash, experiment code, validation split and generated metrics can be reproduced.
- An OOS model with lower error but no corrected significance / stability is described as exploratory or inconclusive, not successful.
- A high level R² without gain over persistence is not a discovery of predictable market movement.
- No model is named the overall winner without a specific target, horizon, metric, uncertainty and comparison.
- Previous manuscripts' results are literature, not results of this fresh experiment. They will not be copied into this table.

## Current conclusion

No model can yet be ranked because no experiment output has been verified. This is a deliberate evidence status, not an empirical finding that all prediction is impossible.

## Latest run status — 2026-10-14

The canonical bounded workflow candidate is [Actions run #34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38525308372) at commit d654d8f825ba19dc8dfc08f9f2e7b8f26779e7d3. Its data validation, feature construction and unit tests were progressing successfully at the last inspection. The experiment stage has not yet emitted a completed metric table; all result cells above remain BLOCKED until that run and artifact review complete.

No best model, final out-of-sample accuracy, statistical significance or calibration claim is made from a pending run.

## Compute-budget amendment

The model grid has been bounded before accepting any out-of-sample result. Full algorithm comparisons are made for next-session return and direction; a core set covers remaining target/horizon cells. This choice is documented in RESEARCH_PLAN.md and all omitted family cells are explicitly blocked. It constrains the scope of conclusions: no cross-family winner is inferred for a target/horizon with only a core screen. No empirical performance figure is available from the superseded runs.
