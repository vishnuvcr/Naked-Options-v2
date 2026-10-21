# Research execution policy

Version: NIFTY-PRED-1.0  
Applies to: this repository, all research phase branches, GitHub Actions runs, and final developer/tester review.

## Scope and fixed plan

- This research predicts NIFTY 50 price level, log returns, direction and future volatility only. It must not create, backtest or recommend a trading strategy.
- Follow the nine phases and their acceptance criteria in [RESEARCH_PLAN.md](RESEARCH_PLAN.md). End after Phase 9; do not extend the experiment universe because a result is attractive or disappointing.
- Do not modify the frozen plan for convenience. A genuine scope/method change must include a dated amendment stating the old/new decision, reason, impact on comparability and gate record.
- Report the best model separately for each target and horizon; do not claim a universal winner from a mixed metric.
- Do not confuse external literature's reported results with fresh results measured by this repository.

## Audit and source handling

- Before a phase begins, inspect README, research plan, questions, literature, data catalog, phase status, experiment log, error log, current datasets/source code/workflows and the previous phase's test report.
- Preserve historical work and failed experiments. Record actual actions/results/commit SHAs/workflow IDs where observed.
- Search public and official free sources before declaring data unavailable. Use DHAN_ACCESS_TOKEN and HF_TOKEN only as GitHub Actions secrets. Never print tokens or include them in tracked files, traces, artifacts, or commit messages.
- Prefer official NSE/BSE/NSE Indices or Dhan where valid; record public-source fallbacks clearly. A discovered source is not a successfully ingested dataset.
- Do not fabricate missing values or labels. Do not blindly merge sources, apply today's constituent list historically, substitute current options chains for past quotes, or use a predictor before its publication time.
- Log source, date span, sampling interval, units, timezone, missingness, duplicates, non-trading dates, license, data hashes and retrieval time. Cache reuse is allowed only when the manifest and raw-file hash match.
- Keep licensed/non-redistributable source data out of the public repository; publish schema, retrieval metadata, derived metrics and artifacts only within the permitted terms.

## Model and statistical integrity

- Keep data chronological. The latest 20% is an untouched holdout; preprocessing and tuning are fitted inside training folds; global closes only enter after they were available at the forecast origin.
- Benchmarks are target-specific: level persistence; zero and training-mean returns; autoregressive/ARIMA returns; historical volatility / proper probability baselines.
- Report original-unit errors, benchmark-relative predictive skill, sample counts, effect sizes, uncertainty, and statistical evidence. An OOS R-squared denominator must use a forecast benchmark, not the realized holdout mean.
- Overlapping horizons and time-dependent losses require dependence-aware inference. Apply the prespecified multiple-testing control to the full model comparison family. Raw p-values alone do not establish a discovery.
- Do not tune models on the final test set. Model selection is driven by development-time walk-forward scores; the locked holdout is confirmation only.
- Deep models that cannot run in the fixed resource budget are marked BLOCKED_COMPUTE_BUDGET with their target/horizon and reason; do not omit them silently or imply full hyperparameter optimization.
- Include negative outcomes and failures. “No robust predictive skill found under this protocol” is a valid result.

## Phase branches and gate transitions

| Phase | Branch |
|---|---|
| 1. Audit and design | research/phase-1-audit |
| 2. Literature | research/phase-2-literature |
| 3. Data | research/phase-3-data |
| 4. Baselines | research/phase-4-baselines |
| 5. Models | research/phase-5-models |
| 6. Features / regimes | research/phase-6-features-regimes |
| 7. Statistical validation | research/phase-7-validation |
| 8. Independent review | research/phase-8-independent-review |
| 9. Manuscript / publication | research/phase-9-publication |

The initial repository was empty, so the protocol, skeleton and early files were bootstrapped on main. Branches for Phases 1–4 are historical checkpoint branches cut from the closest relevant commits; Phase 5 is the active correction/run branch. Future phases must branch from a gate-passing predecessor, not from an unreviewed or failed result.

## Developer and independent tester

- Do not open or merge the final developer/tester tracks before empirical result acquisition.
- After results exist, create one developer branch and one independent-tester branch in this repository.
- The tester must inspect the code/data independently, recompute core metrics from saved predictions, check formulas/signs/target dates/time alignment/data leakage/splits/p-values/multiple testing/manuscript claims, and provide reproductions for defects.
- The developer fixes confirmed defects and resubmits for tester review. The developer must not progress beyond a gate without tester approval.
- A self-test or a second workflow run is not described as an independent human review. Report the actual degree of review autonomy and any blocked permissions honestly.
- Correct critical/high defects and rerun their tests. If a critical issue cannot be resolved with available access, record the blocker and ask for intervention only if no supported alternative exists.

## Automation, status and logs

