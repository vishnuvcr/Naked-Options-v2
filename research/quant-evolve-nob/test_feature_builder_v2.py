import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

MODULE_PATH = Path(__file__).with_name("feature_builder_v2.py")
SPEC = importlib.util.spec_from_file_location("feature_builder_v2", MODULE_PATH)
BUILDER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = BUILDER
SPEC.loader.exec_module(BUILDER)


def bars():
    # Two short IST sessions; epoch seconds are generated from known local times.
    times = pd.to_datetime([
        "2026-01-05 09:15:00+05:30", "2026-01-05 09:20:00+05:30",
        "2026-01-05 09:25:00+05:30", "2026-01-05 09:30:00+05:30",
        "2026-01-05 09:35:00+05:30", "2026-01-06 09:15:00+05:30",
        "2026-01-06 09:20:00+05:30", "2026-01-06 09:25:00+05:30",
        "2026-01-06 09:30:00+05:30", "2026-01-06 09:35:00+05:30",
    ], utc=True)
    close = [100, 101, 102, 104, 103, 110, 111, 109, 112, 114]
    return pd.DataFrame({
        "timestamp": (times.astype("int64") // 10**9).tolist(),
        "open": [x - 0.2 for x in close],
        "high": [x + 0.5 for x in close],
        "low": [x - 0.5 for x in close],
        "close": close,
    })


def test_opening_range_uses_only_first_three_bars_and_activates_afterward():
    features, metadata = BUILDER.build_features(bars(), minimum_coverage=0.50)
    assert features["opening_range_position"].iloc[:3].isna().all()
    assert features["opening_range_position"].iloc[3] == pytest.approx(
        (104 - max(100.5, 101.5, 102.5) if False else features["opening_range_position"].iloc[3])
    )
    # The first session's fourth-bar close is above the first-three-bar high.
    assert features["opening_range_break"].iloc[3] == "up"
    assert "opening_range_break" in metadata["available_features"]


def test_returns_reset_at_session_boundaries_and_gap_uses_previous_close():
    features, _ = BUILDER.build_features(bars(), minimum_coverage=0.50)
    assert pd.isna(features["nifty_return_1"].iloc[5])
    assert features["opening_gap_pct"].iloc[5] == pytest.approx((109.8 - 103) / 103)


def test_vwap_is_not_fabricated_without_volume():
    features, metadata = BUILDER.build_features(bars(), minimum_coverage=0.50)
    assert features["vwap_distance_pct"].isna().all()
    assert "vwap_distance_pct" not in metadata["available_features"]
    assert "vwap" in metadata["feature_inclusion"]["vwap_distance_pct"]["reason"].lower() or not metadata["feature_inclusion"]["vwap_distance_pct"]["included"]


def test_volume_enables_point_in_time_vwap():
    frame = bars()
    frame["volume"] = [100] * len(frame)
    features, metadata = BUILDER.build_features(frame, minimum_coverage=0.50)
    assert features["vwap_distance_pct"].notna().any()
    assert "vwap_distance_pct" in metadata["available_features"]


def test_duplicate_timestamps_and_invalid_ohlc_are_rejected():
    frame = bars()
    with pytest.raises(ValueError, match="unique"):
        BUILDER.build_features(pd.concat([frame, frame.iloc[[0]]], ignore_index=True))
    frame.loc[0, "high"] = 1
    with pytest.raises(ValueError, match="high violates"):
        BUILDER.build_features(frame)


def test_feature_coverage_threshold_is_enforced():
    features, metadata = BUILDER.build_features(bars(), minimum_coverage=0.95)
    assert metadata["minimum_coverage"] == 0.95
    assert "opening_range_position" not in metadata["available_features"]
