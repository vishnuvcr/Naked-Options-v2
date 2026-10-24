# Frozen market snapshot adapter gate

`market_snapshot.py` is a validation boundary for frozen market-only bars. It is deliberately not wired to live Yahoo or the TradingAgents vendor router. It rejects future-dated bars, unordered/duplicate timestamps, instrument mismatch, timezone-naive timestamps, malformed OHLC and invalid volume. Index spot volume may legitimately be zero and is therefore accepted.

This is a data-integrity primitive, not full session validation. It does not establish the source's timestamp convention, session calendar, missing-bar completeness, source accuracy, or whether the input archive itself was retrospectively revised. Those require provenance and external validation. Before any model run, build the exact cutoff snapshot from an immutable source artifact, hash it, and use a market-only analyst path that cannot call unrestricted vendor tools.

The standard TradingAgents graph is not yet approved for historical NIFTY replay. No LLM invocation or prediction score has been produced by this module.
