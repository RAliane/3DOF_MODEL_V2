# main.py
from src.flight_dynamics import FlightDynamicsController
import time

def main():
    # Initialize the flight dynamics controller
    fdc = FlightDynamicsController(
        onnx_model_path="src/flight_model.onnx",
        directus_url="http://localhost:8055",
        directus_email="admin@example.com",
        directus_password="admin",
        dt=0.01
    )

    # Set target altitude and airspeed
    fdc.set_target(altitude=1000.0, airspeed=150.0)

    # Simulate 1000 timesteps
    for i in range(1000):
        # Simulate aircraft state (e.g., from sensors or simulation)
        aircraft_state = {
            "altitude": 500.0 + i * 0.5,  # Ascending
            "airspeed": 120.0 + i * 0.05,
            "pitch": 0.05,
            "roll": 0.0,
            "yaw": 0.0,
            "pitch_rate": 0.01,
            "roll_rate": 0.0,
            "yaw_rate": 0.0,
        }

        # Update control and log to Directus
        control = fdc.update(aircraft_state)
        print(f"Step {i}: Throttle={control['throttle']:.3f}, Elevator={control['elevator']:.3f}")

        # Small delay to simulate real-time
        time.sleep(0.01)

    # Export telemetry to JSON
    fdc.export_telemetry("data/telemetry.json")
    fdc.close()

if __name__ == "__main__":
    main()
