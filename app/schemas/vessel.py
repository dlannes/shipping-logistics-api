from pydantic import BaseModel

class VesselBase(BaseModel):
    name: str
    capacity: int
    current_location: str

class VesselCreate(VesselBase):
    pass

class Vessel(VesselBase):
    id: int

    class Config:
        orm_mode = True
