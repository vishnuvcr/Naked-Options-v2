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




parity = load_module("zigzag_parity", "audit_5m_source_parity.py")
migration = load_module("zigzag_legacy_migration", "migrate_legacy_5m_cache.py")


class SourceParityTests(unittest.TestCase):
    def _write_source(self, path, rows):
        fields = ["timestamp_ist", "date_ist", "open", "high", "low", "close", "volume"]
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_source_parity_reports_close_differences_without_merging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dhan = root / "dhan.csv"
            public = root / "public.csv"
            self._write_source(dhan, [
                {"timestamp_ist": "2024-01-02T09:15:00+05:30", "date_ist": "2024-01-02",
                 "open": 100, "high": 102, "low": 99, "close": 101, "volume": 0},
                {"timestamp_ist": "2024-01-02T09:20:00+05:30", "date_ist": "2024-01-02",
                 "open": 101, "high": 103, "low": 100, "close": 102, "volume": 0},
            ])
            self._write_source(public, [
                {"timestamp_ist": "2024-01-02T09:15:00+05:30", "date_ist": "2024-01-02",
                 "open": 100, "high": 102, "low": 99, "close": 101.02, "volume": 0},
                {"timestamp_ist": "2024-01-02T09:20:00+05:30", "date_ist": "2024-01-02",
                 "open": 101, "high": 103, "low": 100, "close": 104, "volume": 0},
            ])
            report = parity.audit(dhan, public)
            self.assertEqual(report["overlap"]["rows"], 2)
            self.assertEqual(report["absolute_differences"]["close"]["within_0_05"], 1)
            self.assertEqual(report["absolute_differences"]["close"]["over_1"], 1)
            self.assertTrue(report["does_not_authorize_prediction_scoring"])
            self.assertEqual(report["status"], "OVERLAP_AVAILABLE_WITH_UNRESOLVED_DISCREPANCIES")

    def test_source_parity_missing_input_is_a_nonfatal_diagnostic(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = parity.audit(Path(tmp) / "absent.csv", Path(tmp) / "also_absent.csv")
            self.assertEqual(report["status"], "SKIPPED_SOURCE_MISSING")
            self.assertEqual(report["overlap_rows"], 0)

    def test_5m_source_selection_prefers_public_then_dhan_then_legacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(prep, "ROOT", root):
                legacy = root / "nifty50_5m.csv"
                yahoo = root / "nifty50_5m_yahoo_fallback.csv"
                dhan = root / "nifty50_5m_dhan.csv"
                public = root / "nifty50_5m_public_archive.csv"
                legacy.touch()
                self.assertEqual(prep.resolve_5m_source(), legacy)
                yahoo.touch()
                self.assertEqual(prep.resolve_5m_source(), yahoo)
                dhan.touch()
                self.assertEqual(prep.resolve_5m_source(), dhan)
                public.touch()
                self.assertEqual(prep.resolve_5m_source(), public)



    def test_dhan_internal_1m_to_5m_audit_flags_grid_and_ohlc_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            one = root / "one.csv"
            five = root / "five.csv"
            self._write_source(one, [
                {"timestamp_ist": f"2024-01-02T09:{15+i:02d}:00+05:30", "date_ist": "2024-01-02",
                 "open": 100+i, "high": 102+i, "low": 99+i, "close": 101+i, "volume": 0}
                for i in range(11)
            ])
            self._write_source(five, [
                {"timestamp_ist": "2024-01-02T09:15:00+05:30", "date_ist": "2024-01-02",
                 "open": 100, "high": 106, "low": 99, "close": 105, "volume": 0},
                {"timestamp_ist": "2024-01-02T09:20:00+05:30", "date_ist": "2024-01-02",
                 "open": 105, "high": 111, "low": 104, "close": 110, "volume": 0},
                {"timestamp_ist": "2024-01-02T09:16:00+05:30", "date_ist": "2024-01-02",
                 "open": 101, "high": 108, "low": 100, "close": 107, "volume": 0},
            ])
            report = parity.audit_dhan_internal_consistency(one, five)
            self.assertEqual(report["complete_groups"], 2)
            self.assertEqual(report["mismatch_groups"], 1)
            self.assertEqual(report["misaligned_five_minute_timestamps"], 1)


class LegacyCacheMigrationTests(unittest.TestCase):
    def test_legacy_mixed_cache_is_quarantined_with_matching_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy = root / "nifty50_5m.csv"
            raw = b"timestamp_ist,open,high,low,close,volume\nlegacy\n"
            legacy.write_bytes(raw)
            report = migration.migrate(root)
            quarantined = Path(report["quarantined_path"])
            self.assertEqual(report["status"], "QUARANTINED")
            self.assertFalse(legacy.exists())
            self.assertEqual(quarantined.read_bytes(), raw)
            self.assertEqual(report["legacy_sha256"], report["quarantined_sha256"])

    def test_migration_without_legacy_file_is_a_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = migration.migrate(Path(tmp))
            self.assertEqual(report["status"], "NO_LEGACY_FILE")

if __name__ == "__main__":
    unittest.main()
