# TradingView Pine Indicator Candidate Catalogue — NWCP-1.0

This catalogue specifies candidate ideas to implement and test in Python first. It does not imply that any script has passed repainting, licensing or predictive-value gates. Community source code must be audited individually before reuse.

| Indicator family | Candidate definition | Cutoff/repainting checks |
|---|---|---|
| RSI | Wilder-style rolling gain/loss on completed bars | Confirmed 09:59 bar only; verify parity with chosen Pine version |
| MACD | EMA(12) minus EMA(26); signal EMA(9); histogram | No future/negative offsets or unconfirmed values |
| EMA spread and slope | EMA(5/10/20) normalized by spot; slope over fixed past bars | Ensure all spans are trailing and no centered smoothing |
| ATR-normalized trend | Close-to-EMA or multi-session return scaled by ATR(14) | ATR only from information available at the anchor |
| ADX/DMI | Standard directional movement / Wilder smoothing | Verify initialization and warmup; no repainting higher-timeframe requests |
| Supertrend | ATR-band trend state with explicit trailing recursion | Port exact formula/license; test all state transitions |
| Bollinger position/width | Position relative to rolling mean ±2 standard deviations and width normalized by price | No centered windows; match standard-deviation/window semantics |
| Donchian channel position | Position relative to trailing highs/lows | Prefer prior completed windows; no future bars |
| Stochastic momentum | Close location inside trailing high-low range | Current partial-session highs/lows allowed only through anchor cutoff |
| VWAP distance | Spot vs VWAP with eligible traded-volume data | Index itself may not have meaningful volume; only use verified proxy, never fabricate volume |

## Original NWCP indicators

- **AIA — Anchor Impulse/ATR:** normalized change from prior expiry close to the 10:00 anchor, divided by ATR-normalized move. Tests whether post-expiry displacement is large relative to recent volatility.
- **OWPE — Open-Window Path Efficiency:** absolute change from the first session price through 10:00 divided by total absolute path movement across completed one-minute bars.
- **MHDA — Multi-Horizon Directional Agreement:** sign/weighted agreement of trailing returns over 1, 3, 5 and 10 sessions; weights cannot be selected on the sealed test.
- **VSRP — Volatility-Scaled Range Position:** anchor location inside a trailing range, with range width normalized by ATR.
- **CMRP — Cross-Market Risk Pulse:** robust aggregate of eligible standardized global risk-asset changes observed by 10:00 IST; disabled until history and publication-time coverage are verified.
- **TCD — Trend/Chop Divergence:** trend-strength proxy less realized path-choppiness proxy. Treat as hypothesis and test through ablation.

## Source-backed TradingView candidates reviewed on 2026-10-24

| Script | Source page evidence | NWCP treatment |
|---|---|---|
| [Donchian Channels [Gu5]](https://www.tradingview.com/script/Cc7xGmYO-Donchian-Channels-Gu5/) by gu5tavo71 | TradingView marks it OPEN-SOURCE; updated 23 Dec 2024; traditional highest-high/lowest-low channel and trend state | Candidate for channel position and breakout state. Review script offsets, alert conditions and license/House Rules before reuse. |
| [Bollinger Bands](https://www.tradingview.com/script/ViWAOiIc-Bollinger-Bands/) by Madrid | TradingView marks it OPEN-SOURCE; updated 8 May 2018; describes traditional bands and colored moving-average basis | Candidate benchmark; independently implement rolling mean and standard deviation; no right shift. |
| [Better Bollinger Bands](https://www.tradingview.com/script/BP8qbzQm-Better-Bollinger-Bands/) by PyneSys | TradingView marks it OPEN-SOURCE; updated 21 Sep 2024; includes configurable moving-average/deviation methods and optional shifts | Only unshifted, trailing formulas are eligible. Exclude any future plotting offset from prediction features. |
| [SuperTrend [everget]](https://www.tradingview.com/script/VLWVV7tH-SuperTrend-everget/) by evergetWizard | TradingView marks it OPEN-SOURCE; updated 28 Jul 2025; ATR-based trend/stop state; Pine v6 update | Candidate trend-state feature. Needs state-transition tests, initialization parity and explicit confirmed-bar handling. |
| [Donchian Channels Strength](https://www.tradingview.com/script/hCfZsNU2-Donchian-Channels-Strength/) by Daniel_Ge | TradingView marks it OPEN-SOURCE; updated 2 Feb 2025; Pine v6; oscillator based on price versus Donchian average | Candidate alternative strength feature; investigate redundancy with RSI/range position. |
| [Relative Channel Bandwidth](https://www.tradingview.com/script/MCmQBod1-Relative-Channel-Bandwidth/) by TrendoscopeWizard | TradingView marks it OPEN-SOURCE; combines Bollinger, Donchian and Keltner channel bandwidth concepts | Candidate volatility-regime feature only after confirming formulas and avoiding future/shifted bands. |
| [ADX and DI by MiG](https://www.tradingview.com/script/ZPS2KYg2/) | Search result identifies this page as a PROTECTED SOURCE SCRIPT | Excluded from code reuse. Standard ADX/DMI can be implemented independently from documented equations. |

These pages establish that the listed scripts were presented as open-source on TradingView, not that their source carries an OSI-approved permissive software license. TradingView's page notes that republishing remains subject to its House Rules. Accordingly, NWCP will not copy or redistribute script source without a clear rights basis; it will independently implement the documented math and test its timestamp behavior. This is a source catalogue, not an empirical-performance ranking.

## Open-source Pine audit checklist

For each selected source script, record source URL, author, retrieval date, license, exact revision/hash, Pine version, inputs, timeframe, security() usage, lookahead settings, unconfirmed-bar/realtime behavior, future references, offsets, data dependencies and formula tests. If no license is provided or derivative-work terms are unclear, do not copy source; write a separate implementation of a documented formula and attribute the method.

TradingView official repainting documentation: https://www.tradingview.com/pine-script-docs/concepts/repainting/
