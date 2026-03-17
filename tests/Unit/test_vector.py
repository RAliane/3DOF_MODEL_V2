# tests/unit/test_vector.py
import torch
import pytest
from src.vector import Vector

def test_vector_magnitude():
    vec = torch.tensor([3.0, 4.0, 0.0])
    assert torch.allclose(Vector.magnitude(vec), torch.tensor(5.0))

def test_vector_position():
    pos = Vector.position_vector(1.0, 2.0, 3.0)
    assert torch.allclose(pos, torch.tensor([1.0, 2.0, 3.0]))

def test_vector_velocity():
    vel = Vector.velocity_vector(4.0, 5.0, 6.0)
    assert torch.allclose(vel, torch.tensor([4.0, 5.0, 6.0]))
