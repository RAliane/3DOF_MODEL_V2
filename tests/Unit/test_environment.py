# tests/unit/test_environment.py
import pytest
from src.environment import Environment

def test_environment_density():
    # Test sea level density
    assert Environment.density(0.0) == pytest.approx(1.225, rel=1e-3)
    # Test tropopause density
    assert Environment.density(11000.0) == pytest.approx(0.3648, rel=1e-3)

def test_environment_temperature():
    # Test sea level temperature
    assert Environment._temperature(0.0) == 288.15
    # Test tropopause temperature
    assert Environment._temperature(11000.0) == 216.65
