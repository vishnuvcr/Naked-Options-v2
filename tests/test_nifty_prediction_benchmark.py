import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research" / "nifty-prediction" / "evaluate_daily_models.py"
spec = importlib.util.spec_from_file_location("nifty_benchmark", SCRIPT)
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


class NiftyBenchmarkTests(unittest.TestCase):
    def synthetic(self, n=1400):
        rng = np.random.default_rng(123)
        returns = rng.normal(0.0003, 0.01, n)
        close = 18000 * np.cumprod(1 + returns)
        open_ = close * (1 + rng.normal(0, 0.002, n))
        high = np.maximum(open_, close) * 1.003
        low = np.minimum(open_, close) * 0.997
        return pd.DataFrame({
            "date": pd.date_range("2018-01-01", periods=n, freq="B").date,
            "open": open_, "high": high, "low": low, "close": close,
        })

    def test_features_and_targets_are_temporally_aligned(self):
        data = self.synthetic()
        frame, features = benchmark.build_frame(data)
        i = 300
        expected = data.close.iloc[i + 1] / data.close.iloc[i] - 1
        self.assertAlmostEqual(frame.target_return.iloc[i], expected, places=12)
        self.assertAlmostEqual(frame.ret_1.iloc[i], data.close.iloc[i] / data.close.iloc[i-1] - 1, places=12)
        self.assertIn("vol_20", features)
        self.assertTrue(frame.target_return.iloc[-1] != frame.target_return.iloc[-1])

    def test_data_validator_rejects_bad_ohlc(self):
        data = self.synthetic(1200)
        data.loc[5, "high"] = 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            data.rename(columns={"date": "Date", "open": "Open", "high": "High",
                                 "low": "Low", "close": "Close"}).to_csv(path, index=False)
            with self.assertRaises(ValueError):
                benchmark.load_data(path)

    def test_bootstrap_interval_is_bounded(self):
        y = np.array([0, 1] * 60)
        pred = np.array([0, 1] * 60)
        ci = benchmark.block_bootstrap_ci(y, pred, reps=100)
        self.assertLessEqual(ci["lower"], ci["upper"])
        self.assertGreaterEqual(ci["lower"], 0)
        self.assertLessEqual(ci["upper"], 1)


if __name__ == "__main__":
    unittest.main()
