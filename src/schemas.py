from pydantic import BaseModel

class AircraftState(BaseModel):
    altitude: float
    airspeed: float
    pitch: float
    roll: float
    yaw: float
    pitch_rate: float
    roll_rate: float
    yaw_rate: float

class ControlCommand(BaseModel):
    throttle: float
    elevator: float
    aileron: float
    rudder: float
