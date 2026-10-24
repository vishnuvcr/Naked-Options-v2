import pandas as pd
import pytest
from evaluate_predictions import REQUIRED

def test_required_columns_include_signal_availability():
    assert "signal_available_at" in REQUIRED
    assert "cutoff_at" in REQUIRED
    assert "target_at" in REQUIRED
