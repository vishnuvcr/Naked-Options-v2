# Independent tester report — VOL-REGIME-OPT-1.0

**Review date:** 2026-10-15  
**Reviewer role:** Independent source-gate tester  
**Disposition:** BLOCKED — do not calculate or report P&L

## Scope reviewed

Reviewed the frozen protocol, source probe, workflow, saved audit, source-gate disposition and public exchange/API documentation. This review is limited to data feasibility and contract identity; no strategy profitability or statistical claims are tested because no P&L artifact exists.

## Findings

1. **Dhan schema is a partial pass, not contract proof.** The original persisted audit showed WEEK codes 1 and 2 each return 375 CALL and PUT rows in the short 2025-01-06–2025-01-10 sample; WEEK code 0 fails with `DH-905: expiryCode is required`. I independently inspected workflow [#10](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667) logs: code 3 returned 357 CALL and 349 PUT rows with required basic fields and monotonic timestamps. The overall run failed because a runner shutdown canceled the HF fallback probe; audit/cache/artifact steps were skipped. The available log excerpt did not preserve the code-3 PUT hash, and the developer correctly leaves it null. The HF fallback remains unverified.
2. **Expiry mapping is not proven.** The audit's returned fields include timestamps, strike, spot, IV and OHLC, but no explicit expiry-date field. NSE's public specification states that NIFTY weekly options expire on Tuesday (previous trading day if Tuesday is a holiday), but this calendar rule does not itself map Dhan rolling expiry codes to each actual date. Source: https://www.nseindia.com/static/products-services/equity-derivatives-nifty50
3. **Exact-contract continuity is not proven.** Rolling ATM-relative data is not sufficient evidence that the same numeric strike and expiry have executable entry and expiry-exit prices. No contract-level matched ledger or coverage report exists.
4. **Fallback source is not accepted.** The HF probe script records the dataset license as `other` and requires provider-terms review. Its expected audit file was not present on the reviewed developer branch. No successful licensed, quality-checked fallback acquisition is evidenced.
5. **No P&L or cost test exists.** Lot-size mapping, historical charges, slippage, missing-contract coverage, statistical comparisons, tail-risk analysis and independent numerical reproduction have not run.

## Gate-by-gate result

| Gate | Result | Reason |
|---|---|---|
| Weekly endpoint schema | Partial pass | Candidate codes 1/2 schema pass only |
| Code-3 follow-up | Unverified | No newer saved audit |
| Expiry date mapping | Fail / unverified | No code-to-date evidence across historical calendar |
| Exact numeric strike and expiry continuity | Fail / unverified | No matched contract-level entry/exit ledger |
| Licensed fallback | Not established | Audit absent; license flagged for review |
| Full coverage and duplicate gates | Not run | No full acquisition |
| Fees, slippage and lot sizes | Not run | No trade ledger |
| Statistics and risk gates | Not run | No P&L |
| Strategy approval | NO | Required predecessor gates fail |

## Required disposition

**Close the current bounded study as BLOCKED.** The code-3 schema pass does not resolve the key identity problem: no evidence maps each rolling expiry code to actual expiry dates across historical calendar changes, and no matched fixed-contract entry-to-expiry ledger demonstrates strike/expiry continuity. Do not loosen the frozen gates, substitute monthly data, infer profitability from schema success, or present the block as evidence that the strategy loses money. A future study may be opened only with a documented source/contract-identity solution and a preregistered plan.

## Developer instructions

Keep the frozen hypothesis unchanged; update README, phase status, error log and interaction log to reflect the tester's blocked disposition. Do not proceed to P&L. If source data later becomes verifiable, start a separately reviewed correction or version rather than retroactively treating this source gate as passed.


## Final bounded source-gate retest — 2026-10-15

- Rechecked workflow #10 logs and the developer's persisted sanitized audit after the original report.
- WEEK code 3 is now evidenced as a schema pass in the workflow log (357 CALL rows; 349 PUT rows), but this is only a short-window rolling series. No explicit expiry date or fixed contract identifier was returned.
- HF fallback remained unverified because the workflow runner was shut down during the fallback probe. No fallback artifact or license/coverage gate is accepted.
- **Final disposition: BLOCKED / CLOSE FOR THIS PROTOCOL.** No full acquisition, P&L, costs, inference, or profitability result exists. This is a feasibility blocker, not a finding that the hypothesis loses money.

**Developer instructions:** update all main/developer status documents and stop this protocol before P&L. If a verifiable contract-level source is found later, start a new version with a frozen plan. **Tester instruction:** this report is the independent source-gate disposition; no further tester loops are authorized under the current frozen plan.
