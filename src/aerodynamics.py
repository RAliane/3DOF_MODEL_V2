import torch
import math
from vector import Vector
from environment import Environment

class Aerodynamics:
    """Models aerodynamic forces (lift, drag, thrust) in NED coordinates."""

    def __init__(
        self,
        wing_area: float,
        aspect_ratio: float,
        oswald_efficiency: float,
        Cd0: float,  # Zero-lift drag coefficient
        Cl: float,   # Lift coefficient
        propulsion,
    ):
        self.wing_area = wing_area
        self.aspect_ratio = aspect_ratio
        self.oswald_efficiency = oswald_efficiency
        self.Cd0 = Cd0
        self.Cl = Cl
        self.propulsion = propulsion

    def dynamic_pressure(self, velocity: torch.Tensor, position: torch.Tensor) -> float:
        """Calculates dynamic pressure (q) at the given position and velocity."""
        h = -position[2]  # Altitude from NED 'down'
        rho = Environment.density(h)
        v_mag = Vector.magnitude(velocity)
        return 0.5 * rho * v_mag**2

    def lift_force(self, velocity: torch.Tensor, position: torch.Tensor) -> torch.Tensor:
        """Calculates lift force vector (NED)."""
        q = self.dynamic_pressure(velocity, position)
        lift_magnitude = q * self.Cl * self.wing_area

        # Simplified: Lift is perpendicular to velocity (in the N-E plane)
        vel_unit = velocity / Vector.magnitude(velocity)
        lift_direction = torch.tensor([-vel_unit[1], vel_unit[0], 0.0], dtype=torch.float32)
        lift_direction = lift_direction / Vector.magnitude(lift_direction)
        return lift_magnitude * lift_direction

    def parasitic_drag_force(self, velocity: torch.Tensor, position: torch.Tensor) -> torch.Tensor:
        """Calculates parasitic drag force vector (NED)."""
        q = self.dynamic_pressure(velocity, position)
        drag_magnitude = q * self.Cd0 * self.wing_area
        drag_direction = -velocity / Vector.magnitude(velocity)  # Opposes velocity
        return drag_magnitude * drag_direction

    def induced_drag_force(self, velocity: torch.Tensor, position: torch.Tensor) -> torch.Tensor:
        """Calculates induced drag force vector (NED)."""
        q = self.dynamic_pressure(velocity, position)
        lift_magnitude = q * self.Cl * self.wing_area
        induced_drag_magnitude = (lift_magnitude**2) / (q * self.wing_area * math.pi * self.oswald_efficiency * self.aspect_ratio)
        drag_direction = -velocity / Vector.magnitude(velocity)  # Opposes velocity
        return induced_drag_magnitude * drag_direction

    def total_drag_force(self, velocity: torch.Tensor, position: torch.Tensor) -> torch.Tensor:
        """Calculates total drag force (parasitic + induced)."""
        return self.parasitic_drag_force(velocity, position) + self.induced_drag_force(velocity, position)

    def thrust_force(self, thrust_direction: torch.Tensor, throttle: float = 1.0) -> torch.Tensor:
        """Returns thrust force vector (NED) based on throttle setting."""
        thrust_magnitude = self.propulsion.thrust(throttle)
        return thrust_magnitude * thrust_direction / Vector.magnitude(thrust_direction)
