# src/flight_dynamics.py
import json
from typing import Dict
from lqri_pid import LQRIPID, ControlState
from directus_client import DirectusClient

class FlightDynamicsController:
    """Integrates LQRI-PID controller with 6DoF physics engine and Directus logging."""

    def __init__(self, onnx_model_path: str, directus_url: str, directus_email: str, directus_password: str, dt: float = 0.01):
        self.controller = LQRIPID(onnx_model_path, dt)
        self.dt = dt
        self.state = ControlState(
            altitude=0.0,
            airspeed=0.0,
            pitch=0.0,
            roll=0.0,
            yaw=0.0,
            pitch_rate=0.0,
            roll_rate=0.0,
            yaw_rate=0.0,
        )
        self.control_history = []
        self.directus = DirectusClient(directus_url, directus_email, directus_password)

    def update(self, aircraft_state: Dict) -> Dict:
        """Update control based on current aircraft state and log to Directus."""
        self.state.altitude = aircraft_state.get("altitude", 0.0)
        self.state.airspeed = aircraft_state.get("airspeed", 0.0)
        self.state.pitch = aircraft_state.get("pitch", 0.0)
        self.state.roll = aircraft_state.get("roll", 0.0)
        self.state.yaw = aircraft_state.get("yaw", 0.0)
        self.state.pitch_rate = aircraft_state.get("pitch_rate", 0.0)
        self.state.roll_rate = aircraft_state.get("roll_rate", 0.0)
        self.state.yaw_rate = aircraft_state.get("yaw_rate", 0.0)

        control = self.controller.compute_control(self.state)

        # Log to Directus
        log_entry = {
            "timestamp": len(self.control_history) * self.dt,
            "altitude": self.state.altitude,
            "airspeed": self.state.airspeed,
            "throttle": control.throttle,
            "elevator": control.elevator_pitch,
            "aileron": control.aileron_roll,
            "rudder": control.rudder_yaw,
        }
        self.directus.log_data("flight_logs", log_entry)

        self.control_history.append(log_entry)

        return {
            "throttle": control.throttle,
            "elevator": control.elevator_pitch,
            "aileron": control.aileron_roll,
            "rudder": control.rudder_yaw,
        }

    def set_target(self, altitude: float, airspeed: float):
        """Set autopilot target."""
        self.controller.set_setpoints(altitude, airspeed)

    def export_telemetry(self, filename: str = "control_telemetry.json"):
        """Export control history to JSON."""
        with open(filename, "w") as f:
            json.dump(self.control_history, f, indent=2)

    def close(self):
        """Close the Directus client."""
        self.directus.close()
