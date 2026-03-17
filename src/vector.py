import torch

class Vector:
    """
    A utility class for creating and handling 3D vectors
    (position, velocity, acceleration) in a North-East-Down (NED) coordinate system.
    """

    @staticmethod
    def position_vector(north: float, east: float, down: float) -> torch.Tensor:
        """
        Creates a position vector in NED coordinates.
        """
        return torch.tensor([north, east, down], dtype=torch.float32)

    @staticmethod
    def velocity_vector(v_north: float, v_east: float, v_down: float) -> torch.Tensor:
        """
        Creates a velocity vector in NED coordinates.
        """
        return torch.tensor([v_north, v_east, v_down], dtype=torch.float32)

    @staticmethod
    def magnitude(vector: torch.Tensor) -> float:
        """
        Calculates the magnitude of a 3D vector.
        """
        return torch.norm(vector).item()
