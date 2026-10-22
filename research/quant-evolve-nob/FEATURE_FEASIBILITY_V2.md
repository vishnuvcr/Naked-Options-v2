# QE-NOB-2.0 Phase 2 — Feature and source feasibility audit

**Status:** Initial static audit COMPLETE; runtime/cache coverage audit NOT YET RUN on this branch.  
**Evidence basis:** QE-NOB-1.0 source code, config, final reports and documented source limitations. This is a code/document review, not fresh market-data validation.

## Feature availability matrix

| Proposed feature / mechanism | Current evidence in QE-NOB-1.0 pipeline | QE-NOB-2.0 decision |
|---|---|---|
| NIFTY 5-minute OHLC | Cached Dhan underlying bars used in prior run | Eligible after timestamp/session/coverage recheck |
| Opening range / gap / trend / EMA / VWAP | Implemented in existing signal code | Keep as baselines; not considered novel by itself |
| Option OHLC, spot, rolling strike, IV, volume, OI | Dhan rolling endpoint requests these fields; partial multi-year WEEK1 files exist | Active run is weekly expiry only, ATM/OTM1 only; audit actual fields/coverage after fresh acquisition |
| Exact option expiry/contract identity | Not reliably exposed by rolling endpoint | DATA-LIMITED; active WEEK1 family describes the requested source bucket, not exact exchange contract identity |
| Historical bid/ask/depth | Not available in current cached feed | Execution gate remains FAIL; modeled slippage only |
| Historical IV surface / skew / term structure | Single rolling IV observations may be available; complete fixed-contract surface not verified | Conditional only after coverage and identity tests |
| Option-volume/OI changes | Requested by source, but completeness and source timestamp semantics require audit | Conditional; missing/zero distinction must be preserved |
| India VIX | Not confirmed in current QE-NOB cache | Search official/free source; include only with verified timestamps |
| Global index/futures leads | Not confirmed in current cache | Search free sources; align market-close/release timestamps to IST and prevent lookahead |
| FII/DII flows | Not confirmed in current cache | Use official NSE sources if daily values and publication timing can be established; likely daily regime feature only |
| Market breadth / constituent data | Not confirmed in current cache | Do not add until point-in-time constituents and survivorship handling are established |
| Corporate actions | Not relevant to direct index price in the same way as single stocks, but constituent actions can affect index composition | Track index methodology/constituent changes if component-level data are used |
| Scheduled news/events | No verified timestamped event dataset in current pipeline | Search free/licensed sources; otherwise omit from executable grammar |
| Historical option chain PCR | Not verified as complete point-in-time dataset | Conditional; do not infer missing chain from rolling ATM observations |
| Transaction fees / lot size | Dated fee and weekly/monthly lot-size proxy code exists | Active v2 protocol uses WEEK1 only; keep the lot-size estimate labeled as a proxy until reconciled against exact dated contract master |
| Broker fills / queue position | Not present | Cannot claim live execution realism |

## Initial source strategy

1. Reuse the isolated QE-NOB cache as a starting point only after checksums, schema and field-level missingness are recomputed; do not copy performance outcomes into candidate fitness.
2. Check official NSE/NSE Indices sources for India VIX, derivatives contract specifications, lot-size/expiry circulars, FII/DII and index methodology.
3. Check free official global-market data sources (e.g. FRED and exchange/central-bank sources) for broad risk proxies; use only fields with correct timezone and known publication times.
4. Inspect Hugging Face, Zenodo, GitHub and Kaggle catalogue results for licensing, provenance, schema, date coverage and duplicates before any bulk download. A dataset is not approved merely because it is public.
5. If data are absent or incompatible, mark the mechanism untestable; do not interpolate option prices, invent quotes, or silently splice non-equivalent contracts.

## Required Phase 2 runtime deliverable

Create a machine-readable feature availability matrix containing source, field, timestamp timezone, publication lag, coverage, missingness, license/usage status, contract identity, checksum and inclusion decision. Every failed request must record source, endpoint, error class, retry count and cache state without credentials.

## Decision

The current data supports exploratory structural discovery primarily on 5-minute NIFTY bars and rolling option OHLC/IV/OI/volume. It does not yet support all proposed mechanism families. Before Phase 3, run a field-level cache audit and public-source catalogue refresh. The strategy grammar must be feature-gated: unsupported or lookahead-prone features are excluded, not replaced with fabricated values.


## Current scope amendment — 2026-10-23

The latest partial cache audit found 314 historical weekly-option files for the allowed ATM/OTM1 offset set, but no historical underlying bars and no historical monthly-option files. Therefore QE-NOB-2.0's active acquisition/candidate universe is restricted to WEEK1 weekly expiry and ATM/OTM1. This is a run-specific data-feasibility decision, not a conclusion that monthly options cannot be obtained from other sources. Fresh source coverage and field completeness remain unverified until the next bounded acquisition artifact is inspected.
