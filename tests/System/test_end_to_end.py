# tests/system/test_end_to_end.py
import json
import os
import pytest
from main import main
from unittest.mock import patch

@patch("time.sleep")
def test_end_to_end(mock_sleep):
    main()

    # Check if telemetry was exported
    assert os.path.exists("data/telemetry.json")

    # Validate telemetry data
    with open("data/telemetry.json", "r") as f:
        telemetry = json.load(f)
        assert len(telemetry) == 1000
        assert telemetry[0]["altitude"] == 500.0
        assert telemetry[-1]["altitude"] == 999.5
