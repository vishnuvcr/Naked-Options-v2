import csv
import importlib.util
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1] / "research" / "zigzag-expiry-direction"

def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, BASE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

acq = load_module("zigzag_acquire", "acquire_dhan_timeframes.py")
prep = load_module("zigzag_prepare", "prepare_timeframes.py")

class DhanParserTests(unittest.TestCase):
    def test_epoch_timestamp_converts_to_ist(self):
        stamp = acq.parse_timestamp(0)
        self.assertEqual(stamp.isoformat(), "1970-01-01T05:30:00+05:30")

    def test_ohlc_arrays_become_timestamped_rows(self):
        data = {"timestamp":[0,60], "open":[10,11], "high":[12,13],
                "low":[9,10], "close":[11,12], "volume":[100,200]}
        rows = acq.get_rows(data)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["close"], 11.0)
        self.assertEqual(rows[0]["date_ist"], "1970-01-01")

    def test_mismatched_response_arrays_rejected(self):
        data = {"timestamp":[0,60], "open":[10], "high":[12,13],
                "low":[9,10], "close":[11,12]}
        with self.assertRaises(RuntimeError):
            acq.get_rows(data)

class DataValidationTests(unittest.TestCase):
    def test_invalid_ohlc_is_flagged_and_can_be_quarantined(self):
        rows=[{"timestamp_ist":"2024-01-01T09:15:00+05:30",
               "dt":datetime.fromisoformat("2024-01-01T09:15:00+05:30"),
               "date_ist":"2024-01-01","open":10.0,"high":9.0,
               "low":8.0,"close":8.5,"volume":0}]
        self.assertFalse(prep.valid_ohlc(rows[0]))
        self.assertEqual(prep.structural_issues(rows), [])

    def test_valid_six_bar_block_resamples_to_30m(self):
        rows=[]
        for i in range(6):
            stamp=datetime.fromisoformat("2024-01-02T09:15:00+05:30").replace(minute=15+i*5)
            rows.append({"timestamp_ist":stamp.isoformat(),"date_ist":"2024-01-02",
                         "dt":stamp,"open":100+i,"high":102+i,"low":99+i,
                         "close":101+i,"volume":10})
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"data"/"cache"/"zigzag_expiry_direction"
            with patch.object(prep,"ROOT",root):
                derived,dropped,info=prep.derive_30m(rows)
            self.assertEqual(len(derived),1)
            self.assertEqual(derived[0]["open"],100)
            self.assertEqual(derived[0]["close"],106)
            self.assertEqual(derived[0]["high"],107)
            self.assertEqual(derived[0]["low"],99)
            self.assertEqual(derived[0]["volume"],60)
            self.assertEqual(dropped,[])
            self.assertTrue(Path(info).exists())

    def test_incomplete_30m_bucket_is_excluded(self):
        rows=[]
        for i in range(5):
            stamp=datetime.fromisoformat("2024-01-02T09:15:00+05:30").replace(minute=15+i*5)
            rows.append({"timestamp_ist":stamp.isoformat(),"date_ist":"2024-01-02",
                         "dt":stamp,"open":100,"high":102,"low":99,"close":101,"volume":1})
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(prep,"ROOT",Path(tmp)):
                derived,dropped,_=prep.derive_30m(rows)
        self.assertEqual(derived,[])
        self.assertEqual(len(dropped),1)

if __name__ == "__main__":
    unittest.main()
