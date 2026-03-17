import torch
import numpy as np
from dataclasses import dataclass
from collections import deque
from typing import Dict, Optional
from onnx_interpreter import ONNXInterpreter

@dataclass
class ControlState:
    altitude: float
    airspeed: float
    pitch: float
    roll: float
    yaw: float
    pitch_rate: float
    roll_rate: float
    yaw_rate: float
    altitude_error_integral: float = 0.0
    airspeed_error_integral: float = 0.0

@dataclass
class ControlOutput:
    throttle: float
    elevator_pitch: float
    aileron_roll: float
    rudder_yaw: float

class LQRIPID:
    def __init__(self, onnx_model_path: str, dt: float = 0.01):
        self.dt = dt
        self.nn_model = ONNXInterpreter(onnx_model_path)

        # Reference states (setpoints)
        self.altitude_setpoint = 1000.0
        self.airspeed_setpoint = 100.0
        self.pitch_setpoint = 0.0

        # PID gains
        self.pid_gains = {
            "altitude": {"Kp": 0.01, "Ki": 0.001, "Kd": 0.002},
            "airspeed": {"Kp": 0.05, "Ki": 0.002, "Kd": 0.01},
            "pitch": {"Kp": 0.5, "Ki": 0.05, "Kd": 0.1},
            "roll": {"Kp": 0.4, "Ki": 0.02, "Kd": 0.08},
            "yaw": {"Kp": 0.3, "Ki": 0.01, "Kd": 0.05},
        }

        # LQR state-space matrices (simplified)
        self.lqr_gain = torch.tensor([[0.1, 0.05, 0.02], [0.2, 0.1, 0.05], [0.15, 0.08, 0.03]])

        # Error history for derivative term
        self.error_history = {
            "altitude": deque(maxlen=3),
            "airspeed": deque(maxlen=3),
            "pitch": deque(maxlen=3),
            "roll": deque(maxlen=3),
            "yaw": deque(maxlen=3),
        }

        # Output limits
        self.output_limits = {
            "throttle": (0.0, 1.0),
            "elevator": (-1.0, 1.0),
            "aileron": (-1.0, 1.0),
            "rudder": (-1.0, 1.0),
        }

    def set_setpoints(self, altitude: float, airspeed: float, pitch: float = 0.0):
        """Set control objectives."""
        self.altitude_setpoint = altitude
        self.airspeed_setpoint = airspeed
        self.pitch_setpoint = pitch

    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max."""
        return max(min_val, min(max_val, value))

    def _compute_pid_term(self, error: float, error_history: deque, gains: Dict) -> float:
        """Compute PID term: Kp*e + Ki*integral + Kd*derivative."""
        p_term = gains["Kp"] * error
        i_term = gains["Ki"] * sum(error_history) * self.dt
        d_term = gains["Kd"] * (error - error_history[-1]) / self.dt if len(error_history) >= 2 else 0.0
        return p_term + i_term + d_term

    def _get_nn_feedforward(self, state: ControlState) -> np.ndarray:
        """Get feedforward correction from neural network."""
        nn_input = np.array(
            [
                [
                    state.altitude / 10000.0,
                    state.airspeed / 300.0,
                    state.pitch,
                    state.roll,
                    state.yaw,
                ]
            ],
            dtype=np.float32,
        )
        nn_output = self.nn_model.predict(nn_input)
        return nn_output[0]

    def compute_control(self, state: ControlState) -> ControlOutput:
        """Main control law: Combine NN feedforward with PID feedback."""
        altitude_error = self.altitude_setpoint - state.altitude
        airspeed_error = self.airspeed_setpoint - state.airspeed
        pitch_error = self.pitch_setpoint - state.pitch
        roll_error = 0.0 - state.roll
        yaw_error = 0.0 - state.yaw

        # Store errors for derivative term
        self.error_history["altitude"].append(altitude_error)
        self.error_history["airspeed"].append(airspeed_error)
        self.error_history["pitch"].append(pitch_error)
        self.error_history["roll"].append(roll_error)
        self.error_history["yaw"].append(yaw_error)

        # Get NN feedforward predictions
        try:
            nn_ff = self._get_nn_feedforward(state)
        except Exception as e:
            print(f"NN inference failed: {e}")
            nn_ff = np.array([0.0, 0.0, 0.0])

        # Compute PID feedback terms
        alt_pid = self._compute_pid_term(altitude_error, self.error_history["altitude"], self.pid_gains["altitude"])
        airspeed_pid = self._compute_pid_term(airspeed_error, self.error_history["airspeed"], self.pid_gains["airspeed"])
        pitch_pid = self._compute_pid_term(pitch_error, self.error_history["pitch"], self.pid_gains["pitch"])
        roll_pid = self._compute_pid_term(roll_error, self.error_history["roll"], self.pid_gains["roll"])
        yaw_pid = self._compute_pid_term(yaw_error, self.error_history["yaw"], self.pid_gains["yaw"])

        # Combine feedforward (NN) + feedback (PID)
        throttle = nn_ff[0] * 0.3 + (alt_pid + airspeed_pid) * 0.7
        elevator = nn_ff[1] * 0.3 + pitch_pid * 0.7
        aileron = nn_ff[2] * 0.3 + roll_pid * 0.7
        rudder = yaw_pid

        # Apply output limits
        throttle = self._clamp(throttle, *self.output_limits["throttle"])
        elevator = self._clamp(elevator, *self.output_limits["elevator"])
        aileron = self._clamp(aileron, *self.output_limits["aileron"])
        rudder = self._clamp(rudder, *self.output_limits["rudder"])

        return ControlOutput(throttle=throttle, elevator_pitch=elevator, aileron_roll=aileron, rudder_yaw=rudder)

    def update_pid_gains(self, control_type: str, Kp: float, Ki: float, Kd: float):
        """Tune PID gains online."""
        if control_type in self.pid_gains:
            self.pid_gains[control_type] = {"Kp": Kp, "Ki": Ki, "Kd": Kd}
            print(f"Updated {control_type} gains: Kp={Kp}, Ki={Ki}, Kd={Kd}")
