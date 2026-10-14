# Developer Disposition — OPT-BUY-1.0

**Date:** 2026-10-14  
**Developer branch:** `research/option-buying-developer`  
**Result source:** [Actions run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384)  
**Independent review:** [TESTER_REPORT.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-independent-tester/research/option-validation/TESTER_REPORT.md)  
**Disposition:** **ACCEPT TESTER NO-GO; CLOSE THIS BOUNDED STUDY.**

## What was verified

The corrected workflow acquired/reused the 14-series monthly rolling-option grid, completed analysis and report generation, passed all 13 unit tests before and after analysis, and saved its sanitized result artifact. Independent audit of the artifact reproduced the ledger P&L and cost identities to floating-point precision and reproduced the primary paired daily P&L means, block intervals and p-values. The source code uses same-session numeric strike matching, exact +1 CALL/−1 PUT relative-offset requirements for the one-step strangle, and skips missing exits rather than filling or substituting them.

## Why the acceptance gate cannot pass

- Straddle coverage 83.98% passes the 80% threshold; strangle coverage 69.18% fails.
- Conflicting duplicate quote groups are 452/32,085 = 1.409%, above the frozen 1% maximum.
- At ₹10 brokerage/order and 50 bps slippage per premium side, the four candidates' mean daily net P&L is between −₹315.71 and −₹369.43 per one-lot-proxy eligible-day slot. Every candidate 95% interval is negative; all candidates fail the 100-bps and both-chronological-halves positivity tests.
- The positive paired difference versus always-buy is statistically reproducible (Holm-adjusted p=0.002), but it indicates only fewer losses than a worse benchmark. It does not satisfy profitability criteria.

The tester correctly distinguished computational reproducibility from strategy approval. Because both the quality and profitability gates fail, it would be scientifically invalid to change the gate or continue variants just to obtain a pass.

## Final research conclusion

No option-buying strategy is validated by OPT-BUY-1.0. The tested alert-filtered intraday long straddles/strangles are unprofitable after the modeled costs, and incomplete option quote coverage prevents a confirmatory conclusion about the broader volatility-expansion hypothesis. The bounded study is closed as **NO-GO for the tested candidates / INCONCLUSIVE for the general hypothesis**. No paper-trading or live-deployment recommendation is made. Preserve the results, manuscript, charts, artifact hash and test logs.

## Final gates

| Gate | Result |
|---|---|
| Acquisition/API and cache schema | PASS |
| Unit/math/quote-selection tests | PASS (13/13 pre- and post-analysis) |
| P&L/fee arithmetic independent audit | PASS |
| Paired comparisons/CI/p-values reproducibility | PASS |
| Quote coverage | FAIL |
| Conflicting duplicate rate | FAIL |
| Candidate positive net profitability | FAIL |
| 100-bps robustness | FAIL |
| Positive performance in both halves | FAIL |
| Overall strategy approval | NO-GO |

## Instruction to tester

Tester review is accepted as final for this version. Preserve the report and its evidence. Do not issue a PASS for strategy approval, and do not relax thresholds; only a new user-authorized protocol/version may reopen the general hypothesis.
