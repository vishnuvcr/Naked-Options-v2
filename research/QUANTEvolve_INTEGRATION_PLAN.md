# QuantEvolve integration research plan

**Protocol:** QE-NIFTY-1.0  
**Branch:** `research/quantevolve-integration`  
**Status:** Phase 0 audit scaffold committed; automated run status must be verified; no strategy performance claim is permitted.  
**Scope:** NIFTY 50 prediction and NIFTY options strategy discovery as separate experimental tracks.  
**Upstream:** [tarsyang/quantevolve](https://github.com/tarsyang/quantevolve), Apache-2.0 according to its upstream LICENSE.

## Research questions
1. Can QuantEvolve's evolutionary LLM loop be adapted to produce reproducible NIFTY 50 prediction candidates without changing the existing prediction study's outcomes or gates?
2. Can its candidate-generation loop be connected to an options evaluator that uses point-in-time, exact-expiry/exact-strike contract data and realistic Indian execution costs?
3. Does evolutionary search add stable, out-of-sample value beyond frozen simple baselines after accounting for data quality, temporal leakage, multiple testing, fees, slippage, and regime instability?
4. Which findings are blocked by data access, API quota, license, compute, or source-schema limits?

## Non-negotiable inherited constraints
- Existing NIFTY-PRED, OPT-BUY, strike-selection, and VOL-REGIME results are historical evidence and must not be overwritten or silently reinterpreted.
- Prediction and options are separate tracks with separate target definitions, baselines, splits, results, and dispositions.
- Do not use the upstream Binance BTC/USDT evaluator unchanged for NSE data or options.
- Never run LLM-generated code with repository write credentials or other secrets in its process. The evolution process must run in a low-privilege job, with no write token exposed to candidate code.
- No model selection on final holdout. Freeze a time-based final holdout before evolution; use development-only walk-forward evaluation for candidate fitness.
- Report failed/blocked runs as such; do not fabricate, impute, or imply performance.
- Options evaluation must verify instrument identity and expiry, quote/bar provenance, lot-size history, missing-data policy, and executable-side assumptions before P&L.
- Include Paytm Money brokerage and applicable statutory/exchange charges when verifiable, plus adverse slippage/spread sensitivity. OHLC bars are not bid/ask quotes.
- Use finite search budgets, explicit seeds, checkpoints, cache keys, dependency pins, and maximum wall-clock/API budget.
- Any downloaded source data must have a documented license, attribution, hash, and retention policy. The upstream QuantEvolve license does not grant rights to market datasets it consumes.
- User reports that `GOOGLE_API_KEY` has been added as a GitHub Actions repository secret. Treat this as user-reported configuration; the value is not read or logged. Use `secrets.GOOGLE_API_KEY` only in bounded LLM-generation steps, never in config files, artifacts, logs, or candidate execution. If absent/invalid/quota-limited, record a sanitized block and continue offline tests where possible.
- Do not use Dhan/HF tokens in generated candidate code. Secrets are acquisition-only and must be isolated from candidate execution.

## Phases, gates, and finite stopping rule

### P0 — Repository and upstream audit (current)
- Inspect main README, phase status, error log, current workflows, branch history, and existing data/backtest gates.
- Inspect upstream README, license, config, package metadata, evaluator, collector, CLI, and tests.
- Document upstream assumptions and incompatible interfaces.
- Gate: audit report, branch, error log entry, and manual/automatic audit workflow committed. No market performance claim.

### P1 — Reproducible integration shell
- Vendor or pin a specific upstream commit; do not track moving `main` at runtime for confirmatory runs.
- Pin dependencies and capture upstream commit, Python version, config hash, data hashes, seed, model identifier, iteration budget, and run ID.
- Separate the prediction candidate interface from options strategy interface.
- Gate: offline smoke tests, deterministic fixture tests, sanitized logs, no secret exposure, no writes outside run output.

### P2 — NIFTY prediction adapter
- Build a point-in-time feature/target adapter from validated cached NIFTY data.
- Define separate targets: next-session return/direction and volatility/volatility-expansion; do not conflate forecast quality with profitability.
- Compare zero-return/majority and existing frozen baseline models. Use chronological walk-forward development folds and a never-touched final holdout.
- Fitness must be a predeclared metric with complexity and turnover/instability penalties; apply multiplicity control to the reported candidate family.
- Gate: target-offset, lookahead, missingness, reproducibility, and metric tests pass; OOS results complete and confidence intervals/adjusted comparisons reported.

### P3 — Options evaluator and contract/data gate
- Use a separate strategy contract for options. Reject signals until exact expiry, strike, option type, timestamp, lot size, and entry/exit identity are verified.
- Prefer free lawful sources first; use existing Dhan/HF configuration only through isolated acquisition steps. Cache data with hashes and provenance.
- Enforce existing quality thresholds; do not lower them to make evolution run.
- Gate: >=80% eligible-date coverage where applicable, <=1% conflicting duplicate groups, complete fee/slippage arithmetic tests, and a verified source/contract map. Otherwise stop options P&L and record blocked.

### P4 — Bounded options candidate search
- Freeze candidate grammar and search space before running; no arbitrary code access to filesystem/network/secrets.
- Use development-only walk-forward folds; candidate fitness is net P&L/risk with no-trade days, missing fills, realistic costs, drawdown, tails, and turnover included.
- Compare no-trade and simple frozen baselines. Charge all orders in multi-leg structures.
- Gate: candidate family, budgets, costs, missing-fill handling, and statistics preregistered before search.

### P5 — Final validation and disposition
- Evaluate selected candidates once on untouched chronological holdout. Include block-bootstrap intervals, paired baseline comparisons, Holm correction, chronological subperiods, and cost sensitivities.
- Reject any apparent winner that depends on one fold/regime, bad coverage, unverified contracts, or unmodeled costs.
- Gate: automated tests, security/leakage assertions and artifact audit pass; disposition is either validated within tested universe, no-go, or inconclusive/blocked. The user explicitly requires no independent tester branch/report/sign-off; do not add a review handoff, while retaining automated quality gates.

### P6 — Manuscript and closure
- Produce manuscript with abstract, questions, literature review, data sources/licenses, methods, statistical plan, results, charts/tables, discussion, strengths/limitations, conclusion, future work, reproducibility appendix, and machine-readable supplements.
- Update README, phase status, experiment/interaction log, and error log with links. Preserve all prior results.
- Stop after P0–P6, allowing only bounded defect-driven reruns. No unbounded evolutionary loops.

## Statistical and reporting protocol
- Separate forecast metrics (MAE/RMSE, directional accuracy, log loss/Brier where appropriate, QLIKE for volatility) from trading metrics (net rupees, mean/median, drawdown, tail loss, turnover, trade count).
- Use naive and existing validated baselines; report confidence intervals and adjusted p-values where inferential claims are made.
- Use chronological splits, purging/embargo for overlapping targets, point-in-time features, and explicit missing-data rules.
- Treat search itself as multiple testing. Keep final holdout inaccessible to fitness scoring and iterative prompts.
- Every run gets a manifest, source hashes, config hash, seed, environment versions, status, and sanitized logs.

## Workflow design
- Audit/tests run on pushes and pull requests touching integration files, on a bounded schedule, and via `workflow_dispatch`.
- Expensive LLM evolution is manual opt-in and separately budgeted; scheduled automation must not incur unbounded API costs.
- Automatic workflows must never start live orders or connect to a broker execution endpoint.
- GitHub Actions secrets are not readable by this integration; repository owner must add `GOOGLE_API_KEY` if LLM runs are desired. No secret value belongs in artifacts.

## Current result
P0 has begun. Repository and upstream reconnaissance found that upstream's default data collector/evaluator is Binance OHLCV-oriented (README/config default BTCUSDT 1h), with Gemini-backed strategy generation and a large default evolution budget (200 iterations, population 50). These defaults are incompatible with direct NIFTY/options use without an adapter and stricter resource/data gates. This is an architecture finding, not a performance result.
