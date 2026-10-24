# Implementation Limits and Decisions

## Chart timeframe is part of the indicator definition
The supplied Pine script does not set an explicit timeframe. ZigZag calculations run on the chart's active timeframe. A historical test cannot be uniquely reproduced unless the timeframe is fixed. The current protocol omitted this essential choice, so this is a protocol defect to resolve before scoring.

## Signal availability versus pivot location
The returned chart points may identify historical pivot locations. The timestamp when the indicator knows a pivot is confirmed may be later. Evaluation must use signal-availability time and only the latest label knowable by the cutoff.

## Current implementation decision
Do not approximate ZigLib v1 with a generic ZigZag. Public library metadata identifies inputs/outputs but not enough implementation details to guarantee parity. No empirical scoring is authorized until the exact source and chart timeframe are pinned.

## Data interval decision
The protocol's 10:00 IST reference requires intraday spot bars. Daily historical OHLC can validate expiry closing prices but cannot by itself supply the exact reference price.
