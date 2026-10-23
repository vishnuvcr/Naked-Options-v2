# QE-NOB-3.0 — New Strategy Hypothesis Lab

**Status:** Design complete; empirical testing blocked until fresh-data gate passes.  
**Parent:** QE-NOB-2.0, closed DATA-LIMITED.  
**Governance:** Developer-led; no independent tester branch, per explicit user instruction. Automated tests and statistical gates remain mandatory.

## 1. Purpose and research questions

QE-NOB-2.0 found statistically screened candidates but no execution-gate passes. Rolling ATM-relative option OHLC does not prove stable dated contract identity or executable quotes. Its OOS period has already been examined and must not be reused for new strategy selection. QE-NOB-3.0 proposes distinct, falsifiable hypotheses rather than expanding the old parameter search.

Questions:
1. Do failed-breakout/reclaim rules differ from opening-range continuation?
2. Do trend-pullback/reclaim rules improve on simple momentum baselines?
3. Does volatility compression followed by expansion add information beyond simple momentum?
4. Does gap fade work only in range regimes, while gap continuation is a separate trend-regime hypothesis?
5. Can any effect survive chronological OOS, multiple-testing correction, cost stress and execution-data gates?
6. Which families remain untestable because required fields or contract identity are missing?

## 2. Proposed strategies (hypotheses only; none is claimed tested or profitable)

### H1 — Failed opening-range breakout and reclaim
**Hypothesis:** A breakout that closes back inside the frozen opening range and subsequently reclaims in the opposite direction may indicate failed continuation. A failed upside break maps to a PUT hypothesis; failed downside break maps to CALL. Require completed bars and next-bar entry. Risks: intrabar sequence ambiguity, regime dependence, low trade count.

### H2 — Trend pullback and reclaim
**Hypothesis:** In a persistent intraday trend, a pullback followed by a confirmed reclaim may improve entry timing versus buying the initial breakout. Use session-reset EMA(8)/EMA(21) sign for trend state, then a predeclared pullback/reclaim definition. Risks: chop, local-extrema lookahead, late entries.

### H3 — Volatility compression then expansion
**Hypothesis:** A confirmed range expansion after a historically compressed within-session range may be more informative than a plain range break. Estimate percentiles from prior observations only; direction follows the confirmed break. Risks: false breakouts, percentile instability and multiple testing.

### H4 — Opening-gap fade conditioned on regime
**Hypothesis:** Signed gaps may mean-revert in range regimes but continue in trend regimes. Test fade and continuation as separate preregistered hypotheses; do not relabel based on outcomes. Use only prior close and current session open for the gap. Risks: overnight news confounding and signed/absolute gap errors.

### H5 — Time-of-day conditional signal
**Hypothesis:** A fixed, small set of predeclared time buckets may change the quality/cost of trend or reversal signals. Do not mine arbitrary minute cutoffs. Risks: microstructure costs, regime drift and multiple testing.

### H6 — Option premium breakeven filter (disabled until data gate)
**Hypothesis:** Reject underlying signals where a defensible expected move over the horizon is smaller than the option-implied breakeven move. Requires stable exact contract identity, strike, expiry and timestamp-valid premium/quote data. Rolling ATM-relative OHLC alone is insufficient; do not implement this family unless contract and quote coverage pass.

## 3. Baselines and scope

Compare each family with no-trade, simple time-matched momentum, simple opening-range breakout, frozen QE-NOB-2.0 rules as historical references only, and session-preserving placebo signals. Do not use old scores as seed fitness. Long CALL/PUT only; no short option legs, averaging down, martingale or live orders.

## 4. Fresh data gate — mandatory before empirical testing

- Validate Dhan authentication and source timestamp/bar semantics; secrets remain in GitHub Actions and must never be printed.
- Acquire a fresh period not included in the QE-NOB-2.0 OOS block, or another documented historical period not previously examined for strategy selection.
- Preserve cache, checksums, provenance, missingness and source failures.
- Require a sufficiently complete NIFTY underlying series and stable dated option contract identity for option P&L.
- For execution claims, require contemporaneous bid/ask or defensible quote data and documented dated fees.
- Never infer missing prices, silently stitch contracts or treat rolling offsets as exact contracts.

If this gate fails, stop at design and report DATA-LIMITED. Do not substitute the old OOS period.

## 5. Formula, simulator and software tests

Required tests: hand-calculated gap/opening-range/EMA/realized-range fixtures; property tests for no future data; session-boundary and next-bar timing; no-overlap; stop/target ambiguity with conservative stop-first ordering; duplicate timestamps and missing-data fail-closed behavior; stable contract mapping across expiry/strike/lot changes; deterministic signatures and lineage.

## 6. Bounded discovery and statistical protocol

- Maximum 600 unique structurally distinct candidates; four deterministic seeds; at most 12 generations; at most six families.
- Evolution and selection use training/inner validation only. Freeze candidates and analysis choices before one untouched OOS evaluation.
- If an untouched OOS period cannot be established, report no empirical validation.
- Compare against baselines and placebos. Use session-level moving-block bootstrap with block length frozen before OOS, Holm correction across the complete predeclared finalist family, and alpha 0.05.
- Report confidence intervals, median daily P&L, drawdown/tail loss, trade count, turnover, regime/time-block stability and concentration in best days.
- Cost grid: 0/25/50/100/200 bps slippage per side × ₹10/₹20 brokerage per order, plus dated statutory/exchange fees.
- Reject effects dependent on a few extreme winners, one day/month, one cost point, one lot-size regime or insufficient trades.
- A statistical pass cannot override failed contract identity or execution-data gates.

## 7. Phases and stopping rule

| Phase | Deliverable | Exit gate |
|---|---|---|
| 0. Hypothesis design | This preregistered plan | Complete |
| 1. Fresh data feasibility | Source, coverage and contract matrix | Pass data gate or stop |
| 2. Feature/grammar implementation | Typed rules, signatures, tests | All tests pass |
| 3. Simulator/baselines | Hand-calculated fixtures and baselines | Timing, costs and no-overlap verified |
| 4. Bounded discovery | Archive and lineage, ≤600 candidates | Cap reached or gate fails |
| 5. Frozen evaluation | OOS, bootstrap, Holm, cost stress | One frozen evaluation only |
| 6. Manuscript/disposition | Tables, figures, logs, limitations | PASS_FOR_FURTHER_SIMULATION, NO-GO or DATA-LIMITED; stop |

No expansion without a new protocol version. No live trading approval.

## 8. Immediate action order

1. Check repository phase status, source errors and Dhan auth setup.
2. Run existing automated source-client tests before any large acquisition.
3. Attempt bounded acquisition of a fresh untouched period and measure actual row coverage.
4. If exact contract mapping and quote-level data remain unavailable, close empirical testing as DATA-LIMITED.
5. If gates pass, implement H1–H5; keep H6 disabled until its data gate passes.
6. Do not inspect new OOS performance until candidates and statistical protocol are frozen.

## Current decision

**Design: COMPLETE. Empirical testing: NOT STARTED; blocked on fresh-data eligibility.** QE-NOB-2.0 OOS remains sealed from new selection. These are hypotheses, not recommendations or claims of profitability.
