import onnxruntime as ort
import numpy as np
from typing import Dict

class ONNXInterpreter:
    """Lightweight ONNX model inference engine for embedded systems."""

    def __init__(self, model_path: str):
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """Run inference on input data."""
        return self.session.run([self.output_name], {self.input_name: input_data})[0]

    def get_model_info(self) -> Dict:
        """Return input/output shapes and types."""
        return {
            "input_shape": self.session.get_inputs()[0].shape,
            "output_shape": self.session.get_outputs()[0].shape,
        }
