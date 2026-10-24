import unittest
from copy import deepcopy

from forecast_contract import validate_forecast


BASE = {
    "schema_version": "1.0",
    "instrument": "NIFTY 50",
    "forecast_id": "sample-001",
    "cutoff_time": "2026-01-06T10:00:00+05:30",
    "target_start": "2026-01-06T10:00:00+05:30",
    "target_end": "2026-01-13T15:30:00+05:30",
    "prediction": "UP",
    "model_id": "TradingAgents",
    "model_revision": "e8f5503e9b86d5c2710b0c76b1f686703968c9df",
    "prompt_sha256": "a" * 64,
    "input_manifest_sha256": "b" * 64,
    "input_asof_time": "2026-01-06T09:55:00+05:30",
    "created_at": "2026-01-06T10:00:01+05:30",
    "status": "ok",
}


class ForecastContractTests(unittest.TestCase):
    def test_valid_forecast(self):
        self.assertEqual(validate_forecast(BASE), BASE)

    def test_all_classes(self):
        for prediction in ("UP", "DOWN", "ABSTAIN"):
            item = deepcopy(BASE)
            item["prediction"] = prediction
            self.assertEqual(validate_forecast(item)["prediction"], prediction)

    def test_rejects_future_input(self):
        item = deepcopy(BASE)
        item["input_asof_time"] = "2026-01-06T10:00:01+05:30"
        with self.assertRaisesRegex(ValueError, "later than cutoff"):
            validate_forecast(item)

    def test_rejects_naive_timestamps(self):
        item = deepcopy(BASE)
        item["cutoff_time"] = "2026-01-06T10:00:00"
        with self.assertRaisesRegex(ValueError, "timezone offset"):
            validate_forecast(item)

    def test_rejects_reversed_target(self):
        item = deepcopy(BASE)
        item["target_start"] = "2026-01-14T10:00:00+05:30"
        with self.assertRaisesRegex(ValueError, "target_start"):
            validate_forecast(item)

    def test_rejects_unexpected_fields(self):
        item = deepcopy(BASE)
        item["confidence"] = 0.9
        with self.assertRaisesRegex(ValueError, "unexpected fields"):
            validate_forecast(item)

    def test_rejects_invalid_hash(self):
        item = deepcopy(BASE)
        item["prompt_sha256"] = "not-a-hash"
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            validate_forecast(item)

    def test_rejects_non_abstain_unknown_class(self):
        item = deepcopy(BASE)
        item["prediction"] = "BUY_CALL"
        with self.assertRaisesRegex(ValueError, "UP, DOWN, or ABSTAIN"):
            validate_forecast(item)


if __name__ == "__main__":
    unittest.main()
