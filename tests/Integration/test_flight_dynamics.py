# tests/integration/test_flight_dynamics.py
import pytest
from unittest.mock import MagicMock, patch
from src.flight_dynamics import FlightDynamicsController

@patch("src.flight_dynamics.DirectusClient")
def test_flight_dynamics_controller(mock_directus):
    mock_instance = MagicMock()
    mock_directus.return_value = mock_instance

    fdc = FlightDynamicsController(
        onnx_model_path="tests/fixtures/flight_model.onnx",
        directus_url="http://localhost:8055",
        directus_email="admin@example.com",
        directus_password="admin",
        dt=0.01
    )

    aircraft_state = {
        "altitude": 500.0,
        "airspeed": 120.0,
        "pitch": 0.05,
        "roll": 0.0,
        "yaw": 0.0,
        "pitch_rate": 0.0,
        "roll_rate": 0.0,
        "yaw_rate": 0.0,
    }
    fdc.update(aircraft_state)

    mock_instance.log_data.assert_called_once()
    fdc.close()
