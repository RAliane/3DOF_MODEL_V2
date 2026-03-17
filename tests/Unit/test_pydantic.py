# tests/unit/test_pydantic.py
import pytest
from src.schemas import AircraftState, ControlCommand

def test_aircraft_state():
    state = AircraftState(
        altitude=1000.0,
        airspeed=150.0,
        pitch=0.1,
        roll=0.0,
        yaw=0.0,
        pitch_rate=0.01,
        roll_rate=0.0,
        yaw_rate=0.0,
    )
    assert state.altitude == 1000.0
    assert state.airspeed == 150.0

def test_control_command():
    command = ControlCommand(throttle=0.5, elevator=0.1, aileron=-0.2, rudder=0.0)
    assert command.throttle == 0.5
    assert command.elevator == 0.1
