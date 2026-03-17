# scripts/generate_onnx_model.py
import torch
import torch.nn as nn
import numpy as np

class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(5, 3)

    def forward(self, x):
        return self.fc(x)

def generate_onnx_model(output_path="src/flight_model.onnx"):
    model = DummyModel()
    dummy_input = torch.randn(1, 5)
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
    )
    print(f"Dummy ONNX model generated at {output_path}")

if __name__ == "__main__":
    generate_onnx_model()
