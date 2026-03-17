# tests/unit/test_main.py
import pytest
from unittest.mock import patch, MagicMock
from main import main

@patch("main.FlightDynamicsController")
def test_main(mock_fdc):
    mock_instance = MagicMock()
    mock_fdc.return_value = mock_instance

    main()

    mock_fdc.assert_called_once_with(
        onnx_model_path="src/flight_model.onnx",
        directus_url="http://localhost:8055",
        directus_email="admin@example.com",
        directus_password="admin",
        dt=0.01
    )
    mock_instance.set_target.assert_called_once_with(altitude=1000.0, airspeed=150.0)
    assert mock_instance.update.call_count == 1000
    mock_instance.export_telemetry.assert_called_once_with("data/telemetry.json")
    mock_instance.close.assert_called_once()
