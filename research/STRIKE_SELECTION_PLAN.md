# Strike-selection study plan — OPT-BUY-2.0

**Status:** protocol frozen; strike-grid run pending  
**Branch:** `research/option-strike-selection`  
**Predecessor:** OPT-BUY-1.0, closed no-go for the tested candidates  
**Purpose:** test strike placement with the same frozen technical Logistic volatility-expansion classifier. This does not reopen or overwrite NIFTY-PRED-1.0 or OPT-BUY-1.0.

## Research question
Does a prespecified call/put strike-distance combination produce better after-cost same-session long-option outcomes when the prior 5- or 20-session volatility-expansion alert is held fixed?

## Fixed protocol
- Rebuild the same classifier and use the same development-only out-of-fold thresholds and chronological test origins as OPT-BUY-1.0. Do not refit/tune based on option outcomes.
- Entry 09:20 five-minute bar open; exit 15:25 bar close on the same session; require the exact same numeric strike at exit; never forward-fill or substitute strikes.
- Compare call relative offsets {0,+1,+2,+3} with put offsets {0,-1,-2,-3}: 16 prespecified pairs, including ATM straddle, symmetric OTM strangles, and asymmetric pairs. These are rolling relative-offset labels at entry; follow the actual numeric strikes for exits.
- Evaluate each candidate on its own eligible dates and also report a common-date sensitivity subset; show coverage for every candidate. No comparisons across non-comparable samples without explicit warning.
- Primary costs: ₹10 per executed order, four orders per completed two-leg round trip, statutory/exchange fees and 50 bps adverse slippage per premium side. Sensitivity: ₹20 brokerage/order and 0/25/50/100 bps per side.
- Report mean daily net rupee P&L, per-trade return, win rate, 95% moving-block bootstrap intervals, chronological halves, and alert-filtered versus always-buy comparisons. Apply Holm correction across the full prespecified primary comparison family (all candidate × horizon tests).
- Keep the final chronological holdout untouched for any follow-up protocol; this phase is historical screening, not deployment approval.

## Non-negotiable gates
1. Quote coverage at least 80% for each candidate being interpreted confirmatorily.
2. Conflicting duplicate-group rate at most 1%.
3. At least 100 alert trades for a candidate.
4. Positive mean after-cost P&L with 95% block interval lower bound above zero; positive under 100-bps slippage and in both chronological halves.
5. Correctly adjusted multiplicity and an independent tester report before any candidate can be considered for prospective paper testing.

If the inherited quote dataset fails the quality gates, strike-grid outputs are exploratory only and no candidate is declared a winner. Do not relax gates to force a result. Stop after this one predefined grid; no further parameter loops.

## Data availability caveat
OPT-BUY-1.0 acquired rolling options at ATM offsets -3..+3. This permits the proposed grid only where exact entry/exit strikes are represented; it is not stable expiry-specific contract history or historical bid/ask. The predecessor data-quality gate failed (strangle coverage 69.18%; conflicting duplicate groups 1.409%). The current run must remeasure these properties and clearly label any analysis non-confirmatory if the gate still fails.

## Deliverables and phase order
1. Verify cached option data, schema, offsets, quote coverage and conflict rate.
2. Run unit tests for strike matching and cost accounting.
3. Execute the frozen 16-pair × 2-horizon grid, all cost/slippage sensitivities.
4. Publish machine-readable candidate metrics, sanitized ledger, coverage and figures.
5. Developer documents result and proposed disposition.
6. Independent tester on separate branch reproduces candidate mapping, fees, bootstrap and Holm correction. Developer may not advance past tester FAIL.
7. Update main README, phase status, experiment/error/interaction logs and Pages content with actual run evidence.
8. Stop at the gates above; no strategy approval is implied by a statistically better but unprofitable candidate.
