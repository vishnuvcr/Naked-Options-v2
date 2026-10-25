import importlib.util
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research" / "nifty-prediction" / "evaluate_weekly_expiry.py"
spec = importlib.util.spec_from_file_location("weekly_expiry", SCRIPT)
weekly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weekly)


class WeeklyExpiryTests(unittest.TestCase):
    def test_expiry_weekday_regime(self):
        self.assertEqual(weekly.expiry_weekday(pd.Timestamp("2025-08-28")), 3)
        self.assertEqual(weekly.expiry_weekday(pd.Timestamp("2025-09-02")), 1)

    def test_target_is_next_expiry_close_from_prior_expiry_cutoff(self):
        dates = pd.bdate_range("2023-01-02", "2026-10-23")
        rng = np.random.default_rng(18)
        close = 18000 * np.cumprod(1 + rng.normal(0.0002, 0.008, len(dates)))
        open_ = close * (1 + rng.normal(0, 0.001, len(dates)))
        high = np.maximum(open_, close) * 1.002
        low = np.minimum(open_, close) * 0.998
        data = pd.DataFrame({"date": dates, "open": open_, "high": high, "low": low, "close": close})
        frame, meta = weekly.build_weekly_examples(data)
        self.assertGreater(len(frame), 100)
        first = frame.iloc[0]
        cutoff = data.loc[data.date.eq(pd.Timestamp(first.cutoff_date)), "close"].iloc[0]
        expiry = data.loc[data.date.eq(pd.Timestamp(first.expiry_date)), "close"].iloc[0]
        self.assertAlmostEqual(first.target_return, expiry / cutoff - 1, places=12)
        self.assertEqual(int(first.target_up), int(expiry > cutoff))
        self.assertEqual(first.cutoff_date, data.loc[data.date.eq(pd.Timestamp(first.cutoff_date)), "date"].iloc[0].date().isoformat())

    def test_weekly_feature_rows_do_not_include_target_close(self):
        dates = pd.bdate_range("2023-01-02", "2026-10-23")
        close = 18000 * np.cumprod(1 + np.full(len(dates), 0.0001))
        data = pd.DataFrame({"date": dates, "open": close, "high": close * 1.002, "low": close * .998, "close": close})
        frame, meta = weekly.build_weekly_examples(data)
        self.assertNotIn("target_return", meta["feature_columns"])
        self.assertNotIn("expiry_close", meta["feature_columns"])
        self.assertNotIn("target_up", meta["feature_columns"])


if __name__ == "__main__":
    unittest.main()
