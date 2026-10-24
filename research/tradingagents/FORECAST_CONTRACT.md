# Forecast Contract and Causal-Input Gate

## Purpose
This is the first implementation slice of Phase D. It specifies the output record and enforces temporal integrity at the record boundary. It is not a forecast engine and does not prove that model prompts or vendor internals used only the declared inputs.

## Forecast record
Required fields are defined in `forecast_contract.py`: schema version; instrument; unique forecast ID; cutoff and target interval; class (UP/DOWN/ABSTAIN); model identity/revision; SHA-256 hashes for prompt and input manifest; latest input as-of timestamp; record creation time; and status. Uncertainty must be represented by ABSTAIN until probability calibration is designed and validated. Arbitrary confidence numbers are not accepted.

## Temporal rules
- Every timestamp must include an explicit timezone offset.
- Target start must precede target end.
- Declared input as-of time cannot be later than cutoff.
- Record creation cannot precede cutoff.
- Input manifest must enumerate exact data artifacts, source, retrieval time, bar timestamps, transformations, and content hashes. A hash proves identity, not correctness or absence of leakage.
- Historical news, macro, social, and fundamentals are excluded unless point-in-time snapshots are frozen and verifiably timestamped.
- Live Yahoo data is not a substitute for a historical archive.

## Known framework limitation
The pinned TradingAgents market-data tool accepts date-based windows, and the Yahoo vendor converts its index to timezone-naive values for formatted output. This does not by itself enforce an intraday 10:00 IST cutoff. Therefore do not pass an expiry-day daily candle or live/latest context into a historical cutoff run. A future adapter must inject a prefiltered frozen market-only snapshot and prevent the stock tool from retrieving unfiltered data.

## Next gate
Run these deterministic unit tests in CI. Then inspect how to supply a fixed pre-cutoff OHLCV/indicator snapshot to the graph without allowing unrestricted vendor tools. No historical prediction score until this adapter is proven on frozen data.
