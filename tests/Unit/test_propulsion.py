# tests/unit/test_propulsion.py
import pytest
from src.propulsion import Propulsion

def test_propulsion_thrust():
    propulsion = Propulsion("turbofan", 2, 140000, 0.00005, 50000, 20000)
    thrust = propulsion.thrust(0.8)
    assert thrust == 2 * 140000 * 0.8

def test_propulsion_fuel_flow():
    propulsion = Propulsion("turbofan", 2, 140000, 0.00005, 50000, 20000)
    thrust = propulsion.thrust(0.8)
    fuel_flow = propulsion.fuel_flow_rate(thrust)
    assert fuel_flow == 2 * 140000 * 0.8 * 0.00005 / 3600
