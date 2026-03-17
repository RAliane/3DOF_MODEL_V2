# tests/integration/test_lqri_pid.py
import pytest
from src.lqri_pid import LQRIPID, ControlState

def test_lqri_pid_controller():
    controller = LQRIPID("tests/fixtures/flight_model.onnx", dt=0.01)
    state = ControlState(
        altitude=500.0,
        airspeed=120.0,
        pitch=0.05,
        roll=0.0,
        yaw=0.0,
        pitch_rate=0.0,
        roll_rate=0.0,
        yaw_rate=0.0,
    )
    control = controller.compute_control(state)
    assert 0.0 <= control.throttle <= 1.0
    assert -1.0 <= control.elevator_pitch <= 1.0
