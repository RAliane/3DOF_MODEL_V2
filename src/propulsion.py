class Propulsion:
    """Models engine thrust, fuel consumption, and mass updates."""

    def __init__(
        self,
        engine_type: str,  # "turbofan", "turbojet", "piston", etc.
        num_engines: int,
        max_thrust_per_engine: float,  # Newtons
        specific_fuel_consumption: float,  # kg/N/hr (or kg/kN/hr)
        empty_weight: float,  # kg
        fuel_weight: float,  # kg
    ):
        self.engine_type = engine_type
        self.num_engines = num_engines
        self.max_thrust_per_engine = max_thrust_per_engine
        self.specific_fuel_consumption = specific_fuel_consumption
        self.empty_weight = empty_weight
        self.fuel_weight = fuel_weight
        self.total_mass = empty_weight + fuel_weight

    def thrust(self, throttle: float = 1.0) -> float:
        """Calculates total thrust (N) based on throttle setting (0-1)."""
        thrust_per_engine = self.max_thrust_per_engine * throttle
        return thrust_per_engine * self.num_engines

    def fuel_flow_rate(self, thrust: float) -> float:
        """Calculates fuel flow rate (kg/s) based on thrust and SFC."""
        sfc_per_second = self.specific_fuel_consumption / 3600
        return thrust * sfc_per_second

    def update_mass(self, dt: float, thrust: float):
        """Updates total mass (kg) based on fuel consumption over time step dt (seconds)."""
        fuel_used = self.fuel_flow_rate(thrust) * dt
        self.fuel_weight -= fuel_used
        self.total_mass = self.empty_weight + self.fuel_weight
        return self.total_mass
