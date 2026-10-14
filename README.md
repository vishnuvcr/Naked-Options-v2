# Fresh NIFTY 50 Prediction Research

**Research version:** NIFTY-PRED-1.0  
**Scope:** Prediction only. No trading strategy design, optimization, or recommendation in this study.  
**Started:** 2026-10-14  
**Status:** Phase 1 in progress; repository bootstrap.

## Repository audit

The repository was empty at project start: no readable README, files, branches, commits, datasets, experiment logs, or workflows. This project therefore starts a new research record without overwriting prior repository work. Relevant prior literature available in the ChatGPT Project library is cited in `research/LITERATURE_REVIEW.md`; it is not treated as this project's validated experimental output.

## Research navigation

- [Research plan](research/RESEARCH_PLAN.md)
- [Research questions and hypotheses](research/RESEARCH_QUESTIONS.md)
- [Literature review](research/LITERATURE_REVIEW.md)
- [Data catalog](research/DATA_CATALOG.md)
- [Experiment log](research/EXPERIMENT_LOG.md)
- [Results](research/RESULTS.md)
- [Phase status and gates](research/PHASE_STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Independent tester report](research/TESTER_REPORT.md)
- [Scientific manuscript](research/MANUSCRIPT.md)
- [Reproducibility guide](research/REPRODUCIBILITY.md)

## Scientific integrity

No model will be declared best from training fit, shuffled validation, price-level R² alone, or a reused test set. Return, directional, volatility, and level targets will be evaluated separately with chronological walk-forward evaluation, simple benchmarks, uncertainty estimates, and multiplicity control. Results unavailable because of data, credentials, compute, or workflow restrictions will be marked **blocked/not run**, never imputed or fabricated.

## Current summary

- Repository bootstrap: in progress.
- Data access: not yet verified.
- Model experiments: not yet run.
- Final independent review: not yet run.
- No empirical result or best-performing model is claimed at this stage.

See [phase status](research/PHASE_STATUS.md) for the authoritative gate state.

## Corrected run #49 — 2026-10-14

The forward-volatility label defect has been fixed and regression-tested. [Workflow #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) completed successfully. Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`.

- [Corrected results and evidence register](research/RESULTS.md)
- [Phase status and gates](research/PHASE_STATUS.md)
- [Experiment log](research/EXPERIMENT_LOG.md)
- [Error log](research/ERROR_LOG.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md)

Preliminary findings: the 1-session direction result does not survive multiplicity correction; 5-/20-session return forecasts are worse than the zero-return baseline in the selected global models; volatility results are not statistically accepted after correction. Some volatility-expansion classifiers improve log loss, but this remains exploratory. No trading strategy has been validated; options data and broker-specific costs/slippage have not been tested. Phase 5/7 remain open until independent tester approval.
