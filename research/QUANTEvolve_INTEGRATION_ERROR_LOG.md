# QuantEvolve integration audit log

## QE-ERR-001 — upstream evaluator/data assumptions
- **Date:** 2026-10-22
- **Severity:** HIGH
- **Observation:** Upstream README and default config describe Binance OHLCV collection and default BTCUSDT 1h data. The evaluator's documented signal interface is a generic buy/sell/hold series, not an NSE options contract/order ledger.
- **Risk:** Running the upstream pipeline unchanged would not constitute NIFTY prediction research or an executable options backtest and could create false confidence from a mismatched market/data model.
- **Action:** Do not execute the upstream default collector/evaluator for research results. Require separate NIFTY prediction and options adapters, frozen gates, and explicit cost/statistical evaluation.
- **Status:** OPEN — addressed at design level; implementation/test gates pending.

## QE-ERR-002 — evolutionary multiple-testing and holdout leakage
- **Date:** 2026-10-22
- **Severity:** HIGH
- **Observation:** Evolutionary search repeatedly generates candidates based on previous fitness feedback. A naive final score can be overfit by repeated adaptive selection even when each individual backtest is chronologically ordered.
- **Risk:** Final performance may be optimistic if the holdout informs prompts, fitness, selection, or retries.
- **Action:** Reserve a sealed final holdout; use development-only walk-forward folds for fitness; cap iterations/API budget; record all candidates and correct the final comparison family.
- **Status:** OPEN — design gate; implementation pending.

## QE-ERR-003 — credential isolation
- **Date:** 2026-10-22
- **Severity:** HIGH
- **Observation:** QuantEvolve requires `GOOGLE_API_KEY` for Gemini generation. Generated strategy code is untrusted code and must not run in a process that has secrets or repository write permissions.
- **Risk:** Accidental disclosure, unsafe generated code, or unintended repository changes.
- **Action:** Keep secret use limited to the generation client in a restricted job; execute candidate code in a separate low-privilege/no-secret process. Do not expose Dhan/HF tokens to candidate execution. Log only whether a secret is configured, never its value.
- **Status:** OPEN — security architecture must be implemented and tested.

## QE-ERR-004 — no performance evidence
- **Date:** 2026-10-22
- **Severity:** MEDIUM
- **Observation:** Repository/upstream source audit only; no adapted NIFTY data run or verified out-of-sample candidate evaluation has been executed.
- **Risk:** Treating integration as validated strategy research would overstate the evidence.
- **Action:** All current performance fields remain NOT RUN. No strategy/model is endorsed.
- **Status:** CLOSED AS DOCUMENTED LIMITATION; revisit only after P2/P4 gates.

## Scope and audit note
This log records visible technical findings and corrective actions. It does not include private chain-of-thought or hidden reasoning.
