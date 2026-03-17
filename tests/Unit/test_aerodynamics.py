# tests/unit/test_aerodynamics.py
import torch
import pytest
from src.aerodynamics import Aerodynamics
from src.environment import Environment
from src.vector import Vector
from src.propulsion import Propulsion

@pytest.fixture
def aerodynamics():
    propulsion = Propulsion("turbofan", 2, 140000, 0.00005, 50000, 20000)
    return Aerodynamics(20, 8, 0.8, 0.02, 0.8, propulsion)

def test_aerodynamics_lift(aerodynamics):
    env = Environment()
    pos = Vector.position_vector(0, 0, -1000)
    vel = Vector.velocity_vector(100, 0, 0)
    lift = aerodynamics.lift_force(vel, pos)
    assert lift.shape == (3,)

def test_aerodynamics_drag(aerodynamics):
    env = Environment()
    pos = Vector.position_vector(0, 0, -1000)
    vel = Vector.velocity_vector(100, 0, 0)
    drag = aerodynamics.total_drag_force(vel, pos)
    assert drag.shape == (3,)