- GitHub Actions must support both automatic triggers and manual workflow_dispatch. Workflows should be resumable, use reproducible versioned requirements and seeds, cache valid data, and upload the structured reports.
- Do not claim a workflow ran, a commit occurred, data were collected, a Pages deployment succeeded, or a tester passed without verifying the corresponding GitHub record.
- After every meaningful step, update PHASE_STATUS.md, EXPERIMENT_LOG.md, ERROR_LOG.md, relevant data/results, and README.md. Results must be machine-generated or independently recomputed, not typed from guesses.
- The current GitHub Actions workflow writes reports as artifacts. An artifact upload does not itself mean those outputs have been committed to the repository or published to Pages.
- Keep the manuscript complete: abstract, introduction, literature review, research questions/objectives, data, methods, model table, statistics, results, discussion, strengths/limitations, conclusion, references, future directions, appendices and supplementary materials.
- Maintain an auditable action/decision log, not a raw conversation transcript. Private internal reasoning / hidden chain-of-thought is not stored; the factual actions, decisions, and evidence are.


## QuantEvolve integration core-instruction addendum (QE-NIFTY-1.0)

This scoped addendum applies to the QuantEvolve integration branch and its prediction/options experiments. It does not rewrite or reopen the historical findings for prior research versions.

- The user reports that `GOOGLE_API_KEY` has been added as a GitHub Actions repository secret. Treat this as user-reported configuration; never attempt to read or print the secret value. The audit workflow does not require this key.
- Use `secrets.GOOGLE_API_KEY` only in a bounded LLM-generation step that needs Gemini. Do not put the key in YAML/config files, source, shell traces, candidate prompts, artifacts, logs, reports, or commit messages. Never expose it to generated strategy/model execution, data-processing jobs, or untrusted candidate code.
- Keep generation and execution separated: generated code is untrusted, and its run process must have no API secrets, broker credentials, write-capable GitHub token, or network access unless a future, specifically audited need justifies it. No broker order placement is permitted.
- Set explicit maximum iterations, population, model-call count, timeout/wall-clock budget, spend/quota bounds, checkpoint cadence and fixed seed. Use manual opt-in for any expensive LLM evolution; do not run costly evolution on each push or schedule.
- If the secret is absent, invalid, quota-limited, or the provider fails, record a sanitized blocked/failed status and continue only with offline checks where possible. Never infer that the key works solely because the secret name exists.
- Keep NIFTY prediction and options strategy discovery as separate tracks. Preserve all predecessor results and gates. Do not unlock options P&L until expiry/strike/option-type identity, coverage, duplicate quality, lot size, fees and fill/slippage assumptions pass.
- Evolution fitness may use development-only walk-forward results. A sealed chronological holdout must not be read by candidate generation, fitness selection, tuning, debugging prompts or repeated retries. Correct the final comparison family for search multiplicity.
- For this QuantEvolve integration, the user has explicitly stated **no independent review/tester branch or review sign-off is required**. Do not create an independent-tester handoff or wait for it to advance. Automated unit/regression tests, security checks, leakage checks, artifact validation and recorded gate decisions are still mandatory. Do not falsely label automated checks as independent review.
- Maintain the finite QE-NIFTY-1.0 phases in `research/QUANTEvolve_INTEGRATION_PLAN.md`; stop after the prescribed phases or a serious blocker. Record visible actions, decisions, workflow/commit IDs, errors and evidence—not hidden chain-of-thought.


## QuantEvolve guarded integration enforcement

- QE-NIFTY-1.0 is a distinct follow-on; it must not overwrite the historical NIFTY-PRED or options dispositions.
- Pin QuantEvolve upstream to the reviewed revision; do not run moving upstream main for confirmatory experiments.
- LLM-generated candidate source is untrusted. The permitted prediction candidate is one literal STRATEGY_SPEC assignment and is parsed using AST parsing plus ast.literal_eval. Never import, compile, exec, or directly execute candidate source.
- Do not use the default Binance evaluator to produce NIFTY results. The upstream evaluator is not a point-in-time NIFTY/options engine and does not include realistic Indian brokerage/slippage.
- Fitness runs only on the first 80% chronological development sample using development-only folds. Evaluate the final 20% once after model selection. Do not feed holdout metrics, plots or error feedback to the evolution controller.
- GOOGLE_API_KEY is reported by the user as a GitHub Actions secret. Use it only within bounded generation steps; do not store its value. Remove it, along with Dhan/HF/GitHub tokens, from all candidate-evaluation and publication processes.
- No independent tester/review branch or sign-off is required for this integration by explicit user direction. Automated unit tests, secret isolation, causal target/feature, holdout-separation and report validation checks still must pass.
- Options P&L is forbidden until expiry-date and fixed-contract identity, source/license, lot size, timestamp, coverage and conflicting-duplicate gates are verified. Include Paytm Money brokerage, applicable exchange/statutory costs and adverse slippage sensitivity if/when the P&L gate opens.
