import unittest
from copy import deepcopy

from market_snapshot import validate_market_snapshot


BASE = [
    {
        "instrument": "NIFTY 50",
        "timestamp": "2026-01-06T09:15:00+05:30",
        "open": 100.0, "high": 103.0, "low": 99.0, "close": 102.0, "volume": 0,
    },
    {
        "instrument": "NIFTY 50",
        "timestamp": "2026-01-06T09:20:00+05:30",
        "open": 102.0, "high": 104.0, "low": 101.0, "close": 103.0, "volume": 0,
    },
]


class MarketSnapshotTests(unittest.TestCase):
    def test_accepts_ordered_pre_cutoff_bars(self):
        result = validate_market_snapshot(BASE, "2026-01-06T10:00:00+05:30")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[-1]["close"], 103.0)

    def test_rejects_future_bar(self):
        with self.assertRaisesRegex(ValueError, "later than cutoff"):
            validate_market_snapshot(BASE, "2026-01-06T09:17:00+05:30")

    def test_rejects_duplicate_or_unordered_bars(self):
        bad = deepcopy(BASE)
        bad[1]["timestamp"] = bad[0]["timestamp"]
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            validate_market_snapshot(bad, "2026-01-06T10:00:00+05:30")

    def test_rejects_instrument_mismatch(self):
        bad = deepcopy(BASE)
        bad[0]["instrument"] = "NIFTY BANK"
        with self.assertRaisesRegex(ValueError, "instrument mismatch"):
            validate_market_snapshot(bad, "2026-01-06T10:00:00+05:30")

    def test_rejects_invalid_ohlc(self):
        bad = deepcopy(BASE)
        bad[0]["high"] = 98.0
        with self.assertRaisesRegex(ValueError, "inconsistent OHLC"):
            validate_market_snapshot(bad, "2026-01-06T10:00:00+05:30")

    def test_rejects_missing_timezone(self):
        bad = deepcopy(BASE)
        bad[0]["timestamp"] = "2026-01-06T09:15:00"
        with self.assertRaisesRegex(ValueError, "timezone offset"):
            validate_market_snapshot(bad, "2026-01-06T10:00:00+05:30")


if __name__ == "__main__":
    unittest.main()
