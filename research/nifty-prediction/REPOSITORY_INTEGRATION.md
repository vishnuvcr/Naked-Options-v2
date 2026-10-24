# Repository integration and evidence ledger — NIFTY 50 research

**Updated:** 2026-10-25  
**Purpose:** Use all seven repositories named in the project instructions as reviewed research inputs. “Reviewed” is not the same as cloned, installed, executed, or empirically validated. No performance claim is credited to a framework without an actual run and recorded artifact.

## Current baseline

The production daily benchmark workflow completed successfully in GitHub Actions run [#34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710). The current daily spot-index holdout is third-party data, not exchange-certified. The previous-session direction rule achieved 54.19% accuracy and 54.10% balanced accuracy; the supervised models did not demonstrate a reliable improvement over that simple rule. This is the starting point, not a final strategy claim.

## Seven-repository use matrix

| Repository | What the project provides | Use in this research | Status / guardrail |
|---|---|---|---|
| [tarsyang/quantevolve](https://github.com/tarsyang/quantevolve) | LLM-assisted evolutionary generation and backtest-based strategy search; README architecture references Binance market data and Gemini | Borrow the bounded hypothesis/evaluate/retain-or-reject loop for candidate-rule experiments. Candidate search must use training/validation windows only; final holdout is used once after rules are frozen. | **Reviewed; controlled adaptation planned.** Do not run its Binance-oriented collector as the NIFTY data source. No unbounded autonomous optimization or holdout search. |
| [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | Multi-agent financial analysis and research orchestration | Use its analyst/debate workflow as a structured way to formulate candidate hypotheses and summarize dated public evidence, where dependencies and provider/data availability permit. Quantitative scoring stays in the deterministic benchmark harness. | **Reviewed; research-only adaptation.** LLM statements cannot become target labels or override backtest metrics. Preserve source/date and point-in-time rules. |
| [0xethanq/astra-quant-agent](https://github.com/0xethanq/astra-quant-agent) | Autonomous crypto trading stack, multi-LLM analysis and deterministic risk controls; README states execution is OKX-native | Reuse the architectural idea of separating signal generation from deterministic risk/execution checks; use as a risk-control checklist for any later candidate strategy. | **Reviewed; direct execution stack rejected for this study.** OKX-native crypto execution is not an NSE cash/options broker adapter. Do not connect or execute live orders. |
| [astroautomata/PySR](https://github.com/astroautomata/PySR) | Symbolic regression via Python and Julia | Test whether a small interpretable expression built from lagged returns, volatility and moving-average gaps improves on simple predeclared rules. Constrain operators/complexity; fit only on chronological training folds. | **Reviewed; conditional experiment.** Julia/runtime and dependency install must pass first. Symbolic expression is exploratory until it beats baselines out-of-sample and survives costs. |
| [bashtage/arch](https://github.com/bashtage/arch) | ARCH/GARCH and related financial econometrics | Fit a GARCH-family conditional-volatility forecast on lagged returns; compare forecasts using a predeclared volatility loss (e.g. QLIKE where the proxy is valid). Separately test whether lagged volatility regime conditions a direction rule. | **Reviewed; direct fit for volatility experiment.** Volatility accuracy is not directional skill; do not call it a directional model unless separately evaluated. |
| [X-DataInitiative/tick](https://github.com/X-DataInitiative/tick) | Time-dependent statistical learning, regularized GLMs and point-process tools | Inspect a regularized logistic/linear model as an alternative to sklearn if install and Python compatibility permit. Only use point-process components if timestamped event/order-flow data is acquired. | **Reviewed; compatibility gate required.** Do not force a fragile dependency into the core workflow. If unavailable, log the install/runtime evidence and retain sklearn equivalent as a transparent comparator. |
| [scikit-learn-contrib/MAPIE](https://github.com/scikit-learn-contrib/MAPIE) | Conformal prediction intervals/sets and risk control | Evaluate a classification prediction set / abstention policy with strictly chronological calibration, reporting coverage, set size and conditional performance. | **Reviewed; conditional uncertainty experiment.** Check current API/version and exchangeability assumptions. No IID coverage guarantee is claimed for serially dependent market data without qualification. |

## Pipeline integration implementation (2026-10-25)

All seven upstream repositories are now pinned as Git submodules under [vendor/research-repositories](../../vendor/research-repositories). The submodule-vendoring workflow succeeded in [Actions run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40143722351), and GitHub's contents API confirms seven pinned commit references.

Added `research/nifty-prediction/audit_repository_integrations.py` and [the integration audit workflow](../../.github/workflows/repository-integration-audit.yml). The workflow checks out pinned submodules, installs the stable `arch` and `MAPIE` pipeline dependencies, and records a machine-readable integration audit. This is an integration/provenance smoke audit—not a claim that every upstream project is executed in the forecasting model.

Pipeline boundaries:
- `arch`: active GARCH volatility experiment in `evaluate_volatility_forecast.py`; volatility remains separate from direction prediction.
- `MAPIE`: dependency included for the next chronological calibration/abstention experiment; not yet used to make predictions.
- `PySR` and `tick`: pinned and audited, but must pass dedicated runtime/API compatibility experiments before joining model comparisons.
- `Quantevolve` and `TradingAgents`: their bounded search and evidence synthesis concepts inform research orchestration; agent outputs cannot create labels or override deterministic scores. No paid LLM calls are made by the audit.
- `Astra Quant Agent`: risk-control design reference only. Its crypto exchange execution is deliberately excluded from NSE/NFO.
- No live trading, order submission, or holdout-driven tuning is enabled.

### Pipeline integration status
| Component | Wired into automation | Empirical model experiment | Status |
|---|---|---|---|
| Seven pinned submodules | Yes | N/A | Vendoring verified |
| `arch` | Yes | GARCH forecast run completed in workflow logs | Active, volatility-only |
| `MAPIE` | Dependency check/audit | Not yet | Pending chronological calibration |
| `PySR` | Audit/provenance only | Not yet | Compatibility gate pending |
| `tick` | Audit/provenance only | Not yet | Compatibility gate pending |
| `Quantevolve` | Bounded-search design only | Not yet | No autonomous holdout search |
| `TradingAgents` | Evidence-workflow design only | Not yet | No API/LLM execution |
| `Astra Quant Agent` | Risk checklist only | Not applicable to NSE execution | Exchange executor excluded |

## Work completed vs. pending

### Completed
- Read the README of each of the seven named repositories on 2026-10-25.
- Recorded each project's intended contribution and scope mismatch/guardrails.
- Established the production benchmark as the comparator; the baseline result does not yet establish a tradable edge.
- Confirmed the benchmark workflow run #34 completed successfully.

### Next bounded experiments
1. **Rule candidates first:** predeclare 1–3 simple momentum and short-horizon mean-reversion rules; evaluate on identical chronological holdout rows against previous-session direction and buy/hold/flat references as applicable.
2. **Volatility/regime:** use `arch` for volatility forecasts and test one lagged-volatility-conditioned rule, not an open-ended grid search.
3. **Regularized comparator:** attempt `tick` only if install/runtime compatibility works; compare with sklearn logistic regression.
4. **Symbolic model:** attempt a low-complexity `PySR` expression only after a clean chronological validation protocol is in place.
5. **Uncertainty:** attempt `MAPIE` with a chronological calibration window; report coverage and abstention results rather than treating intervals as guaranteed.
6. **Research agents/search:** use `TradingAgents` to structure hypothesis/evidence summaries and `Quantevolve` concepts for a bounded search over predeclared rules, never to supply ground-truth scores.
7. **Risk/execution audit:** use AstraQuant's signal/risk separation as a checklist; do not import its OKX crypto order executor. If a candidate survives, estimate NSE/NFO costs and Paytm Money fees/slippage from verified current terms before claiming net profitability.

## Acceptance criteria for every experiment

- Record exact source data/hash, feature availability time, dates and sample counts.
- Use chronological train/validation/test boundaries; do not tune on final test data.
- Compare on common eligible observations against simple baselines.
- Report metrics, uncertainty and failures, not only the best score.
- For any strategy-like rule, calculate turnover, realistic slippage, brokerage, taxes/charges, and execution timing before a net-return claim.
- Persist code, machine-readable result, status update and errors in this repository.
- Never present framework documentation or an installed dependency as empirical proof.

## Source links
- https://github.com/tarsyang/quantevolve
- https://github.com/TauricResearch/TradingAgents
- https://github.com/0xethanq/astra-quant-agent
- https://github.com/astroautomata/PySR
- https://github.com/bashtage/arch
- https://github.com/X-DataInitiative/tick
- https://github.com/scikit-learn-contrib/MAPIE
