# tests/unit/test_onnx.py
import numpy as np
import pytest
from src.onnx_interpreter import ONNXInterpreter

def test_onnx_inference():
    interpreter = ONNXInterpreter("tests/fixtures/flight_model.onnx")
    dummy_input = np.random.rand(1, 5).astype(np.float32)
    output = interpreter.predict(dummy_input)
    assert output.shape == (1, 3)
