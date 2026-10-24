# Phase Status — ZigZag Expiry Direction

Updated: 2026-10-25

| Phase | Status | Evidence / blocker |
|---|---|---|
| 1. Protocol/source audit | PARTIALLY COMPLETE — BLOCKED | TradingView ZigLib page states the function returns direction and two chart points (library page dated Oct 9, 2023); TradingView's generic Zigzag documentation explicitly warns that confirmed labels are drawn into the past and the latest solid line is not final. A public GitHub mirror of the wrapper script confirms `repaint=true` is the default and that the non-repaint branch only draws on direction changes using prior-bar point values; however, it does not contain the imported ZigLib implementation and is not an authoritative source. Exact ZigLib v1 source semantics and signal-availability time remain unverified. NSE official contract page confirms current Tuesday expiry with previous-session holiday shift, but historical circular mapping remains incomplete. |
| 2. Data audit | BLOCKED | Existing NWCP data has unresolved source overlap, timestamp/provenance and expiry-calendar issues; it is not automatically admissible for this experiment. |
| 3. Causal reconstruction | BLOCKED | Cannot safely substitute a generic ZigZag or guessed port for the exact imported library. |
| 4. Evaluation | NOT STARTED | No eligible ZigZag predictions scored. |
| 5. Robustness/inference | NOT STARTED | Depends on valid out-of-sample results. |
| 6. Manuscript/decision | PROTOCOL DRAFTED | Manuscript skeleton exists; results, figures, tables and conclusions cannot be populated without validated empirical output. |

## Evidence reviewed
- TradingView ZigLib library page: https://www.tradingview.com/script/NC3cgEcT-ZigLib/ — describes `zigzag(_low, _high, depth, deviation, backstep)` and its returned direction and two chart points, but the accessible page summary does not expose enough implementation detail to validate historical availability.
- TradingView ZigZag++ page: https://www.tradingview.com/script/lj8djt1n-ZigZag/ — release notes mention advanced repainting control; that does not prove this exact pasted script/library combination is non-repainting.
- TradingView general ZigZag explanation: https://www.tradingview.com/support/solutions/43000591664-zigzag-indicator/ — explains confirmation lag and that the latest displayed line may be revised. This is general background, not a substitute for ZigLib v1 source.

**Current decision:** DATA-LIMITED / NO PERFORMANCE CLAIM. This run did not produce an empirical accuracy estimate. No tester gate was added because the user explicitly waived independent tester review for this experiment.
