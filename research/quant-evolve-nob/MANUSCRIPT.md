# QE-NOB-1.0: A bounded QuantEvolve-inspired search for NIFTY 50 naked option buying

**Status:** exploratory manuscript; no deployable strategy identified; no independent tester per user's explicit instruction.  
**Run:** [GitHub Actions #39712854501](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501) · **Period:** 2021-10-25 to 2026-10-21.  
**Protocol:** [PLAN.md](PLAN.md) · [Results](RESULTS.md) · [Phase status](PHASE_STATUS.md) · [Error log](ERROR_LOG.md).

## Abstract

This study used a bounded QuantEvolve-inspired quality-diversity search to explore NIFTY 50 long-premium option-buying rules. Eligible positions were long calls, long puts, long straddles and long strangles; short-option legs were excluded. Four islands evaluated 600 unique candidates over nine completed generations. The dataset comprised 92,510 underlying rows and 2,588,918 option rows after duplicate-conflict filtering across 1,241 sessions. Candidates were selected using chronological training/validation data, and the latest 20% chronology was reserved for final evaluation. After-cost P&L, baseline comparisons, Holm multiplicity correction, block-bootstrap uncertainty, split-half checks and adverse cost stress tests were included.

Zero candidates passed the statistical gate and zero passed the execution/promotion gate. Data quality failed because 453 of 471 duplicate groups conflicted. Historical bid/ask/depth, exact expiry/strike continuity, dated lot sizes and the effective-date broker tariff remain unverified. The leading validation-selected opening-gap candidate had OOS mean daily net ₹10.68, a 95% block-bootstrap interval of -₹188.62 to ₹237.43, Holm-adjusted p=1.0, and stressed mean daily net of -₹98.54 at 100-bps slippage/₹20 per order. Conclusion: **DATA-LIMITED / NO-GO for strategy approval**. This does not prove all possible strategies unprofitable; the available data are insufficient to establish executable profitability.

## 1. Research questions and hypotheses

1. Can a bounded evolutionary search discover after-cost rules that outperform fixed-buy benchmarks?
2. Does any candidate retain positive, statistically credible net performance on a locked chronological OOS block after family-wise correction?
3. Are candidate results stable across OOS halves and adverse cost assumptions?
4. Are the data and execution assumptions sufficiently verified to interpret simulated P&L as executable?

H1 predicted a positive OOS edge; H2 a significant edge after multiplicity correction and paired benchmark comparison; H3 stability under split-half and stress testing; H4 valid data and execution gates. The run did not support H2–H4; H1 is not established robustly.

## 2. Scope and method

The study started from a fresh evidence namespace; prior research findings were not used as candidate rankings, parameter seeds or evidence. The implementation is **QuantEvolve-inspired**, not a reproduction of the original LLM multi-agent system: it uses deterministic research/evaluation roles and a constrained rule grammar, not unrestricted LLM-generated strategy code.

The bounded search evaluated 600 unique candidates in four islands, completed nine generations, and retained a quality-diversity archive of 28 niches. Validation selection used a composite of net P&L, Sharpe, profit factor and drawdown; final OOS metrics did not drive candidate discovery.

```mermaid
flowchart TD
 A[Freeze protocol and candidate grammar] --> B[Acquire isolated market data]
 B --> C[Validate duplicates and contract identity]
 C --> D[Build cost-aware candidates and baselines]
 D --> E[Search at most 600 unique candidates]
 E --> F[Freeze validation-selected finalists]
 F --> G[Evaluate locked final 20% chronology]
 G --> H[Holm correction, block CI and stress costs]
 H --> I{Statistical and execution gates pass?}
 I -->|No| J[DATA-LIMITED / NO-GO]
 I -->|Yes| K[Prospective paper testing only]
```

### Chronology

Training ended 2024-10-17; validation ended 2025-10-17; the final 20% chronology was held for confirmation. Search decisions used training/validation only.

## 3. Data and quality

| Measure | Result |
|---|---:|
| Window | 2021-10-25–2026-10-21 |
| Sessions | 1,241 |
| Underlying rows | 92,510 |
| Option rows after conflict filtering | 2,588,918 |
| Unique candidates / islands / generations | 600 / 4 / 9 |
| Duplicate groups | 471 |
| Conflicting duplicate groups | 453 (96.18% of groups) |
| Rows excluded for conflicts | 906 |
| Option timestamp coverage | 99.772% |
| Row-grid coverage | 99.947% |
| Statistical gate passes | 0 |
| Execution/promotion gate passes | 0 |

The source provided rolling ATM-relative OHLC, IV, OI, volume and spot—not a stable fixed-contract tape with historical executable bid/ask and depth. Intermittent Dhan HTTP 502 failures are recorded in `source_failures.csv`. The duplicate conflict rate caused the basic data-quality gate to fail; high row-grid coverage does not resolve identity conflicts.

## 4. Costs and statistical analysis

Primary results used one-lot simulated P&L with next-bar-open pricing and prespecified adverse slippage. Stress scenarios included 100 and 200 basis points of adverse slippage with ₹20 per order. Broker charges remain provisional because the effective-date Paytm Money tariff has not been verified. There are no historical bid/ask/depth observations to validate fill prices. Consequently, P&L is a simulation from rolling OHLC, not proof of executable returns.

Evaluation included Holm-adjusted candidate-family p-values, block-bootstrap intervals for daily net P&L, OOS split-half metrics, drawdown/profit-factor diagnostics, and paired comparisons with fixed-buy baselines. No candidate cleared all gates.

## 5. Results

### Best validation-selected candidate

Candidate 86: opening-gap continuation after a gap of at least 0.15%, MONTH1 rolling-option flag, moneyness offset 1, 120-minute hold.

| Metric | Result |
|---|---:|
| Validation mean daily net | ₹157.94 |
| OOS trades | 151 |
| OOS total net P&L | ₹2,659.70 |
| OOS mean daily net | ₹10.68 |
| OOS median daily net | ₹0.00 |
| 95% block-bootstrap CI for OOS mean daily net | -₹188.62 to ₹237.43 |
| OOS win rate / profit factor | 49.67% / 1.021 |
| OOS Sharpe / max drawdown fraction | 0.097 / 6.46% |
| Holm-adjusted p | 1.0 |
| Paired difference vs fixed-buy benchmark | +₹65.45/day |
| Paired 95% interval | -₹250.19 to ₹397.71 |
| Paired one-sided HAC p | 0.350 |
| First OOS half mean daily net | +₹109.76 |
| Second OOS half mean daily net | -₹87.60 |
| 100-bps + ₹20/order stress mean daily net | -₹98.54 |
| 200-bps + ₹20/order stress mean daily net | -₹288.37 |

The positive base point estimate is small relative to uncertainty, OOS halves have opposite signs, adjusted significance is absent, the paired interval crosses zero, and stress-cost returns are negative.

### Selected finalist comparison

| Candidate | Family | OOS mean/day | 95% CI low | Holm p | Gate |
|---:|---|---:|---:|---:|---|
| 86 | Gap continuation | ₹10.68 | -₹188.62 | 1.0 | Fail |
| 548 | Gap continuation | ₹15.73 | -₹182.11 | 1.0 | Fail |
| 223 | Gap continuation | -₹24.58 | -₹214.72 | 1.0 | Fail |
| 13 | Fixed-time long call | -₹172.22 | -₹427.51 | 1.0 | Fail |
| 45 | Initial-move momentum | -₹54.76 | -₹357.99 | 1.0 | Fail |
| 349 | Gap continuation | ₹1.61 | -₹209.33 | 1.0 | Fail |
| 166 | Opening-range breakout | -₹25.85 | -₹262.20 | 1.0 | Fail |
| 173 | Gap continuation | ₹23.67 | -₹121.18 | 1.0 | Fail |
| 332 | Gap continuation | ₹70.35 | -₹49.03 | 1.0 | Fail |
| 303 | Gap continuation | ₹61.11 | -₹69.99 | 1.0 | Fail |

All 20 validation-selected finalists failed the statistical gate; all 600 candidates failed the strict execution/promotion gate. The full 600-candidate metrics and 20-finalist table are in the [workflow artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501).

### Stress comparison (mean daily net, ₹; simulated)

```text
Base modeled costs       +10.68 | █
100 bps + ₹20/order      -98.54 | █████
200 bps + ₹20/order     -288.37 | ██████████████
```

## 6. Discussion and inferences

1. **No evidence-supported winner was discovered.** Zero of 600 candidates passed the statistical gate.
2. **This is data-limited, not proof of universal inefficiency.** Rolling ATM-relative rows do not establish exact contract identity or executable quotes.
3. **Duplicate conflicts are a primary blocker.** Their source key and schema semantics must be diagnosed; arbitrary deduplication could distort trades.
4. **Execution realism is unresolved.** Bid/ask, depth, contract identity, expiry, lot size and date-specific charges must be reconciled before profitability claims.
5. **Evolution increases selection risk.** A large candidate search can select chance patterns; multiplicity correction and locked OOS testing did not validate these candidates.
6. **Method label matters.** This was a deterministic constrained adaptation inspired by QuantEvolve, not the original LLM multi-agent implementation.

## 7. Strengths and limitations

**Strengths:** fresh isolated research namespace; bounded candidate budget; chronological train/validation/OOS; OOS not used for evolution; Holm correction and block uncertainty; fixed-buy comparisons; cost stress; failed requests preserved; 11 automated tests passed both before and after the run.

**Limitations:** duplicate-quality gate failed; no historical bid/ask/depth; exact expiry/strike continuity and dated lot sizes are unverified; broker costs are provisional; intermittent HTTP 502s; candidate point estimates are unstable; automated checks are not an independent audit; the study does not reproduce original QuantEvolve. The user explicitly declined a tester, so no independent review is claimed.

## 8. Conclusion

The bounded search completed, but **did not identify a strategy that can responsibly be described as profitable**. The strongest validation-selected candidate had a near-zero OOS mean, wide uncertainty, no adjusted significance, inconsistent OOS halves and negative stressed-cost performance. Data-quality and execution gates failed. Final decision: **DATA-LIMITED / NO-GO for paper or live deployment**. No strategy is recommended.

## 9. Future directions

1. Diagnose rolling-relative duplicate-key semantics using small reproducible samples and payload hashes.
2. Reconcile expiry dates, strikes, option types, instrument IDs and lot sizes against dated official NSE contract files.
3. Exhaust lawful free sources for executable bid/ask/depth data before considering paid sources.
4. Freeze Paytm Money brokerage, STT, exchange fees, GST and stamp duty by effective date.
5. Rerun the frozen protocol only after the data gates pass; do not tune rules based on locked OOS outcomes.
6. If any candidate clears all gates, require a separately approved prospective paper-trading period with quote/order logs. No automatic live deployment.
7. Stop if lawful free data cannot resolve contract identity and execution limitations; do not search endlessly.

## Appendix A. Gate summary

| Gate | Outcome | Reason |
|---|---|---|
| Data volume | Passed | Multi-year underlying/options rows acquired |
| Basic data quality | **Failed** | 453/471 duplicate groups conflict |
| Search budget | Passed | 600 unique candidates, 9 generations |
| Locked OOS evaluation | Completed | Final chronology evaluated after selection |
| Statistical significance | **Failed** | Zero candidates passed; reported finalists Holm p=1.0 |
| Baseline comparison | **Failed** | Paired interval crosses zero; top finalist p=0.350 |
| Cost robustness | **Failed** | Top finalist negative under stress scenarios |
| Execution realism | **Failed** | No validated historical bid/ask/depth or exact contract identity |
| Promotion | **Failed** | Zero candidates passed strict gate |

## Appendix B. Reproducibility and artifact map

- [Workflow run and artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501)
- `run_summary.json`: splits, evolution trace, gates and best finalist.
- `candidate_results.csv`: all 600 candidates and metric families.
- `validation_finalists_oos.csv`: validation-selected OOS finalists and paired baselines.
- `source_probe.json`, `acquisition_summary.json`, `underlying_summary.json`: acquisition/source diagnostics.
- `source_failures.csv`: failed request log.
- `trade_ledger_sanitized.csv`: large per-trade ledger retained in downloadable artifact rather than Git.
- [Automated tests](test_run_research.py) · [Workflow](../../.github/workflows/quant-evolve-nob.yml).

## Appendix C. Developer handoff

Resolve open issues in [ERROR_LOG.md](ERROR_LOG.md), then rerun data-quality and contract-identity gates. Keep candidate rules frozen with respect to locked OOS outcomes. Do not recommend paper or live deployment. No tester branch/report is requested by the user.
